import boto3
import calendar
import datetime
import os
import json
import yaml

from botocore.exceptions import ClientError
from logging import getLogger


logger = getLogger(__name__)


def default_serializer(obj):
    """Default JSON serializer."""

    if isinstance(obj, datetime.datetime):
        if obj.utcoffset() is not None:
            obj = obj - obj.utcoffset()
        millis = int(calendar.timegm(obj.timetuple()) * 1000 + obj.microsecond / 1000)
        return millis
    raise TypeError(f"Not sure how to serialize {obj}")


def lower_keys(list_of_dictionaries):
    lowered_list = []
    for record in list_of_dictionaries:
        for k, v in record.items():
            k = k.lower()
            v = v.lower()
            lowered_list.append({k: v})

    return lowered_list


def load_policy():
    this_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(this_path, "policies/instance-scoped-policy.yml")
    return yaml.safe_load(open(path))


def generate_arn_for_instance(region, instance_id):
    return "arn:aws:ssm:*:*:managed-instance/{}".format(instance_id)


def get_session_token(region=None):
    if not region:
        region = "us-west-2"
    client = boto3.client("sts")
    try:
        response = client.get_session_token(DurationSeconds=900,)
    except ClientError:
        response = dict(
            Credentials=dict(
                AccessKeyId=os.getenv("AWS_ACCESS_KEY_ID"),
                SecretAccessKey=os.getenv("AWS_SECRET_ACCESS_KEY"),
                SessionToken=os.getenv("AWS_SESSION_TOKEN"),
            )
        )
    return response


def get_limited_policy(region, instance_id):
    policy_template = load_policy()
    instance_arn = generate_arn_for_instance(region, instance_id)
    s3_bucket = os.getenv("EVIDENCE_BUCKET", "public.demo.reinvent2019")
    for permission in policy_template["PolicyDocument"]["Statement"]:
        if permission["Action"][0] == "s3:PutObject":
            s3_arn = "arn:aws:s3:::{}/{}".format(s3_bucket, instance_id)
            s3_keys = "arn:aws:s3:::{}/{}/*".format(s3_bucket, instance_id)
            record_index = policy_template["PolicyDocument"]["Statement"].index(
                permission
            )
            policy_template["PolicyDocument"]["Statement"][record_index]["Resource"][
                0
            ] = s3_arn
            policy_template["PolicyDocument"]["Statement"][record_index]["Resource"][
                1
            ] = s3_keys
        elif permission["Action"][0].startswith("ssm:Send"):
            record_index = policy_template["PolicyDocument"]["Statement"].index(
                permission
            )
            policy_template["PolicyDocument"]["Statement"][record_index]["Resource"][
                1
            ] = instance_arn
        elif permission["Sid"] == "STMT4":
            s3_arn = "arn:aws:s3:::{}".format(s3_bucket)
            s3_keys = "arn:aws:s3:::{}/*".format(s3_bucket)
            record_index = policy_template["PolicyDocument"]["Statement"].index(
                permission
            )
            policy_template["PolicyDocument"]["Statement"][record_index]["Resource"][
                0
            ] = s3_arn
            policy_template["PolicyDocument"]["Statement"][record_index]["Resource"][
                1
            ] = s3_keys
    statements = json.dumps(policy_template["PolicyDocument"])
    logger.info("Limited scope role generated for assumeRole: {}".format(statements))
    return statements
