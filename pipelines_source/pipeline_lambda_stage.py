from aws_cdk import core

from .pipeline_lambda_stack import PipelineLambdaStack

class LambdaServiceStage(core.Stage):
  def __init__(self, scope: core.Construct, id: str, **kwargs):
    super().__init__(scope, id, **kwargs)

    service = PipelineLambdaStack(self, 'PipelineLambdaService')

    self.url_output = service.url_output

