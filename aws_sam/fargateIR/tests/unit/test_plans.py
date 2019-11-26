import boto3
import datetime
from moto import mock_s3
from moto import mock_ssm

from lambda_handler import plans


class TestSSM2Risk(object):
    def setup(self):
        self.boto_session = boto3.session.Session(region_name="us-west-2")
        self.instance_ids = ["i-123456"]
        self.credentials = dict(
            Credentials=dict(
                AccessKeyId="foo",
                SecretAccessKey="bar",
                SessionToken="baz"
            )
        )

    def test_object_init(self):
        ssm2risk = plans.SSMRisk2Plan("MAXIMUM", self.boto_session, evidence_info={}, credentials=self.credentials)
        assert ssm2risk is not None

    def test_risk_to_commands(self):
        ssm2risk = plans.SSMRisk2Plan("MAXIMUM", self.boto_session, evidence_info={}, credentials=self.credentials)
        commands = ssm2risk.commands()
        assert commands is not None
        assert len(commands) > 0

    @mock_ssm
    @mock_s3
    def test_run(self):
        s3 = boto3.client('s3', region_name="us-west-2")
        s3.create_bucket(Bucket="public.demo.reinvent2019")
        ssm2risk = plans.SSMRisk2Plan("MAXIMUM", self.boto_session, evidence_info={}, credentials=self.credentials)
        result = ssm2risk.run(instance_ids=["i-1234567"])
        assert result is not None
