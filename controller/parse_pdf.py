# input (string), output (list)
from langchain.text_splitter import RecursiveCharacterTextSplitter

import tiktoken


from unstructured.documents.elements import NarrativeText, Text, Title, Image, FigureCaption, Table, Header, Footer, ListItem
from unstructured.partition.pdf import partition_pdf
from unstructured.chunking.title import chunk_by_title

from typing import Dict, List

from docx import Document


enc = tiktoken.get_encoding("cl100k_base")

def parse_pdf(pdf_data):
    def length_function(text: str) -> int:
        return len(enc.encode(text))


    splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", " ", ""],
        chunk_size=500, 
        chunk_overlap=125,
        length_function=length_function,
    )

    list_of_documents = splitter.split_text(pdf_data) 
    return list_of_documents


