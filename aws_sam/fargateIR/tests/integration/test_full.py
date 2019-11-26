import os
from lambda_handler import handle


# Use an event structure that follows GuardDuty Schema 2.0 to simulate a ticketing system integration.
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
                    {"Key": "app", "Value": "fluffykittenwww"},
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


def test_phases():
    os.environ["SLACK_CHANNEL"] = "alert-triage"
    event = EVENT_FIXTURE
    notify = handle.notify(event, context={})
    event = notify

    detect = handle.detect(event, context={})
    event = detect

    protect = handle.protect(event, context={})
    event = protect

    assert protect["detail"]["remediation"]["risk"] == "MAXIMUM"
    assert notify is not None
    assert detect is not None
    assert protect is not None

    respond = handle.maximum_respond(event, context={})
    assert response["detail"]["remediation"]["evidence"]["artifact_count"] > 0
