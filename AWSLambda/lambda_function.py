from main import main


def lambda_handler(event, context):
    try:
        main()

        return {
            'statusCode': 200,
            'body': 'Lambda function executed successfully!'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }