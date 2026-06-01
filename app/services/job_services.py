from typing import List, Optional
from app.dtos.job_dtos import JobResponseDto, CreateJobDto
from app.models.application import Application
from app.models.job import Job
from app.repositories.job_repository import JobRepository
from app.repositories.application_repository import ApplicationRepository


class JobServices:

    @staticmethod
    def list_jobs(user_id: Optional[int] = None) -> List[JobResponseDto]:
        jobs = JobRepository.get_all()
        result = []
        for job in jobs:
            has_applied = False
            if user_id:
                app_record = ApplicationRepository.get_by_user_and_job(user_id, job.id)
                has_applied = app_record is not None

            result.append(JobResponseDto(
                id=job.id,
                title=job.title,
                company=job.company,
                category=job.category,
                type=job.type,
                description=job.description,
                requirements=job.requirements,
                salary=float(job.salary),
                location=job.location,
                experience_level=job.experience_level,
                has_applied=has_applied
            ))
        return result

    @staticmethod
    def create_job(dto: CreateJobDto) -> JobResponseDto:
        """
        Create a new job listing (admin only).

        Validates that:
        - All required fields are provided and not empty
        - Salary is non-negative

        Args:
            dto (CreateJobDto): Job creation data

        Returns:
            JobResponseDto: Newly created job listing

        Raises:
            ValueError: If validation fails
        """
        if dto.salary < 0:
            raise ValueError("Salary cannot be negative")

        new_job = Job(
            title=dto.title,
            company=dto.company,
            category=dto.category,
            type=dto.type,
            description=dto.description,
            requirements=dto.requirements,
            salary=dto.salary,
            location=dto.location,
            experience_level=dto.experience_level
        )

        created_job = JobRepository.create(new_job)

        return JobResponseDto(
            id=created_job.id,
            title=created_job.title,
            company=created_job.company,
            category=created_job.category,
            type=created_job.type,
            description=created_job.description,
            requirements=created_job.requirements,
            salary=float(created_job.salary),
            location=created_job.location,
            experience_level=created_job.experience_level,
            has_applied=False
        )


    @staticmethod
    def get_job_details(job_id: int, user_id: Optional[int] = None) -> JobResponseDto:
        job = JobRepository.get_by_id(job_id)
        if not job:
            raise ValueError("Job not found")

        has_applied = False
        if user_id:
            app_record = ApplicationRepository.get_by_user_and_job(user_id, job_id)
            has_applied = app_record is not None

        return JobResponseDto(
            id=job.id,
            title=job.title,
            company=job.company,
            category=job.category,
            type=job.type,
            description=job.description,
            requirements=job.requirements,
            salary=float(job.salary),
            location=job.location,
            experience_level=job.experience_level,
            has_applied=has_applied
        )

    @staticmethod
    def apply_to_job(job_id: int, user_id: int) -> dict:
        job = JobRepository.get_by_id(job_id)
        if not job:
            raise ValueError("Job not found")

        existing_app = ApplicationRepository.get_by_user_and_job(user_id, job_id)
        if existing_app:
            raise ValueError("Already applied to this job")

        new_app = Application(
            user_id=user_id,
            job_id=job_id,
            status="Applied"
        )
        created_app = ApplicationRepository.create(new_app)
        return {
            "id": created_app.id,
            "user_id": created_app.user_id,
            "job_id": created_app.job_id,
            "status": created_app.status,
            "applied_at": created_app.applied_at.isoformat()
        }
