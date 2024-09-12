from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from ..services.file_processing import process_file
from ..services.vector_db import store_vector_in_db
from ..services.vector_db import find_similar_vectors
from sentence_transformers import SentenceTransformer
from ..services.answer_generation import generate_answer
from ..services.conversation import save_conversation, get_conversation


query_bp = Blueprint('query', __name__)

UPLOAD_FOLDER = 'uploads/'
model = SentenceTransformer('all-MiniLM-L6-v2')


@query_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    
    text_data, vector = process_file(file_path)
    
    message = store_vector_in_db(file_path, vector, text_data.replace('\x00', ''))
    
    return jsonify({'message': message}), 200

@query_bp.route('/query', methods=['POST'])
def handle_query():
    user_query = request.json.get('query')
    is_followup = request.json.get("is_followup", False)

    if not user_query:
        return jsonify({'error': 'No query provided'}), 400
    
    query_vector = model.encode(user_query)
        
    if is_followup:
        conversation_history = get_conversation()
        documents = "\n\n\n\n".join([conv['documents'] for conv in conversation_history])
    else:
        documents = find_similar_vectors(query_vector)
        documents = "\n\n\n\n".join([doc['text'] for doc in documents])

    answer = generate_answer(user_query, documents)

    save_conversation(user_query, answer, documents, is_followup)
    
    return jsonify({"answer": answer}), 200