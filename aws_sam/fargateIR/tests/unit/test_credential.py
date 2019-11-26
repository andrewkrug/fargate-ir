import os
from moto import mock_sts
from lambda_handler.common import get_limited_policy


class TestSTSManager(object):
    @mock_sts
    def test_generation(self):
        ACCOUNT_ID = "1234567"
        role_name = "fargateResponder"
        dummy_role = "arn:aws:iam::{account_id}:role/{role_name}".format(
            account_id=ACCOUNT_ID, role_name=role_name
        )

        from lambda_handler import credential

        os.environ["FARGATE_IR_ROLE_ARN"] = dummy_role
        limited_scope_policy = get_limited_policy("us-west-2", "mi-00fe9059acfd61abb")
        c = credential.StsManager(
            region_name="us-west-2", limited_scope_policy=limited_scope_policy
        )

        result = c.auth()
        assert result["Credentials"] is not None

        for k in result["Credentials"]:
            assert result["Credentials"][k] is not None
