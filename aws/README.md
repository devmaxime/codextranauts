# AWS API Gateway

Here we defined an API Gateway that uses custom domain name and hosts documentation for the API using Swagger hosted UI hosted on S3 bucket.

API Specifications
We store the API specifications in the api-spec directory which contains your OpenAPI specifications. The structure is as follows:

The paths subdirectory has separate .yaml files for each endpoint of your API. For instance, hello.yaml contains specifications for the /hello endpoint, and goodbye.yaml for the /goodbye endpoint.

The components subdirectory contains separate files for each type of component. For instance, the schemas subdirectory contains individual .yaml files for each schema.
If you're not using Route53, remember to map your CNAME accordingly.

Bundling and Validating OpenAPI 3.0 Schema Files
It's essential to combine your OpenAPI specifications into a single bundled.yaml file. Use the following command:
`openapi bundle main.yaml -o bundled.yaml`

Ensure that your files are error-free with the following validation command:
`openapi lint bundled.yaml`

If not already installed, you can get the OpenAPI CLI using:
`npm install -g @redocly/openapi-cli`

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
