import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PW'),
        host=os.getenv('POSTGRES_URL')
    )
    return conn

def store_vector_in_db(file_path, vector, text):
    conn = connect_db()
    cur = conn.cursor()

    check_query = "SELECT COUNT(*) FROM file_vectors WHERE vector = %s"

    vector_str = str(vector.tolist())

    cur.execute(check_query, (vector_str,))

    count = cur.fetchone()[0]
    result = ''

    if count == 0:
        insert_query = "INSERT INTO file_vectors (file_path, vector, text) VALUES (%s, %s, %s)"
        cur.execute(insert_query, (file_path, vector.tolist(), text))
        conn.commit()
        result = 'Vector inserted successfully.'
    else:
        result = 'Vector already exists in the database.'

    cur.close()
    conn.close()
    return result

def find_similar_vectors(query_vector, top_k=5):
    conn = connect_db()
    cur = conn.cursor()

    query = """
        SELECT file_path, text, vector <=> %s AS similarity
        FROM file_vectors
        ORDER BY similarity
        LIMIT %s;
    """

    cur.execute(query, (str(query_vector.tolist()), top_k))
    results = cur.fetchall()
    
    cur.close()
    conn.close()
    
    formatted_results = [
        {'file_path': row[0], 'text': str(row[1]).replace('\n', '. '), 'similarity': row[2]} for row in results
    ]
    
    return formatted_results