import os
from app import db
from app.dtos.profile_dtos import ProfileResponseDto, ProfileCourseDto, ProfileJobDto, ProfileUpdateDto
from app.repositories.user_repository import UserRepository


class ProfileServices:

    @staticmethod
    def get_profile(user_id: int) -> ProfileResponseDto:
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        courses_dto = []
        for enrollment in user.enrollments:
            course = enrollment.course
            courses_dto.append(ProfileCourseDto(
                course_id=course.id,
                title=course.title,
                category=course.category,
                level=course.level,
                instructor=course.instructor,
                progress=enrollment.progress,
                is_completed=enrollment.is_completed
            ))

        jobs_dto = []
        for application in user.applications:
            job = application.job
            jobs_dto.append(ProfileJobDto(
                job_id=job.id,
                title=job.title,
                company=job.company,
                location=job.location,
                status=application.status,
                applied_at=application.applied_at.isoformat()
            ))

        return ProfileResponseDto(
            id=user.id,
            name=user.name,
            username=user.username,
            email=user.email,
            phone=user.phone,
            summary=user.summary,
            cv_path=user.cv_path,
            enrolled_courses=courses_dto,
            applied_jobs=jobs_dto
        )

    @staticmethod
    def update_profile(user_id: int, dto: ProfileUpdateDto) -> ProfileResponseDto:
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        if dto.email and dto.email != user.email:
            if UserRepository.user_exists_by_email(dto.email):
                raise ValueError("Email already exists")
            user.email = dto.email

        if dto.phone and dto.phone != user.phone:
            if UserRepository.user_exists_by_phone(dto.phone):
                raise ValueError("Phone number already exists")
            user.phone = dto.phone

        if dto.name is not None:
            user.name = dto.name
        if dto.summary is not None:
            user.summary = dto.summary

        db.session.commit()
        return ProfileServices.get_profile(user_id)

    @staticmethod
    def update_cv(user_id: int, new_cv_path: str) -> ProfileResponseDto:
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        old_path = user.cv_path
        if old_path and os.path.exists(old_path):
            try:
                os.remove(old_path)
            except Exception:
                pass

        user.cv_path = new_cv_path
        db.session.commit()
        return ProfileServices.get_profile(user_id)
