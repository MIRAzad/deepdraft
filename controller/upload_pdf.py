from langchain.document_loaders import PyPDFLoader

                                                                                                                                                
def upload_pdf(pdf_name):
    loader = PyPDFLoader(pdf_name)
    pages = loader.load_and_split()

    pdf_data=''
    for i in pages:
        pdf_data+=i.page_content
        
    return pdf_data