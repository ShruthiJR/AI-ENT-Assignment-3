from flask import Flask
from flask_cors import CORS, cross_origin
import pymysql
from flask import jsonify
from flask import flash, request
from flaskext.mysql import MySQL

app = Flask(__name__)

# Configuration for MySQL connection
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'student_record'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# Helper functions to handle responses
def error_response(error=None):
    message = {
        'status': 404,
        'message': error if error else "Please try again later since there was a problem",
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone

def success_response(message,data=None):
    message = {
        'status': 200,
        'message': message,
    }
    if(data!=None):
        message['data']=data

    respone = jsonify(message)
    respone.status_code = 200
    return respone

# Endpoint for the root URL
@app.route("/")
def hello_world():
    print("test")
    return "Hello, World for AI Enterprise Demo!"

# Endpoint for saving a new student record
@app.route('/api/v1/save_student_record', methods=['POST'])
def save_student_info():
    # Retrieve data from the request body
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    date_of_birth = request.form.get('date_of_birth')    
    if request.method == 'POST' and first_name and last_name and date_of_birth:
        # Connect to MySQL database
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        try:  
            # Execute INSERT statement to save new student record
            sqlQuery = "INSERT INTO student_master(first_name,last_name,date_of_birth) VALUES(%s, %s, %s)"
            bindData = (first_name,last_name,date_of_birth)            
            cursor.execute(sqlQuery, bindData)

            # Retrieve the last added record    
            lastId = cursor.lastrowid
            cursor.execute("SELECT * FROM student_master WHERE student_id =%s", lastId)
            inserted_record = cursor.fetchone()

            # Commit the transaction and return success response
            conn.commit()

            return success_response(message='Student Infomation saved successfully', data = inserted_record)
        except Exception as e:
            print(e)
            respone = jsonify('error')
            respone.status_code = 200
            return error_response(str(e))    
        finally:
            cursor.close() 
            conn.close()
    else:
        # Return error response if required data is missing
        return error_response('Enter valid parameters') 

# Endpoint for updating an existing student record
@app.route('/api/v1/update_student_record/<int:id>', methods=['PUT'])
def update_student_info(id):
    # Get the data to update from the request body
    data = request.form

    # Generate the update statement dynamically based on which fields are present in the form data
    query = 'UPDATE student_master SET '
    values = []
    if 'first_name' in data:
        query += 'first_name=%s, '
        values.append(data['first_name'])
    if 'last_name' in data:
        query += 'last_name=%s, '
        values.append(data['last_name'])
    if 'date_of_birth' in data:
        query += 'date_of_birth=%s, '
        values.append(data['date_of_birth'])
    if 'amount_due' in data:
        query += 'amount_due=%s, '
        values.append(data['amount_due'])

    # Remove the trailing comma and space
    query = query[:-2]

    # Add the WHERE clause to update the specific row
    query += ' WHERE student_id=%s'
    values.append(id)


    if request.method == 'PUT':
        # Establish a connection to the database and create a cursor object
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        try:  
            # Execute the update statement
            cursor.execute(query, tuple(values))

            # Retrieve the updated record from the database and send it as the response
            cursor.execute("SELECT * FROM student_master WHERE student_id =%s", id)
            updated_record = cursor.fetchone()

            # Commit the transaction
            conn.commit()

            # Return a success response with the updated record as the data
            return success_response(message='Student Infomation saved successfully', data = updated_record)
        except Exception as e:
            # Print any errors that occur and return an error response
            print(e)
            respone = jsonify('error')
            respone.status_code = 200
            return error_response(str(e))    
        finally:
            # Close the cursor and the connection
            cursor.close() 
            conn.close()

    else:
        return error_response('Enter valid parameters') 

@app.route('/api/v1/student_record/<int:id>', methods=['GET'])
def get_student_info(id):
    # Check if request method is GET and a valid student ID has been provided
    if request.method == 'GET' and id:
        # Connect to the database
        conn = mysql.connect()
        # Create a cursor to execute queries
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        try:  
            # Execute a SQL query to fetch student record by ID
            cursor.execute("SELECT * FROM student_master WHERE student_id =%s", id)
            # Fetch the record using fetchone() method
            student_record = cursor.fetchone()
            # Commit the transaction
            conn.commit()
   
            # Return a success response with the student record data
            return success_response(message='Student information has been fetched successfully', data = student_record)
        except Exception as e:
            # If an error occurs, log the error and return an error response
            print(e)
            response = jsonify('error')
            response.status_code = 200
            return error_response(str(e))    
        finally:
            # Close the cursor and database connection
            cursor.close() 
            conn.close()

    else:
        # If the request method is not GET or no valid student ID has been provided, return an error response
        return error_response('Enter valid parameters')


@app.route('/api/v1/student_record/', methods=['GET'])
def get_all_student_info():
    # check if the request method is GET
    if request.method == 'GET':
        # establish a connection to the database
        conn = mysql.connect()
        # create a cursor object
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        try:  
            # execute a SELECT query to fetch all records from the student_master table
            cursor.execute("SELECT * FROM student_master")
            # fetch all the records and store them in a variable
            student_records = cursor.fetchall()
            # commit the transaction
            conn.commit()
            # return a success response with the message and the data
            return success_response(message='Students information fetched successfully', data = student_records)
        except Exception as e:
            # if an exception is thrown, print the error and return an error response
            print(e)
            respone = jsonify('error')
            respone.status_code = 200
            return error_response(str(e))    
        finally:
            # close the cursor object
            cursor.close() 
            # close the database connection
            conn.close()

    else:
        # if the request method is not GET, return an error response
        return error_response('Enter valid parameters')


@app.route('/api/v1/student_record/<int:id>', methods=['DELETE'])
def delete_student_info(id):

    # Check if the method is DELETE and an id is provided
    if request.method == 'DELETE' and id:
        # Connect to the database
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        try:  
            # Execute the DELETE query for the provided id
            cursor.execute("DELETE FROM student_master WHERE student_id=%s", (id,))
            conn.commit()
   
            # Return a success response message
            return success_response(message='Student information deleted successfully')
        except Exception as e:
            print(e)
            # If there's an exception, return an error response message with the exception details
            response = jsonify('error')
            response.status_code = 200
            return error_response(str(e))    
        finally:
            # Close the database connection and cursor
            cursor.close() 
            conn.close()

    else:
         # If the request method or id is invalid, return an error response message
        return error_response('Enter valid parameters') 

app.run()

CORS(app)