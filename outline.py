# To generate the outline, consider the information explicitly given for the format of outline.


#     Based on this information, Organize the content into a structured outline that aligns with the RFP's requirements. 
#     - Below are steps to help you generate an effective outline:
#     1. Refer to the Instructions for the format of the outline of the response .
#     2. Identify the appropriate approaches to be included in the response .
#     3. Add relevant sections  to each approach.
#     4. Fetch descriptions of each section extracted above.
#     5. Subdivide Each Section wherever required.
#     6. Understand the Evaluation Criteria:
#         - Pay close attention to how the proposal will be assessed.
#         - This can guide you in prioritizing and emphasizing certain aspects.
#         Take the following sample output  as example:
#         <outline>    
#             <section>
#                 <name>name of the sections</name>
#                 <Description>Description of the section </Description>              
#                 <sub-section>
#                     <name>name of the sub section</name>
#                     <title>Title of the Sub section</title>
#                     <Description> Description of the sub-section </Description>
#                 </sub-section>
#                 .
#                 .
#                 .
#             </section>
#             .
#             .
#             .  
#         </outline>

import streamlit as st
from st_pages import add_page_title

add_page_title(layout="wide")

from main import   create_pdf_from_list
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
if 'stored_outline' not in st.session_state:
    st.session_state['stored_outline']=[]
if 'generated_outline' not in st.session_state:
    st.session_state['generated_outline'] = []
if 'past_outline' not in st.session_state:
    st.session_state['past_outline'] = []
if 'messages_outline' not in st.session_state:
    st.session_state['messages_outline'] = [{"role": "system", "content": """
     -Act as an expert proposal manager who is responsible for generating outline for the forthcoming response of an RFP. 
     -The outline must be a structured and organized framework that serves as the foundation for proposals generated in response to
        a Request for Proposal (RFP). In the context of proposal management, creating a well-structured outline is the 
        first critical step in the proposal development process. 
     - Answer the question truthfully based on the instructions and scope of work provided by the user
     - Strictly refer to the Instructions for formatting the outline of the response .
             
        """}    ]


    # counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
clear_button_outline = st.sidebar.button("Clear Conversation", key="clear_outline")

# reset everything
if clear_button_outline:
    st.session_state['generated_outline'] = []
    st.session_state['past_outline'] = []
    st.session_state['messages_outline'] = [{"role": "system", "content":"""
     -Act as an expert proposal manager who is responsible for generating outline for the forthcoming response of an RFP. 
     -The outline must be a structured and organized framework that serves as the foundation for proposals generated in response to
        a Request for Proposal (RFP). In the context of proposal management, creating a well-structured outline is the 
        first critical step in the proposal development process. 
     - Answer the question truthfully based on the instructions and scope of work provided by the user
     - Strictly refer to the Instructions for formatting the outline of the response .
             
        """}    ]


pdf_name=st.session_state['option_pdf']


    # write pdf name in sessionnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn

# generate a response
def generate_response(prompt, merged_references_outline):
    prompt_with_references =  f"USER INPUT:{prompt}. \n\n\n\n CONTEXT:{merged_references_outline}"
    st.session_state['messages_outline'].append({"role": "user", "content": prompt_with_references})
    
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo-16k',
        messages=st.session_state['messages_outline']   
    )   
    response = completion.choices[0].message.content
    st.session_state['messages_outline'].pop()
    st.session_state['messages_outline'].append({"role": "user", "content": prompt})
    st.session_state['messages_outline'].append({"role": "assistant", "content": response})

    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    return response, total_tokens, prompt_tokens, completion_tokens


# container for chat history
response_container = st.container()
# container for text box
container = st.container()

with container:

    with st.form(key='form_outline', clear_on_submit=True):
        user_input = st.text_area("Query:", key='input_outline', height=200, value='''To generate the outline, consider the information explicitly given for the format of outline.


    Based on this information, Organize the content into a structured outline that aligns with the RFP's requirements. 
    - Below are steps to help you generate an effective outline:
    1. Refer to the Instructions for the format of the outline of the response .
    2. Identify the appropriate approaches to be included in the response .
    3. Add relevant sections  to each approach.
    4. Fetch descriptions of each section extracted above.
    5. Subdivide Each Section wherever required.
    6. Understand the Evaluation Criteria:
        - Pay close attention to how the proposal will be assessed.
        - This can guide you in prioritizing and emphasizing certain aspects.
        Take the following sample output  as example:
        <outline>    
            <section>
                <name>name of the sections</name>
                <Description>Description of the section </Description>              
                <sub-section>
                    <name>name of the sub section</name>
                    <title>Title of the Sub section</title>
                    <Description> Description of the sub-section </Description>
                </sub-section>
                .
                .
                .
            </section>
            .
            .
            .  
        </outline>''')
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        
        
        separator = ", "
        merged_references_outline = separator.join(st.session_state['stored_response'])
        print(merged_references_outline)
        # add context hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
        output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input,merged_references_outline)
        st.session_state['past_outline'].append(user_input)
        st.session_state['generated_outline'].append(output)
        # st.session_state['references'].append(references)
        # st.session_state['model_name'].append(model_name)
        # st.session_state['total_tokens'].append(total_tokens)


