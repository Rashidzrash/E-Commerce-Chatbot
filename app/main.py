import streamlit as st
from router import router
from faq import faq_chain,faq_ingest
from pathlib import Path
from sql import genarate_answer
from smalltalk import genarate_talk

faq_path=Path(__file__).parent /'resources'/'faq_data.csv'
faq_ingest(faq_path)
def ask(query):
  router_name=router(query).name
  if router_name=='faq':
      return faq_chain(query)
  elif router_name=='sql':
      return genarate_answer(query)
  elif router_name=='smalltalk':
      return genarate_talk(query)
  else:
      return "Please ask a valid product-related question."



st.session_state.setdefault('messages',[])
st.title('E-commerce Chatbot')
query=st.chat_input('Enter your query')
for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.markdown(message['content'],unsafe_allow_html=True)

if query:
    with st.chat_message('user'):
        st.markdown(query,unsafe_allow_html=True)
        st.session_state['messages'].append({'role':'user','content':query})
    with st.chat_message('assistant'):
        response=ask(query)
        st.markdown(response,unsafe_allow_html=True)
        st.session_state['messages'].append({'role':'assistant','content':response})