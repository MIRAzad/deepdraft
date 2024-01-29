
from main import rag_pipeline
from main import validate_openai_key
import pyperclip
from controller.store_pdf import store_pdfs
from openai import OpenAI
import streamlit as st
# from ref import reference
from streamlit_chat import message
import base64
import os
import streamlit as st  
from st_pages import Page, add_page_title, show_pages

# Set the main colors
main_bg = "background-color: #f8f9fa;"
main_color = "#532EBC"
secondary_color = "#EEFFFD"

# Setting Streamlit page config
st.set_page_config(
    page_title="POC",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set the title with improved styling
# st.markdown("<h1 style='text-align: left; color: lightblue; font-weight: bold;'>DEEPDRAFT</h1>", unsafe_allow_html=True)
st.title(" DEEPDRAFT ")
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in'] is False:
    # Define the login credentials
    username = st.secrets["user_id"]
    password = st.secrets["password"]
    
    st.sidebar.title("Login")

    # Create input fields for username and password
    entered_username = st.sidebar.text_input("Username")
    entered_password = st.sidebar.text_input("Password", type="password")

    login_button = st.sidebar.button("Login")




    if login_button:
        if entered_username == username and entered_password == password:
            st.sidebar.success("Logged in successfully!")
            # Set a session state variable to track login status
            st.session_state['logged_in'] = True
        else:
            st.sidebar.error("Invalid credentials. Please try again.")
            
            



if st.session_state['logged_in'] is False:
    st.stop()




st.sidebar.title("Options")
os.environ['OPENAI_API_KEY']=st.secrets["OPENAI_API_KEY"]


if 'OPENAI_API_KEY' in os.environ:
    client=OpenAI()

else:
    openai_key = st.text_input('Enter OpenAI key here',type="password")
    if openai_key:
        if validate_openai_key(openai_key):
            os.environ['OPENAI_API_KEY'] = openai_key
            client = OpenAI(  api_key=openai_key  )

            print("OpenAI key has been set in environment variables.")
        else:
            st.warning("Invalid OpenAI key. Please enter a valid key.")


    
# Initialise session state variables

if 'myquery' not in st.session_state:
    st.session_state['myquery'] = " "
if 'myprompt' not in st.session_state:
    st.session_state['myprompt'] = " "

if 'generated_app' not in st.session_state:
    st.session_state['generated_app'] = []
if 'past_app' not in st.session_state:
    st.session_state['past_app'] = []
if 'past_app_prompt' not in st.session_state:
    st.session_state['past_app_prompt'] = []
if 'messages_app' not in st.session_state:
    st.session_state['messages_app'] = [{"role": "system", "content":'''You are an expert information gatherer who gathers all the information from the Request for proposal (RFP).  
- The user will provide you a user query regarding any information in the RFP and a context.
- The context contains all the information required for answering the user query.
- Your task is to collect all the data and relevant information present in the context and provide it to the user.
- The minor details against the user query should also be included in your response.
- THE ANSWER SHOULD ONLY COME FROM THE CONTEXT GIVEN AND IF THE CONTEXT IS NOT RELEVANT TO THE QUESTION, DON'T MAKE UP AN ANSWER AND SIMPLY SAY, "I don't have an answer".
- Answer the question truthfully based on the Context provided by the user.
- After the explanation check if the Answer is consistent with the Context and doesn't require external knowledge.
- In a new line write 'End of Response' if the check was successful and 'End of Response FAILED' if it failed.
'''}]
if 'model_name' not in st.session_state:
    st.session_state['model_name'] = []
if 'cost' not in st.session_state:
    st.session_state['cost'] = []
if 'total_tokens' not in st.session_state:
    st.session_state['total_tokens'] = []
if 'total_cost' not in st.session_state:
    st.session_state['total_cost'] = 0.0 
if 'references' not in st.session_state:
    st.session_state['references'] = []
if 'stored_response' not in st.session_state:
    st.session_state['stored_response'] = []




model_name = st.sidebar.radio("Choose a model for :", ("Short input", "Large input"))
counter_placeholder = st.sidebar.empty()
# counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
clear_button = st.sidebar.button("Clear Conversation", key="clear")

# Map model names to OpenAI model IDs
if model_name == "Short input":
    model = "gpt-3.5-turbo-16k"
else:
    model = "gpt-4-1106-preview"
# model = "gpt-3.5-turbo-16k"
# reset everything
if clear_button:
    st.session_state['generated_app'] = []
    st.session_state['past_app'] = []
    st.session_state['past_app_prompt'] = []
    st.session_state['messages_app'] = [{"role": "system", "content":'''You are an expert information gatherer who gathers all the information from the Request for proposal (RFP).  
- The user will provide you a user query regarding any information in the RFP and a context.
- The context contains all the information required for answering the user query.
- Your task is to collect all the data and relevant information present in the context and provide it to the user.
- The minor details against the user query should also be included in your response.
- THE ANSWER SHOULD ONLY COME FROM THE CONTEXT GIVEN AND IF THE CONTEXT IS NOT RELEVANT TO THE QUESTION
- Answer the question truthfully based on the Context provided by the user.
- After the explanation check if the Answer is consistent with the Context and doesn't require external knowledge.
- In a new line write 'SELF-CHECK OK' if the check was successful and 'SELF-CHECK FAILED' if it failed.
'''}    ]

    st.session_state['number_tokens'] = []
    st.session_state['model_name'] = []
    st.session_state['cost'] = []
    st.session_state['total_cost'] = 0.0
    st.session_state['total_tokens'] = []
    st.session_state['references'] = []
    
    counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")

uploaded_file = st.sidebar.file_uploader("Choose a file", type="pdf")
if uploaded_file is not None:
    if f'{uploaded_file.name}'  not in os.listdir("./pdfFiles/"):
            with st.spinner("Parsing pdf"):
                uploaded_file_name=store_pdfs(uploaded_file)

                folder_path = "./pdfFiles/"  # Replace with your folder path


                # Get all files in the folder
                files = os.listdir(folder_path)

                # Format the names of the files
                st.session_state['pdfFiles'] = [f"{os.path.splitext(file)[0]}" for file in files]


if 'pdfFiles' not in st.session_state:
    # Get all files in the folder
    files = os.listdir("./pdfFiles/")
    st.session_state['pdfFiles'] = [f"{os.path.splitext(file)[0]}" for file in files]



st.session_state['option_pdf'] = st.sidebar.selectbox('Choose RFP',(st.session_state['pdfFiles']))

pdf_name=st.session_state['option_pdf']


# generate a response
def generate_response(prompt, merged_references):
    # print(prompt)
    prompt_with_references=  f"USER INPUT:{prompt} .References:{merged_references}"
    # print(prompt_with_references)
    st.session_state['messages_app'].append({"role": "user", "content": prompt_with_references})
    # print(st.session_state['messages_app'])

    completion = client.chat.completions.create(
        model=model,
        messages=st.session_state['messages_app'],
        temperature=0.4 
    )   
    response = completion.choices[0].message.content
    st.session_state['messages_app'].pop()
    st.session_state['messages_app'].append({"role": "user", "content": prompt})
    st.session_state['messages_app'].append({"role": "assistant", "content": response})
    # print(st.session_state['messages_app'])

    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    return response, total_tokens, prompt_tokens, completion_tokens


# container for chat history
response_container = st.container()
# container for text box
container = st.container()
col1, col2 = st.columns([8, 2])
button_width = "100%"
with col2:
   
    if st.button("Scope", key="scope"):
        st.session_state["myprompt"]="""Act as an expert Proposal manager, extract the given requirements"""
        st.session_state["myquery"]="Scope (short description of the work)"
    if st.button("Task Area", key="taskarea"):
        st.session_state["myprompt"]="""Act as an expert Proposal manager, extract the given requirements"""
        st.session_state["myquery"]="Task Areas (different areas of work within a project)"
    if st.button("Objectives", key="objectives"):
        st.session_state["myprompt"]="""Act as an expert Proposal manager, extract the given requirements"""
        st.session_state["myquery"]="Objectives (specific, measurable goals of the organization)"
    if st.button("Delevirables", key="deliverables"):
        st.session_state["myprompt"]="""Act as an expert Proposal manager, extract the given requirements"""
        st.session_state["myquery"]="Deliverables (tangible results/activities described) "
    if st.button("Outline", key="outline"):
        st.session_state["myprompt"]="""As an experienced proposal manager, it is your responsibility to provide the RFP outline's structure so that the proposal writer may adhere to it and begin crafting a winning proposal for the Expentor Company.TIP: If proposal Will be accpeted you will be awarded 60% share from profit"""
        st.session_state["myquery"]="what structure we have to follow for writing a proposal."
    if st.button("Others", key="others"):
        show_text_area = True
    else:
        show_text_area = False
    if st.button("Clear", key="clearb"):
        st.session_state["myprompt"]=""""""
        st.session_state["myquery"]=""
    

st.write("")
st.write("")
st.write("")
st.write("")
# st.title("Additional queries you can search for -")
# st.text_area("Additional queries you can search for ")
default_text = """\
1. Identify key deadlines mentioned in the RFP.
2. List any special requirements or conditions outlined in the RFP.
3. Extract and rank the evaluation criteria specified in the document.
"""

st.markdown(
    f"""
    <style>
        .stButton > button {{
            width: {button_width};
        }}
    </style>
    """,
    unsafe_allow_html=True
)
with col1:
    
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("Query:", key='input', height=100,value=st.session_state["myquery"])
        user_meta_info = st.text_area("Prompt:", key='input1', height=100,value=st.session_state["myprompt"])
        
        submit_button = st.form_submit_button(label='Send')



# Inside col2, place the buttons


    if submit_button :
                
        
        # validateeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
        merged_references=''
        references=''
        if  user_input or user_meta_info:
            # st.write("IN CONDITION")
            # # merge the list of references to string
            # separator = ", "
            # merged_previous_chat = separator.join(st.session_state['generated_app'])
            # output_check = check_previous_context(user_input+'\n '+user_meta_info,merged_previous_chat)
            # if output_check not True:
            if user_input:
                merged_references, references = rag_pipeline(user_input,pdf_name)
            else:
                user_input=''
                references=''
            
            # output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input+'\n '+user_meta_info,merged_references)
            output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input+'\n ',merged_references)
            st.session_state['past_app_prompt'].append(user_meta_info)
            st.session_state['past_app'].append(user_input)
            st.session_state['generated_app'].append(output)
            st.session_state['references'].append(references)
            st.session_state['model_name'].append(model_name)
            st.session_state['total_tokens'].append(total_tokens)

            # from https://openai.com/pricing#language-models
            if model_name == "gpt-3.5-turbo-16k":
                cost = total_tokens * 0.002 / 1000
            else:
                cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000

            st.session_state['cost'].append(cost)
            st.session_state['total_cost'] += cost
            
