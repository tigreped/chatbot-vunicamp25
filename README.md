# Chatbot Vunicamp 2025

Este é um projeto de chatbot com interação com LLMs desenvolvido para responder de maneira automatizada com texto generativo a perguntas sobre a resolução GR-029/2024 do vestibular UNICAMP 2025.

Para testar o projeto ao vivo, basta acessar [clicando aqui](https://chatbot-vunicamp25.streamlit.app/)

## Funcionalidades

- Responde perguntas sobre o vestibular UNICAMP 2025.
- Utiliza embeddings FAISS para busca eficiente a partir do modelo sentence-transformers/all-MiniLM-L6-v2.
- Integração com a API Groq com o modelo gratuito "llama3-70b-8192" para respostas inteligentes de texto generativo de maneira gratuita (limitada)

## Estrutura do Projeto

- `resolucao_unicamp_2025_v2.txt`: Arquivo de texto contendo a resolução do vestibular baixada pelo script texto.py.
- `chatgroqvu2025.py`: Script principal contendo a lógica do chatbot e o processamento dos embeddings.
- `app.py`: Script para executar o chatbot na nuvem usando Streamlit.
- `text_sections.txt`: Arquivo contendo as seções indexadas da resolução, para reutilização eficiente sem a necessidade de reprocessamento a cada instanciação
- `resolucao_unicamp_2025.faiss`: Arquivo utilizado para armazenar o índice FAISS com os embeddings em disco para reutilização.

## Como Executar Localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/tigreped/chatbot-vunicamp25.git
   ```
   2. Instale as dependências do projeto:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o aplicativo localmente, baixando primeiro a resolução e em seguida iniciando a aplicação para realizar a ETL e interação via chat com interface Streamlit:
  ```bash
  python texto.py
  streamlit run app.py
  ```

## Dados de teste

Ao inicializar o chat no Streamlit localmente ou na nuvem, realize interações passando perguntas para a aplicação, como por exemplo:

1. Quais os cursos disponíveis na área de Humanas?
2. Quais os cursos disponíveis na área de Exatas?
3. Quais desse cursos são considerados da área de Tecnologia da Informação?
4. Como faço para me inscrever? Quais as taxas e datas mais importantes?
5. Explique o que é o PAAIS.

Como o chat possui uma memória do histórico da conversa, é possível realizar questionamentos sobre a própria conversa, por exemplo:

1. Faça um resumo das respostas dadas até o momento ao Usuário
2. Quantos cursos foram listados até o momento?
3. Quantas perguntas foram feitas até o momento?

É possível verificar que a resposta a esse tipo de perguntas é bastante satisfatória, com respostas completas e coerentes, principalmente no tocante ao desenvolvimento de uma sequência de trocas de mensagens.

## Licensa

  O projeto é gratuito e livre e está licenciado sob GNU/GPL-3.
  Responsável: Pedro Guimarães (tigreped@gmail.com)
