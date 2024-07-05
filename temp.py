from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

# Replace with your MySQL database connection details
app = Flask(_name_)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'username'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'database_name'

# Function to connect to MySQL database
def connect():
    try:
        conn = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DB']
        )
        if conn.is_connected():
            print('Connected to MySQL database')
        return conn
    except Error as e:
        print(e)
        return None

# API routes
@app.route('/items', methods=['GET'])
def get_items():
    try:
        conn = connect()
        if conn is not None:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM items')
            items = cursor.fetchall()
            cursor.close()
            conn.close()
            return jsonify(items), 200
        else:
            return 'Error: Could not connect to database', 500
    except Error as e:
        print(e)
        return 'Error: Could not fetch items', 500

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    try:
        conn = connect()
        if conn is not None:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM items WHERE id = %s', (item_id,))
            item = cursor.fetchone()
            cursor.close()
            conn.close()
            if item:
                return jsonify(item), 200
            else:
                return 'Item not found', 404
        else:
            return 'Error: Could not connect to database', 500
    except Error as e:
        print(e)
        return 'Error: Could not fetch item', 500

@app.route('/items', methods=['POST'])
def create_item():
    try:
        data = request.get_json()
        conn = connect()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO items (name) VALUES (%s)', (data['name'],))
            conn.commit()
            new_item_id = cursor.lastrowid
            cursor.close()
            conn.close()
            return jsonify({'id': new_item_id, 'name': data['name']}), 201
        else:
            return 'Error: Could not connect to database', 500
    except Error as e:
        print(e)
        return 'Error: Could not create item', 500

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    try:
        data = request.get_json()
        conn = connect()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute('UPDATE items SET name = %s WHERE id = %s', (data['name'], item_id))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'id': item_id, 'name': data['name']}), 200
        else:
            return 'Error: Could not connect to database', 500
    except Error as e:
        print(e)
        return 'Error: Could not update item', 500

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        conn = connect()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM items WHERE id = %s', (item_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return '', 204
        else:
            return 'Error: Could not connect to database', 500
    except Error as e:
        print(e)
        return 'Error: Could not delete item', 500

if _name_ == '_main_':
    app.run(debug=True)