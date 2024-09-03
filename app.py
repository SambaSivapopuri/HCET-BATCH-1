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
            name =[data['name']]
            conn =get_db_connection()
            mycommand=conn.cursor()
            Is_exists ="select * from course where name =%s"
            mycommand.execute(Is_exists , name)
            result=mycommand.fetchone()
            if result :
                mycommand.close()
                conn.close()                
                return jsonify({'status_code':400 ,'message':'data already  exists'})
            else :
                query="insert into course (name) values (%s)"        
                mycommand.execute(query ,name)
                conn.commit()
                mycommand.close()
                conn.close()
                return jsonify({'status_code':201})
            
        except :
            
            return jsonify({'status_code':404, "error":"the code isnt runnig"})
        
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
                return jsonify({'status_code':400 , 'message':'the records are empty'})
       except :
           return jsonify({'status_code':404})
       
       
        
        
        
@app.route('/course/<int:id>',methods=["GET","PUT","DELETE"])
def update_course(id):
    if request.method=="PUT" :
        try :
            conn=get_db_connection()            
            data =request.json
            name=data['name']
            mycommand =conn.cursor()
            Is_exists ="select * from course where id =%s"
            mycommand.execute(Is_exists,[id] )
            result =mycommand.fetchone()
            
            
            
            if result :
                query ="UPDATE course SET  name = %s WHERE id=%s"
                mycommand.execute(query, [name,id])
                conn.commit()
                conn.close()
                mycommand.close()
                return jsonify({'status_code':201,'data':[result]})
            else :
                conn.close()
                mycommand.close()
                return jsonify({'status_code':404 ,' message ':' the record doesnot exists '})
            
        except :
            
            return jsonify({'status_code':400, 'message':'error'})
    
    if request.method=="GET" :
        
       
        
        
        try :
            conn=get_db_connection()
            mycommand =conn.cursor(dictionary=True)
           
             
            if id :
                 query  ="select * from course where id =%s "
                 mycommand.execute(query ,[id])
                 result =mycommand.fetchone()                      
                 
                 if result :
                     conn.close()
                     mycommand.close()
                     return jsonify({'status_code':200 ,'message' :[result]})
                 else :
                     conn.close()
                     mycommand.close()
                     return jsonify({'status_code':400 ,'message' :'the records are not existing'})
                     
                       
             
            else :
                 conn.close()
                 mycommand.close()
                 return jsonify({'status_code':404 ,'message': 'the arguments are missing'})
             
        except :
            
            return jsonify({'status_code':500 , 'messsage ':'error'})
        
        
    if request.method=="DELETE" :
        try :
        
            conn =get_db_connection()
            mycommand =conn.cursor(dictionary=True)
            exists ="select * from course where id =%s"
            mycommand.execute(exists ,[id])
            Is_exists =mycommand.fetchone()
            
            if Is_exists :
                query ="delete  from course where id =%s"
                mycommand.execute(query,[id])
                conn.commit()
                mycommand.close()
                conn.close()
                return jsonify({'status_code':204 , 'message' :'the record  deleted successfully'})
            else :
                mycommand.close()
                conn.close()
                return jsonify({'status_code':400 ,'message':'no records to delete'})
            
        except :
            return jsonify({'status_code':404})
            
            
        
        
        
        
# @app.route('/year',methods =['POST','GET'])
# def year_insert() :
#      if request.method=="POST" :
#         try :
#             data = request.json
#             conn =get_db_connection()
#             mycommand=conn.cursor()
#             exists="select * from year where id=%s"
#             mycommand.execute(exists,[data['id']])
#             Is_exists =mycommand.fetchall()
#             if Is_exists:
#                 mycommand.close()
#                 conn.close()
#                 return jsonify({'status_code':400,'message':'the record already existed '})
                
#             else :
#                 query ="insert into year (year) values (%s);"
#                 result =mycommand.execute(query,[data['year']])
#                 conn.commit()
#                 mycommand.close()
#                 conn.close()
#                 return  jsonify({'status_code':201,'data':result })
#         except :
            
            
#             return jsonify({'status_code':404})
        
        
        
