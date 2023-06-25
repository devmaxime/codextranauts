You need to create an .env file in the root directory of the project and add the following variables:
```
OPENAI_API_KEY
ACTIVELOOP_TOKEN
```

You can replace all the settings in config.py using env variables.
Settings by default:
```
    environment: str = "dev"
    vector_db: str = "deeplake"
    llm_model_name: str = "gpt-3.5-turbo"
    template_name: str = "template_2"
```