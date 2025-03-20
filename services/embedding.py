from chromadb.utils import embedding_functions
default_ef = embedding_functions.DefaultEmbeddingFunction()

def get_embedding(text : str):
    val = default_ef([text])
    print(val)
    return val[0].tolist()




