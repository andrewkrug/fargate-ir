import boto3

try:
    import common
except ImportError:
    from lambda_handler import common


def get_all_clusters(client):
    clusters = []
    response = client.list_clusters()

    for cluster in response["clusterArns"]:
        clusters.append(cluster)
    return clusters


def get_task_definitions_for_tag(client, tags):
    tasks = []

    tags = common.lower_keys(tags)

    response = client.list_task_definitions(status="ACTIVE", sort="ASC",)

    for task in response.get("taskDefinitionArns", []):
        task_definition_json = client.describe_task_definition(
            taskDefinition=task, include=["TAGS"]
        )

        task_tags = common.lower_keys(
            client.list_tags_for_resource(resourceArn=task).get("tags", [])
        )

        for tag_kv in task_tags:
            if tag_kv in task_tags:
                tasks.append(task_definition_json)
    return tasks


def get_running_tasks_for_definition(client, clusters, task_definition_json):
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


def get_running_tasks_for_definitions(client, clusters, task_definition_list):
    tasks = []
    for task_definition_json in task_definition_list:
        tasks.extend(
            get_running_tasks_for_definition(client, clusters, [task_definition_json])
        )

    return tasks


def get_eni_info(boto_session, eni_id):
    ec2 = boto_session.client("ec2")
    response = ec2.describe_network_interfaces(NetworkInterfaceIds=[eni_id,],)
    # Note: Public Ip will be in PublicIp key if exists
    return response["NetworkInterfaces"][0]


def event_to_task_arn(event):
    task_arns = []
    for task in event['detail']['resource']['fargateTasks']:
        task_arns.append(dict(taskArn=task['taskArn'],clusterArn=task['clusterArn']))
    return task_arns


def stop_task(boto_session, task_dict):
    ecs = boto_session.client("ecs")
    response = ecs.stop_task(
        cluster=task_dict['clusterArn'],
        task=task_dict['taskArn'],
        reason='Task stopped as part of incident response.'
    )
    return response
