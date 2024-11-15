from flask import Flask, request, jsonify
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/suggestions', methods=['GET'])
def get_suggestions():
    query = request.args.get('q', '')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT task_text 
            FROM task_suggestions 
            WHERE task_text LIKE %s 
            ORDER BY frequency DESC 
            LIMIT 5
        """, (f"%{query}%",))
        suggestions = cursor.fetchall()
        return jsonify(suggestions), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/suggestions/add', methods=['POST'])
def add_suggestion():
    data = request.get_json()
    task_text = data.get('task_text')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO task_suggestions (task_text, frequency) 
            VALUES (%s, 1) 
            ON DUPLICATE KEY UPDATE frequency = frequency + 1
        """, (task_text,))
        conn.commit()
        return jsonify({'message': 'Suggestion added/updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(port=5003) 