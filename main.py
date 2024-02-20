from controller.query_embeddings_ada import generate_query_embeddings
from controller.similarity_search import get_similar_documents
from controller.mmr import get_relevant_references
# from controller.cross_encoder_reranking import rerank_references
# from controller.get_answer_gpt import get_answer

import json
from openai import OpenAI
import openai

# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas


def rag_pipeline(user_query, pdf_name):
    
    with open(f'./documents/{pdf_name}/parent_chunk_list.json', 'r') as json_file:
        parent_chunk_list = json.load(json_file)
    
    with open(f'./documents/{pdf_name}/document_embeddings_dict.json', 'r') as json_file:
        document_embeddings_dict = json.load(json_file)

    
    # with open(f'./documents/{pdf_name}/child_chunk_list.json', 'r') as json_file:
    #     child_chunk_list = json.load(json_file)
        

    


    query_embeddings = generate_query_embeddings(user_query)
    print('pass 3')

    # Cosine Similarity
    
    similar_chunk_dict = get_similar_documents(query_embeddings, document_embeddings_dict)

    print('pass 4')

    # MMR
    MMR_chunk_dict = get_relevant_references(query_embeddings, similar_chunk_dict )
    print('pass 5')
    # here we get splitted list, what is the fun of chunkingbgathering then before MMR?



    # Cross Encoder
    # reranked_relevant_reference_chunks = rerank_references(user_query, MMR_chunk_dict )
    print('pass 6')
    # remove redundancy
    chunk_ids = [i['chunk_id'] for i in MMR_chunk_dict]
    parent_chunk_ids=set(chunk_ids)


    # Use a list comprehension to filter dictionaries by chunk_id
    references_selected_for_answer_generation = [item['chunk'] for item in parent_chunk_list if item['chunk_id'] in parent_chunk_ids]
    print(len(references_selected_for_answer_generation))



    # merge the list of references to string
    separator = ", "
    merged_references = separator.join(references_selected_for_answer_generation)

    # answer = get_answer(user_query, merged_references)
    
    
    return merged_references, references_selected_for_answer_generation





def validate_openai_key(openai_key):
    client = OpenAI(  api_key=openai_key  )
    try:
        # Attempt a simple API call to verify the key
        client.chat.completions.create(model="text-davinci-003", messages=[{"role": "system", "content": "Test"}])
        return True  # Key is valid
    except openai.APIError as e:
        print("Invalid OpenAI key:", e)
        return False  # Key is invalid



# generate a response
def check_previous_context(prompt,merged_previous_chat):
    prompt=[]
    prompt=[{"role": "system", "content": """You are a helpful assistant "
                                     "the user will provide you with a user query and a context, your job is to decide whether the user query can be answered from the given context or  you require additional context.
                                     "your response should be boolean:
                                     True (if you can answer the query from the provided context)
                                     False (if you cannot answer the query from the provided context)"
                                     """},
            ]
    prompt_with_previous_chat=  f"USER INPUT:{prompt}. \n\n\n\n CONTEXT:{merged_previous_chat}"
    prompt.append({"role": "user", "content": prompt_with_previous_chat})
    
    completion = client.chat.completions.create(
        model=model,
        messages=st.session_state['messages_app']   
    )   
    response = completion.choices[0].message.content
    print(response)
    return response






def create_pdf_from_list(data_list, file_name):
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter

    # Set up the text style
    c.setFont("Helvetica", 12)

    y_offset = height - 100  # Initial y-coordinate for text

    for index, item in enumerate(data_list):
        # Split the text into lines manually to fit the width
        lines = []
        line = ""
        for word in item.split():
            if c.stringWidth(line + word, "Helvetica", 12) < (width - 120):
                line += word + " "
            else:
                lines.append(line)
                line = word + " "
        if line:
            lines.append(line)

        required_height = len(lines) * 12

        if y_offset - required_height < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_offset = height - 100

        # c.drawString(100, y_offset, f"Index {index}:")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(70, y_offset, f"Response {index + 1}")
        c.setFont("Helvetica", 12)

        for line in lines:
            c.drawString(70, y_offset - 15, line.strip())
            y_offset -= 15

        y_offset -= 15  # Adjust for a line space between items

    c.save()