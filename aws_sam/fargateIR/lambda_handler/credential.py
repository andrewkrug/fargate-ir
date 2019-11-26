# -*- coding: utf-8 -*-
import boto3
import os


class StsManager(object):
    def __init__(self, region_name, limited_scope_policy):
        self.boto_session = boto3.session.Session(region_name=region_name)
        self.sts_client = self.boto_session.client("sts")
        self.limited_scope_policy = limited_scope_policy

    def auth(self):
        return self.assume_role(self.sts_client, os.getenv("FARGATE_IR_ROLE_ARN"))

    def get_session_token(self, client):
        response = client.get_session_token(DurationSeconds=900)
        return response

    def assume_role(self, client, role_arn):
        response = client.assume_role(
            RoleArn=role_arn,
            RoleSessionName="fargate-ir",
            DurationSeconds=3600,
            Policy=self.limited_scope_policy,
        )
        return response
