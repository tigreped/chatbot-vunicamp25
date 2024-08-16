import os
import re
import streamlit as st
import faiss

from chatgroqvu2025 import FAISSIndexer, chat_interaction
from dotenv import load_dotenv
from groq import Groq

# Script utilizado para realizar a interação com Streamlit para a interface gráfica

# LLM utilizada para geração de texto
default_model = "llama3-70b-8192"

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
# Chave API Groq
api_key = os.getenv('GROQ_API_KEY')

# Instanciação da classe FAISSIndexer
indexer = FAISSIndexer()

# Nome do arquivo produzido pelo script texto.py
file_path = 'resolucao_unicamp_2025_v2.txt'
faiss_index_path = 'resolucao_unicamp_2025.faiss'

# Verifica se o conteúdo de contexto já está indexado. Se já tiver executado anteriormente, não precisa reprocessar o texto,
# Basta carregar em memória o índice persistido no disco em um arquivo .faiss
if os.path.exists(faiss_index_path):
    try:
        indexer.index = faiss.read_index(faiss_index_path)
        indexer.sections = indexer.load_sections("text_sections.txt")
    except Exception as e:
        st.error(f"Erro ao carregar índice FAISS: {e}")
else:
    structured_json = indexer.load_text_src(file_path)
    indexer.index_text(structured_json)
    faiss.write_index(indexer.index, faiss_index_path)

# Permite a criação de contexto a partir do histórico da conversa.
def create_context_from_history(history):
    context = ""
    for speaker, message in history:
        context += f"{speaker}: {message}\n"
    return context

# Gerencia a interação estilo chat com a conversa entre usuário e LLM para responder perguntas sobre o contexto fornecido, Vestibular da UNICAMP 2025
def chat_interaction(api_key, relevant_sections, question, model_provided=default_model):
    client = Groq(api_key=api_key)
    prompt = "Você é um auxiliar responsável por responder as dúvidas a respeito da resolução GR-029/2024, contendo o edital do vestibular Unicamp para 2025, de acordo com o contexto fornecido. Responda: " + question
    context = create_context_from_history(st.session_state.chat_history) + " ".join(relevant_sections)
    return client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{prompt}\n\nContexto: {context}"
            }
        ],
        model=model_provided
    )

# Interface Streamlit
st.title("Chatbot do Vestibular UNICAMP 2025 (Resolução GR-029/2024)")
st.write("Estou aqui para responder perguntas a respeito do processo seletivo de Vestibular UNICAMP 2025. Em que posso ajudar?")

# Inicializa o histórico de conversa na sessão do Streamlit para permitir interação com as perguntas anteriores realizadas ao longo da conversa
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

with st.form(key='chat_form', clear_on_submit=True):
    question = st.text_input("Digite a sua pergunta:")
    submit_button = st.form_submit_button(label='Enviar')

    if submit_button and question:
        relevant_sections = indexer.search(question)
        try:
            chat_completion = chat_interaction(api_key, relevant_sections, question)
            response = chat_completion.choices[0].message.content

            # Adiciona a pergunta e a resposta ao início do histórico de conversa
            st.session_state.chat_history.insert(0, ("Usuário", question))
            st.session_state.chat_history.insert(1, ("Chatbot", response))
        except Exception as e:
            st.error(f"Erro ao interagir com a API do Groq: {e}")

# Exibe o histórico de conversa
for speaker, message in st.session_state.chat_history:
    if speaker == "Usuário":
        st.write(f"**{speaker}:** {message}")
    else:
        st.write(f"**{speaker}:** {message}")
