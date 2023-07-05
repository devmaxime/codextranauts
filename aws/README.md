# AWS API Gateway

Here we defined an API Gateway that uses custom domain name.

## API specs

The api-spec directory contains your OpenAPI specification.

- The paths directory now has a separate .yaml file for each endpoint of your API. For example, hello.yaml would contain the specifications for the /hello endpoint, and goodbye.yaml would contain the specifications for the /goodbye endpoint.
- The components directory now has separate files for each type of component. In the schemas subdirectory, there's a separate .yaml file for each schema.

Make sure to map CNAME (in not using Route53)

## Preparing OpenAPI 3.0 schema file

Need to combine openAPI specs into one bundled.yaml
`openapi bundle main.yaml -o bundled.yaml`

Validate your files:
`openapi lint bundled.yaml`

To install:
`npm install -g @redocly/openapi-cli`

## Host documentaion on S3

TBD

## Implemet CI/CD

- Need to update documentation by uploading the latest bundled.yaml
- Need to run test
