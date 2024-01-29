from unstructured.documents.elements import NarrativeText, Title
from unstructured.partition.pdf import partition_pdf
from unstructured.staging.base import elements_to_json
import json
from unstructured.partition.auto import partition


# elements = partition(filename="example-10k.html")


def parse_pdf(data):
    elements = partition(filename=data, strategy="fast")

    # elements = partition_pdf(filename=data, strategy="fast")
    
    return elements



chunk_list = parse_pdf('./pdfFiles/A28 Solicitation 06-30-2020.pdf')

# print(chunk_list)
    # Save the data to a JSON file
filename = "outputs3.json"
elements_to_json(chunk_list, filename=filename)
    