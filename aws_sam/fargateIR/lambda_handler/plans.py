import os
import time


class SSMRisk2Plan(object):
    def __init__(self, risk_level, boto_session, evidence_info, credentials):
        self.risk_level = risk_level
        self.boto_session = boto_session
        self.evidence_bucket = evidence_info.get("bucket", "public.demo.reinvent2019")
        self.case_folder = evidence_info.get("case_folder", "123456")
        self.credentials = credentials["Credentials"]

    def connect(self):
        return self.boto_session.client("ssm")

    def low(self):
        commands = []
        return commands

    def medium(self):
        commands = []
        commands.extend(self.low())
        return commands

    def high(self):
        commands = []
        commands.extend(self.low())
        commands.extend(self.medium())
        return commands

    def maximum(self):
        commands = [
            f"sudo yum install tcpdump -y \
        && sudo tcpdump -i eth0 -G 60 -W 1 -s0 -w capture.pcap \
        && AWS_ACCESS_KEY_ID={self.credentials['AccessKeyId']} \
        AWS_SECRET_ACCESS_KEY={self.credentials['SecretAccessKey']} \
        AWS_SESSION_TOKEN={self.credentials['SessionToken']} \
        aws s3 cp capture.pcap \
        s3://{self.evidence_bucket}/{self.case_folder}/`echo $HOSTNAME`-capture.pcap"
        ]

        commands.extend(self.low())
        commands.extend(self.medium())
        commands.extend(self.high())
        return commands

    def commands(self):
        """Turn our ultimate risk level initialized in the object into action
        using the LOW, MED, HIGH, MAXIMUM scale."""

        return eval(f"self.{self.risk_level.lower()}()")

    def _get_object_keys(self):
        object_keys = []
        client = self.boto_session.client("s3")
        response = client.list_objects_v2(
            Bucket=self.evidence_bucket, Prefix=self.case_folder,
        ).get("Contents")

        if response:
            for object_key in response:
                object_keys.append(object_key["Key"])

        return object_keys

    def run(self, instance_ids, wait=True):
        """Run an ssm command.  Return the boto3 response."""
        if len(instance_ids) > 0:
            client = self.boto_session.client("ssm", region_name="us-west-2")
            response = client.send_command(
                InstanceIds=list(set(instance_ids)),
                DocumentName="AWS-RunShellScript",
                Comment="Incident response step execution for: {}".format(
                    len(list(set(instance_ids)))
                ),
                Parameters={"commands": self.commands()},
            )

            command_id = response["Command"]["CommandId"]
            execution_conditions = ["Pending", "InProgress", "Delayed", "Cancelling"]

            if wait:
                time.sleep(5)
                executing = True
                execution_states = []
                while executing:
                    for instance in list(set(instance_ids)):
                        response = client.get_command_invocation(
                            CommandId=command_id, InstanceId=instance,
                        )
                        if response.get("Status") in execution_conditions:
                            pass
                        else:
                            execution_states.append(response.get("Status"))

                        if len(execution_states) == len(list(set(instance_ids))):
                            executing = False
                    time.sleep(5)
            return self._get_object_keys()


