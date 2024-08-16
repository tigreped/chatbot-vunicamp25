import requests
from bs4 import BeautifulSoup

# Ao executar este script com python texto.py o link do edital será visitado com requests
# e o conteúdo HTML da página será salvo como texto corrente em uma única linha em um txt para posterior processamento

# URL da resolução
url = "https://www.pg.unicamp.br/norma/31879/0"

# Fazendo a requisição HTTP para obter o conteúdo da página
response = requests.get(url, verify=False)
html_content = response.content

# Usando BeautifulSoup para parsear o HTML
soup = BeautifulSoup(html_content, "html.parser")

# Extraindo o texto da resolução
# Remove elementos indesejados como scripts, styles, etc.
for script in soup(["script", "style"]):
    script.decompose()

# Extraindo o texto bruto
text = soup.get_text(separator="\n")

# Quebrar em linhas e remover espaços em branco nas bordas
lines = (line.strip() for line in text.splitlines())
# Quebrar linhas longas e remover espaços extras
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# Juntar o texto novamente, ignorando linhas em branco
text = ' '.join(chunk for chunk in chunks if chunk)

# Salvando o texto extraído em um arquivo
with open("resolucao_unicamp_2025_v2.txt", "w", encoding="utf-8") as file:
    file.write(text)
