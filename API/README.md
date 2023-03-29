# Student Record API
This is a Flask API for a student record system that allows saving, updating, and retrieving student information. The API uses the Flask framework and Flask-CORS extension for handling cross-origin requests. It also uses PyMySQL to interact with a MySQL database.

### The endpoints include:
- "/api/v1/save_student_record" for saving a new student record via POST request
- "/api/v1/update_student_record/int:id" for updating an existing student record via PUT request with a specific student ID
- "/api/v1/update_student_record/" for retrieving all student record via GET
- "/api/v1/student_record/int:id" for retrieving a student record via GET request with a specific student ID.
- "/api/v1/student_record/int:id" for deleting a student record via DELETE request with a specific student ID.

There are also helper functions for handling responses:
- error_response for error handling
- success_response for successful requests.