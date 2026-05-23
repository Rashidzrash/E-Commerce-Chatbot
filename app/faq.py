import chromadb
import pandas as pd
from groq import Groq
from pathlib import Path
from chromadb.utils import embedding_functions
import dotenv
import os
from prompt import faq_prompt

dotenv.load_dotenv()

faq_path=Path(__file__).parent /'resources'/'faq_data.csv'
client=chromadb.Client()
Groq_client=Groq()
collection_name='faq_v2'
ef=embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
def faq_ingest(path):
    if collection_name not in [c.name for c in client.list_collections()]:
        collection = client.get_or_create_collection(
            name=collection_name,
            embedding_function=ef
        )
        df = pd.read_csv(path)
        docs =df['question'].tolist()
        metadatas = [{'answer': ans} for ans in df['answer']]
        ids=[f'id_{i}' for i in range(len(docs)) ]
        collection.add(
            documents=docs,
            metadatas=metadatas,
            ids=ids
        )
        print(f'FAQ Data successfully ingested to collection: {collection_name}')
    else:
        print(f'Collection: {collection_name} already exist.')
def get_relevent_qa(query):
    collection=client.get_collection(name=collection_name)
    results=collection.query(
        query_texts=[query],
        n_results=2,
    )
    return results

def faq_chain(query):
    results=get_relevent_qa(query)
    context=''.join([r.get('answer') for r in results['metadatas'][0]])
    answer=generate_answers(query,context)
    return answer
def generate_answers(query,context):
    print(f'query: {query}, context: {context}')

    completion = Groq_client.chat.completions.create(
            model=os.environ['GROQ_MODEL'],
            messages=[
                {
                    "role": "system",
                    "content": faq_prompt
                },
                {
                    "role": "user",
                    "content": f'User Question: {query} CONTEXT: {context}'
                }
            ]
    )
    return completion.choices[0].message.content
if __name__ == '__main__':
    faq_ingest(faq_path)
    query="fast delivery available?"
    answer=faq_chain(query)
    print(answer)