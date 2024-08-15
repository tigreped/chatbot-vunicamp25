import re
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

class FAISSIndexer:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.sections = None
        self.index = None

    def load_text(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def extract_chapters_and_annexes(self, text):
        pattern = re.compile(r'\b(Capítulo\s+[IVXLCDM]+|ANEXO\s+[IVXLCDM]+)\b')
        parts = pattern.split(text)
        structured_data = []
        current_section = None

        for i in range(len(parts)):
            part = parts[i].strip()
            if pattern.match(part):
                if current_section:
                    structured_data.append(current_section)
                current_section = {"titulo": part, "conteudo": ""}
            else:
                if current_section:
                    current_section["conteudo"] += part + " "
        if current_section:
            structured_data.append(current_section)
        return structured_data

    def extract_articles(self, structured_data):
        article_pattern = re.compile(r"\bArt\. \d+º?\b")
        for section in structured_data:
            content = section["conteudo"]
            new_content_list = []

            if isinstance(content, str):
                parts = article_pattern.split(content)
                titles = article_pattern.findall(content)
                if titles:
                    articles = []
                    for i in range(len(titles)):
                        article_content = parts[i+1].strip() if i + 1 < len(parts) else ""
                        title = titles[i].strip()
                        article = {"resumo": title, "texto": section["titulo"] + " - " + title + " - " + article_content}
                        articles.append(article)
                    new_content_list.extend(articles)
                else:
                    new_content_list.append({"texto": section["titulo"] + " - " + content})
            else:
                new_content_list.extend(content)
            section["conteudo"] = new_content_list
        return structured_data

    def generate_sections_list(self, structured_text):
        strut_sections = []
        for item in structured_text:
            conteudo = item["conteudo"]
            if len(conteudo) > 1:
                for c in conteudo:
                    strut_sections.append(c['texto'])
            if len(conteudo) == 1:
                strut_sections.append(conteudo[0]['texto'])
        return strut_sections

    def generate_embeddings(self, texts):
        embeddings = self.model.encode(texts)
        return np.array(embeddings)

    def persist_sections(self, sections_file_path):
        with open(sections_file_path, "w", encoding='utf-8') as f:
            for section in self.sections:
                f.write(section + '\n')

    def load_sections(self, sections_file_path):
        with open(sections_file_path, 'r', encoding='utf-8') as file:
            return file.read().split('\n')

    def load_text_src(self, url):
        text = self.load_text(url)
        structured_text = self.extract_chapters_and_annexes(text)
        self.extract_articles(structured_text)
        return self.generate_sections_list(structured_text)

    def index_text(self, structured_json):
        self.sections = structured_json
        self.persist_sections("text_sections.txt")
        embeddings = self.generate_embeddings(self.sections)
        d = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(d)
        self.index.add(embeddings)

    def search(self, query, top_k=7):
        query_embedding = self.generate_embeddings([query])[0]
        query_embedding = np.expand_dims(query_embedding, axis=0)
        distances, indices = self.index.search(query_embedding, top_k)
        results = [self.sections[idx] for idx in indices[0]]
        return results

# Método que auxilia o processo de interação com o cliente Groq para realizar as buscas na LLM na nuvem, passando as sessões relevantes, o prompt e o contexto
def chat_interaction(api_key, relevant_sections, question, model_provided="llama3-70b-8192"):
    client = Groq(api_key=api_key)
    prompt = "Você é um auxiliar responsável por responder as dúvidas a respeito da resolução GR-029/2024, contendo o edital do vestibular Unicamp para 2025, de acordo com o contexto fornecido. Responda: " + question
    context = " ".join(relevant_sections)
    return client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{prompt}\n\nContexto: {context}"
            }
        ],
        model=model_provided
    )
