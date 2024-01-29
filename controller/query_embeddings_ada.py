# from sentence_transformers import SentenceTransformer
import numpy as np
import openai
from openai import OpenAI
import json
import os

# ST_model_name=config['ST_model_name']

# model = SentenceTransformer(ST_model_name)


def generate_query_embeddings(user_query):
    openai_key = os.environ.get('OPENAI_API_KEY')

    # openai.api_key=openai_key
    client = OpenAI(  api_key=openai_key  )
    response = client.embeddings.create(input=user_query, model="text-embedding-ada-002")

    # response= openai.Embedding.create(input=user_query,  model="text-embedding-ada-002")
    # query_embeddings= response['data'][0]['embedding']
    query_embeddings = response.data[0].embedding 
    query_embeddings =np.array(query_embeddings)
    query_embeddings = query_embeddings.reshape(1, -1)
    
    return query_embeddings