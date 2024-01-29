from sentence_transformers import SentenceTransformer
from openai import OpenAI
import os
from concurrent.futures import ThreadPoolExecutor, as_completed



# def generate_doc_embeddings(recursive_list_of_chunk):
#     openai_key = os.environ.get('OPENAI_API_KEY')

#     client = OpenAI(  api_key=openai_key  )

#     # j=1
#     for child_chunk in recursive_list_of_chunk:

#         # j+=1
#         response = client.embeddings.create(input=child_chunk['child_chunk'],  model="text-embedding-ada-002")
#         child_chunk['embedding']=response.data[0].embedding 


#     return recursive_list_of_chunk  


def generate_doc_embeddings(child_chunk_list):
    openai_key = os.environ.get('OPENAI_API_KEY')
    client = OpenAI(api_key=openai_key)

    def process_chunk(child_chunk):
        response = client.embeddings.create(input=child_chunk['child_chunk'], model="text-embedding-ada-002")
        child_chunk['embedding'] = response.data[0].embedding
        return child_chunk

    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_chunk = {executor.submit(process_chunk, chunk): chunk for chunk in child_chunk_list}
        for future in as_completed(future_to_chunk):
            try:
                result = future.result()
            except Exception as exc:
                print(f"Chunk failed with exception: {exc}")

    return child_chunk_list

# def generate_doc_embeddings(child_chunk_list):
#     child_chunk_list_with_embeddings = generate_doc_embeddings(child_chunk_list)
#     return child_chunk_list_with_embeddings