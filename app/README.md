# Codextranauts - APP - Where the langchains components are located.
Use it as an API.

## Installation
This is a FastAPI folder. To run it, you need to install the requirements located in requirements.txt :
```
pip install -r requirements.txt
```

## Configuration

You need to create an .env file in the root directory of the project and add the following variables:
```
OPENAI_API_KEY
PINECONE_API_KEY #Only if you intend to use Pinecone
ACTIVELOOP_TOKEN #Only if you intend to use Deeplake (As backup for Pinecone)
```

All other settings are located in config.py. You can change them there or by using env variables that will override the default settings.

Settings by default:
```
    environment: str = "dev"
    vector_db: str = "pinecone"
    llm_model_name: str = "gpt-3.5-turbo"
    template_name: str = "template_2"
    ...
    and more
```

## Run

Once you have installed the requirements and configured the .env file, you can run the app with:
```
python -m uvicorn main:app --reload
```

This will run the app in the port 8000. You can access the docs in http://localhost:8000/docs

You can test the app by using the following curl command:
```
curl -X 'GET' \
  'http://localhost:8000/ping' \
  -H 'accept: application/json'
```

## Prompt Engineering

You can modify the template and the prompt by changing the files located in the templates folder.
It is recommended to create a new template file when you want to modify the template. You can use the template_2.py file as a base.

## Deploy

You can deploy the app in any server. We recommend using Docker. You can find a Dockerfile and a Dockerfile.prod in the root directory of the project.