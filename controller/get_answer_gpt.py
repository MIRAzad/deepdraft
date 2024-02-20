import json
from openai import OpenAI
# from anthropic import AI_PROMPT, HUMAN_PROMPT, Anthropic
import os
# Read the JSON configuration file
with open('./config.json', 'r') as file:
    config = json.load(file)


gpt_model= config['gpt_model']

conversation=[]
def make_prompt(user_query, references):
    prompt = f"""You are an experienced proposal writer working with SysUSA. Give a detailed answer as a professional proposal writer for the question given below delimited by angle brackets. For generating the answer use the context given below. 
	REMEMBER THE ANSWER HAS TO BE AS DETAILED AS POSSIBLE SUCH THAT IT CAN BE USED IN A PROPOSAL AS-IS.
	THE ANSWER SHOULD ONLY COME FROM THE CONTEXT GIVEN AND IF THE CONTEXT IS NOT RELEVANT TO THE QUESTION, DON'T MAKE UP AN ANSWER AND SIMPLY SAY, "I don't have an answer." 

	Question: {user_query}

	Context: {references}
	
	Helpful Answer:
"""
        
    return prompt


def get_completion(messages, model=gpt_model):
    openai_key = os.environ.get('OPENAI_API_KEY')
    # openai.api_key =openai_key
    client = OpenAI(  api_key=openai_key  )

    promptList=[{"role":"user", "content":messages}]
    # promptList.append({"role":"user", "content":messages})
    response = client.chat.completions.create(
        model=model,
        messages=promptList,
        temperature=0,
        stream=False
        
    )
    return response

def getAnswerFromGpt(user_query, references):

    prompt = make_prompt(user_query, references)
    # conversation.append({"role":"user", "content":prompt})
    response = get_completion(prompt)
    # conversation.pop()
    # conversation.append({"role":"user", "content":user_query})

    return response


def get_answer(user_query, references):
    answer=getAnswerFromGpt(user_query,references)
    
    return answer.choices[0].message.content

