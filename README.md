
# Provisioning IAM & SageMaker via CloudFormation with CDK

1. Install CDK: https://github.com/aws/aws-cdk
2. Put credentials in `firebase_credentials.json`
3. Setup virualenv and requirements:
```
$ python3 -m venv .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.
```
$ cdk synth
```

Or deploy
```
$ cdk deploy
```
