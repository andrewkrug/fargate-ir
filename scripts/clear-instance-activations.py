#!/usr/bin/python


def clear_all_activations():
    ssm = boto3.client("ssm", region_name="us-west-2")

    response = ""
    while response is not None:
        for instance in ssm.describe_instance_information()["InstanceInformationList"]:
            response = ssm.deregister_managed_instance(
                InstanceId=instance["InstanceId"]
            )
