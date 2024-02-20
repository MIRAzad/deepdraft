from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

import json

with open('./config.json', 'r') as file:
    config = json.load(file)

references_count=config['references_count']
embedding_shape=config['embedding_shape']
# 1024 for sentence_transfrmers 

def get_similar_documents(query_embeddings, document_embeddings_dict):
    document_embeddings = [i['embedding'] for i in document_embeddings_dict]
    document_embeddings=np.array(document_embeddings)
    # print("document_embeddings SHAPE: ", document_embeddings.shape)
    document_embeddings = document_embeddings.reshape( -1, embedding_shape)
    # 1536
    
    sim = cosine_similarity(query_embeddings,document_embeddings)
    # accuracy=np.max(sim)
    # print(accuracy) 
    # print('SIM: ',sim)
    arr=np.argsort(sim)[0][references_count:]


    # print('embeddings SIMILARITY ARRAY:',arr)


    similar_chunk_dict = [document_embeddings_dict[i] for i in arr]

    return similar_chunk_dict