#      if request.method=="GET" :
#         try :
#             data = request.json
#             id = int(request.args.get("id"))
            
#             conn =get_db_connection()
#             mycommand=conn.cursor(dictionary=True)
#             exists="select * from year where id=%d"
#             mycommand.execute(exists,id)
#             Is_exists =mycommand.fetchall()
#             if Is_exists :
                
#                 mycommand.execute(exists,id)
#                 mycommand.fetchall()
#                 mycommand.close()
#                 conn.close()
#                 return jsonify({'status_code':200})
#             else :
#                 mycommand.close()
#                 conn.close()
#                 return jsonify({'status_code':400 , 'message':'the record doesnt exists '})
                
            
             
#         except :
            
#             conn.close()
#             return jsonify({'status_code':404})
        
        
# @app.route('/year/<int:id>',methods =['POST','GET','DELETE'])
# def year_update():
#     if request.method=='POST' :
#         try :
#             conn=get_db_connection()
#             mycommand=conn.cursor()
#             id=int(request.args.get('id'))
#             year =int(request.args.get('year'))
#             exists ="select * from year where id =%d"
#             mycommand.execute(exists ,id)
#             Is_exists =mycommand.fetchall()
#             if Is_exists :
#                 query ="update year set id =%d and year=%d where id =%d;"
#                 mycommand.execute(query ,id ,year,id)
#                 conn.commit()
#                 mycommand.close()
#                 conn.close()
#                 return jsonify({'status_code':204 , id :'the record has been updated successfully'})
#             else :
#                 conn.close()
#                 mycommand.close()
#                 return jsonify({'status_code':400, 'message':'the record doesnt exists'})
#         except :
#             conn.close()
#             return jsonify({'status_code':404})
    
    
#     if request.method=="GET" :
#         try :
            
#             conn =get_db_connection()
#             id =int(request.args.get('id'))
#             year=int(request.args.get('year'))
#             mycommand=conn.cursor(dictionary=True)
#             exists ="select * from year where id =%d"
#             mycommand.execute(exists ,id )
#             Is_exists=mycommand.fetchall()
#             if Is_exists :
#                 mycommand.execute(exists ,id )
#                 mycommand.fetchall()
#                 conn.close()
#                 mycommand.close()
#                 return jsonify({'status_code':200})
#             else :
#                 conn.close()
#                 mycommand.close()
#                 return jsonify({'status_code':400, 'message':'the record doesnot exists'})
            
                
                
#         except :
#             conn.close()
            
#             return jsonify({'status_code':404, 'message':'the record doesnot exists'})
            
#     if request.method=="DELETE" :
#         try :
            
#             conn =get_db_connection()
#             id =int(request.args.get('id'))
#             year=int(request.args.get('year'))
#             mycommand=conn.cursor(dictionary=True)
#             exists ="select * from year where id =%d"
#             mycommand.execute(exists ,id )
#             Is_exists=mycommand.fetchall()
#             if Is_exists :
#                 query ="delete year where id =%d"
#                 mycommand.execute(query,id)
#                 conn.commit()
#                 conn.close()
#                 mycommand.close()
#                 return jsonify({'status_code':204})
#             else :
#                 conn.close()
#                 mycommand.close()
#                 return jsonify({'status_code':400, 'message':'the record doesnot exists'})
            
                
                
#         except :
#             conn.close()
#             mycommand.close()
#             return jsonify({'status_code':404, 'message':'the record doesnot exists'})
        
        
            


# @app.route('/sem',methods =['POST','GET'])
# def sem_insert() :
#      if request.method=="POST" :
#         try :
#             data = request.json
#             conn =get_db_connection()
#             mycommand=conn.cursor()
#             exists="select * from sem where id=%s"
#             mycommand.execute(exists,[data['id']])
#             Is_exists =mycommand.fetchall()
#             if Is_exists:
#                 mycommand.close()
#                 conn.close()
#                 return jsonify({'status_code':400,'message':'the record already existed '})
                
