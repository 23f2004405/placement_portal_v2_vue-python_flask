from flask import Flask,request
from flask_security import Security, SQLAlchemyUserDatastore,login_user
from controllers.database import db
from controllers.model import *
from controllers.config import Config
from controllers.user_datastore import user_datastore
from flask_restful import Api,Resource
from flask_cors import CORS
import os
from extensions import cache

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    CORS(app)
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    
    
    cache.init_app(app)

    db.init_app(app)
    security =Security(app,user_datastore)


    api =Api(app)

    with app.app_context():
        db.create_all()

        admin_role = user_datastore.find_or_create_role(name='ADMIN',description="Administrator")
        student_role = user_datastore.find_or_create_role(name='STUDENT',description="Student User")
        company_role = user_datastore.find_or_create_role(name='COMPANY',description="Company User")

        if not user_datastore.find_user(username="admin123"):
            user_datastore.create_user(
                username="admin123",email='admin123@gmail.com',password="12345ab",roles=[admin_role]
            )

        db.session.commit()

    return app , api , cache

app,api,cache = create_app()

from controllers.authentication_apis import LoginApi,LogoutApi,RegisterApi
api.add_resource(LoginApi,'/api/login')
api.add_resource(LogoutApi,'/api/logout')
api.add_resource(RegisterApi,'/api/register')

from controllers.crud_api import CompanyDetailApi,DriveDetailResource,StudentDetailApi,ViewResumeApi
api.add_resource(CompanyDetailApi,'/api/company/<int:company_id>','/api/admin/company/<company_id>')
api.add_resource(DriveDetailResource,'/api/company/drives/<drive_id>','/api/admin/drive/<drive_id>')
api.add_resource(StudentDetailApi,'/api/student/<student_id>','/api/admin/student/<student_id>')
api.add_resource(ViewResumeApi,'/api/resume/<filename>')

from controllers.company_api import MyDrivesApi,CompanyDriveResource,CompanyCloseDriveResource,CompanyDriveApplicationsApi,CompanyApplicationDetailApi,CompanyUpdateApplicationStatusApi
api.add_resource(MyDrivesApi,'/api/company/drives')
api.add_resource(CompanyDriveResource,'/api/company/create_drive')
api.add_resource(CompanyCloseDriveResource,'/api/company/drives/<drive_id>/close')
api.add_resource(CompanyDriveApplicationsApi,'/api/company/drive/<drive_id>/applications')
api.add_resource(CompanyApplicationDetailApi,'/api/company/application/<application_id>')
api.add_resource(CompanyUpdateApplicationStatusApi,'/api/company/application/change_status/<application_id>')

from controllers.student_api import UploadResumeApi,ApprovedDrives,StudentDriveDetails,StudentApplyDrive,UpdateProfile,StudentApplicationHistory,ExportApplicationsAPI
api.add_resource(ApprovedDrives,'/api/student/approved_drives')
api.add_resource(StudentDriveDetails, '/api/student/drive/<drive_id>')
api.add_resource(StudentApplyDrive,'/api/student/drive/<drive_id>/apply')
api.add_resource(UpdateProfile, '/api/student/edit_profile')
api.add_resource(StudentApplicationHistory, '/api/student/applications')
api.add_resource(UploadResumeApi,'/api/student/upload_resume')
api.add_resource(ExportApplicationsAPI,'/api/student/export_history')

from controllers.admin_api import AdminDriveApprovalResource,AdminDashboard,AdminCompanyRegistrations,CompanyApprovalStatusChange,Companies,ToggleBlacklist,Students,PlacementDrivesList,ApplicationList
api.add_resource(AdminDashboard,'/api/admin/dashboard')
api.add_resource(AdminDriveApprovalResource,'/api/admin/drive/<drive_id>/approval')
api.add_resource(AdminCompanyRegistrations,'/api/admin/company/registrations')
api.add_resource(CompanyApprovalStatusChange,'/api/admin/company/approval/<company_id>')
api.add_resource(Companies,'/api/admin/companies')
api.add_resource(ToggleBlacklist,'/api/admin/company/blacklist/<role_based_id>','/api/admin/student/blacklist/<role_based_id>')
api.add_resource(Students,'/api/admin/students')
api.add_resource(PlacementDrivesList,'/api/admin/drives')
api.add_resource(ApplicationList,'/api/admin/drive/<drive_id>/applications')

if __name__ == "__main__":
    app.run(debug=True)

