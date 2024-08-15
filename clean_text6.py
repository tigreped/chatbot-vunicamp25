import re
import json

def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def parse_text_to_json(text):
    # Regex patterns
    chapter_pattern = re.compile(r'\bCapítulo\s+([IVXLCDM]+)\s+-\s+(.*)\b')
    annex_pattern = re.compile(r'\bANEXO\s+([IVXLCDM]+)\b')
    article_pattern = re.compile(r'\bArt\.\s*\d+\b')
    paragraph_pattern = re.compile(r'\b§\s*\d+º?\b')

    structured_data = []

    # Split text into chapters and annexes
    chapters_and_annexes = re.split(r'\b(Capítulo\s+[IVXLCDM]+\s+-\s+.*|ANEXO\s+[IVXLCDM]+)\b', text)

    # Process each chapter or annex
    current_chapter_or_annex = None
    current_items = []

    for segment in chapters_and_annexes:
        if chapter_pattern.match(segment) or annex_pattern.match(segment):
            # Save the previous chapter or annex if exists
            if current_chapter_or_annex:
                structured_data.append(current_chapter_or_annex)

            # Start a new chapter or annex
            match = chapter_pattern.match(segment)
            if match:
                current_chapter_or_annex = {
                    "capitulo": match.group(1),
                    "titulo": match.group(2),
                    "itens": []
                }
            else:
                match = annex_pattern.match(segment)
                if match:
                    current_chapter_or_annex = {
                        "anexo": match.group(1),
                        "conteudo": segment
                    }

            current_items = []

        else:
            # Process the content of the current chapter or annex
            if current_chapter_or_annex:
                items = re.split(r'\b(Art\.\s*\d+|§\s*\d+º?)\b', segment)
                for item in items:
                    item = item.strip().replace("\n", " ")
                    if item:
                        if article_pattern.match(item):
                            current_items.append({
                                "tipo": "artigo",
                                "conteudo": item
                            })
                        elif paragraph_pattern.match(item):
                            current_items.append({
                                "tipo": "paragrafo",
                                "conteudo": item
                            })
                        else:
                            current_items.append({
                                "tipo": "texto",
                                "conteudo": item
                            })

                current_chapter_or_annex["itens"] = current_items

    # Add the last chapter or annex
    if current_chapter_or_annex:
        structured_data.append(current_chapter_or_annex)

    return structured_data

def save_to_json(structured_data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(structured_data, file, ensure_ascii=False, indent=4)

def main():
    file_path = 'resolucao_unicamp_2025.txt'
    output_file = 'resolucao_unicamp_2025_v6.json'

    text = load_text(file_path)
    structured_data = parse_text_to_json(text)
    save_to_json(structured_data, output_file)

if __name__ == '__main__':
    main()
