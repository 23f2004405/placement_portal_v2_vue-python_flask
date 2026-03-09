from flask_restful import Resource
from flask import request ,jsonify,make_response
from flask_security import utils,auth_token_required,current_user
import sqlalchemy as sa 
from controllers.user_datastore import user_datastore
from controllers.database import db
from controllers.model import User,Company,Student
import uuid

class LoginApi(Resource):
    def post(self):
        login_credentials = request.get_json()

        if not login_credentials:
            result = {'message':'Login credentials are required.'}

            return make_response(jsonify(result),400)
        
        username = login_credentials.get('username',None)
        
        password = login_credentials.get('password',None)

        if  not password or not username:
            result ={'message':'All fields are required.Dont miss any.'}

            return make_response(jsonify(result),400)
        
        user = user_datastore.find_user(username=username)
        
        if not user:
            result ={'message':'User Not Found.'}

            return make_response(jsonify(result),400)
        
        if not utils.verify_password(password,user.password):
            result={'message':'Invalid Password'}
            
            return make_response(jsonify(result),401)
        
        if not user.active:
            return make_response(jsonify({'message':'User is Blacklisted'}),403)
        
    

        auth_token = user.get_auth_token()
        role_names = [role.name for role in user.roles]
        role_based_id = None

        if "ADMIN" in role_names:
            role_based_id = user.id

        elif "STUDENT" in role_names:
            if user.student:
                role_based_id = user.student.id

        elif "COMPANY" in role_names:
            if user.company:
                role_based_id = user.company.id

        response = {
            'message':'Login successful.',
            'user_details':{
                'role_based_id':role_based_id,
                'username':user.username,
                'roles':[role.name for role in user.roles],
                'auth_token':auth_token
            }
        }
        
        return make_response(jsonify(response),200)
    
class LogoutApi(Resource):
     @auth_token_required
     def post(self):
        user_datastore.set_token_uniquifier(current_user)
        db.session.commit()

        return make_response(jsonify({
            "message": "Logged out successfully."
        }), 200)


class RegisterApi(Resource):

    def post(self):

        creds = request.get_json()

        if not creds:
            return make_response(jsonify({
                "message": "Credentials required."
            }), 400)

        username = creds.get("username")
        email = creds.get("email")
        password = creds.get("password")
        role = creds.get("role")

        if not username or not email or not password or not role:
            return make_response(jsonify({
                "message": "Username, email, password and role are required."
            }), 400)

       
        if user_datastore.find_user(username=username):
            return make_response(jsonify({
                "message": "Username already exists."
            }), 400)

        user_role = user_datastore.find_role(role)

        if not user_role:
            return make_response(jsonify({
                "message": "Invalid role."
            }), 400)


        if role == "STUDENT":

            name = creds.get("name")
            roll_number = creds.get("roll_number")
            department = creds.get("department")
            cgpa = creds.get("cgpa")
            passing_out_year = creds.get("passing_out_year")

            if not name or not roll_number:
                return make_response(jsonify({
                    "message": "Name and roll number are required."
                }), 400)

            existing_student = db.session.scalar(
                sa.select(Student).where(Student.roll_number == roll_number)
            )

            if existing_student:
                return make_response(jsonify({
                    "message": "Roll number already exists."
                }), 400)

        elif role == "COMPANY":

            company_name = creds.get("company_name")
            hr_contact = creds.get("hr_contact")
            website = creds.get("website")

            if not company_name:
                return make_response(jsonify({
                    "message": "Company name is required."
                }), 400)


        try:

            user = user_datastore.create_user(
                username=username,
                email=email,
                password=password,
                roles=[user_role]
            )

            if role == "STUDENT":

                student = Student(
                    name=name,
                    roll_number=roll_number,
                    department=department,
                    cgpa=cgpa,
                    passing_out_year=passing_out_year,
                    user=user
                )

                db.session.add(student)

            elif role == "COMPANY":

                company = Company(
                    company_name=company_name,
                    hr_contact=hr_contact,
                    website=website,
                    user=user
                )

                db.session.add(company)

            db.session.commit()

        except Exception as e:

            db.session.rollback()

            return make_response(jsonify({
                "message": "Registration failed",
                "error": str(e)
            }), 500)

        return make_response(jsonify({
            "message": "Registration successful",
            "user_details": {
                "username": user.username,
                "email": user.email,
                "role": user_role.name
            }
        }), 201)