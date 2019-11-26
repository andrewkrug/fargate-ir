import boto3
import json
import os
import slack


# Global Variables
channel = f"#{os.getenv('SLACK_CHANNEL', 'alert-triage')}"
token_bot = os.getenv("SLACK_TOKEN_NAME", "bot-token-guardduty")


def getSlackToken(user):
    ssm = boto3.client("ssm")

    token = ssm.get_parameter(Name=f"{user}", WithDecryption=True)

    token = token["Parameter"]["Value"]

    return token


def getSevColor(sev):
    if sev >= 8:
        color = "#ff0000"
    elif sev < 8 and sev >= 4:
        color = "#ffa500"
    else:
        color = "0000ff"

    return color


def getRemColor(rem):
    if rem == False:
        color = "#ff0000"
    else:
        color = "#83F52C"

    return color


def PostMessage(channel, token_bot, message, thread_ts):

    # Get Bot Token
    gd_token = getSlackToken(token_bot)

    # Slack Client for Web API Requests
    slack_client = slack.WebClient(gd_token)

    if thread_ts == "NA":
        # Post Slack Message
        post = slack_client.chat_postMessage(
            channel=channel, text=None, attachments=message
        )
    else:
        # Post Slack Message
        post = slack_client.chat_postMessage(
            channel=channel, text=None, attachments=message, ts=thread_ts
        )

    return post


def PublishEvent(event, context):
    # Set Event Variables
    gd_sev = event["detail"]["severity"]
    gd_account = event["detail"]["accountId"]
    gd_region = event["detail"]["region"]
    gd_desc = event["detail"]["description"]
    gd_type = event["detail"]["type"]
    thread_ts = "NA"

    # Set Severity Color
    gd_color = getSevColor(gd_sev)

    # Set Generic GD Finding Message
    message = [
        {
            "title": gd_type,
            "fields": [
                {"title": "AccountID", "value": gd_account, "short": "true"},
                {"title": "Region", "value": gd_region, "short": "true"},
            ],
            "fallback": "Required plain-text summary of the attachment.",
            "color": gd_color,
            "text": gd_desc,
        }
    ]

    # Post Slack Message
    post = PostMessage(channel, token_bot, message, thread_ts)

    # Add Slack Thread Id to Event
    event["ts"] = post["message"]["ts"]

    return event


def PublishRemediation(event, context):

    # Set Event Variables
    gd_rem = event["remediation"]["success"]
    gd_rem_desc = event["remediation"]["description"]
    gd_rem_title = event["remediation"]["title"]
    evidence = event["remediation"]["evidence"]["artifact_count"]
    evidence_package = event["remediation"]["evidence"]["artifact_package"]
    quicksight_dashboard = event["remediation"]["evidence"]["quicksight_url"]
    confirm = event["remediation"]["evidence"].get("confirm")
    # Set Severity Color
    gd_color = getRemColor(gd_rem)

    # Set Generic GD Finding Message
    if evidence > 0:
        message = [
            {
                "title": gd_rem_title,
                "color": gd_color,
                "text": gd_rem_desc,
                "fields": [
                    {"title": "Evidence", "value": evidence, "short": "true"},
                    {
                        "title": "Evidence Package",
                        "value": evidence_package,
                        "short": "true",
                    },
                    {
                        "title": "Quicksight Dashboard",
                        "value": quicksight_dashboard,
                        "short": "true",
                    },
                    {"title": "Status", "value": gd_rem, "short": "true"},
                ],
            },

        ]
    else:
        message = [
            {
                "title": gd_rem_title,
                "color": gd_color,
                "text": gd_rem_desc,
                "fields": [{"title": "Status", "value": gd_rem, "short": "true"},],
            }
        ]


    if confirm:
        message.append(
            {
                "title": "Decision",
                "color": gd_color,
                "text": "Was the problem remediated successfully?",
            }
        )
        message.append(
            {
                "fallback": "TBD",
                "color": gd_color,
                "actions": [
                    {
                    "type": "button",
                    "text": "Yes",
                    "style": "primary",
                    "url": "https://localhost"
                    },
                    {
                    "type": "button",
                    "text": "No",
                    "style": "danger",
                    "url": "https://localhost"
                    },
                ]
            }
        )
    # Post Slack Message
    post = PostMessage(channel, token_bot, message, event["ts"])

    return event
