import sqlite3
import pandas as pd
from groq import Groq
import dotenv
import os
from prompt import sql_prompt,comprehension_prompt
import re



dotenv.load_dotenv()
sql_groq=Groq()


def generate_sql_query(question):
    sql_completion = sql_groq.chat.completions.create(
        model=os.getenv('GROQ_MODEL'),
        messages=[
            {
                "role": "system",
                "content": sql_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0.2,
        max_completion_tokens=120,
    )
    return sql_completion.choices[0].message.content


def final_sqlquery(query):
    sql_query = generate_sql_query(query)
    match = re.search(r"<sql>(.*?)</sql>", sql_query, re.DOTALL)
    if match:
        sql_query = match.group(1).strip()

        return sql_query
    else:
        raise RuntimeError('Query not found.')


def run_query(query):
    sql_query=final_sqlquery(query)
    if sql_query.strip().upper().startswith('SELECT'):
        with sqlite3.connect('db.sqlite') as conn:
            df = pd.read_sql_query(sql_query, conn)
            context = df.head(15).to_dict(orient='records')
            return context
    else:
        raise RuntimeError('Query not found.')

def genarate_answer(query):
    answer=run_query(query)
    completion = sql_groq.chat.completions.create(
        model=os.getenv('GROQ_MODEL'),
        messages=[
            {
                "role": "system",
                "content": comprehension_prompt
            },
            {
                "role": "user",
                "content": f'QUESTION:{query} DATA:{answer}'
            }
        ],
        temperature=0.2,
        max_completion_tokens=120,
    )
    return completion.choices[0].message.content
if __name__ == '__main__':
  query = 'all nike shoes'
  print(genarate_answer(query))


