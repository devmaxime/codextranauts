from aws.api.v1.src.lambdas.bye_world.app import lambda_handler


def test_lambda_handler_success():
    event = {'test': 'value'}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert response['body'] == '{"message": "Bye, World!"}'


def test_lambda_handler_empty_event():
    event = {}
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert response['body'] == '{"message": "Bye, World!"}'


def test_lambda_handler_null_event():
    event = None
    context = {}
    response = lambda_handler(event, context)
    assert response['statusCode'] == 200
    assert response['body'] == '{"message": "Bye, World!"}'
