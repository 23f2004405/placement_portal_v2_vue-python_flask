from flask_restful import Resource
from flask import request ,jsonify,make_response,current_app,send_from_directory
from flask_security import auth_token_required,roles_accepted,current_user
import sqlalchemy as sa
from extensions import cache

from controllers.database import db
from controllers.model import *

class DriveDetailResource(Resource):
#this class gives the drive details for a drive .. the roles who can access it are company and admin.each get their own respective response
    @auth_token_required
    @roles_accepted("ADMIN", "COMPANY")
    def get(self, drive_id):

        drive = db.session.get(PlacementDrive, drive_id)

        if not drive:
            return make_response(jsonify({"message": "Drive not found"}), 404)

        if current_user.has_role("ADMIN"):
            pass

        
        elif current_user.has_role("COMPANY"):
            if drive.company_id != current_user.company.id:
                return make_response(jsonify({"message": "Unauthorized"}), 403)
        
        application_count = db.session.scalar(sa.select(sa.func.count(Application.id)).where(Application.drive_id == drive.id))

        return make_response(jsonify({
            "id": drive.id,
            "title": drive.title,
            "description": drive.description,
            "min_cgpa": drive.min_cgpa,
            "deadline": drive.application_deadline.isoformat() if drive.application_deadline else None,
            "status": drive.status.value,
            "company": drive.company.company_name,
            "application_count":application_count
        }),200)

class StudentDetailApi(Resource):
    #this class is a resource for student details only for the admin and the student .each have their own respective responses
    @auth_token_required
    @roles_accepted("STUDENT","ADMIN")
    @cache.cached(timeout=300, key_prefix=lambda: f"student_{request.view_args['student_id']}")
    def get(self, student_id):

        student = db.session.get(Student, student_id)

        if not student:
            return make_response(jsonify({"message": "Student not found."}), 404)

        
        if current_user.has_role("STUDENT") and student.id == current_user.student.id:
            return make_response(jsonify({
                "name": student.name,
                "roll_number": student.roll_number,
                "department": student.department,
                "cgpa": student.cgpa,
                "resume": student.resume,
                "username": student.user.username,
                "email": student.user.email,
                "passing_out_year":student.passing_out_year
            }), 200)

        if current_user.has_role("ADMIN"):
            return make_response(jsonify({
                "name": student.name,
                "roll_number": student.roll_number,
                "department": student.department,
                "cgpa": student.cgpa,
                "resume": student.resume,
                "username": student.user.username,
                "email": student.user.email,
                "student_id": student.id,
                "is_blacklisted":not student.user.active
            }), 200)

        return make_response(jsonify({"message": "Unauthorized"}), 403)

class CompanyDetailApi(Resource):
    #this class is for company details for the admin and the company with each having their own respective responses.
    @auth_token_required
    @roles_accepted("ADMIN","COMPANY")
    @cache.cached(timeout=300, key_prefix=lambda: f"company_{request.view_args['company_id']}")
    def get(self, company_id):

        company = db.session.get(Company, company_id)

        if not company:
            response = {
                "message": "Company not found."
            }
            return make_response(jsonify(response), 404)

        
        if current_user.has_role("COMPANY"):
            if current_user.company.id != company_id:
                response = {
                    "message": "Unauthorized."
                }
                return make_response(jsonify(response), 403)

        
        elif current_user.has_role("ADMIN"):
            pass

        else:
            response = {
                "message": "Unauthorized."
            }
            return make_response(jsonify(response), 403)

        response = {
                "company_id": company.id,
                "company_name": company.company_name,
                "hr_contact": company.hr_contact,
                "website": company.website,
                "username": company.user.username,
                "email": company.user.email,
                "approval_status":company.approval_status.value,
                "is_blacklisted":not company.user.active
            }
        

        return make_response(jsonify(response), 200)
    

class ViewResumeApi(Resource):
    def get(self, filename):
        print(current_app.config["UPLOAD_FOLDER"])
        print(filename)

        return send_from_directory(
            current_app.config["UPLOAD_FOLDER"],
            filename
        )

