import json
from typing import Dict, List
from unstructured.documents.elements import NarrativeText, Title
from unstructured.partition.pdf import partition_pdf
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tiktoken

with open('./config.json', 'r') as file:
    config = json.load(file)

recursive_text_splitter_chunk_size = config['recursive_text_splitter_chunk_size']
recursive_text_splitter_overlap = config['recursive_text_splitter_overlap'] 

enc = tiktoken.get_encoding("cl100k_base")


def split_chunk(pdf_data):
    def length_function(text: str) -> int:
        return len(enc.encode(text))

# make chunk document script file
    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=recursive_text_splitter_chunk_size, 
        chunk_overlap=recursive_text_splitter_overlap,
        length_function=length_function,
    )

    list_of_documents = splitter.split_text(pdf_data) 
    return list_of_documents


def parse_pdf(data) -> List[Dict]:
    elements = partition_pdf(filename=data, strategy="fast")
    filtered_data = {}
    chunk_list=[]
    temp=''
    i=0
    for  item in elements:
        filtered_data = {}
   
        if isinstance(item, Title):
            words = temp.split()
            if len(words) > 200:
                filtered_data["chunk"] = temp
                i+=1
                filtered_data["chunk_id"] = i
                filtered_data["page_no"] = item.metadata.page_number

                chunk_list.append(filtered_data)
                temp=''
            temp+=item.text
            temp+='---'
            
            
        elif isinstance(item, NarrativeText):
            temp+=item.text
            
        else:
            temp+=item.text
        
    filtered_data["chunk"] = temp
    i+=1
    filtered_data["chunk_id"] = i
    filtered_data["page_no"] = item.metadata.page_number

    chunk_list.append(filtered_data)
    
    return chunk_list


def recursive_split_chunk(chunk_list):
    recursive_list_of_chunk=[]
    splitted_chunk={}
    for item in chunk_list:
        words = item['chunk'].split()
        # decrease 50 if  needed
        if len(words) - 150 >50:
            chunk_size=len(words)
            splitted_chunk_list= split_chunk(item['chunk'])
            for tokens in splitted_chunk_list:
                splitted_chunk={}
                splitted_chunk['child_chunk']=tokens
                splitted_chunk['chunk_id']=item['chunk_id']
                recursive_list_of_chunk.append(splitted_chunk)
        else:
                splitted_chunk={}
                splitted_chunk['child_chunk']=item['chunk']
                splitted_chunk['chunk_id']=item['chunk_id']
                recursive_list_of_chunk.append(splitted_chunk)
                    
    
    return recursive_list_of_chunk 
    

      
def parse_pdf_unstructured(file_name):
    chunk_list = parse_pdf(file_name)
    
    recursive_list_of_chunk=recursive_split_chunk(chunk_list)
        
    # with open('recursive_list_of_chunk.json', 'w') as json_file:
    #     json.dump(recursive_list_of_chunk, json_file)
    return  recursive_list_of_chunk ,chunk_list



