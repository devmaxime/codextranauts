# AWS Serverless Application Model (SAM) Usage Guide

This guide provides a quick reference on how to use AWS SAM to manage and deploy your serverless applications.

## Prerequisites

- AWS Account - [Sign up here if you don't have one](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html)
- AWS CLI - [Install guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
- AWS SAM CLI - [Install guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

## Setup

Before you can use AWS SAM, make sure your AWS credentials are configured. Run `aws configure` and follow the prompts to enter your AWS Access Key ID, Secret Access Key, and default region.

```bash
aws configure
```

## Building Your SAM Application

Navigate to the project directory (**codextranauts/chatgpt/aws**) and use the sam build command to build your application:

```bash
cd aws
sam build
```

This prepares your application for deployment by compiling source code, downloading dependencies, and packaging it with any necessary resources.

## Testing Your SAM Application Locally

Before deploying your application, you can test it locally using the sam local invoke command:

```bash
sam local invoke
```

## Deploying Your SAM Application

To deploy your application, use the sam deploy command:

```bash
sam deploy
```

This command will package your application, upload it to the specified S3 bucket, and create or update a CloudFormation stack to manage your application's resources.

## Useful Links

- [AWS SAM Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)
- [AWS CLI Documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)
- [AWS Console](https://console.aws.amazon.com/)
