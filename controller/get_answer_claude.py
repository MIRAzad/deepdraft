import json
from anthropic import AI_PROMPT, HUMAN_PROMPT, Anthropic

# Read the JSON configuration file
with open('./config.json', 'r') as file:
    config = json.load(file)


claude_key = config['claude_key']
anthropic = Anthropic(api_key=claude_key)


def getAnswerFromClaude(user_query, reference):
    # try:

        completion = anthropic.completions.create(
            temperature=0,
            model="claude-2.0",
            stream=False,
            max_tokens_to_sample=100000,
            prompt=f"""
        {HUMAN_PROMPT}
        Claude, You are an experienced proposal writer working with SysUSA,I need you to answer the user query: {user_query}.
        I will provide you with some relevant references: {reference}.
        Your task is to gather all the information present in the refrences and answer the user query.

        Important requirements:
        Make sure you do not miss/skip any information.
        Only use details from the provided passages, do not include any outside information.
        Feel free to reword, reorder, and improve the writing to create a clear and detailed content.
        Structure the answer logically, using numbered steps if needed.
        Make sure the content flows well and is written professionally.
        The end result should be a focused, comprehensive, and professional  aligned with the question and the references.

        {AI_PROMPT}
    """,
        )

        # for response in completion:
        return completion 

    # except Exception as err:
    #     logging.error("claude function encountered an error: %s", str(err))
    #     logging.error(err)
    #     return []
    

def get_answer(user_query, top_5_reference_string):



    answer=getAnswerFromClaude(user_query,top_5_reference_string)
    # print(answer.completion)
    
    return answer.completion