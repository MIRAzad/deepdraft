from controller.parse_pdf_unstructured import parse_pdf_unstructured
from controller.doc_embeddings_ada import generate_doc_embeddings

import os
import json
     

def store_pdfs(uploaded_file):
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    file_name_without_extension = uploaded_file.name.replace('.pdf', '')

    # Save the uploaded PDF file to the processed_pdfs folder
    file_path = os.path.join('pdfFiles', uploaded_file.name)
    with open(file_path, "wb") as file:
        file.write(bytes_data)



    child_chunk_list ,parent_chunk_list = parse_pdf_unstructured(file_path)



    file_path = f"./documents/{file_name_without_extension}"
    os.mkdir(file_path)

    # Save the data to a JSON file
    with open(f'./documents/{file_name_without_extension}/child_chunk_list.json', 'w') as json_file:
        json.dump(child_chunk_list, json_file)
        
        # Save the data to a JSON file
    with open(f'./documents/{file_name_without_extension}/parent_chunk_list.json', 'w') as json_file:
        json.dump(parent_chunk_list, json_file)
        

    document_embeddings_dict = generate_doc_embeddings(child_chunk_list)

    print('pass 2')
    
    # Save the data to a JSON file
    with open(f'./documents/{file_name_without_extension}/document_embeddings_dict.json', 'w') as json_file:
        json.dump(document_embeddings_dict, json_file)

    return file_name_without_extension