from sentence_transformers import SentenceTransformer
import numpy as np


import json

# Read the JSON configuration file
with open('./config.json', 'r') as file:
    config = json.load(file)


ST_model_name=config['ST_model_name']


# TOKEN LENGTH SHOULD NOT BE MORE THAN 516
model = SentenceTransformer(ST_model_name)



def generate_doc_embeddings(recursive_list_of_chunk):
    # PDF EMBEDDINGS
    document_embeddings_dict=[]
    j=1
    for child_chunk in recursive_list_of_chunk:
        embedding_dict={}

        # print("embeddings generated for chunk: ",j)
        j+=1
        response = model.encode(child_chunk['child_chunk'], normalize_embeddings=True)
        embedding_dict['embedding']=response
        embedding_dict['chunk_id']=child_chunk['chunk_id']
        embedding_dict['child_chunk']=child_chunk['child_chunk']
        document_embeddings_dict.append( embedding_dict)


    return document_embeddings_dict


