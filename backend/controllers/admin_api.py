from flask_restful import Resource
from flask import request ,jsonify,make_response
from flask_security import utils,auth_token_required,roles_required,current_user
import sqlalchemy as sa
from extensions import cache

from controllers.database import db
from controllers.model import *

class AdminDriveApprovalResource(Resource):
    ##{"action":"approve"}
    @auth_token_required
    @roles_required("ADMIN")
    def put(self, drive_id):
        drive = db.session.get(PlacementDrive, drive_id)

        if not drive:
            return make_response(jsonify({"message": "Drive not found."}), 404)

        if drive.status == DriveStatus.CLOSED:
            return make_response(jsonify({
                "message": "Closed drives cannot be modified."
            }), 400)

        fields = request.get_json()
        action = fields.get("action")  

        if action == "approve":
            drive.status = DriveStatus.APPROVED

        elif action == "reject":
            drive.status = DriveStatus.CANCELLED

        else:
            return make_response(jsonify({
                "message": "Invalid action."
            }), 400)

        db.session.commit()

        return make_response(jsonify({
            "message": "Action successful."
        }), 200)


class AdminDashboard(Resource):
    @auth_token_required
    @roles_required("ADMIN")
    def get(self):

        total_students = db.session.scalar(sa.select(sa.func.count()).select_from(Student))

        total_drives = db.session.scalar(sa.select(sa.func.count()).select_from(PlacementDrive))

        total_approved_companies = db.session.scalar(sa.select(sa.func.count()).select_from(Company).where(Company.approval_status ==CompanyApprovalStatus.APPROVED))

        total_pending_companies = db.session.scalar(sa.select(sa.func.count()).select_from(Company).where(Company.approval_status == CompanyApprovalStatus.PENDING))

        return make_response(jsonify({
            "total_students": total_students,
            "total_placement_drives": total_drives,
            "approved_companies": total_approved_companies,
            "pending_companies": total_pending_companies
        }), 200)
    
class AdminCompanyRegistrations(Resource):
    @auth_token_required
    @roles_required("ADMIN")
    def get(self):
        registrations=db.session.scalars(sa.select(Company).where(Company.approval_status==CompanyApprovalStatus.PENDING)).all()
        result = []
        for reg in registrations:
            data =  {
                "company_name":reg.company_name,
                "username":reg.user.username,
                "email":reg.user.email,
                "website":reg.website,
                'company_id':reg.id
            }
            result.append(data)
        return make_response(jsonify(result),200)
    
class CompanyApprovalStatusChange(Resource):
    ## {"new_status":"approve" or "reject"}

    @auth_token_required
    @roles_required("ADMIN")
    def put(self, company_id):

        data = request.get_json()
        company = db.session.get(Company, company_id)
        if not company:
            return make_response(jsonify({"message": "Company not found"}), 404)

        new_status = data.get("new_status")

        if new_status == "approve":
            if company.approval_status not in [CompanyApprovalStatus.PENDING,CompanyApprovalStatus.REJECTED]:
                return make_response(jsonify({"message": "Approval not allowed."}), 403)
            company.approval_status = CompanyApprovalStatus.APPROVED

            db.session.commit()
            cache.delete(f"company_{company.id}")

            return make_response(jsonify({"message": "Company Approved.","approval_status": "APPROVED"}), 200)


        elif new_status == "reject":

            if company.approval_status != CompanyApprovalStatus.PENDING:
                return make_response(jsonify({"message": "Rejection not allowed."}), 403)

            company.approval_status = CompanyApprovalStatus.REJECTED

            db.session.commit()
            cache.delete(f"company_{company.id}")

            return make_response(jsonify({"message": "Company Registration Rejected.","approval_status": "REJECTED"}), 200)

        else:
            return make_response(jsonify({"message": "Invalid Status"}), 400)
        
