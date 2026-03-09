from flask_restful import Resource
from flask import request ,jsonify,make_response
from flask_security import utils,auth_token_required,roles_required,current_user
import sqlalchemy as sa
from datetime import datetime

from controllers.database import db
from controllers.model import *

class CompanyDriveResource(Resource):
    @auth_token_required
    @roles_required("COMPANY")
    def post(self):
        fields = request.get_json()

        company = current_user.company

        title = fields.get("title")
        description = fields.get("description")
        min_cgpa = fields.get("min_cgpa")
        deadline = fields.get("application_deadline")
        passing_out_year = fields.get("passing_out_year")

        if deadline:
            application_deadline = datetime.fromisoformat(deadline)
        else:
            application_deadline = None

        if not all([title, description, min_cgpa, application_deadline]):
            return make_response(jsonify({
                "message": "All fields are required."
            }), 400)

        if company.approval_status != CompanyApprovalStatus.APPROVED:
            return make_response(jsonify({
                "message": "Company not approved by admin."
            }), 403)

        drive = PlacementDrive(
            company=company,
            title=title,
            description=description,
            min_cgpa=min_cgpa,
            application_deadline=application_deadline,
            status=DriveStatus.PENDING,
            passing_out_year=passing_out_year
        )

        db.session.add(drive)
        db.session.commit()

        return make_response(jsonify({
            "message": "Drive created and pending admin approval."
        }), 201)


    # @auth_token_required
    # @roles_required("COMPANY")
    # def put(self, drive_id):

    #     drive = db.session.get(PlacementDrive, drive_id)

    #     if not drive:
    #         return make_response(jsonify({"message": "Drive not found."}), 404)

    #     if drive.company_id != current_user.company.id:
    #         return make_response(jsonify({"message": "Unauthorized."}), 403)

    #     if drive.status == DriveStatus.CLOSED:
    #         return make_response(jsonify({
    #             "message": "Cannot edit a closed drive."
    #         }), 400)

    #     fields = request.get_json()

    #     drive.title = fields.get("title", drive.title)
    #     drive.description = fields.get("description", drive.description)
    #     drive.min_cgpa = fields.get("min_cgpa", drive.min_cgpa)
    #     drive.application_deadline = fields.get(
    #         "application_deadline",
    #         drive.application_deadline
    #     )

    #     db.session.commit()

    #     return make_response(jsonify({
    #         "message": "Drive updated successfully."
    #     }), 200)
    
class CompanyCloseDriveResource(Resource):

    @auth_token_required
    @roles_required("COMPANY")
    def put(self, drive_id):

        drive = db.session.get(PlacementDrive, drive_id)

        if not drive:
            return make_response(jsonify({"message": "Drive not found."}), 404)

        if drive.company_id != current_user.company.id:
            return make_response(jsonify({"message": "Unauthorized."}), 403)

        if drive.status != DriveStatus.APPROVED:
            return make_response(jsonify({
                "message": "Only approved drives can be closed."
            }), 400)

        drive.status = DriveStatus.CLOSED
        db.session.commit()

        return make_response(jsonify({
            "message": "Drive closed successfully."
        }), 200)
    
class CompanyDriveApplicationsApi(Resource):
    @auth_token_required
    @roles_required("COMPANY")
    def get(self, drive_id):

        
        drive = db.session.scalar(sa.select(PlacementDrive).where(PlacementDrive.id == drive_id,PlacementDrive.company_id == current_user.company.id))

        if not drive:
            return make_response(jsonify({"message": "Drive not found or unauthorized."}), 404)

        applications = db.session.scalars(sa.select(Application).where(Application.drive_id == drive_id)).all()

        result = []

        for app in applications:
            result.append({
                "application_id": app.id,
                "student_name": app.student.name,
                "roll_number": app.student.roll_number,
                "cgpa": app.student.cgpa,
                "status": app.status.value
            })

        return make_response(jsonify(result),200)
    
class CompanyApplicationDetailApi(Resource):
    @auth_token_required
    @roles_required("COMPANY")
    def get(self, application_id):

        application = db.session.scalar(sa.select(Application).join(PlacementDrive).where(Application.id == application_id,PlacementDrive.company_id == current_user.company.id))

        if not application:
            return make_response(jsonify({"message": "Application not found or unauthorized."}), 404)

        student = application.student

        return make_response(jsonify({
            "application_id": application.id,
            "status": application.status.value,
            "student_details": {
                "name": student.name,
                "roll_number": student.roll_number,
                "department": student.department,
                "cgpa": student.cgpa,
                "resume": student.resume
            }
        }), 200)
    
class CompanyUpdateApplicationStatusApi(Resource):
    @auth_token_required
    @roles_required("COMPANY")
    def put(self, application_id):

        data = request.get_json()
        new_status = data.get("status")

        if new_status not in ["SHORTLISTED", "SELECTED", "REJECTED"]:
            return {"message": "Invalid status."}, 400

        application = db.session.scalar(
            sa.select(Application)
            .join(PlacementDrive)
            .where(
                Application.id == application_id,
                PlacementDrive.company_id == current_user.company.id
            )
        )

        if not application:
            return {"message": "Application not found or unauthorized."}, 404
        
        if application.drive.status == DriveStatus.CLOSED:
            return {"message": "Cannot update application. Drive is closed."}, 400


        # Optional rule: prevent changing after selected
        if application.status == ApplicationStatus.SELECTED:
            return {"message": "Cannot modify a selected candidate."}, 400

        application.status = ApplicationStatus[new_status]

        db.session.commit()

        return {
            "message": f"Application marked as {new_status.lower()}."
        }, 200
    
class MyDrivesApi(Resource):
    @auth_token_required
    @roles_required("COMPANY")
    def get(self):
        company=current_user.company
        status_param = request.args.get("status")
        
        if not status_param:
            return make_response(jsonify({"message": "Status query parameter is required."}), 400)

        try:
            status_enum = DriveStatus(status_param.upper())
        except ValueError:
            return make_response(jsonify({"message": "Invalid status value."}), 400)

        drives = db.session.scalars(sa.select(PlacementDrive).where(PlacementDrive.company_id == company.id,PlacementDrive.status == status_enum)).all()
        response=[]
        for drive in drives:
            result={
                'drive_id':drive.id,
                'title':drive.title,
                'application_deadline':drive.application_deadline.isoformat() if drive.application_deadline else None,
                'status':drive.status.value
            }
            response.append(result)
        return make_response(jsonify(response),200)
