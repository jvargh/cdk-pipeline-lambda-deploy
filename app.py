#!/usr/bin/env python3

from aws_cdk import core

# from pipelines_source.pipeline_lambda_stack import PipelineLambdaStack
from pipelines_source.pipeline_stack import PipelineStack

PIPELINE_ACCOUNT = '524517701320'
REGION = 'us-east-1'

app = core.App()
# PipelineLambdaStack(app, 'cdk-lambda-stack')
PipelineStack(app, 'cdk-lambda-pipeline-stack', env={
  'account': PIPELINE_ACCOUNT,
  'region' : REGION,
})

app.synth()