class Companies(Resource):
    @auth_token_required
    @roles_required("ADMIN")
    def get(self):
        company_name = request.args.get('company_name',None)
        username = request.args.get('username',None)
        company_id = request.args.get('company_id',None)
        if company_id is not None:
            company_id= int(company_id)
        query= sa.select(Company).join(User)
        if company_name:
            query=query.where(Company.company_name.ilike(f"%{company_name}%"))
        if username:
            query=query.where(User.username==username)
        if company_id:
            query=query.where(Company.id==company_id)
        companies= db.session.scalars(query).all()
        if not companies:
            return make_response(jsonify({"message":"Not found."}),404)
        result=[]
        for company in companies:
            data={
                "company_name":company.company_name,
                "username":company.user.username,
                "company_id":company.id
            }
            result.append(data)
        return make_response(jsonify(result),200)
    
class ToggleBlacklist(Resource):
    @auth_token_required
    @roles_required("ADMIN")
    def put(self, role_based_id):

        data = request.get_json()
        role = data.get("role")

        if role not in ["COMPANY", "STUDENT"]:
            return {"message": "Invalid role."}, 400

        user = None

        if role == "COMPANY":
            company = db.session.get(Company, role_based_id)
            if not company:
                return {"message": "Company not found."}, 404
            user = company.user
            user.active= not user.active
            cache.delete(f"company_{company.id}")
            db.session.commit()

        elif role == "STUDENT":
            student = db.session.get(Student, role_based_id)
            if not student:
                return {"message": "Student not found."}, 404
            user = student.user
            user.active= not user.active
            cache.delete(f"student_{student.id}")
            db.session.commit()
        
        return make_response(jsonify({
            "message":"Action success.",
            "is_blacklisted": not user.active
        }), 200)

class Students(Resource):
    @auth_token_required
    @roles_required("ADMIN")
    def get(self):
        name = request.args.get('name',None)
        username = request.args.get('username',None)
        student_id = request.args.get('student_id',None)
        if student_id is not None:
            student_id= int(student_id)
        query= sa.select(Student).join(User)
        if name:
            query=query.where(Student.name.ilike(f"%{name}%"))
        if username:
            query=query.where(User.username==username)
        if student_id:
            query=query.where(Student.id==student_id)
        students= db.session.scalars(query).all()
        if not students:
            return make_response(jsonify({"message":"Not found."}),404)
        result=[]
        for student in students:
            data={
                "name": student.name,
                "username":student.user.username,
                "student_id":student.id
            }
            result.append(data)
        return make_response(jsonify(result),200)
       
class PlacementDrivesList(Resource):
    @auth_token_required
    @roles_required("ADMIN")
    def get(self):
        company_name=request.args.get("company_name",None)
        company_username=request.args.get("company_username",None)
        drive_id= request.args.get("drive_id",None)
        status = request.args.get("status", None)
        if drive_id is not None:
            drive_id= int(drive_id)
        query=sa.select(PlacementDrive).join(Company).join(User)
        if status:
            query = query.where(PlacementDrive.status == DriveStatus[status.upper()])
        if company_name:
            query=query.where(Company.company_name.ilike(f"%{company_name}%"))
        if company_username:
            query=query.where(User.username==company_username)
        if drive_id:
            query=query.where(PlacementDrive.id==drive_id)
        drives=db.session.scalars(query).all()
        if not drives:
            return make_response(jsonify([]),200)
        results=[]
        for drive in drives:
            data={
                "title":drive.title,
                "drive_id":drive.id,
                "company_name":drive.company.company_name,
                "company_username":drive.company.user.username,
                "status": drive.status.value
            }
            results.append(data)
        return make_response(jsonify(results),200)
    
class ApplicationList(Resource):
    @auth_token_required
    @roles_required("ADMIN")
    def get(self,drive_id):
        drive = db.session.scalar(sa.select(PlacementDrive).where(PlacementDrive.id == drive_id))

        if not drive:
            return make_response(jsonify({"message": "Drive not found or unauthorized."}), 404)

        applications = db.session.scalars(sa.select(Application).where(Application.drive_id == drive_id)).all()

        result = []

        for app in applications:
            result.append({
                "application_id": app.id,
                "student_name": app.student.name,
                "roll_number": app.student.roll_number,
                'student_id':app.student_id,
                "status": app.status.value
            })

        return make_response(jsonify(result),200)
    
