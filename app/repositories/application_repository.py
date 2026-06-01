from typing import List, Optional
from app import db
from app.models.application import Application


class ApplicationRepository:

    @staticmethod
    def get_by_user_and_job(user_id: int, job_id: int) -> Optional[Application]:
        return Application.query.filter_by(user_id=user_id, job_id=job_id).first()

    @staticmethod
    def create(application: Application) -> Application:
        db.session.add(application)
        db.session.commit()
        return application

    @staticmethod
    def get_by_user(user_id: int) -> List[Application]:
        return Application.query.filter_by(user_id=user_id).order_by(Application.applied_at.desc()).all()
