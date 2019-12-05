"""Reset fluffy kitten security to pre-incident response."""


import boto3


SERVICE = "FluffyKitten-ServiceDefinition-1X6MT2KIFBI91"
CLUSTER = "FargateSSMDemo"
ROUTE53_ZONE = "Z2U0MJZ98F8AGO"


def lower_keys(list_of_dictionaries):
    lowered_list = []
    for record in list_of_dictionaries:
        for k, v in record.items():
            k = k.lower()
            v = v.lower()
            lowered_list.append({k: v})

    return lowered_list


def scale_out(boto_session, cluster=CLUSTER, service=SERVICE, count=3):
    ecs = boto_session.client("ecs")

    response = ecs.update_service(
        cluster=cluster,
        service=service,
        desiredCount=count,
        deploymentConfiguration={
            "maximumPercent": 125,
            "minimumHealthyPercent": 25,
        },
    )

    return response


def dump_route_53_records(boto_session):
    route53 = boto_session.client("route53")
    response = route53.list_resource_record_sets(
        HostedZoneId=ROUTE53_ZONE,
        StartRecordName='fluffykitten.threatrespon.se',
        StartRecordType='A',
    )
    
    delete_response = None
    if len(response['ResourceRecordSets']) > 0:
        for x in range(0, len(response['ResourceRecordSets'])):
            delete_response = route53.change_resource_record_sets(
                HostedZoneId=ROUTE53_ZONE,
                ChangeBatch={
                    'Comment': 'Remove all records for fluffy kitten.',
                    'Changes': [
                        {
                            'Action': 'DELETE',
                            'ResourceRecordSet': response['ResourceRecordSets'][x]
                        },
                    ]
                }
            )

    return delete_response


def get_task_definitions_for_tag(boto_session, tags):
    client = boto_session.client('ecs')
    tasks = []

    tags = lower_keys(tags)

    response = client.list_task_definitions(status="ACTIVE", sort="ASC",)

    for task in response.get("taskDefinitionArns", []):
        task_definition_json = client.describe_task_definition(
            taskDefinition=task, include=["TAGS"]
        )

        task_tags = lower_keys(
            client.list_tags_for_resource(resourceArn=task).get("tags", [])
        )

        for tag_kv in task_tags:
            if tag_kv in task_tags:
                tasks.append(task_definition_json)
    return tasks


def stop_tasks(boto_session, task_dict):
    ecs = boto_session.client("ecs")
    response = ecs.stop_task(
        cluster=task_dict["clusterArn"],
        task=task_dict["taskArn"],
        reason="Task stopped as part of cleanup for demo.",
    )
    return response


def get_running_tasks_for_definition(boto_session, clusters, task_definition_json):
    client = boto_session.client('ecs')
    running_tasks = []
    task_arns = []

    for task in task_definition_json:
        task_arns.append(task["taskDefinition"]["taskDefinitionArn"])

    for cluster in clusters:
        task_list = client.list_tasks(cluster=cluster, desiredStatus="RUNNING",)

        if len(task_list.get("taskArns")) > 0:
            task_detail = client.describe_tasks(
                cluster=cluster, tasks=task_list.get("taskArns"), include=["TAGS",]
            )

        for running_task in task_detail.get("tasks"):
            if running_task["taskDefinitionArn"] in task_arns:
                running_tasks.append(running_task)

    for task in running_tasks:
        task.pop("overrides", None)
        task.pop("containers", None)

    return running_tasks


def clear_all_activations():
    instance_information = []
    ssm = boto3.client("ssm", region_name="us-west-2")
    response = ssm.describe_instance_information()

    while response.get('NextToken') is not None:
        instance_information.extend(response.get("InstanceInformationList"))
        response = ssm.describe_instance_information(
            NextToken=response.get('NextToken')
        )
    
    instance_information.extend(response.get("InstanceInformationList"))

    if len(instance_information) > 0:
        for instance in instance_information:
            print(f"Deregistering instance: {instance}")
            response = ssm.deregister_managed_instance(
                  InstanceId=instance["InstanceId"]
            )


if __name__ == "__main__":
    tags = [
        {
            "Key": "app",
            "Value": "fluffykittenwww"
        },
        {
            "Key": "risk",
            "Value": "maximum"
        }
    ]
    session = boto3.session.Session(region_name="us-west-2")
    result = scale_out(session)
    print(result)
    tasks = get_task_definitions_for_tag(session, tags)
    print(tasks)
    running_tasks = get_running_tasks_for_definition(session, [CLUSTER], tasks)
    print(running_tasks)
    print(clear_all_activations())
    print(dump_route_53_records(session))
    for task in running_tasks:
        print(stop_tasks(session, task))
    
    

