from typing import List, Optional
from app import db
from app.models.job import Job


class JobRepository:

    @staticmethod
    def get_all() -> List[Job]:
        return Job.query.order_by(Job.created_at.desc()).all()

    @staticmethod
    def get_by_id(job_id: int) -> Optional[Job]:
        return Job.query.get(job_id)

    @staticmethod
    def create(job: Job) -> Job:
        db.session.add(job)
        db.session.commit()
        return job
