import boto3
import json
import logging
import os
import socket
import sys


try:
    import agent
    import common
    import fargate
    from custom_logger import JsonFormatter
    from plans import FargateRisk2Plan
    from plans import SSMRisk2Plan
    from risk import Finding
    from notify import PublishEvent
    from notify import PublishRemediation
    from pcap import Analyze
except ImportError:
    from lambda_handler import agent
    from lambda_handler import common
    from lambda_handler import fargate

    from lambda_handler.custom_logger import JsonFormatter
    from lambda_handler.plans import FargateRisk2Plan
    from lambda_handler.plans import SSMRisk2Plan
    from lambda_handler.risk import Finding
    from lambda_handler.notify import PublishEvent
    from lambda_handler.notify import PublishRemediation
    from lambda_handler.pcap import Analyze


def setup_logging():
    logger = logging.getLogger()
    for h in logger.handlers:
        logger.removeHandler(h)
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(JsonFormatter(extra={"hostname": socket.gethostname()}))
    logger.addHandler(h)
    logger.setLevel(logging.DEBUG)
    return logger


def protect(event, context):
    logger = setup_logging()
    success = False
    logger.info("Running the protect phase.")
    region_name = event["detail"]["region"]
    boto_session = boto3.session.Session(region_name=region_name)
    ecs_client = boto_session.client("ecs")

    tags = event["detail"]["resource"]["instanceDetails"].get("tags")

    if tags:
        # Interrogate ECS Api for additional targeting information.
        clusters = fargate.get_all_clusters(ecs_client)
        task_definitions = fargate.get_task_definitions_for_tag(ecs_client, tags)
        running_tasks = fargate.get_running_tasks_for_definitions(
            ecs_client, clusters, task_definitions
        )

        # Interrogate SSM for the instances associated with this tag.
        ssm_instance_ids = agent.get_instance_ids_for_tags(boto_session, tags)

        # Enrich the guardDuty event with information about the running tasks for the tags
        event["detail"]["resource"]["fargateTasks"] = running_tasks
        event["detail"]["resource"]["ssmInstanceIds"] = ssm_instance_ids

        # Need to deserialize and reserialze to convert pydatetime objects.
        event = json.loads(json.dumps(event, default=common.default_serializer))

        # Increase the number of running instances in the fargate service associated
        # Work on tasks that were only part of the incident at the time of reporting.
        # Can't isolate the eni-xxxx involved but we can remove from DNS!
        fargate_responder = FargateRisk2Plan(
            event["detail"]["remediation"]["risk"], boto_session
        )
        success = fargate_responder.run(event)
        event["detail"]["remediation"]["success"] = success
    else:
        raise ValueError("No tags were present in the event.")
    return event


def detect(event, context):
    logger = setup_logging()
    logger.info("Running the detect phase.")
    event["detail"]["remediation"] = {}
    # Map the risk in this stage using our risk mapper.
    risk_level = Finding(event).risk_level()
    event["detail"]["remediation"]["risk"] = risk_level
    return event


def low_respond(event, context):
    logger = setup_logging()
    event["detail"]["remediation"]["evidence"] = {}
    event["detail"]["remediation"]["evidence"]["artifact_count"] = 0
    return event


def medium_respond(event, context):
    logger = setup_logging()
    event["detail"]["remediation"]["evidence"] = {}
    event["detail"]["remediation"]["evidence"]["artifact_count"] = 0
    return event


def high_respond(event, context):
    logger = setup_logging()
    event["detail"]["remediation"]["evidence"] = {}
    event["detail"]["remediation"]["evidence"]["artifact_count"] = 0
    return event


def maximum_respond(event, context):
    logger = setup_logging()
    event["detail"]["remediation"]["evidence"] = {}
    event["detail"]["remediation"]["evidence"]["artifact_count"] = 0
    event["detail"]["remediation"]["success"] = True

    # Use the guardDuty ID as a means of containing all evidence around the incident.
    evidence_info = dict(
        bucket=os.getenv("EVIDENCE_BUCKET", "public.demo.reinvent2019"),
        case_folder=event["detail"]["id"],
    )

    # Take our risk levels and map them to discrete actions in code.
    ssm_responder = SSMRisk2Plan(
        risk_level=event["detail"]["remediation"]["risk"],
        boto_session=boto3.session.Session(),
        evidence_info=evidence_info,
        credentials=common.get_session_token(),
    )

    # Execute our pre-defined plans as ssm_runcommand and wait.
    evidence = ssm_responder.run(
        instance_ids=event["detail"]["resource"]["ssmInstanceIds"]
    )

    # Enrich our state with the number of evidence items gathered.
    event["detail"]["remediation"]["evidence"]["artifact_count"] = len(evidence)
    event["detail"]["remediation"]["evidence"]["objects"] = evidence
    return event


def recover(event, context):
    logger = setup_logging()
    logger.info("Running the recover phase. ")
    # Stop all the containers we have been working on.
    tasks = fargate.event_to_task_arn(event)
    boto_session = boto3.session.Session()

    # Stop the tasks now that we have extracted the evidence.
    # In low, medium risks scenarios we migh leave these running for further investigation.
    for task_dict in tasks:
        fargate.stop_task(boto_session, task_dict)
    return event


def process_evidence(event, context):
    logger = setup_logging()
    logger.info("Processing the evidence.")
    
    # Check to see if we have evidence to process.
    if event["detail"]["remediation"]["evidence"]["objects"] != []:
        s3_bucket = os.getenv('EVIDENCE_BUCKET', "public.demo.reinvent2019")
        logger.info(f"Processing evidence from: {s3_bucket}")

        # Process all of our packet captures to VPC-Flowlike json and parquet.
        for object_key in event["detail"]["remediation"]["evidence"][
            "objects"
        ]:
            try:
                logger.info(f"Attempting to process: {object_key}")
                full_path = f"s3://{s3_bucket}/{object_key}"
                logger.info(f"Full path to file: {full_path}")
                a = Analyze(full_path)
                a.get_geoip_database()
                logger.info(f"Geolite database retrieved.")
                a.load_pcap()
                extraction = a.get_extraction()
                result = a.extraction_to_json(extraction)
                a.json_to_parquet(result)
                a.upload_all_processed()
                logger.info("Uploading processed.")
            except Exception as e:
                logger.error(f"Could not reason about: {object_key} due to: {e}.")
    return event


def notify(event, context):
    logger = setup_logging()
    logger.info("Sending a notification to slack.")
    event = PublishEvent(event, context)
    return event


def notify_complete(event, context):
    logger = setup_logging()
    logger.info("Sending a notification to slack.")
    event = PublishRemediation(event, context)
    return event

