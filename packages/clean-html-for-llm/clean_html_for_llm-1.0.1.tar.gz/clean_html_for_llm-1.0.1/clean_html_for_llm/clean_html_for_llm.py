# clean_html/clean_html.py

import re

def clean_html_for_llm(html_to_clean, tags_to_remove=['style', 'svg', 'script'], attributes_to_keep=['id', 'href']):
    for tag in tags_to_remove:
        html_to_clean = re.sub(rf'<{tag}[^>]*>.*?</{tag}>', '', html_to_clean, flags=re.DOTALL)

    attributes_to_keep = '|'.join(attributes_to_keep)
    pattern = rf'\b(?!({attributes_to_keep})\b)\w+(?:-\w+)?\s*=\s*["\'][^"\']*["\']'
    cleaned_html = re.sub(pattern, '', html_to_clean)
    return cleaned_html
