import os
from sentence_transformers import SentenceTransformer
from .text_extraction import extract_text

model = SentenceTransformer('all-MiniLM-L6-v2')

def process_file(file_path):
    text = extract_text(file_path)
    vector = model.encode(text)
    return text, vector

