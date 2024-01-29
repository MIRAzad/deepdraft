from sentence_transformers import SentenceTransformer
import numpy as np

import json

with open('./config.json', 'r') as file:
    config = json.load(file)
ST_model_name=config['ST_model_name']


model = SentenceTransformer(ST_model_name)


def generate_query_embeddings(user_query):
    query_embeddings=model.encode(user_query, normalize_embeddings=True)
    
    
                             
    query_embeddings =np.array(query_embeddings)
    query_embeddings = query_embeddings.reshape(1, -1)
    
    return query_embeddings