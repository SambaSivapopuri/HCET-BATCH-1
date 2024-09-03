from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import mysql.connector
from database import db_config,JWT_SECRET_KEY

app = Flask(__name__)

# Configure the Flask app with a secret key for JWT
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY  # Change this to a secure random key

# Initialize JWT manager
jwt = JWTManager(app)
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']  # In a real app, hash the password before storing it

    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        connection.commit()
        return jsonify(message="User registered successfully"), 201
    except mysql.connector.Error as err:
        return jsonify(message=f"Error: {err}"), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    
    cursor.close()
    connection.close()

    if user:
        access_token = create_access_token(identity={'username': username})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message="Invalid credentials"), 401

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
def test():
    return "test"

if __name__ == '__main__':
    app.run(debug=True)