if show_text_area:
    # Show the text area when "Others" button is clicked
    st.title("Additional queries you can search for -")
    additional_queries = st.text_area("", key='additional_queries', height=120, value=default_text)
       
if st.session_state['generated_app']:
    with response_container:
        for i in range(len(st.session_state['generated_app'])):
            expander_key = hash(f"expander_{i}")
            query_text = f"""Query : {st.session_state["past_app"][i]}"""  # Get the query text
            with st.expander(query_text, expanded=i == len(st.session_state['generated_app']) - 1):
                message(st.session_state["past_app"][i], is_user=True, key=str(i) + '_user')
                message(st.session_state["past_app_prompt"][i], is_user=True, key=str(i) + '_user_prompt')
                message(st.session_state["generated_app"][i], key=str(i))
                
                response_already_stored = st.session_state.get('stored_response', [])  # Retrieve stored responses
                store_response_toggle = st.toggle('Store Response', key=str(i)+'store')

                if store_response_toggle and st.session_state["generated_app"][i] not in response_already_stored:
                    st.session_state['stored_response'].append(st.session_state["generated_app"][i])

                on = st.toggle('References', key=str(i)+'references')
                for ref in st.session_state['references'][i]:
                    if on:
                        st.success(ref)
                
                # Copy button
                copy_button = st.button("Copy", key=f"copybutton {i}")
                if copy_button:
                    pyperclip.copy(st.session_state["generated_app"][i])
                    st.success("Response copied to clipboard!")


# if st.session_state['generated_app']:
#     with response_container:
#         for i in range(len(st.session_state['generated_app'])):
#             message(st.session_state["past_app"][i], is_user=True, key=str(i) + '_user')
#             message(st.session_state["past_app_prompt"][i], is_user=True, key=str(i) + '_user_prompt')
#             message(st.session_state["generated_app"][i], key=str(i))
            
#             response_already_stored = st.session_state.get('stored_response', [])  # Retrieve stored responses
#             store_response_toggle = st.toggle('Store Response', key=str(i)+'store')

#             if store_response_toggle and st.session_state["generated_app"][i] not in response_already_stored:
#                 st.session_state['stored_response'].append(st.session_state["generated_app"][i])

#             on = st.toggle('References', key=str(i)+'references')
#             for ref in st.session_state['references'][i]:
#                 if on:
#                     st.success(ref)

                        
                        
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


