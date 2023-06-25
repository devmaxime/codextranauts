import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPEN_AI_MODEL")


def get_embedding_openAI(texts, model=MODEL):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']


def test_embedding_openAI():
    text = "ciao"
    embedding = get_embedding_openAI(text)
    print(embedding)

# if __name__ == '__main__':
#     test_embedding_openAI()
