
from openai import OpenAI
import requests
import json




listt=[{"role": "system", "content": """You are a helpful assistant "
                                     "Give a detailed answer as a professional proposal writer for the question asked by the user."
                                     "Answer the question truthfully based on the Context provided by the user." 
	"REMEMBER THE ANSWER HAS TO BE AS DETAILED AS POSSIBLE SUCH THAT IT CAN BE USED IN A PROPOSAL AS-IS."
	"THE ANSWER SHOULD ONLY COME FROM THE CONTEXT GIVEN AND IF THE CONTEXT IS NOT RELEVANT TO THE QUESTION, DON'T MAKE UP AN ANSWER AND SIMPLY SAY, I don't have an answer."
    "Strictly make sure you do not skip any required information present in the context"
    "DO NOT SUMARIZE YOUR ANSWER"
    "After the explanation check if the Answer is consistent with the Context and doesn't require external knowledge. "
    "In a new line write 'SELF-CHECK OK' if the check was successful and 'SELF-CHECK FAILED' if it failed."
"""}]




def cogni_pipeline(user_query):
    api_url = f"https://api.cogniverse.expentor.com/v1/aiengine/references?query={user_query}"

    response = requests.get(api_url)
    
    if response.status_code == 200:
        json_response = response.json()
        
        references = json_response['response']['ref']

        ref_para_concatenated_cogniverse = '\n\n '.join(reference['ref_para'] for reference in references)

    else:
        print(f"Failed to retrieve data from the API for query: {user_query}. Status code: 0")

    
    return  references




def generate_response(prompt, final_combined_references,model, openai_key):
    client = OpenAI(  api_key=openai_key  )
    
    prompt_with_references=  f"USER INPUT:{prompt}. \n\n CONTEXT:{final_combined_references}"
    listt.append({"role": "user", "content": prompt_with_references})
    
    completion = client.chat.completions.create(
        model=model,
        messages=listt   
    )   
    response = completion.choices[0].message.content


    return response



def get_answer_from_gpt(model, user_query, openai_key):

    references=cogni_pipeline(user_query)

    combined_strings = []

    for item in references:
        if 'ref_para' in item and 'page_number' in item:
            combined_reference = f"Ref para: {item['ref_para']}\nPage number: {item['page_number']}\n"
            combined_strings.append(combined_reference)

    final_combined_references = '\n'.join(combined_strings)


    response = generate_response(user_query,references, model, openai_key)
    return response



response=get_answer_from_gpt(model='gpt-4-1106-preview', user_query='instructions for the offerors', openai_key='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')

print(response)

