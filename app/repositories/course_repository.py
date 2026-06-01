from typing import List, Optional
from app import db
from app.models.course import Course


class CourseRepository:

    @staticmethod
    def get_all() -> List[Course]:
        return Course.query.all()

    @staticmethod
    def get_by_id(course_id: int) -> Optional[Course]:
        return Course.query.get(course_id)

    @staticmethod
    def create(course: Course) -> Course:
        db.session.add(course)
        db.session.commit()
        return course
