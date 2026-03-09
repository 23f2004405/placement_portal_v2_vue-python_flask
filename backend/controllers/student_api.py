from flask_restful import Resource
from flask import request ,jsonify,make_response,current_app,send_from_directory
from flask_security import auth_token_required,roles_required,current_user
import sqlalchemy as sa
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid
from extensions import cache


from controllers.database import db
from controllers.model import *

class UploadResumeApi(Resource):
    @auth_token_required
    @roles_required("STUDENT")
    def post(self):

        if "resume" not in request.files:
            return make_response(jsonify({"message": "No file uploaded"}), 400)

        file = request.files["resume"]

       
        if file.filename == "":
            return make_response(jsonify({"message": "No selected file"}), 400)

      
        if not file.filename.lower().endswith(".pdf"):
            return make_response(jsonify({"message": "Only PDF allowed"}), 400)

        student = current_user.student

        upload_folder = current_app.config["UPLOAD_FOLDER"]

        if student.resume:
            old_file_path = os.path.join(upload_folder, student.resume)

            if os.path.exists(old_file_path):
                os.remove(old_file_path)

       
        original_filename = secure_filename(file.filename)

   
        unique_id = uuid.uuid4().hex
        new_filename = f"{unique_id}_{original_filename}"

        file_path = os.path.join(upload_folder, new_filename)

        file.save(file_path)

        student.resume = new_filename
        db.session.commit()
        cache.delete(f"student_{student.id}")

        return make_response(jsonify({"message": "Resume uploaded successfully"}), 200)

class ApprovedDrives(Resource):
    @auth_token_required
    @roles_required("STUDENT")
    def get(self):
        cgpa=request.args.get('cgpa',None)
        if cgpa is not None:
            cgpa = float(cgpa)
        drive_id=request.args.get('drive_id',None)
        if drive_id is not None:
            drive_id=int(drive_id)
        company_name=request.args.get('company_name',None)
        year=request.args.get('year',None)
        if year is not None:
            year=int(year)
        student = current_user.student

        subquery = (sa.select(Application.id).where(Application.student_id == student.id,Application.drive_id == PlacementDrive.id))

        query = (sa.select(PlacementDrive).join(Company).where(PlacementDrive.status == DriveStatus.APPROVED,PlacementDrive.application_deadline > datetime.utcnow(),~sa.exists(subquery)))
        if cgpa:
            query=query.where(PlacementDrive.min_cgpa<=cgpa)
        if company_name:
            query=query.where(Company.company_name.ilike(f"%{company_name}%"))
        if year:
            query=query.where(PlacementDrive.passing_out_year==year)
        if drive_id:
            query=query.where(PlacementDrive.id==drive_id)
        drives=db.session.scalars(query).all()
        result=[]
        for drive in drives:
            data={
                "drive_id":drive.id,
                "company_name":drive.company.company_name,
                "title":drive.title,
                 "application_deadline":drive.application_deadline.isoformat() if drive.application_deadline else None
            }
            result.append(data)
        return make_response(jsonify(result),200)

class StudentDriveDetails(Resource):
    @auth_token_required
    @roles_required("STUDENT")
    def get(self,drive_id):
        drive=db.session.get(PlacementDrive,drive_id)
        if not drive:
            return make_response(jsonify({"message":"Drive not found."}),404)
        if drive.status!=DriveStatus.APPROVED:
            return make_response(jsonify({"message":"Drive not yet available for application."}),403)
        can_apply=True
        if drive.min_cgpa:
            if drive.min_cgpa>current_user.student.cgpa:
                can_apply=False
        if drive.passing_out_year:
            if drive.passing_out_year!=current_user.student.passing_out_year:
                can_apply=False
        if drive.application_deadline and drive.application_deadline < datetime.utcnow():
            can_apply = False
        application=db.session.scalar(sa.select(Application).where(Application.drive_id==drive_id,Application.student_id==current_user.student.id))
        if application:
            can_apply=False
        result = {
            "title":drive.title,
            "description":drive.description,
            "company_id":drive.company_id,
            "company_name":drive.company.company_name,
            "hr_contact":drive.company.hr_contact,
            "website":drive.company.website,
            "min_cgpa":drive.min_cgpa,
            "passing_out_year":drive.passing_out_year,
            "application_deadline":drive.application_deadline.isoformat() if drive.application_deadline else None,
            "can_apply":can_apply,
            'status':drive.status.value
        }
        return make_response(jsonify(result),200)

