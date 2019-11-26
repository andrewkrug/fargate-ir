import boto3


def test_agent():
    boto_session = boto3.session.Session(region_name="us-west-2")
    tags = [{"Key": "app", "Value": "fluffykittenwww"}]

    from lambda_handler import agent

    instance_ids = agent.get_instance_ids_for_tags(boto_session, tags)
    assert len(instance_ids) > 0

    from lambda_handler import common

    token = common.get_session_token("us-west-2")
    bucket = "public.demo.reinvent2019"
    case_folder = "abcd123"

    from lambda_handler import plans

    evidence_info = {"bucket": bucket, "case_folder": case_folder}
    p = plans.SSMRisk2Plan("MAXIMUM", boto_session, evidence_info, token)
    p.run(instance_ids)
