# AWS API Gateway

Here we defined an API Gateway that uses custom domain name and hosts documentation for the API using Swagger hosted UI hosted on S3 bucket.

## API Specifications

We store the API specifications in the api-spec directory which contains your OpenAPI specifications. The structure is as follows:

The paths subdirectory has separate .yaml files for each endpoint of your API. For instance, `hello.yaml` contains specifications for the `/hello` endpoint, and `goodbye.yaml` for the `/goodbye` endpoint.

The components subdirectory contains separate files for each type of component. For instance, the schemas subdirectory contains individual .yaml files for each schema.
If you're not using Route53, remember to map your CNAME accordingly.

### Bundling and Validating OpenAPI 3.0 Schema Files

It's essential to combine your OpenAPI specifications into a single bundled.yaml file. Use the following command:

```bash
openapi bundle main.yaml -o bundled.yaml
```

Ensure that your files are error-free with the following validation command:

```bash
openapi lint bundled.yaml
```

If not already installed, you can get the OpenAPI CLI using:

```bash
npm install -g @redocly/openapi-cli
```

### Configuring CNAME for Your API (if using DNS hosted service other than AWS Route53)

Create a CNAME record with the docs subdomain pointing to the domain name specified by the CloudFront of you API Gateway.

## Hosting API docs

### Hosting API Documentation with Swagger UI on S3

Follow these steps to host your API documentation using Swagger UI:

1. Visit the Swagger UI download page: https://swagger.io/tools/swagger-ui/.
2. Download Swagger UI and locate the dist directory.
3. In the dist directory, update swagger-initializer.js by setting url: "bundled.yaml".
4. Upload all contents of the dist directory, along with the bundled.yaml file, to the API documentation S3 bucket.

### Configuring CNAME for Your Documentation URL

If you're not using Route53 for DNS management, follow these steps:

Create a CNAME record with the docs subdomain pointing to the domain name specified by the MyCloudFrontDistributionOutput value. This value is returned by running the sam deploy command.

## AWS SAM

This guide provides a quick reference on how to use AWS SAM to manage and deploy your serverless applications.

### Prerequisites

- AWS Account - [Sign up here if you don't have one](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html)
- AWS CLI - [Install guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
- AWS SAM CLI - [Install guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)

### Setup

Before you can use AWS SAM, make sure your AWS credentials are configured. Run `aws configure` and follow the prompts to enter your AWS Access Key ID, Secret Access Key, and default region.

```bash
aws configure
```

### Building Your SAM Application

Navigate to the project directory (**codextranauts/chatgpt/aws**) and use the sam build command to build your application:

```bash
cd aws
sam build
```

This prepares your application for deployment by compiling source code, downloading dependencies, and packaging it with any necessary resources.

### Testing Your SAM Application Locally

Before deploying your application, you can test it locally using the sam local invoke command:

```bash
sam local invoke
```

### Deploying Your SAM Application

To deploy your application, use the sam deploy command:

```bash
sam deploy
```

This command will package your application, upload it to the specified S3 bucket, and create or update a CloudFormation stack to manage your application's resources.

### Useful Links

- [AWS SAM Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)
- [AWS CLI Documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)
- [AWS Console](https://console.aws.amazon.com/)
