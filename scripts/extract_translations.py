import os
import re
import json
import glob
from pypdf import PdfReader

def extract_translations_from_pdf(pdf_path):
    translations = []
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                for line in lines:
                    # Look for pattern: Term = Translation
                    # allowing for some flexibility in whitespace
                    match = re.match(r'^(.+?)\s*=\s*(.+)$', line.strip())
                    if match:
                        term = match.group(0).strip() # The whole matching line
                        # We might want to separate key and value, but the current dictionary uses 
                        # "term": "Whole String", "content": "Whole String"
                        # So we will keep that format.
                        
                        # Basic filtering to avoid garbage
                        if len(term) < 3 or len(term) > 200:
                            continue
                            
                        translations.append({
                            "term": term,
                            "content": term
                        })
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return translations

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fontes_dir = os.path.join(base_dir, 'fontes')
    output_file = os.path.join(base_dir, 'scripts', 'extracted_translations.json')
    
    all_translations = []
    
    pdf_files = glob.glob(os.path.join(fontes_dir, '*.pdf'))
    print(f"Found {len(pdf_files)} PDF files in {fontes_dir}")
    
    for pdf_file in pdf_files:
        print(f"Processing {os.path.basename(pdf_file)}...")
        translations = extract_translations_from_pdf(pdf_file)
        print(f"  Found {len(translations)} translations.")
        all_translations.extend(translations)
        
    # Deduplicate based on 'term'
    unique_translations = []
    seen_terms = set()
    
    for item in all_translations:
        if item['term'] not in seen_terms:
            seen_terms.add(item['term'])
            unique_translations.append(item)
            
    print(f"Total unique translations found: {len(unique_translations)}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(unique_translations, f, indent=2, ensure_ascii=False)
        
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    main()
