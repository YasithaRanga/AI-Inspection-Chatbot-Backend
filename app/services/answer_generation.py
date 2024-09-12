from transformers import pipeline

qa_model = pipeline("question-answering", model="deepset/roberta-base-squad2")

def generate_answer(question, documents):    
    result = qa_model(question=question, context=documents)
    return result["answer"]