#             else :
#                 query ="insert into sem (sem) values (%s);"
#                 result =mycommand.execute(query,[data['sem']])
#                 conn.commit()
#                 mycommand.close()
#                 conn.close()
#                 return  jsonify({'status_code':201,'data':result })
#         except :
#             mycommand.close()
#             conn.close()
#             return jsonify({'status_code':404})
#      if request.method=="GET" :
#         try :
#             data = request.json
#             id = int(request.args.get("id"))
            
#             conn =get_db_connection()
#             mycommand=conn.cursor(dictionary=True)
#             exists="select * from sem where id=%d"
#             mycommand.execute(exists,id)
#             Is_exists =mycommand.fetchall()
#             if Is_exists :
                
#                 mycommand.execute(exists,id)
#                 mycommand.fetchall()
#                 mycommand.close()
#                 conn.close()
#                 return jsonify({'status_code':200})
#             else :
#                 mycommand.close()
#                 conn.close()
#                 return jsonify({'status_code':400 , 'message':'the record doesnt exists '})
                
            
             
#         except :
            
#             conn.close()
#             return jsonify({'status_code':404})
        
        
        


# @app.route('/sem/<int:id>',methods =['POST','GET','DELETE'])
# def sem_update(id):
#     if request.method=='POST' :
#         try :
#             conn=get_db_connection()
#             mycommand=conn.cursor()
#             data =request.get_json
#             exists ="select * from sem where id =%d"
#             mycommand.execute(exists ,[data['id']])
#             Is_exists =mycommand.fetchall()
#             if Is_exists :
#                 query ="update sem set id =%d and sem=%d where id =%d;"
#                 mycommand.execute(query ,[data['id'] ,['sem'],['id']])
#                 conn.commit()
#                 mycommand.close()
#                 conn.close()
#                 return jsonify({'status_code':204 , id :'the record has been updated successfully'})
#             else :
#                 mycommand.close()
#                 conn.close()
               
#                 return jsonify({'status_code':400, 'message':'the record doesnt exists'})
#         except :
            
#             return jsonify({'status_code':404})
    
    
#     if request.method=="GET" :
#         try :
            
#             conn =get_db_connection()
#             id =int(request.args.get('id'))
#             sem=int(request.args.get('sem'))
#             mycommand=conn.cursor(dictionary=True)
#             exists ="select * from sem where id =%d"
#             mycommand.execute(exists ,id )
#             Is_exists=mycommand.fetchall()
#             if Is_exists :
#                 mycommand.execute(exists ,id )
#                 mycommand.fetchall()
#                 conn.close()
#                 mycommand.close()
#                 return jsonify({'status_code':200})
#             else :
#                 conn.close()
#                 mycommand.close()
#                 return jsonify({'status_code':400, 'message':'the record doesnot exists'})
            
                
                
#         except :
            
            
#             return jsonify({'status_code':404, 'message':'the record doesnot exists'})
            
#     if request.method=="DELETE" :
#         try :
            
#             conn =get_db_connection()
#             id =int(request.args.get('id'))
#             mycommand=conn.cursor(dictionary=True)
#             exists ="select * from sem where id =%d"
#             mycommand.execute(exists ,id )
#             Is_exists=mycommand.fetchall()
#             if Is_exists :
#                 query ="delete sem where id =%d"
#                 mycommand.execute(query,id)
#                 conn.commit()
#                 mycommand.close()
#                 conn.close()
                
#                 return jsonify({'status_code':204})
#             else :
#                 conn.close()
#                 mycommand.close()
#                 return jsonify({'status_code':400, 'message':'the record doesnot exists'})
            
                
                
#         except :
#             conn.close()
#             mycommand.close()
#             return jsonify({'status_code':404, 'message':'the record doesnot exists'})
        
        
            


        
        

             



if __name__ == '__main__' :
    app.run(debug=True)
