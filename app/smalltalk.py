from groq import Groq
import os
from prompt import small_talk_prompt
import dotenv
dotenv.load_dotenv()

smalltalk_groq=Groq()

def genarate_talk(query):
    completion = smalltalk_groq.chat.completions.create(
        model=os.getenv('GROQ_MODEL'),
        messages=[
            {
                "role": "system",
                "content": small_talk_prompt
            },
            {
                "role": "user",
                "content": f'QUESTION:{query}'
            }
        ],
        temperature=2,
        max_completion_tokens=1024,
    )
    return completion.choices[0].message.content
if __name__=='__main__':
    print(genarate_talk('hi how are you?'))