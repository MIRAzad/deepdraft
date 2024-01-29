# considering the given context, your task is to create an outline for the rfp response , make sure you only include those things which are required for the outline
from main import rag_pipeline, validate_openai_key, check_previous_context
from controller.store_pdf import store_pdf
from openai import OpenAI
import streamlit as st
from streamlit_chat import message
import base64
import os
import streamlit as st  


st.set_page_config(page_title="AVA", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>DeepDraft chatbot </h1>", unsafe_allow_html=True)

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
            
            


# # Check if the user is logged in before continuing
# if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
#     st.stop()  # Stop execution if not logged in
if st.session_state['logged_in'] is False:
    st.stop()
# # from streamlitChatgptUi import main
# st.set_page_config(page_title="AVA", page_icon=":robot_face:")
# st.markdown("<h1 style='text-align: center;'>DeepDraft chatbot </h1>", unsafe_allow_html=True)


from st_pages import Page, add_page_title, show_pages


# show_pages(
#     [
#         Page("./app2.py", "Document Repository", "🏠"),
#         # Can use :<icon-name>: or the actual icon
#         Page("./outline.py", "Generate Outline", "🧰"),
#         Page("./questions.py", "Generate Questions", "🧰"),
#         Page("./answers.py", "Generate Answers", "🧰"),
#         Page("./final_content.py", "Generate Final Content", "🧰")


#     ]
# )

# add_page_title()  # Optional method to add title and icon to current page






st.sidebar.title("Sidebar")
os.environ['OPENAI_API_KEY']=st.secrets["OPENAI_API_KEY"]
# # Remove the OpenAI key from the environment variables
# os.environ.pop('OPENAI_API_KEY')

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
if 'generated_app' not in st.session_state:
    st.session_state['generated_app'] = []
if 'past_app' not in st.session_state:
    st.session_state['past_app'] = []
if 'messages_app' not in st.session_state:
    st.session_state['messages_app'] = [{"role": "system", "content": """"You are a helpful assistant "
                                     "Give a detailed answer as a professional proposal writer for the question asked by the user."
                                     "Answer the question truthfully based on the Context provided by the user." 
	"REMEMBER THE ANSWER HAS TO BE AS DETAILED AS POSSIBLE SUCH THAT IT CAN BE USED IN A PROPOSAL AS-IS."
	"THE ANSWER SHOULD ONLY COME FROM THE CONTEXT GIVEN AND IF THE CONTEXT IS NOT RELEVANT TO THE QUESTION, DON'T MAKE UP AN ANSWER AND SIMPLY SAY, I don't have an answer."
    "Strictly make sure you do not skip any required information present in the context"
    "After the explanation check if the Answer is consistent with the Context and doesn't require external knowledge. "
    "In a new line write 'SELF-CHECK OK' if the check was successful and 'SELF-CHECK FAILED' if it failed. " 
"""}]
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

# Sidebar - let user choose model, show total cost of current conversation, and let user clear the current conversation 



model_name = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-4"))
counter_placeholder = st.sidebar.empty()
counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
clear_button = st.sidebar.button("Clear Conversation", key="clear")

# Map model names to OpenAI model IDs
if model_name == "GPT-3.5":
    model = "gpt-3.5-turbo-16k"
else:
    model = "gpt-3.5-turbo-16k"

# reset everything
if clear_button:
    st.session_state['generated_app'] = []
    st.session_state['past_app'] = []
    st.session_state['messages_app'] = [{"role": "system", "content": """"You are a helpful assistant "
                                     "Give a detailed answer as a professional proposal writer for the question asked by the user."
                                	"REMEMBER THE ANSWER HAS TO BE AS DETAILED AS POSSIBLE SUCH THAT IT CAN BE USED IN A PROPOSAL AS-IS."
	"THE ANSWER SHOULD ONLY COME FROM THE CONTEXT GIVEN AND IF THE CONTEXT IS NOT RELEVANT TO THE QUESTION, DON'T MAKE UP AN ANSWER AND SIMPLY SAY, I don't have an answer."
    "Strictly make sure you do not skip any required information present in the context"
    "After the explanation check if the Answer is consistent with the Context and doesn't require external knowledge. "
    "In a new line write 'SELF-CHECK OK' if the check was successful and 'SELF-CHECK FAILED' if it failed. " 
    
"""}    ]

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
                uploaded_file_name=store_pdf(uploaded_file)

                folder_path = "./pdfFiles/"  # Replace with your folder path

                # Get all files in the folder
                files = os.listdir(folder_path)

                # Format the names of the files
                st.session_state['pdfFiles'] = [f"{os.path.splitext(file)[0]}" for file in files]


if 'pdfFiles' not in st.session_state:
    # Get all files in the folder
    files = os.listdir("./pdfFiles/")
    st.session_state['pdfFiles'] = [f"{os.path.splitext(file)[0]}" for file in files]



st.session_state['option_pdf'] = st.sidebar.selectbox('Select RFP?',(st.session_state['pdfFiles']))

pdf_name=st.session_state['option_pdf']


# generate a response
def generate_response(prompt, merged_references):
    prompt_with_references=  f"USER INPUT:{prompt}. \n\n\n\n CONTEXT:{merged_references}"
    st.session_state['messages_app'].append({"role": "user", "content": prompt_with_references})
    
    completion = client.chat.completions.create(
        model=model,
        messages=st.session_state['messages_app']   
    )   
    response = completion.choices[0].message.content
    st.session_state['messages_app'].pop()
    st.session_state['messages_app'].append({"role": "user", "content": prompt})
    st.session_state['messages_app'].append({"role": "assistant", "content": response})

    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    return response, total_tokens, prompt_tokens, completion_tokens




def check_previous_context(prompt,merged_previous_chat):
    prompt=[]
    prompt=[{"role": "system", "content": """ "the user will provide you with a user query and a context, your job is to decide whether the context provided contains the answer for the given user query."
                                     "your response should be a boolean data type:
                                     True (if you can answer the query from the provided context)
                                     False (if you cannot answer the query from the provided context)"
                                     """}
            ]
    prompt_with_previous_chat=  f"USER INPUT:{prompt}. \n\n\n\n CONTEXT:{merged_previous_chat}"
    prompt.append({"role": "user", "content": prompt_with_previous_chat})
    
    completion = client.chat.completions.create(
        model=model,
        messages=prompt 
    )   
    response = completion.choices[0].message.content
    return response



# container for chat history
response_container = st.container()
# container for text box
container = st.container()

with container:

    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("Query:", key='input', height=100)
        user_meta_info = st.text_area("Prompt:", key='input1', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        
            
        # # merge the list of references to string
        separator = ", "
        merged_previous_chat = separator.join(st.session_state['generated_app'])
        output_check = check_previous_context(user_input+'\n '+user_meta_info,merged_previous_chat)
        print(output_check)
        if output_check is True:
            print("output check is True")
            # merged_references, references = rag_pipeline(user_input,pdf_name)
            output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input+'\n '+user_meta_info,merged_previous_chat)
            
        else: 
            print("output check is False")

            merged_references, references = rag_pipeline(user_input,pdf_name)
            output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input+'\n '+user_meta_info,merged_references)
            
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

