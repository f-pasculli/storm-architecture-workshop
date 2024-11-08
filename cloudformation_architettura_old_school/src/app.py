from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Retrieve environment variables
DB_ENDPOINT = os.environ.get('DB_ENDPOINT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

# Database connection function
def get_db_connection():
    return pymysql.connect(
        host=DB_ENDPOINT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# GET /items
@app.route('/items', methods=['GET'])
def get_items():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT id, animale, verso FROM example_table"
            cursor.execute(sql)
            result = cursor.fetchall()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

# POST /items
@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    animale = data.get('animale')
    verso = data.get('verso')
    if not animale or not verso:
        return jsonify({'error': 'Input non valido'}), 400
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Check if the animale already exists
            sql = "SELECT id FROM example_table WHERE animale = %s"
            cursor.execute(sql, (animale,))
            existing = cursor.fetchone()
            if existing:
                return jsonify({'error': 'Elemento già esistente'}), 409
            # Insert new item
            sql = "INSERT INTO example_table (animale, verso) VALUES (%s, %s)"
            cursor.execute(sql, (animale, verso))
            connection.commit()
            return jsonify({'message': 'Elemento aggiunto'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

# PUT /items/<int:id>
@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    data = request.get_json()
    verso = data.get('verso')
    if not verso:
        return jsonify({'error': 'Input non valido'}), 400
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Check if the item exists
            sql = "SELECT id FROM example_table WHERE id = %s"
            cursor.execute(sql, (id,))
            existing = cursor.fetchone()
            if not existing:
                return jsonify({'error': 'Elemento non esistente'}), 404
            # Update item
            sql = "UPDATE example_table SET verso = %s WHERE id = %s"
            cursor.execute(sql, (verso, id))
            connection.commit()
            return jsonify({'message': 'Elemento aggiornato'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

# DELETE /items/<int:id>
@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Check if the item exists
            sql = "SELECT id FROM example_table WHERE id = %s"
            cursor.execute(sql, (id,))
            existing = cursor.fetchone()
            if not existing:
                return jsonify({'error': 'Elemento non esistente'}), 404
            # Delete item
            sql = "DELETE FROM example_table WHERE id = %s"
            cursor.execute(sql, (id,))
            connection.commit()
            return jsonify({'message': 'Elemento eliminato'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
