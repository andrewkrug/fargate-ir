import os


EVENT_FIXTURE = {
    "detail-type": "GuardDuty Finding",
    "source": "aws.guardduty",
    "detail": {
        "schemaVersion": "2.0",
        "accountId": "874153891031",
        "region": "us-west-2",
        "partition": "aws",
        "id": "b2b7236dda0e4eff8aa17738d9ad18c5",
        "type": "Custom:UserReport/WebsiteDefacement",
        "resource": {
            "resourceType": "FargateContainer",
            "instanceDetails": {
                "tags": [
                    {"Key": "app", "Value": "fullykittenwww"},
                    {"Key": "risk", "Value": "maximum"},
                ],
            },
        },
        "severity": 10,
        "createdAt": "2019-11-07T17:13:53.948Z",
        "updatedAt": "2019-11-09T17:41:09.360Z",
        "title": "A user has reported a defacement of fluffykitten securities main www site.",
        "description": "All images on the site have been replaced with dogs instead of fluffy cats.",
        "detail": {},
    },
}


EVENT_FIXTURE_COMPLETE = {
    "detail-type": "GuardDuty Finding",
    "source": "aws.guardduty",
    "detail": {
        "schemaVersion": "2.0",
        "accountId": "874153891031",
        "region": "us-west-2",
        "partition": "aws",
        "id": "b2b7236dda0e4eff8aa17738d9ad18c5",
        "type": "Custom:UserReport/WebsiteDefacement",
        "resource": {
            "resourceType": "FargateContainer",
            "instanceDetails": {
                "tags": [
                    {"Key": "app", "Value": "fullykittenwww"},
                    {"Key": "risk", "Value": "maximum"},
                ],
            },
        },
        "severity": 10,
        "createdAt": "2019-11-07T17:13:53.948Z",
        "updatedAt": "2019-11-09T17:41:09.360Z",
        "title": "A user has reported a defacement of fluffykitten securities main www site.",
        "description": "All images on the site have been replaced with dogs instead of fluffy cats.",
        "detail": {"risk": "MAXIMUM"},
    },
    "remediation": {
        "evidence": {
            "artifact_count": 6,
            "quicksight_url": "https://foo.bar.com",
            "artifact_package": "https://s3.us-west-2.foo.bar.com",
            "confirm": True
        },
        "success": True,
        "description": "The plan MAXIMUM was initiated.",
        "title": "Maximum Risk Fargate Remediation",
    },
}


def test_slackbot_notify():
    os.environ["SLACK_CHANNEL"] = "alert-triage"
    os.environ["SLACK_TOKEN_NAME"] = "bot-token-guardduty"
    from lambda_handler import notify

    p = notify.PublishEvent(event=EVENT_FIXTURE, context={})

    os.environ["SLACK_CHANNEL"] = "alert-triage"
    os.environ["SLACK_TOKEN_NAME"] = "bot-token-guardduty"
    from lambda_handler import notify

    EVENT_FIXTURE_COMPLETE["ts"] = p["ts"]
    p = notify.PublishRemediation(event=EVENT_FIXTURE_COMPLETE, context={})