class FargateRisk2Plan(object):
    def __init__(self, risk_level, boto_session):
        self.boto_session = boto_session
        self.risk_level = risk_level

    def find_isolation_sg(self, vpc_id):
        ec2 = self.boto_session.client("ec2")
        response = ec2.describe_security_groups(
            Filters=[
                {"Name": "vpc-id", "Values": [vpc_id]},
                {"Name": "group-name", "Values": ["isolation_sg"]},
            ],
        )

        if len(response.get("SecurityGroups", [])) > 0:
            return response.get("SecurityGroups")[0]

    def _add_revoke_rule(self, group):
        ec2 = self.boto_session.client("ec2")
        result = ec2.revoke_security_group_egress(
            GroupId=group["GroupId"], IpPermissions=group["IpPermissionsEgress"]
        )
        return result

    # This is traditional ec2 isolation.
    # Does not work for fargate due to separation of concerns.
    def create_isolation_sg(self, vpc_id):
        ec2 = self.boto_session.client("ec2")
        result = ec2.create_security_group(
            GroupName="isolation_sg",
            Description="Isolation Security Group",
            VpcId=vpc_id,
        )
        self._add_revoke_rule(self.find_isolation_sg(vpc_id))
        return result["GroupId"]

    # Abandoned method due to the above and below.
    def find_or_create_isolate_sg(self, vpc_id):
        existing_id = self.find_isolation_sg(vpc_id)["GroupId"]
        if existing_id:
            return existing_id
        else:
            return self.create_isolation_sg(vpc_id)

    # This does not work because AWS is responsible for managing the interface.
    # Need to use a different tactic.
    def isolate(self, eni_id, security_group_id):
        ec2 = self.boto_session.client("ec2")
        response = ec2.modify_network_interface_attribute(
            Groups=[security_group_id,], NetworkInterfaceId=eni_id,
        )
        return response

    def _enrich_interface_with_vpc_info(self, eni_info):
        ec2 = self.boto_session.client("ec2")
        for interface in eni_info:
            if interface.get("eni_id"):
                subnet_response = ec2.describe_subnets(
                    SubnetIds=[interface.get("subnet_id"),]
                )
                eni_response = ec2.describe_network_interfaces(
                    NetworkInterfaceIds=[interface.get("eni_id"),],
                )

                item = eni_info.index(interface)
                eni_info[item]["vpc_id"] = subnet_response["Subnets"][0]["VpcId"]
                eni_info[item]["sg_id"] = eni_response["NetworkInterfaces"][0][
                    "Groups"
                ][0]["GroupId"]
        return eni_info

    def _get_eni_information(self, event):
        eni_info = []
        for task in event["detail"]["resource"]["fargateTasks"]:
            subnet_id = None
            eni_id = None
            ip_addr = None
            interface_detail = task["attachments"][0]["details"]
            for row in interface_detail:
                if row["name"] == "subnetId":
                    subnet_id = row["value"]
                elif row["name"] == "networkInterfaceId":
                    eni_id = row["value"]
                elif row["name"] == "privateIPv4Address":
                    ip_addr = row["value"]
                else:
                    continue
            eni_info.append(dict(subnet_id=subnet_id, eni_id=eni_id, ip_addr=ip_addr))
        return eni_info

    def scale_out(self, cluster, service, count):
        ecs = self.boto_session.client("ecs")
        desired_count = count + 2

        # Maximum size guardrail.
        if desired_count > 7:
            desired_count = 7

        response = ecs.update_service(
            cluster=cluster,
            service=service,
            desiredCount=desired_count,
            deploymentConfiguration={
                "maximumPercent": 125,
                "minimumHealthyPercent": 25,
            },
        )
        return response

    def remove_record_from_dns(self, eni_id):
        ZONE_ID = os.getenv("ZONE_ID", "Z2U0MJZ98F8AGO")
        ec2 = self.boto_session.client("ec2")
        eni_response = ec2.describe_network_interfaces(NetworkInterfaceIds=[eni_id,],)

        public_ip = eni_response["NetworkInterfaces"][0]["Association"]["PublicIp"]
        route53 = self.boto_session.client("route53")
        response = route53.list_resource_record_sets(HostedZoneId=ZONE_ID,)
        result = None
        for dns_record in response.get("ResourceRecordSets"):
            if dns_record.get("ResourceRecords"):
                record_ip = dns_record["ResourceRecords"][0]["Value"]
                if record_ip == public_ip:
                    result = route53.change_resource_record_sets(
                        HostedZoneId=ZONE_ID,
                        ChangeBatch={
                            "Changes": [
                                {
                                    "Action": "DELETE",
                                    "ResourceRecordSet": {
                                        "Name": dns_record.get("Name"),
                                        "SetIdentifier": dns_record.get(
                                            "SetIdentifier"
                                        ),
                                        "Type": dns_record.get("Type"),
                                        "MultiValueAnswer": dns_record.get(
                                            "MultiValueAnswer"
                                        ),
                                        "TTL": dns_record.get("TTL"),
                                        "ResourceRecords": dns_record.get(
                                            "ResourceRecords"
                                        ),
                                    },
                                }
                            ]
                        },
                    )
        return result

    def run(self, event):
        """Execute any additional protections deemed necessary based on the risk."""
        success = True
        eni_infomation = self._enrich_interface_with_vpc_info(
            self._get_eni_information(event)
        )

        # Option 1 Remove our tainted instances from DNS
        # Scale out to replace with known good.
        for eni in eni_infomation:
            self.remove_record_from_dns(eni.get("eni_id"))

        self.scale_out(
            cluster=event["detail"]["resource"]["fargateTasks"][0]["clusterArn"],
            service=event["detail"]["resource"]["fargateTasks"][0]["group"].split(
                "service:"
            )[1],
            count=len(eni_infomation),
        )

        # Option 2 Isolate them all by revoking all egress.
        # self._add_revoke_rule(eni_infomation[0].get('sg_id'))
        # Note: This would cause loss of service.

        # Option 3 XXX TBD Duplicate the service.
        # Then isolate the current service.

        return success
