import logging
from typing import  List
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

with open('./config.json', 'r') as file:
    config = json.load(file)

k_mmr=config['k_mmr']
lambda_mult_mmr=config['lambda_mult_mmr']

def maximal_marginal_relevance(
    query_embedding: np.ndarray,
    embedding_list: list,
    lambda_mult: float,
    k: int,
) -> List[int]:
    """Calculate maximal marginal relevance."""
    try:
        if min(k, len(embedding_list)) <= 0:
            return []
        if query_embedding.ndim == 1:
            query_embedding = np.expand_dims(query_embedding, axis=0)
        similarity_to_query = cosine_similarity(query_embedding, embedding_list)[0]
        most_similar = int(np.argmax(similarity_to_query))

        idxs = [most_similar]

        selected = np.array([embedding_list[most_similar]])

        while len(idxs) < min(k, len(embedding_list)):
            best_score = -np.inf
            idx_to_add = -1
            similarity_to_selected = cosine_similarity(embedding_list, selected)

            for i, query_score in enumerate(similarity_to_query):
                if i in idxs:
                    continue
                redundant_score = max(similarity_to_selected[i])
                equation_score = (
                    lambda_mult * query_score - (1 - lambda_mult) * redundant_score
                )
                if equation_score > best_score:
                    best_score = equation_score
                    idx_to_add = i
            idxs.append(idx_to_add)
            selected = np.append(selected, [embedding_list[idx_to_add]], axis=0)
        return idxs

    except Exception as err:
        logging.error(
            "maximal_marginal_relevance function encountered an error: %s", str(err)
        )
        logging.exception(err)

        return []


def get_relevant_references(query_embeddings, similar_chunk_dict ):
    # print("similar documents data: ",similar_documents)

    document_embeddings = [i['embedding'] for i in similar_chunk_dict]
    document_embeddings=np.array(document_embeddings)
    document_embeddings = document_embeddings.reshape( -1, 1536)
    
    
    mmr_index = maximal_marginal_relevance(query_embeddings, document_embeddings, lambda_mult_mmr, k_mmr)

    MMR_chunk_dict= [similar_chunk_dict[i] for i in mmr_index]
        
    return MMR_chunk_dict






