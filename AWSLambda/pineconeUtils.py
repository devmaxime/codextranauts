def insert_vectors(index, ids, vectors):
    upsert_response = index.upsert(ids=ids, vectors=vectors)
    print(upsert_response)
