from celery import Celery
from flask import render_template
import sqlalchemy as sa
from datetime import datetime, timedelta
from mail import send_html_email,send_mail,send_file_mail
import pandas as pd
import os

celery = Celery('tasks',broker='redis://localhost:6379/0')

celery.conf.update(
    timezone='Asia/Kolkata',
    enable_utc=False
)

EXPORT_FOLDER = "exports"
os.makedirs(EXPORT_FOLDER, exist_ok=True)

from app import app
from controllers.database import db
from controllers.model import *

@celery.task()
def monthly_admin_report():
    with app.app_context():
        subject="Monthly Placement Report"
        one_month_ago = datetime.utcnow() - timedelta(days=30)
        total_drives=db.session.scalar(sa.select(sa.func.count()).select_from(PlacementDrive).where( PlacementDrive.created_at >= one_month_ago))
        total_applications=db.session.scalar(sa.select(sa.func.count()).select_from(Application).where(Application.applied_on >= one_month_ago))
        total_selections=db.session.scalar(sa.select(sa.func.count()).select_from(Application).where(Application.applied_on >= one_month_ago,Application.status==ApplicationStatus.SELECTED))

        html = render_template("monthly_admin_report.html",total_drives=total_drives,total_applications=total_applications,total_selections=total_selections)

        send_html_email(to_email="admin@gmail.com",subject="Monthly Placement Report",html_content=html)
        print("Monthly report emailed to admin.")

@celery.task()
def daily_reminders():
    with app.app_context():
        today=datetime.utcnow().date()
        two_days_later=today+timedelta(days=2)

        subject = "Application Deadline Reminder"
        body="There are upcoming application deadlines. Check the Placement Portal for drives you can apply to."
        drives=db.session.scalars(sa.select(PlacementDrive).where(PlacementDrive.application_deadline>=today,PlacementDrive.application_deadline<=two_days_later)).all()
        if not drives:
            print ("No upcoming drive application deadline.")
            return

        students=db.session.scalars(sa.select(User).join(Student).where(User.active==True)).all()
        for student in students:
            send_mail(student.email,subject=subject,body=body)
        print('Daily Reminders sent.')

@celery.task()
def export_applications_csv(id):
    with app.app_context():
        user=db.session.get(User,id)
        student=user.student
        applications=db.session.scalars(sa.select(Application).where(Application.student_id==student.id)).all()
        result=[]
        for application in applications:
            row=[application.student.id,application.drive.company.company_name,application.drive.title,application.status.value,application.applied_on.isoformat()]
            result.append(row)
        
        df = pd.DataFrame(result,columns=["Student ID","Company Name","Drive Title","Application Status","Date"])

        filename = f"placement_history_{student.id}.csv"
        filepath = os.path.join(EXPORT_FOLDER, filename)

        df.to_csv(filepath, index=False)

        send_file_mail(
            user.email,
            subject="Your Placement Application History",
            body="Your placement application history CSV is attached.",
            attachment=filepath
        )

        print("CSV created and email sent.")

from celery.schedules import crontab

celery.conf.beat_schedule={
    'send-monthly-admin-report':{
        'task':'celery_app.monthly_admin_report',
        #'schedule':crontab(day_of_month=1,hour=0,minute=0)
        'schedule':timedelta(seconds=30)
    },
    'send-daily-reminders':{
        'task': 'celery_app.daily_reminders',
        #'schedule':crontab(hour=10,minute=0)
        'schedule':timedelta(seconds=60)
    },
}