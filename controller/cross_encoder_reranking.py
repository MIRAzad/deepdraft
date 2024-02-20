import torch 
from transformers import AutoModelForSequenceClassification, AutoTokenizer

import numpy as np
import json

with open('./config.json', 'r') as file:
    config = json.load(file)

cross_encoder_rerank_model = config['cross_encoder_rerank_model']
crossencoder_references_count=config['crossencoder_references_count']



tokenizer = AutoTokenizer.from_pretrained(cross_encoder_rerank_model)
model = AutoModelForSequenceClassification.from_pretrained(cross_encoder_rerank_model)
model.eval()


def rerank_references(user_query, mmr_document_embeddings_dict ):
    score_list=[]
    for i in mmr_document_embeddings_dict:
        with torch.no_grad():
            inputs = tokenizer([[user_query,i['child_chunk']]], padding=True, truncation=True, return_tensors='pt', max_length=512)
            scores = model(**inputs, return_dict=True).logits.view(-1, ).float()
            score_list.append(scores.item() )
            
    arr=np.argsort(score_list)[crossencoder_references_count:]
    
    # print('SCORE LIST CROSS ENCODER: ',score_list)
    
    reranked_child_chunks=[mmr_document_embeddings_dict[i] for i in arr]
                                                    
    return reranked_child_chunks