class StudentApplyDrive(Resource):
    @auth_token_required
    @roles_required("STUDENT")
    def post(self,drive_id):
        student=current_user.student
        drive=db.session.get(PlacementDrive,drive_id)
        if not drive:
            return make_response(jsonify({"message":"Drive not found."}),404)
        if drive.status != DriveStatus.APPROVED:
            return make_response(jsonify({"message": "Drive not open for applications."}), 403)
        if drive.application_deadline and drive.application_deadline < datetime.utcnow():
            return make_response(jsonify({"message": "Application deadline passed."}), 403)
        application=db.session.scalar(sa.select(Application).where(Application.drive_id==drive_id,Application.student_id==current_user.student.id))
        if application:
             return make_response(jsonify({"message":"Already Applied!!!."}),403)
        appl= Application(student=student,drive=drive)
        db.session.add(appl)
        try:
            db.session.commit()
            return make_response(jsonify({"message":"Application successful!!!."}),200)
        except:
            db.session.rollback()
            return make_response(jsonify({"message":"Action failed."}),403)
        
class UpdateProfile(Resource):
    @auth_token_required
    @roles_required("STUDENT")
    def put(self):
        student=current_user.student
        data= request.get_json()

        student.name = data.get("name")
        student.cgpa = data.get("cgpa")
        student.department = data.get("department")
        student.roll_number = data.get("roll_number")
        student.passing_out_year = data.get("passing_out_year")
        student.user.email = data.get("email")
        try:
            db.session.commit()
            cache.delete(f"student_{student.id}")
            return make_response(jsonify({"message":"Profile Updated"}),200)
        except:
            db.session.rollback()
            return make_response(jsonify({"message":"An Error Occurred."}),400)
        
class StudentApplicationHistory(Resource):
    @auth_token_required
    @roles_required("STUDENT")
    def get(self):
        student = current_user.student
        
        application_status= request.args.get("application_status")

        if application_status:
            application_status = application_status.upper()

        if application_status:
            try:
                application_status = ApplicationStatus[application_status]
            except:
                return make_response(jsonify({"error": "Invalid application status"}, 400))
        
        applications=db.session.scalars(sa.select(Application).where(Application.status==application_status,Application.student_id==student.id)).all()
        result=[]
        for application in applications:
            data = {
                "application_id":application.id,
                "drive_id":application.drive_id,
                "title":application.drive.title,
                "company_name":application.drive.company.company_name,
                "status":application.status.value
            }
            result.append(data)
        return make_response(jsonify(result),200)
    

# class ExportApplicationsCsv(Resource):
#     @auth_token_required
#     @roles_required("STUDENT")
#     def get(self):
#         student_id = current_user.student.id  

#         export_applications_csv.delay(student_id)

#         return make_response(jsonify({
#             "message": "CSV export started. You will get an email when it's ready."
#         }), 200)

# EXPORT_FOLDER = "exports"

# class DownloadCSV(Resource):
#     @auth_token_required
#     @roles_required("STUDENT")
#     def get(self,filename):
#         file_path=os.path.join(EXPORT_FOLDER,filename)
#         if not os.path.exists(file_path):
#             return make_response(jsonify({"message": "File not found"}), 404)
#         return send_from_directory(EXPORT_FOLDER, filename, as_attachment=True)


