import boto3

try:
    from lambda_handler import common
except ImportError:
    import common


def get_instance_ids_for_tags(boto_session, tags):
    tags = common.lower_keys(tags)
    targets = []
    client = boto_session.client("ssm")
    response = client.describe_instance_information()

    if len(response.get("InstanceInformationList", [])):
        for instance in response.get("InstanceInformationList"):
            if instance.get("PingStatus") == "Online":
                instance_tags = client.list_tags_for_resource(
                    ResourceType="ManagedInstance", ResourceId=instance["InstanceId"]
                )

                for it in common.lower_keys(instance_tags["TagList"]):
                    if it in tags:
                        targets.append(instance["InstanceId"])
    return targets
