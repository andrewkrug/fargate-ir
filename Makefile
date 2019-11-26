
ROOT_DIR	:= $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PY_DIR			:= python/lib/python3.7/site-packages


all:
	@echo 'Available make targets:'
	@grep '^[^#[:space:]^\.PHONY.*].*:' Makefile\

.PHONY: setup
setup:
	aws cloudformation create-stack --stack-name FargateIRStepFunctionDeployment \
	--template-body file://cloudformation/step-function-deployment.yml

.PHONY: get-code-bucket-name
get-code-bucket-name:
	aws cloudformation describe-stacks --stack-name FargateIRStepFunctionDeployment \
	| jq '.Stacks[0].Outputs[0].OutputValue' | tr -d '"'

.PHONY: clean
clean:
	rm -rf aws_sam/fargateIR/.aws-sam
	rm -rf aws_sam/fargateIR/general_layer/python
	rm -rf aws_sam/fargateIR/pandas_layer/python

.PHONY: cache-depends
cache-depends: clean
	mkdir -p $(ROOT_DIR)/aws_sam/fargateIR/pandas_layer/$(PY_DIR)
	pip3 install -r $(ROOT_DIR)/aws_sam/fargateIR/pandas_layer/requirements.txt -t $(ROOT_DIR)/aws_sam/fargateIR/pandas_layer/$(PY_DIR)/
	mkdir -p $(ROOT_DIR)/aws_sam/fargateIR/general_layer/$(PY_DIR)
	pip3 install -r $(ROOT_DIR)/aws_sam/fargateIR/general_layer/requirements.txt -t $(ROOT_DIR)/aws_sam/fargateIR/general_layer/$(PY_DIR)/

.PHONY: create-layer
create-layer:
	docker run -v $(ROOT_DIR):/var/task lambci/lambda:build-python3.7  bash -c "make cache-depends"

.PHONY: build
build: create-layer
	cd aws_sam/fargateIR/ && sam build --use-container

.PHONY: package
package:
	cd aws_sam/fargateIR/ && rm -f packaged.yml
	cd aws_sam/fargateIR/ && \
	sam package --s3-bucket \
	`aws cloudformation describe-stacks --stack-name FargateIRStepFunctionDeployment \
	| jq '.Stacks[0].Outputs[0].OutputValue' | tr -d '"'`  --output-template packaged.yml

.PHONY: deploy
deploy:
	aws cloudformation deploy \
	--template-file $(ROOT_DIR)/aws_sam/fargateIR/packaged.yml \
	--stack-name fargateResponderFunction --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM

.PHONY: setup-test
setup-test:
	pip install pytest pytest-mock pytest-watch flake8 black boto3 moto
	pip install -r $(ROOT_DIR)/aws_sam/fargateIR/lambda_handler/requirements.txt

.PHONY: run-test
run-test:
	black aws_sam/fargateIR/lambda_handler/*.py
	black aws_sam/fargateIR/tests/unit/*.py
	cd aws_sam/fargateIR/ flake8 .
	cd aws_sam/fargateIR/ && python -m pytest tests/ -v

.PHONY: test-watch
test-watch:
	docker run -v $(ROOT_DIR):/var/task lambci/lambda:build-python3.7 bash -c "make setup-test && cd aws_sam/fargateIR/ && ptw --runner python -m pytest tests/ -v -- --capture=no"

.PHONY: test
test:
	docker run -v $(ROOT_DIR):/var/task lambci/lambda:build-python3.7 bash -c "make setup-test && make run-test"

.PHONY: install-sam
install-sam:
	rm -rf awscli-bundle
	curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
	unzip awscli-bundle.zip
	./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws
	sam --version

.PHONY: run-local-lambda
run-local-lambda:
	cd aws_sam/fargateIR/ && sam local start-lambda &

.PHONY: run-local-state-machine
run-local-state-machine:
	docker run -d --rm --name state-machine --env-file localsettings.txt -p 8083:8083 amazon/aws-stepfunctions-local

.PHONY: kill-local-lambda
kill-local-lambda:
	ps aux | grep -i 'sam local' | grep -v 'grep' | awk '{print $$2}' | xargs kill -9

.PHONY: test-state-machine
test-state-machine:
	@echo "foo"

.PHONY: create-local-state-machine
create-local-state-machine:
	aws stepfunctions create-state-machine --endpoint http://localhost:8083 --definition file://aws_sam/fargateIR/tests/state-machine.json --name "fargateIR" --role-arn "arn:aws:iam::012345678901:role/DummyRole"

.PHONY: update-local-state-machine
update-local-state-machine:
	aws stepfunctions update-state-machine --endpoint http://localhost:8083 --definition file://aws_sam/fargateIR/tests/state-machine.json \
    --role-arn "arn:aws:iam::012345678901:role/DummyRole" --state-machine-arn arn:aws:states:us-east-1:123456789012:stateMachine:fargateIR

.PHONY: delete-local-state-machine
delete-local-state-machine:
	aws stepfunctions delete-state-machine --endpoint http://localhost:8083 --state-machine-arn arn:aws:states:us-east-1:123456789012:stateMachine:fargateIR

