import streamlit as st
from st_pages import add_page_title

add_page_title(layout="wide")

from main import rag_pipeline, validate_openai_key, create_pdf_from_list
# from controller.store_pdf import store_pdf
from openai import OpenAI
import streamlit as st
from streamlit_chat import message
import base64
import os

from st_pages import Page, add_page_title, show_pages

client=OpenAI()

st.sidebar.title("Sidebar")
os.environ['OPENAI_API_KEY']=st.secrets["OPENAI_API_KEY"]
# # Remove the OpenAI key from the environment variables
# os.environ.pop('OPENAI_API_KEY')




# Initialise session state variables
if 'stored_questions' not in st.session_state:
    st.session_state['stored_questions'] = []
if 'generated_questions' not in st.session_state:
    st.session_state['generated_questions'] = []
if 'past_questions' not in st.session_state:
    st.session_state['past_questions'] = []
if 'messages_questions' not in st.session_state:
    st.session_state['messages_questions'] = [{"role": "system", "content": """you are a helpful assistant
    
"""}]

# if 'references' not in st.session_state:
#     st.session_state['references'] = []



clear_button = st.sidebar.button("Clear Conversation", key="clear")


# reset everything
if clear_button:
    st.session_state['stored_questions']=[]
    st.session_state['generated_questions'] = []
    st.session_state['past_questions'] = []
    st.session_state['messages_questions'] = [{"role": "system", "content": """you are a helpful assistant"""
                                               }    ]


    # counter_placeholder.write(f"Total cost of this conversation: $    {st.session_state['total_cost']:.5f}")





pdf_name=st.session_state['option_pdf']


    # write pdf name in sessionnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn

# generate a response
def generate_response(prompt, merged_references_questions):
    prompt_with_references =  f"USER INPUT:{prompt}. \n\n\n\n CONTEXT:{merged_references_questions}"
    st.session_state['messages_questions'].append({"role": "user", "content": prompt_with_references})
    
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo-16k',
        messages=st.session_state['messages_questions']   
    )   
    response = completion.choices[0].message.content
    st.session_state['messages_questions'].pop()
    st.session_state['messages_questions'].append({"role": "user", "content": prompt})
    st.session_state['messages_questions'].append({"role": "assistant", "content": response})

    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    return response, total_tokens, prompt_tokens, completion_tokens


# container for chat history
response_container = st.container()
# container for text box
container = st.container()

with container:

    with st.form(key='my_formm', clear_on_submit=True):
        user_input = st.text_area("Query:", key='inputt', height=100)
        submit_button = st.form_submit_button(label='Sendd')

    if submit_button and user_input:
        
        
        separator = ", "
        merged_references_questions = separator.join(st.session_state['stored_outline'])
        print(merged_references_questions)
        # add context hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
        output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input, merged_references_questions)
        st.session_state['past_questions'].append(user_input)
        st.session_state['generated_questions'].append(output)
        # st.session_state['references'].append(references)
        # st.session_state['model_name'].append(model_name)
        # st.session_state['total_tokens'].append(total_tokens)


if st.session_state['generated_questions']:
    with response_container:
        for i in range(len(st.session_state['generated_questions'])):
            message(st.session_state["past_questions"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated_questions"][i], key=str(i))
            if st.toggle('Store Response', key=str(i)+'store'):
                st.session_state['stored_questions'].append(st.session_state["generated_questions"][i]) 
            # on = st.toggle('References', key=str(i)+'references')
            # for i in st.session_state['references'][i]:
            #     if on:
            #         st.success(i)
                        
            # st.write(f"Model used: {st.session_state['model_name'][i]}; Number of tokens: {st.session_state['total_tokens'][i]}; Cost: ${st.session_state['cost'][i]:.5f}")
            # counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")





# Opening file from file path
with open(f'./pdfFiles/{pdf_name}.pdf', "rb") as f:
    base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}"  style=" width: 100%; height: 400px;" type="application/pdf"></iframe>'

    # Embedding PDF in HTML
    # pdf_display =  f"""<embed sandbox="allow-scripts allow-same-origin"  class="pdfobject"  type="application/pdf"  title="Embedded PDF"
    # src="data:application/pdf;base64,{base64_pdf}"  style=" width: 100%; height: 400px;">"""

    # Displaying File
    st.sidebar.markdown(pdf_display, unsafe_allow_html=True)



# Create a PDF using the entire list content
create_pdf_from_list(st.session_state['stored_outline'], "output1.pdf")


if st.session_state['stored_outline']:
    # Opening file from file path
    with open('output1.pdf', "rb") as f:
        base64_pdf_outline = base64.b64encode(f.read()).decode('utf-8')
        pdf_display_outline = F'<iframe src="data:application/pdf;base64,{base64_pdf_outline}"  style=" width: 100%; height: 400px;" type="application/pdf"></iframe>'

        # Embedding PDF in HTML
        # pdf_display =  f"""<embed sandbox="allow-scripts allow-same-origin"  class="pdfobject"  type="application/pdf"  title="Embedded PDF"
        # src="data:application/pdf;base64,{base64_pdf}"  style=" width: 100%; height: 400px;">"""

        # Displaying File
        st.sidebar.markdown(pdf_display_outline, unsafe_allow_html=True)

