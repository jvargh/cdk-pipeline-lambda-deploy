from aws_cdk import core
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines

from .pipeline_lambda_stage import LambdaServiceStage
import aws_cdk.aws_codecommit as codecommit

APP_ACCOUNT = 'AWS Account'
REGION = 'us-east-1'
CODECOMMIT_REPO = 'cdk_lambda_pipeline_repo'

class PipelineStack(core.Stack):
  def __init__(self, scope: core.Construct, id: str, **kwargs):
    super().__init__(scope, id, **kwargs)

    source_artifact = codepipeline.Artifact()
    cloud_assembly_artifact = codepipeline.Artifact()

    repo_arn = f"arn:aws:codecommit:{REGION}:{APP_ACCOUNT}:{CODECOMMIT_REPO}"
    repo = codecommit.Repository.from_repository_arn(self, "cdk-lambda-pipeline", repo_arn)

    pipeline = pipelines.CdkPipeline(self, 'Pipeline',
      cloud_assembly_artifact=cloud_assembly_artifact,
      pipeline_name='CDK_Lambda_Pipeline',

      source_action = cpactions.CodeCommitSourceAction(
        action_name='CodeCommit', 
        repository=repo, 
        branch='master',
        output=source_artifact
      ),

      synth_action=pipelines.SimpleSynthAction(
        source_artifact=source_artifact,
        cloud_assembly_artifact=cloud_assembly_artifact,
        install_command='npm install -g aws-cdk && pip install -r requirements.txt',
        # build_command='pytest unittests',
        synth_command='cdk synth'
      )      
    )

    pre_prod_app = LambdaServiceStage(self, 'Pre-Prod', env={
      'account': APP_ACCOUNT,
      'region': REGION,
    })

    pre_prod_stage = pipeline.add_application_stage(pre_prod_app)

    # pre_prod_stage.add_actions(pipelines.ShellScriptAction(
    #   action_name='Integ',
    #   run_order=pre_prod_stage.next_sequential_run_order(),
    #   additional_artifacts=[source_artifact],
    #   commands=[
    #     'pip install -r requirements.txt',
    #     'pytest integtests',
    #   ],
    #   use_outputs={
    #     'SERVICE_URL': pipeline.stack_output(pre_prod_app.url_output)
    #   }))

    # pre_prod_stage.add_manual_approval_action(action_name="PromoteToProd")

    # pipeline.add_application_stage(LambdaServiceStage(self, 'Prod', env={
    #   'account': APP_ACCOUNT_PROD,
    #   'region': REGION_PROD,
    # }))



