from typing import Optional
from app import db
from app.models.enrollment import Enrollment


class EnrollmentRepository:

    @staticmethod
    def get_by_user_and_course(user_id: int, course_id: int) -> Optional[Enrollment]:
        return Enrollment.query.filter_by(user_id=user_id, course_id=course_id).first()

    @staticmethod
    def create(enrollment: Enrollment) -> Enrollment:
        db.session.add(enrollment)
        db.session.commit()
        return enrollment

    @staticmethod
    def save() -> None:
        db.session.commit()