# if st.session_state['generated_outline']:
#     with response_container:
#         for i in range(len(st.session_state['generated_outline'])):
#             message(st.session_state["past_outline"][i], is_user=True, key=str(i) + '_user')
#             message(st.session_state["generated_outline"][i], key=str(i))
#             if st.toggle('Store Response', key=str(i)+'store'):
#                 st.session_state['stored_outline'].append(st.session_state["generated_outline"][i]) 
#             # on = st.toggle('References', key=str(i)+'references')
#             # for i in st.session_state['references'][i]:
#             #     if on:
#             #         st.success(i)
                        
#             # st.write(f"Model used: {st.session_state['model_name'][i]}; Number of tokens: {st.session_state['total_tokens'][i]}; Cost: ${st.session_state['cost'][i]:.5f}")
#             # counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")


if st.session_state['generated_outline']:
    with response_container:
        for i in range(len(st.session_state['generated_outline'])):
            message(st.session_state["past_outline"][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated_outline"][i], key=str(i))
            
            response_already_stored_outline = st.session_state.get('stored_outline', [])  # Retrieve stored responses
            store_response_toggle_outline = st.toggle('Store Response', key=str(i)+'store')

            if store_response_toggle_outline and st.session_state["generated_outline"][i] not in response_already_stored_outline:
                st.session_state['stored_outline'].append(st.session_state["generated_outline"][i])

            on = st.toggle('References', key=str(i)+'references')
            for ref in st.session_state['references'][i]:
                if on:
                    st.success(ref)


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
create_pdf_from_list(st.session_state['stored_response'], "output.pdf")


if st.session_state['stored_response']:
    # Opening file from file path
    with open('output.pdf', "rb") as f:
        base64_pdf_outline = base64.b64encode(f.read()).decode('utf-8')
        pdf_displayy = F'<iframe src="data:application/pdf;base64,{base64_pdf_outline}"  style=" width: 100%; height: 400px;" type="application/pdf"></iframe>'

        # Embedding PDF in HTML
        # pdf_display =  f"""<embed sandbox="allow-scripts allow-same-origin"  class="pdfobject"  type="application/pdf"  title="Embedded PDF"
        # src="data:application/pdf;base64,{base64_pdf}"  style=" width: 100%; height: 400px;">"""

        # Displaying File
        st.sidebar.markdown(pdf_displayy, unsafe_allow_html=True)








# "role": "system", "content": """"You are a helpful professional proposal writer"
#                                       "your job is to create outline for an rfp response from the given context only"
    
#                                 	"REMEMBER THE ANSWER HAS TO BE AS DETAILED AS POSSIBLE SUCH THAT IT CAN BE USED IN A PROPOSAL AS-IS."
# 	"THE ANSWER SHOULD ONLY COME FROM THE CONTEXT GIVEN AND IF THE CONTEXT IS NOT RELEVANT TO THE QUESTION, DON'T MAKE UP AN ANSWER AND SIMPLY SAY, I don't have an answer."
#     "After the explanation check if the Answer is consistent with the Context and doesn't require external knowledge. "
#     "In a new line write 'SELF-CHECK OK' if the check was successful and 'SELF-CHECK FAILED' if it failed. " 
    
# """















# [{"role": "system", "content": """"You are a helpful assistant, the user will provide you with the scope of work ,instructions and evaluation criteria  given in an RFP 
#         you are tasked to act as a proposal manager .Review the scope of work ,instructions and evaluation criteria thoroughly,
#         extract all the tasks or requirements or deliverables from the scope of work and compile them in a list in the following format:
#         Requirements to be addressed by the offeror
#         Generate an outline for its forthcoming response,the contents of which will be filled by a junior proposal writer .
#         Ensure the response is generated in the following format:
#         <outline>    
#                         <section name="name of the section" volume_name="Name of the volume the section will be included in" volume_number="serial number of the volume the section will be included in" No of pages= "no: of pages the section will span over">
#                             <Tasks>"List of the tasks to be accomplished in the section</Tasks >
                
#                             <sub section>
#                                 <title>Title of the Sub section</title>
#                                  <Tasks>"List of the tasks to be accomplished in the sub-section</Tasks >
                                
#                             </sub section>
#                             .
#                             .
#                             .
#                         </section>
#                         .
#                         .
#                         .  
#                     </outline>
#         Put N/A for volume_name,volume_number and No_of_pages, if not given expliictly 
#         Make sure to describe each element in the outline well so that the proposal writer  does not need to read the RFP  or scope of work or instructions. The outline you generate should be self contained enough  that the proposal writer completely understands the deliverables to be addressed by the offeror and acts accordingly.
#         Come up with appropriate names for the sections to be included in the outline and find the requirements to be addressed under them. 
#         if under any section a particular   task or requirement is to be addressed , make sure to write the task or requirement or deliverable verbatim.
#         The outline generated should not depend on the scope of work ,instructions or evaluation criteria for upcoming steps like content filling.
                
# """}    ]