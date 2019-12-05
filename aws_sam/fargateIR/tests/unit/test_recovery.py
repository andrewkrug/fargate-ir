import boto3
import json
from moto import mock_ec2
from moto import mock_ecs
from moto.ec2 import utils as ec2_utils


fh = open("tests/unit/fixtures/recover_fixture.json")
EVENT_FIXTURE = json.loads(fh.read())
fh.close()


@mock_ecs
@mock_ec2
class TestRecovery(object):
    def test_event_to_task_arns(self):
        from lambda_handler import fargate

        arns = fargate.event_to_task_arn(EVENT_FIXTURE)
        assert arns is not None

    def test_stop_task(self):
        from lambda_handler import fargate

        client = boto3.client("ecs", region_name="us-east-1")
        response = client.create_cluster(clusterName="test_ecs_cluster")

        client = boto3.client("ecs", region_name="us-east-1")
        ec2 = boto3.resource("ec2", region_name="us-east-1")

        test_cluster_name = "test_ecs_cluster"

        test_instance = ec2.create_instances(
            ImageId="ami-1234abcd", MinCount=1, MaxCount=1
        )[0]

        instance_id_document = json.dumps(
            ec2_utils.generate_instance_identity_document(test_instance)
        )

        response = client.register_container_instance(
            cluster=test_cluster_name, instanceIdentityDocument=instance_id_document
        )

        _ = client.register_task_definition(
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
        )
        response = client.run_task(
            cluster="test_ecs_cluster",
            overrides={},
            taskDefinition="test_ecs_task",
            count=2,
            startedBy="moto",
        )
        task_arn = response["tasks"][0]["taskArn"]
        boto_session = boto3.session.Session(region_name="us-east-1")
        task_dict = dict(taskArn=task_arn, clusterArn=test_cluster_name)
        result = fargate.stop_task(boto_session=boto_session, task_dict=task_dict)
        assert result is not None
