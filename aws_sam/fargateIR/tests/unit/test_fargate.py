import boto3
import json
from moto import mock_ec2
from moto import mock_ecs
from moto.ec2 import utils as ec2_utils


@mock_ec2
@mock_ecs
class TestFargate(object):
    def setup(self):
        self.client = boto3.client("ecs", region_name="us-west-2")
        self.client.create_cluster(clusterName="test_ecs_cluster")

    def test_discover_task_for_tag(self):
        from lambda_handler import fargate

        self.client.register_task_definition(
            family="test_ecs_task",
            containerDefinitions=[
                {
                    "name": "hello_world",
                    "image": "docker/hello-world:latest",
                    "cpu": 1024,
                    "memory": 400,
                    "essential": True,
                    "environment": [
                        {"name": "AWS_ACCESS_KEY_ID", "value": "SOME_ACCESS_KEY"}
                    ],
                    "logConfiguration": {"logDriver": "json-file"},
                }
            ],
            tags=[{"key": "app", "value": "fluffykittenwww"},],
        )

        tags = [{"key": "app", "value": "fluffykittenwww"}]

        ec2 = boto3.resource("ec2")
        test_instance = ec2.create_instances(
            ImageId="ami-1234abcd", MinCount=1, MaxCount=1
        )[0]

        instance_id_document = json.dumps(
            ec2_utils.generate_instance_identity_document(test_instance)
        )

        response = self.client.register_container_instance(
            cluster="test_ecs_cluster", instanceIdentityDocument=instance_id_document
        )

        container_instances = self.client.list_container_instances(
            cluster="test_ecs_cluster"
        )
        container_instance_id = container_instances["containerInstanceArns"][0].split(
            "/"
        )[-1]

        response = self.client.start_task(
            cluster="test_ecs_cluster",
            taskDefinition="test_ecs_task",
            overrides={},
            containerInstances=[container_instance_id],
            startedBy="moto",
        )

        assert response is not None

        clusters = fargate.get_all_clusters(self.client)
        task_definitions = fargate.get_task_definitions_for_tag(self.client, tags)
        running_tasks = fargate.get_running_tasks_for_definition(
            self.client, clusters, task_definitions
        )

        assert len(running_tasks) == 1

    def test_get_eni_information(self):
        client = boto3.client("ec2", region_name="us-west-2")
        vpc = client.create_vpc(CidrBlock="10.0.0.0/16",)["Vpc"]["VpcId"]

        subnet = client.create_subnet(CidrBlock="10.0.1.0/24", VpcId=vpc,)

        client.modify_subnet_attribute(
            MapPublicIpOnLaunch={"Value": True}, SubnetId=subnet["Subnet"]["SubnetId"]
        )

        eni = client.create_network_interface(
            Description="testymctestinterface",
            InterfaceType="efa",
            SubnetId=subnet["Subnet"]["SubnetId"],
        )

        eni_id = eni["NetworkInterface"]["NetworkInterfaceId"]

        from lambda_handler import fargate

        boto_session = boto3.session.Session(region_name="us-west-2")
        info = fargate.get_eni_info(boto_session, eni_id)

        assert info is not None
