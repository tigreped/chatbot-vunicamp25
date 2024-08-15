import requests
from bs4 import BeautifulSoup
import re

# URL da resolução
url = "https://www.pg.unicamp.br/norma/31879/0"

# Fazendo a requisição HTTP para obter o conteúdo da página
response = requests.get(url, verify=False)
html_content = response.content

# Usando BeautifulSoup para parsear o HTML
soup = BeautifulSoup(html_content, "html.parser")

# Função para limpar e extrair o texto de um elemento, incluindo texto de tabelas
def extract_text(element):
    for table in element.find_all('table'):
        table_text = '\n'.join([' '.join(cell.get_text(strip=True) for cell in row.find_all(['th', 'td']))
                                for row in table.find_all('tr')])
        table.replace_with(BeautifulSoup('<p>' + table_text + '</p>', 'html.parser'))
    return element.get_text(separator=' ', strip=True)

# Função para processar o HTML e extrair os elementos desejados
def parse_html(soup):
    # Remove elementos indesejados como scripts e styles
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Procurar pelos elementos de capítulo, artigo, parágrafo, etc.
    chapters = []
    current_chapter = None
    current_article = None

    for element in soup.find_all(['p', 'ol', 'li']):
        text = extract_text(element)
        
        # Verificar se o texto corresponde a um capítulo, artigo, parágrafo, ou anexo usando expressões regulares
        if re.match(r'Capítulo \d+', text, re.IGNORECASE):
            current_chapter = {'type': 'Capítulo', 'title': text, 'content': []}
            chapters.append(current_chapter)
            current_article = None
        elif re.match(r'Art\. \d+', text, re.IGNORECASE):
            current_article = {'type': 'Artigo', 'title': text, 'content': []}
            if current_chapter:
                current_chapter['content'].append(current_article)
        elif re.match(r'§\d+', text):
            paragraph = {'type': 'Parágrafo', 'title': text, 'content': []}
            if current_article:
                current_article['content'].append(paragraph)
            elif current_chapter:
                current_chapter['content'].append(paragraph)
        elif re.match(r'Anexo \d+', text, re.IGNORECASE):
            current_chapter = {'type': 'Anexo', 'title': text, 'content': []}
            chapters.append(current_chapter)
            current_article = None
        else:
            if current_article:
                current_article['content'].append(text)
            elif current_chapter:
                current_chapter['content'].append(text)

    return chapters

# Função para exibir o conteúdo de forma estruturada
def display_content(content):
    for chapter in content:
        print(f"{chapter['type']}: {chapter['title']}")
        for article in chapter['content']:
            if isinstance(article, dict):
                print(f"  {article['type']}: {article['title']}")
                for paragraph in article['content']:
                    if isinstance(paragraph, dict):
                        print(f"    {paragraph['type']}: {paragraph['title']}")
                        for para_content in paragraph['content']:
                            print(f"      {para_content}")
                    else:
                        print(f"    {paragraph}")
            else:
                print(f"  {article}")

# Executar as funções
content = parse_html(soup)
display_content(content)

# Salvando o texto extraído em um arquivo
with open("resolucao_unicamp_2025.txt", "w", encoding="utf-8") as file:
    for chapter in content:
        file.write(f"{chapter['type']}: {chapter['title']}\n")
        for article in chapter['content']:
            if isinstance(article, dict):
                file.write(f"  {article['type']}: {article['title']}\n")
                for paragraph in article['content']:
                    if isinstance(paragraph, dict):
                        file.write(f"    {paragraph['type']}: {paragraph['title']}\n")
                        for para_content in paragraph['content']:
                            file.write(f"      {para_content}\n")
                    else:
                        file.write(f"    {paragraph}\n")
            else:
                file.write(f"  {article}\n")
