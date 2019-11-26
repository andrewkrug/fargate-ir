import boto3

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
                ]
            },
            "fargateTasks": [
                {
                    "taskArn": "arn:aws:ecs:us-west-2:874153891031:task/FargateSSMDemo/0ae46ee698884c8dab6866945c75ebcf",
                    "clusterArn": "arn:aws:ecs:us-west-2:874153891031:cluster/FargateSSMDemo",
                    "taskDefinitionArn": "arn:aws:ecs:us-west-2:874153891031:task-definition/FluffyKittenDemo:7",
                    "overrides": {
                        "containerOverrides": [{"name": "FluffyKittenDemo"}],
                        "inferenceAcceleratorOverrides": [],
                    },
                    "lastStatus": "RUNNING",
                    "desiredStatus": "RUNNING",
                    "cpu": "256",
                    "memory": "512",
                    "containers": [
                        {
                            "containerArn": "arn:aws:ecs:us-west-2:874153891031:container/14215c52-5c6c-485f-a401-2450abfd279c",
                            "taskArn": "arn:aws:ecs:us-west-2:874153891031:task/FargateSSMDemo/0ae46ee698884c8dab6866945c75ebcf",
                            "name": "FluffyKittenDemo",
                            "image": "874153891031.dkr.ecr.us-west-2.amazonaws.com/fluffykitten:latest",
                            "imageDigest": "sha256:8305d145ca446a6e07e6890a85215d3ddf63e75ee5a9a7d36068ba4f1e84212e",
                            "runtimeId": "df69ef0ef57091405d3adcc9be66f10fe54b8f31fec80ffbf110713ebcf0ea52",
                            "lastStatus": "RUNNING",
                            "networkBindings": [],
                            "networkInterfaces": [
                                {
                                    "attachmentId": "35e5cfd5-7088-4e5e-9a64-639c43c80776",
                                    "privateIpv4Address": "172.31.46.36",
                                }
                            ],
                            "healthStatus": "UNKNOWN",
                            "cpu": "256",
                            "memory": "512",
                        }
                    ],
                    "startedBy": "ecs-svc/9223370462914324694",
                    "version": 3,
                    "connectivity": "CONNECTED",
                    "connectivityAt": 1573943232015,
                    "pullStartedAt": 1573943241362,
                    "pullStoppedAt": 1573943257362,
                    "createdAt": 1573943228000,
                    "startedAt": 1573943259362,
                    "group": "service:FluffyKitten-ServiceDefinition-1X6MT2KIFBI91",
                    "launchType": "FARGATE",
                    "platformVersion": "1.3.0",
                    "attachments": [
                        {
                            "id": "35e5cfd5-7088-4e5e-9a64-639c43c80776",
                            "type": "ElasticNetworkInterface",
                            "status": "ATTACHED",
                            "details": [
                                {"name": "subnetId", "value": "subnet-2597df6e"},
                                {
                                    "name": "networkInterfaceId",
                                    "value": "eni-0f0c44770a4b5758c",
                                },
                                {"name": "macAddress", "value": "06:f9:2e:95:be:dc"},
                                {"name": "privateIPv4Address", "value": "172.31.46.36"},
                            ],
                        }
                    ],
                    "healthStatus": "UNKNOWN",
                    "tags": [],
                },
                {
                    "taskArn": "arn:aws:ecs:us-west-2:874153891031:task/FargateSSMDemo/65060dc81dd848c7a935f242b1e3d71b",
                    "clusterArn": "arn:aws:ecs:us-west-2:874153891031:cluster/FargateSSMDemo",
                    "taskDefinitionArn": "arn:aws:ecs:us-west-2:874153891031:task-definition/FluffyKittenDemo:7",
                    "overrides": {
                        "containerOverrides": [{"name": "FluffyKittenDemo"}],
                        "inferenceAcceleratorOverrides": [],
                    },
                    "lastStatus": "RUNNING",
                    "desiredStatus": "RUNNING",
                    "cpu": "256",
                    "memory": "512",
                    "containers": [
                        {
                            "containerArn": "arn:aws:ecs:us-west-2:874153891031:container/fa69b077-c727-465b-86c9-99d8f22f782e",
                            "taskArn": "arn:aws:ecs:us-west-2:874153891031:task/FargateSSMDemo/65060dc81dd848c7a935f242b1e3d71b",
                            "name": "FluffyKittenDemo",
                            "image": "874153891031.dkr.ecr.us-west-2.amazonaws.com/fluffykitten:latest",
                            "imageDigest": "sha256:8305d145ca446a6e07e6890a85215d3ddf63e75ee5a9a7d36068ba4f1e84212e",
                            "runtimeId": "a07db0ee7880bdff8801d89b0fcce7acc106c7144dbbac1a4dd9bb8aa6334969",
                            "lastStatus": "RUNNING",
                            "networkBindings": [],
                            "networkInterfaces": [
                                {
                                    "attachmentId": "56434de7-2625-48e8-9769-3a55edd31488",
                                    "privateIpv4Address": "172.31.47.140",
                                }
                            ],
                            "healthStatus": "UNKNOWN",
                            "cpu": "256",
                            "memory": "512",
                        }
                    ],
                    "startedBy": "ecs-svc/9223370462914324694",
                    "version": 3,
                    "connectivity": "CONNECTED",
                    "connectivityAt": 1573943232128,
                    "pullStartedAt": 1573943244548,
                    "pullStoppedAt": 1573943258548,
                    "createdAt": 1573943228000,
                    "startedAt": 1573943263548,
                    "group": "service:FluffyKitten-ServiceDefinition-1X6MT2KIFBI91",
                    "launchType": "FARGATE",
                    "platformVersion": "1.3.0",
                    "attachments": [
                        {
                            "id": "56434de7-2625-48e8-9769-3a55edd31488",
                            "type": "ElasticNetworkInterface",
                            "status": "ATTACHED",
                            "details": [
                                {"name": "subnetId", "value": "subnet-2597df6e"},
                                {
                                    "name": "networkInterfaceId",
                                    "value": "eni-0ead9542973de2178",
                                },
                                {"name": "macAddress", "value": "06:79:e9:b2:cf:3e"},
                                {
                                    "name": "privateIPv4Address",
                                    "value": "172.31.47.140",
                                },
                            ],
                        }
                    ],
                    "healthStatus": "UNKNOWN",
                    "tags": [],
                },
                {
                    "taskArn": "arn:aws:ecs:us-west-2:874153891031:task/FargateSSMDemo/0ae46ee698884c8dab6866945c75ebcf",
                    "clusterArn": "arn:aws:ecs:us-west-2:874153891031:cluster/FargateSSMDemo",
                    "taskDefinitionArn": "arn:aws:ecs:us-west-2:874153891031:task-definition/FluffyKittenDemo:7",
                    "overrides": {
                        "containerOverrides": [{"name": "FluffyKittenDemo"}],
                        "inferenceAcceleratorOverrides": [],
                    },
                    "lastStatus": "RUNNING",
                    "desiredStatus": "RUNNING",
                    "cpu": "256",
                    "memory": "512",
                    "containers": [
                        {
                            "containerArn": "arn:aws:ecs:us-west-2:874153891031:container/14215c52-5c6c-485f-a401-2450abfd279c",
                            "taskArn": "arn:aws:ecs:us-west-2:874153891031:task/FargateSSMDemo/0ae46ee698884c8dab6866945c75ebcf",
                            "name": "FluffyKittenDemo",
                            "image": "874153891031.dkr.ecr.us-west-2.amazonaws.com/fluffykitten:latest",
                            "imageDigest": "sha256:8305d145ca446a6e07e6890a85215d3ddf63e75ee5a9a7d36068ba4f1e84212e",
                            "runtimeId": "df69ef0ef57091405d3adcc9be66f10fe54b8f31fec80ffbf110713ebcf0ea52",
                            "lastStatus": "RUNNING",
                            "networkBindings": [],
                            "networkInterfaces": [
                                {
                                    "attachmentId": "35e5cfd5-7088-4e5e-9a64-639c43c80776",
                                    "privateIpv4Address": "172.31.46.36",
                                }
                            ],
                            "healthStatus": "UNKNOWN",
                            "cpu": "256",
                            "memory": "512",
                        }
                    ],
                    "startedBy": "ecs-svc/9223370462914324694",
                    "version": 3,
                    "connectivity": "CONNECTED",
                    "connectivityAt": 1573943232015,
                    "pullStartedAt": 1573943241362,
                    "pullStoppedAt": 1573943257362,
                    "createdAt": 1573943228000,
                    "startedAt": 1573943259362,
                    "group": "service:FluffyKitten-ServiceDefinition-1X6MT2KIFBI91",
                    "launchType": "FARGATE",
                    "platformVersion": "1.3.0",
                    "attachments": [
                        {
                            "id": "35e5cfd5-7088-4e5e-9a64-639c43c80776",
                            "type": "ElasticNetworkInterface",
                            "status": "ATTACHED",
                            "details": [
                                {"name": "subnetId", "value": "subnet-2597df6e"},
                                {
                                    "name": "networkInterfaceId",
                                    "value": "eni-0f0c44770a4b5758c",
                                },
                                {"name": "macAddress", "value": "06:f9:2e:95:be:dc"},
                                {"name": "privateIPv4Address", "value": "172.31.46.36"},
                            ],
                        }
                    ],
                    "healthStatus": "UNKNOWN",
                    "tags": [],
                },
                {
                    "taskArn": "arn:aws:ecs:us-west-2:874153891031:task/FargateSSMDemo/65060dc81dd848c7a935f242b1e3d71b",
                    "clusterArn": "arn:aws:ecs:us-west-2:874153891031:cluster/FargateSSMDemo",
                    "taskDefinitionArn": "arn:aws:ecs:us-west-2:874153891031:task-definition/FluffyKittenDemo:7",
                    "overrides": {
                        "containerOverrides": [{"name": "FluffyKittenDemo"}],
                        "inferenceAcceleratorOverrides": [],
                    },
                    "lastStatus": "RUNNING",
                    "desiredStatus": "RUNNING",
                    "cpu": "256",
                    "memory": "512",
                    "containers": [
                        {
                            "containerArn": "arn:aws:ecs:us-west-2:874153891031:container/fa69b077-c727-465b-86c9-99d8f22f782e",
                            "taskArn": "arn:aws:ecs:us-west-2:874153891031:task/FargateSSMDemo/65060dc81dd848c7a935f242b1e3d71b",
                            "name": "FluffyKittenDemo",
                            "image": "874153891031.dkr.ecr.us-west-2.amazonaws.com/fluffykitten:latest",
                            "imageDigest": "sha256:8305d145ca446a6e07e6890a85215d3ddf63e75ee5a9a7d36068ba4f1e84212e",
                            "runtimeId": "a07db0ee7880bdff8801d89b0fcce7acc106c7144dbbac1a4dd9bb8aa6334969",
                            "lastStatus": "RUNNING",
                            "networkBindings": [],
                            "networkInterfaces": [
                                {
                                    "attachmentId": "56434de7-2625-48e8-9769-3a55edd31488",
                                    "privateIpv4Address": "172.31.47.140",
                                }
                            ],
                            "healthStatus": "UNKNOWN",
                            "cpu": "256",
                            "memory": "512",
                        }
                    ],
                    "startedBy": "ecs-svc/9223370462914324694",
                    "version": 3,
                    "connectivity": "CONNECTED",
                    "connectivityAt": 1573943232128,
                    "pullStartedAt": 1573943244548,
                    "pullStoppedAt": 1573943258548,
                    "createdAt": 1573943228000,
                    "startedAt": 1573943263548,
                    "group": "service:FluffyKitten-ServiceDefinition-1X6MT2KIFBI91",
                    "launchType": "FARGATE",
                    "platformVersion": "1.3.0",
                    "attachments": [
                        {
                            "id": "56434de7-2625-48e8-9769-3a55edd31488",
                            "type": "ElasticNetworkInterface",
                            "status": "ATTACHED",
                            "details": [
                                {"name": "subnetId", "value": "subnet-2597df6e"},
                                {
                                    "name": "networkInterfaceId",
                                    "value": "eni-0ead9542973de2178",
                                },
                                {"name": "macAddress", "value": "06:79:e9:b2:cf:3e"},
                                {
                                    "name": "privateIPv4Address",
                                    "value": "172.31.47.140",
                                },
                            ],
                        }
                    ],
                    "healthStatus": "UNKNOWN",
                    "tags": [],
                },
                {
                    "taskArn": "arn:aws:ecs:us-west-2:874153891031:task/FargateSSMDemo/0ae46ee698884c8dab6866945c75ebcf",
                    "clusterArn": "arn:aws:ecs:us-west-2:874153891031:cluster/FargateSSMDemo",
                    "taskDefinitionArn": "arn:aws:ecs:us-west-2:874153891031:task-definition/FluffyKittenDemo:7",
                    "overrides": {
                        "containerOverrides": [{"name": "FluffyKittenDemo"}],
                        "inferenceAcceleratorOverrides": [],
                    },
                    "lastStatus": "RUNNING",
                    "desiredStatus": "RUNNING",
                    "cpu": "256",
                    "memory": "512",
                    "containers": [
                        {
                            "containerArn": "arn:aws:ecs:us-west-2:874153891031:container/14215c52-5c6c-485f-a401-2450abfd279c",
                            "taskArn": "arn:aws:ecs:us-west-2:874153891031:task/FargateSSMDemo/0ae46ee698884c8dab6866945c75ebcf",
                            "name": "FluffyKittenDemo",
                            "image": "874153891031.dkr.ecr.us-west-2.amazonaws.com/fluffykitten:latest",
                            "imageDigest": "sha256:8305d145ca446a6e07e6890a85215d3ddf63e75ee5a9a7d36068ba4f1e84212e",
                            "runtimeId": "df69ef0ef57091405d3adcc9be66f10fe54b8f31fec80ffbf110713ebcf0ea52",
                            "lastStatus": "RUNNING",
                            "networkBindings": [],
                            "networkInterfaces": [
                                {
                                    "attachmentId": "35e5cfd5-7088-4e5e-9a64-639c43c80776",
                                    "privateIpv4Address": "172.31.46.36",
                                }
                            ],
                            "healthStatus": "UNKNOWN",
                            "cpu": "256",
                            "memory": "512",
                        }
                    ],
                    "startedBy": "ecs-svc/9223370462914324694",
                    "version": 3,
                    "connectivity": "CONNECTED",
                    "connectivityAt": 1573943232015,
                    "pullStartedAt": 1573943241362,
                    "pullStoppedAt": 1573943257362,
                    "createdAt": 1573943228000,
                    "startedAt": 1573943259362,
                    "group": "service:FluffyKitten-ServiceDefinition-1X6MT2KIFBI91",
                    "launchType": "FARGATE",
                    "platformVersion": "1.3.0",
                    "attachments": [
                        {
                            "id": "35e5cfd5-7088-4e5e-9a64-639c43c80776",
                            "type": "ElasticNetworkInterface",
                            "status": "ATTACHED",
                            "details": [
                                {"name": "subnetId", "value": "subnet-2597df6e"},
                                {
                                    "name": "networkInterfaceId",
                                    "value": "eni-0f0c44770a4b5758c",
                                },
                                {"name": "macAddress", "value": "06:f9:2e:95:be:dc"},
                                {"name": "privateIPv4Address", "value": "172.31.46.36"},
                            ],
                        }
                    ],
                    "healthStatus": "UNKNOWN",
                    "tags": [],
                },
                {
                    "taskArn": "arn:aws:ecs:us-west-2:874153891031:task/FargateSSMDemo/65060dc81dd848c7a935f242b1e3d71b",
                    "clusterArn": "arn:aws:ecs:us-west-2:874153891031:cluster/FargateSSMDemo",
                    "taskDefinitionArn": "arn:aws:ecs:us-west-2:874153891031:task-definition/FluffyKittenDemo:7",
                    "overrides": {
                        "containerOverrides": [{"name": "FluffyKittenDemo"}],
                        "inferenceAcceleratorOverrides": [],
                    },
                    "lastStatus": "RUNNING",
                    "desiredStatus": "RUNNING",
                    "cpu": "256",
                    "memory": "512",
                    "containers": [
                        {
                            "containerArn": "arn:aws:ecs:us-west-2:874153891031:container/fa69b077-c727-465b-86c9-99d8f22f782e",
                            "taskArn": "arn:aws:ecs:us-west-2:874153891031:task/FargateSSMDemo/65060dc81dd848c7a935f242b1e3d71b",
                            "name": "FluffyKittenDemo",
                            "image": "874153891031.dkr.ecr.us-west-2.amazonaws.com/fluffykitten:latest",
                            "imageDigest": "sha256:8305d145ca446a6e07e6890a85215d3ddf63e75ee5a9a7d36068ba4f1e84212e",
                            "runtimeId": "a07db0ee7880bdff8801d89b0fcce7acc106c7144dbbac1a4dd9bb8aa6334969",
                            "lastStatus": "RUNNING",
                            "networkBindings": [],
                            "networkInterfaces": [
                                {
                                    "attachmentId": "56434de7-2625-48e8-9769-3a55edd31488",
                                    "privateIpv4Address": "172.31.47.140",
                                }
                            ],
                            "healthStatus": "UNKNOWN",
                            "cpu": "256",
                            "memory": "512",
                        }
                    ],
                    "startedBy": "ecs-svc/9223370462914324694",
                    "version": 3,
                    "connectivity": "CONNECTED",
                    "connectivityAt": 1573943232128,
                    "pullStartedAt": 1573943244548,
                    "pullStoppedAt": 1573943258548,
                    "createdAt": 1573943228000,
                    "startedAt": 1573943263548,
                    "group": "service:FluffyKitten-ServiceDefinition-1X6MT2KIFBI91",
                    "launchType": "FARGATE",
                    "platformVersion": "1.3.0",
                    "attachments": [
                        {
                            "id": "56434de7-2625-48e8-9769-3a55edd31488",
                            "type": "ElasticNetworkInterface",
                            "status": "ATTACHED",
                            "details": [
                                {"name": "subnetId", "value": "subnet-2597df6e"},
                                {
                                    "name": "networkInterfaceId",
                                    "value": "eni-0ead9542973de2178",
                                },
                                {"name": "macAddress", "value": "06:79:e9:b2:cf:3e"},
                                {
                                    "name": "privateIPv4Address",
                                    "value": "172.31.47.140",
                                },
                            ],
                        }
                    ],
                    "healthStatus": "UNKNOWN",
                    "tags": [],
                },
                {
                    "taskArn": "arn:aws:ecs:us-west-2:874153891031:task/FargateSSMDemo/0ae46ee698884c8dab6866945c75ebcf",
                    "clusterArn": "arn:aws:ecs:us-west-2:874153891031:cluster/FargateSSMDemo",
                    "taskDefinitionArn": "arn:aws:ecs:us-west-2:874153891031:task-definition/FluffyKittenDemo:7",
                    "overrides": {
                        "containerOverrides": [{"name": "FluffyKittenDemo"}],
                        "inferenceAcceleratorOverrides": [],
                    },
                    "lastStatus": "RUNNING",
                    "desiredStatus": "RUNNING",
                    "cpu": "256",
                    "memory": "512",
                    "containers": [
                        {
                            "containerArn": "arn:aws:ecs:us-west-2:874153891031:container/14215c52-5c6c-485f-a401-2450abfd279c",
                            "taskArn": "arn:aws:ecs:us-west-2:874153891031:task/FargateSSMDemo/0ae46ee698884c8dab6866945c75ebcf",
                            "name": "FluffyKittenDemo",
                            "image": "874153891031.dkr.ecr.us-west-2.amazonaws.com/fluffykitten:latest",
                            "imageDigest": "sha256:8305d145ca446a6e07e6890a85215d3ddf63e75ee5a9a7d36068ba4f1e84212e",
                            "runtimeId": "df69ef0ef57091405d3adcc9be66f10fe54b8f31fec80ffbf110713ebcf0ea52",
                            "lastStatus": "RUNNING",
                            "networkBindings": [],
                            "networkInterfaces": [
                                {
                                    "attachmentId": "35e5cfd5-7088-4e5e-9a64-639c43c80776",
                                    "privateIpv4Address": "172.31.46.36",
                                }
                            ],
                            "healthStatus": "UNKNOWN",
                            "cpu": "256",
                            "memory": "512",
                        }
                    ],
                    "startedBy": "ecs-svc/9223370462914324694",
                    "version": 3,
                    "connectivity": "CONNECTED",
                    "connectivityAt": 1573943232015,
                    "pullStartedAt": 1573943241362,
                    "pullStoppedAt": 1573943257362,
                    "createdAt": 1573943228000,
                    "startedAt": 1573943259362,
                    "group": "service:FluffyKitten-ServiceDefinition-1X6MT2KIFBI91",
                    "launchType": "FARGATE",
                    "platformVersion": "1.3.0",
                    "attachments": [
                        {
                            "id": "35e5cfd5-7088-4e5e-9a64-639c43c80776",
                            "type": "ElasticNetworkInterface",
                            "status": "ATTACHED",
                            "details": [
                                {"name": "subnetId", "value": "subnet-2597df6e"},
                                {
                                    "name": "networkInterfaceId",
                                    "value": "eni-0f0c44770a4b5758c",
                                },
                                {"name": "macAddress", "value": "06:f9:2e:95:be:dc"},
                                {"name": "privateIPv4Address", "value": "172.31.46.36"},
                            ],
                        }
                    ],
                    "healthStatus": "UNKNOWN",
                    "tags": [],
                },
                {
                    "taskArn": "arn:aws:ecs:us-west-2:874153891031:task/FargateSSMDemo/65060dc81dd848c7a935f242b1e3d71b",
                    "clusterArn": "arn:aws:ecs:us-west-2:874153891031:cluster/FargateSSMDemo",
                    "taskDefinitionArn": "arn:aws:ecs:us-west-2:874153891031:task-definition/FluffyKittenDemo:7",
                    "overrides": {
                        "containerOverrides": [{"name": "FluffyKittenDemo"}],
                        "inferenceAcceleratorOverrides": [],
                    },
                    "lastStatus": "RUNNING",
                    "desiredStatus": "RUNNING",
                    "cpu": "256",
                    "memory": "512",
                    "containers": [
                        {
                            "containerArn": "arn:aws:ecs:us-west-2:874153891031:container/fa69b077-c727-465b-86c9-99d8f22f782e",
                            "taskArn": "arn:aws:ecs:us-west-2:874153891031:task/FargateSSMDemo/65060dc81dd848c7a935f242b1e3d71b",
                            "name": "FluffyKittenDemo",
                            "image": "874153891031.dkr.ecr.us-west-2.amazonaws.com/fluffykitten:latest",
                            "imageDigest": "sha256:8305d145ca446a6e07e6890a85215d3ddf63e75ee5a9a7d36068ba4f1e84212e",
                            "runtimeId": "a07db0ee7880bdff8801d89b0fcce7acc106c7144dbbac1a4dd9bb8aa6334969",
                            "lastStatus": "RUNNING",
                            "networkBindings": [],
                            "networkInterfaces": [
                                {
                                    "attachmentId": "56434de7-2625-48e8-9769-3a55edd31488",
                                    "privateIpv4Address": "172.31.47.140",
                                }
                            ],
                            "healthStatus": "UNKNOWN",
                            "cpu": "256",
                            "memory": "512",
                        }
                    ],
                    "startedBy": "ecs-svc/9223370462914324694",
                    "version": 3,
                    "connectivity": "CONNECTED",
                    "connectivityAt": 1573943232128,
                    "pullStartedAt": 1573943244548,
                    "pullStoppedAt": 1573943258548,
                    "createdAt": 1573943228000,
                    "startedAt": 1573943263548,
                    "group": "service:FluffyKitten-ServiceDefinition-1X6MT2KIFBI91",
                    "launchType": "FARGATE",
                    "platformVersion": "1.3.0",
                    "attachments": [
                        {
                            "id": "56434de7-2625-48e8-9769-3a55edd31488",
                            "type": "ElasticNetworkInterface",
                            "status": "ATTACHED",
                            "details": [
                                {"name": "subnetId", "value": "subnet-2597df6e"},
                                {
                                    "name": "networkInterfaceId",
                                    "value": "eni-0ead9542973de2178",
                                },
                                {"name": "macAddress", "value": "06:79:e9:b2:cf:3e"},
                                {
                                    "name": "privateIPv4Address",
                                    "value": "172.31.47.140",
                                },
                            ],
                        }
                    ],
                    "healthStatus": "UNKNOWN",
                    "tags": [],
                },
            ],
            "ssmInstanceIds": [
                "mi-0359c029cfe9f94cb",
                "mi-0359c029cfe9f94cb",
                "mi-0badcfeaa8820fb83",
                "mi-0badcfeaa8820fb83",
            ],
        },
        "severity": 10,
        "createdAt": "2019-11-07T17:13:53.948Z",
        "updatedAt": "2019-11-09T17:41:09.360Z",
        "title": "A user has reported a defacement of fluffykitten securities main www site.",
        "description": "All images on the site have been replaced with dogs instead of fluffy cats.",
        "detail": {},
        "remediation": {
            "risk": "MAXIMUM",
            "success": True,
            "evidence": {
                "artifact_count": 2,
                "objects": [
                    "b2b7236dda0e4eff8aa17738d9ad18c5/ip-172-31-46-36.us-west-2.compute.internal-capture.pcap",
                    "b2b7236dda0e4eff8aa17738d9ad18c5/ip-172-31-47-140.us-west-2.compute.internal-capture.pcap",
                ],
            },
        },
    },
    "ts": "1573943386.000100",
}


class TestEvidenceProcessor(object):
    def test_processing_evidence(self):
        from lambda_handler.pcap import Analyze

        if EVENT_FIXTURE["detail"]["remediation"]["evidence"]["objects"] != []:
            for object_key in EVENT_FIXTURE["detail"]["remediation"]["evidence"][
                "objects"
            ]:
                full_path = f"s3://public.demo.reinvent2019/{object_key}"
                a = Analyze(full_path)
                a.get_geoip_database()
                a.load_pcap()
                extraction = a.get_extraction()
                result = a.extraction_to_json(extraction)
                a.json_to_parquet(result)
                a.upload_all_processed()
