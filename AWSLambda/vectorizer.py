from transformers import AutoModel, AutoTokenizer, pipeline

model = AutoModel.from_pretrained("microsoft/codebert-base")
tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")


def tokenize(text):
    tokens = tokenizer.tokenize(text)
    return tokens


def get_tokens_ids(tokens):
    tokens_ids = tokenizer.convert_tokens_to_ids(tokens)
    return tokens_ids


# def get_embedding_vector(text):
#     tokens = tokenize(text)
#     tokens_ids = get_tokens_ids(tokens)
#     # context_embeddings = model(torch.tensor(tokens_ids)[None, :])[0]
#     context_embeddings = model.encode(text)
#     return context_embeddings


def get_embedding_vector(text):
    feature_extractor = pipeline("feature-extraction", model=model, tokenizer=tokenizer)

    # Generate the embeddings
    embeddings = feature_extractor(text)

    return embeddings[0]
