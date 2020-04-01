from aws_cdk import (
    aws_iam as iam,
    aws_sagemaker as sagemaker,
    core
)

class SageMakerStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, users, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        nb_role = iam.Role(self, id, assumed_by=iam.ServicePrincipal('sagemaker.amazonaws.com'))
        # XXX: add ro access to some S3 bucket

        for user_data in users:
            user = user_data['email']
            iam_user = iam.User(self, user, user_name=user, password=core.SecretValue.plain_text(user_data['password']))

            nb = sagemaker.CfnNotebookInstance(self, 'nb_%s' % user,
                                               instance_type='ml.t2.medium',
                                               role_arn=nb_role.role_arn,
                                               notebook_instance_name='nb-%s-%s' % (id, user.translate(str.maketrans('@.', '--'))))
            nb_policy = iam.Policy(self, 'nb_policy_%s' % user, statements=[
                iam.PolicyStatement(actions=['sagemaker:CreatePresignedNotebookInstanceUrl'], 
                                    resources=[nb.ref]),
                iam.PolicyStatement(actions=['sagemaker:ListNotebookInstances'], resources=["*"])
            ])
            iam_user.attach_inline_policy(nb_policy)
