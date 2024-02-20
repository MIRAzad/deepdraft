import os
import asyncio
from openai import OpenAI

async def generate_embeddings(client, chunk):
    response = await client.embeddings.create(input=chunk['child_chunk'], model="text-embedding-ada-002")
    embedding_dict = {
        'embedding': response.data[0].embedding,
        'chunk_id': chunk['chunk_id'],
        'child_chunk': chunk['child_chunk']
    }
    return embedding_dict

async def generate_doc_embeddings(recursive_list_of_chunk):
    openai_key = os.environ.get('OPENAI_API_KEY')
    client = OpenAI(api_key=openai_key)

    tasks = []
    for chunk in recursive_list_of_chunk:
        tasks.append(generate_embeddings(client, chunk))

    document_embeddings_dict = await asyncio.gather(*tasks)
    return document_embeddings_dict

# Assuming recursive_list_of_chunk is populated with your data
# Split recursive_list_of_chunk into batches of size 10
batch_size = 10
chunks = [recursive_list_of_chunk[i:i + batch_size] for i in range(0, len(recursive_list_of_chunk), batch_size)]

# Call generate_doc_embeddings for each batch concurrently
results = []
loop = asyncio.get_event_loop()
for chunk_batch in chunks:
    result = loop.run_until_complete(generate_doc_embeddings(chunk_batch))
    results.extend(result)

print(results)