# if st.session_state['generated_app']:
#     with response_container:
#         for i in range(len(st.session_state['generated_app'])):
#             message(st.session_state["past_app"][i], is_user=True, key=str(i) + '_user')
#             message(st.session_state["generated_app"][i], key=str(i))
#           h 
#             if st.toggle('Store Response', key=str(i)+'store'):
#                 st.session_state['stored_response'].append(  st.session_state["generated_app"][i])  

#             on = st.toggle('References', key=str(i)+'references')
#             for i in st.session_state['references'][i]:
#                 if on:
#                     st.success(i)


if st.session_state['generated_app']:
    with response_container:
        for i in range(len(st.session_state['generated_app'])):
            message(st.session_state["past_app"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated_app"][i], key=str(i))
            
            response_already_stored = st.session_state.get('stored_response', [])  # Retrieve stored responses
            store_response_toggle = st.toggle('Store Response', key=str(i)+'store')

            if store_response_toggle and st.session_state["generated_app"][i] not in response_already_stored:
                st.session_state['stored_response'].append(st.session_state["generated_app"][i])

            on = st.toggle('References', key=str(i)+'references')
            for ref in st.session_state['references'][i]:
                if on:
                    st.success(ref)

                        
                        
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






# "role": "system", "content": """"You are a helpful assistant "
#                                      "Give a detailed answer as a professional proposal writer for the question asked by the user."
#                                      "Answer the question truthfully based on the Context provided by the user." 
# 	"REMEMBER THE ANSWER HAS TO BE AS DETAILED AS POSSIBLE SUCH THAT IT CAN BE USED IN A PROPOSAL AS-IS."
# 	"THE ANSWER SHOULD ONLY COME FROM THE CONTEXT GIVEN AND IF THE CONTEXT IS NOT RELEVANT TO THE QUESTION, DON'T MAKE UP AN ANSWER AND SIMPLY SAY, I don't have an answer."
#     "Strictly make sure you do not skip any required information present in the context"
#     "After the explanation check if the Answer is consistent with the Context and doesn't require external knowledge. "
#     "In a new line write 'SELF-CHECK OK' if the check was successful and 'SELF-CHECK FAILED' if it failed. " 
# """