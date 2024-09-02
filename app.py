from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import mysql.connector
from database import db_config,JWT_SECRET_KEY

app = Flask(__name__)

# # Configure the Flask app with a secret key for JWT
# app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY  # Change this to a secure random key

# # Initialize JWT manager
# jwt = JWTManager(app)
def get_db_connection():
    return mysql.connector.connect(**db_config)

# @app.route('/register', methods=['POST'])
# def register():
#     data = request.json
#     username = data['username']
#     password = data['password']  # In a real app, hash the password before storing it

#     connection = get_db_connection()
#     cursor = connection.cursor()
    
#     try:
#         cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
#         connection.commit()
#         return jsonify(message="User registered successfully"), 201
#     except mysql.connector.Error as err:
#         return jsonify(message=f"Error: {err}"), 500
#     finally:
#         cursor.close()
#         connection.close()

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     username = data['username']
#     password = data['password']

#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)
    
#     cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
#     user = cursor.fetchone()
    
#     cursor.close()
#     connection.close()

#     if user:
#         access_token = create_access_token(identity={'username': username})
#         return jsonify(access_token=access_token), 200
#     else:
#         return jsonify(message="Invalid credentials"), 401

# @app.route('/protected', methods=['GET'])
# @jwt_required()
# def protected():
#     current_user = get_jwt_identity()
#     return jsonify(logged_in_as=current_user), 200




@app.route('/course',methods=['POST','GET'])
def course_insert() :
   if request.method=="POST" :
        try :
            data = request.json
            conn =get_db_connection()
            mycommand=conn.cursor()
            Is_exists ="select * from course where name =%s"
            mycommand.execute(Is_exists , [data['name']])
            result=mycommand.fetchall()
            if result :
                mycommand.close()
                conn.close()                
                return jsonify({'status_code':400 ,'message':'data already  exists'})
            else :
                query="insert into course(name) values (%s);"        
                mycommand.execute(query ,[data['name']])
                conn.commit()
                mycommand.close()
                conn.close()
                return jsonify({'status_code':201})
            
        except :
            
            return jsonify({'status_code':404})
        
   if request.method=="GET" :
       try :
            
            conn =get_db_connection()
            mycommand=conn.cursor()
            query ="select * from course "
            mycommand.execute(query)
            result =mycommand.fetchall()
            if result :
                mycommand.close()
                conn.close()
                return jsonify({'status_code':200, 'data':result})     
             
            else :
                return jsonify({'status_code':404 , 'message':'the records are empty'})
       except :
           return jsonify({'status_code':400})
       
       
        
        
        
@app.route('/course/<int:id>',methods=["GET","POST","DELETE"])
def update_course(id):
    if request.method=="POST" :
        try :
            conn=get_db_connection()
            id = [request.args.get("id")]
            name = [request.args.get("name")]
            # data =request.json
            mycommand =conn.cursor()
            Is_exists ="select * from course where id =%s"
            mycommand.execute(Is_exists,id)
            result =mycommand.fetchall()
            if result :
                query ="UPDATE `course` SET `id`='%s',`name`='%s' WHERE id=%s"
                mycommand.execute(query,id ,name,id)
                conn.commit()
                conn.close()
                mycommand.close()
                return jsonify({'status_code':201})
            else :
                conn.close()
                mycommand.close()
                return jsonify({'status_code':404 ,' message ':' the record doesnot exists '})
                
            
        except :
            conn.close()
            mycommand.close()
            return jsonify({'status_code':400})
    
    if request.method=="GET" :
        id = [request.args.get("id")]
        name = [request.args.get("name")]
        
        try :
            conn=get_db_connection()
            mycommand =conn.cursor(dictionary=True)
            if name and id :
                 query ="select * from course where name =%s and id =%s"
                 mycommand.execute(query , name ,id )
                 conn.close()
                 mycommand.close()
                 return jsonify({'status_code':200 , [id ,name] :result})
            elif name :
                 query  ="select * from course where name =%s "
                 result =mycommand.execute(query ,name )            
                 conn.close()
                 mycommand.close()
                 return jsonify({'status_code':200 , name:result})
            elif id :
                 query  ="select * from course where id =%s "
                 result =mycommand.execute(query ,id )            
                 conn.close()
                 mycommand.close()
                 return jsonify({'status_code':200 ,id :result})
            else :
                 conn.close()
                 mycommand.close()
                 return jsonify({'status_code':404 ,'message': 'the arguments are missing'})
        except :
            conn.close()
            mycommand.close()
            return jsonify({'status_code':404})
            
            
        
        



if __name__ == '__main__' :
    app.run(debug=True)
