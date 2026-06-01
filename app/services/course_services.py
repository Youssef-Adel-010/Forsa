from typing import List, Optional
from app.dtos.course_dtos import CourseResponseDto, CourseContentResponseDto, VideoResponseDto, CreateCourseDto
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.repositories.course_repository import CourseRepository
from app.repositories.enrollment_repository import EnrollmentRepository


def _get_short_description(description: str) -> str:
    if len(description) <= 150:
        return description
    return description[:147] + "..."


def _get_playlist_videos(playlist_id: str, total_videos: int) -> List[dict]:
    videos = []
    topics = [
        "Introduction and Course Overview",
        "Setting Up Your Development Environment",
        "Understanding Core Concepts & Architecture",
        "Practical Session: First Implementation",
        "Deep Dive into Advanced Features",
        "Error Handling, Debugging & Troubleshooting",
        "Best Practices, Patterns & Performance Optimization",
        "Integrating with Third-Party APIs and Services",
        "Unit and Integration Testing Strategies",
        "Deployment, CI/CD, and Hosting in Production"
    ]
    for i in range(total_videos):
        topic = topics[i % len(topics)]
        video_id = f"mock_vid_{playlist_id}_{i}"
        minutes = 8 + (i * 7) % 21
        seconds = (i * 13) % 60
        duration_str = f"{minutes:02d}:{seconds:02d}"
        videos.append({
            "index": i,
            "video_id": video_id,
            "title": f"Lesson {i + 1}: {topic}",
            "duration": duration_str
        })
    return videos


class CourseServices:

    @staticmethod
    def list_courses(user_id: Optional[int] = None) -> List[CourseResponseDto]:
        courses = CourseRepository.get_all()
        result = []
        for course in courses:
            is_enrolled = False
            progress = 0
            is_completed = False

            if user_id:
                enrollment = EnrollmentRepository.get_by_user_and_course(user_id, course.id)
                if enrollment:
                    is_enrolled = True
                    progress = enrollment.progress
                    is_completed = enrollment.is_completed

            result.append(CourseResponseDto(
                id=course.id,
                title=course.title,
                category=course.category,
                level=course.level,
                instructor=course.instructor,
                description=course.description,
                short_description=_get_short_description(course.description),
                total_videos=course.total_videos,
                duration_in_hours=course.duration_in_hours,
                youtube_playlist_id=course.youtube_playlist_id,
                is_enrolled=is_enrolled,
                progress=progress,
                is_completed=is_completed
            ))
        return result

    @staticmethod
    def create_course(dto: CreateCourseDto) -> CourseResponseDto:
        """
        Create a new course (admin only).

        Validates that:
        - YouTube playlist ID is not empty
        - Total videos is at least 1
        - Duration is at least 1 hour

        Args:
            dto (CreateCourseDto): Course creation data

        Returns:
            CourseResponseDto: Newly created course

        Raises:
            ValueError: If validation fails
        """
        if not dto.youtube_playlist_id or len(dto.youtube_playlist_id.strip()) == 0:
            raise ValueError("YouTube playlist ID cannot be empty")

        new_course = Course(
            title=dto.title,
            category=dto.category,
            level=dto.level,
            instructor=dto.instructor,
            description=dto.description,
            total_videos=dto.total_videos,
            duration_in_hours=dto.duration_in_hours,
            youtube_playlist_id=dto.youtube_playlist_id
        )

        created_course = CourseRepository.create(new_course)

        return CourseResponseDto(
            id=created_course.id,
            title=created_course.title,
            category=created_course.category,
            level=created_course.level,
            instructor=created_course.instructor,
            description=created_course.description,
            short_description=_get_short_description(created_course.description),
            total_videos=created_course.total_videos,
            duration_in_hours=created_course.duration_in_hours,
            youtube_playlist_id=created_course.youtube_playlist_id,
            is_enrolled=False,
            progress=0,
            is_completed=False
        )


    @staticmethod
    def get_course_details(course_id: int, user_id: Optional[int] = None) -> CourseResponseDto:
        course = CourseRepository.get_by_id(course_id)
        if not course:
            raise ValueError("Course not found")

        is_enrolled = False
        progress = 0
        is_completed = False

        if user_id:
            enrollment = EnrollmentRepository.get_by_user_and_course(user_id, course.id)
            if enrollment:
                is_enrolled = True
                progress = enrollment.progress
                is_completed = enrollment.is_completed

        return CourseResponseDto(
            id=course.id,
            title=course.title,
            category=course.category,
            level=course.level,
            instructor=course.instructor,
            description=course.description,
            short_description=_get_short_description(course.description),
            total_videos=course.total_videos,
            duration_in_hours=course.duration_in_hours,
            youtube_playlist_id=course.youtube_playlist_id,
            is_enrolled=is_enrolled,
            progress=progress,
            is_completed=is_completed
        )

    @staticmethod
    def enroll_in_course(course_id: int, user_id: int) -> dict:
        course = CourseRepository.get_by_id(course_id)
        if not course:
            raise ValueError("Course not found")

        existing_enrollment = EnrollmentRepository.get_by_user_and_course(user_id, course_id)
        if existing_enrollment:
            raise ValueError("Already enrolled in this course")

        new_enrollment = Enrollment(
            user_id=user_id,
            course_id=course_id,
            watched_videos=0,
            progress=0,
            is_completed=False
        )
        created_enrollment = EnrollmentRepository.create(new_enrollment)
        return {
            "id": created_enrollment.id,
            "user_id": created_enrollment.user_id,
            "course_id": created_enrollment.course_id,
            "progress": created_enrollment.progress,
            "is_completed": created_enrollment.is_completed,
            "enrolled_at": created_enrollment.enrolled_at.isoformat()
        }

    @staticmethod
    def get_course_content(course_id: int, user_id: int) -> CourseContentResponseDto:
        course = CourseRepository.get_by_id(course_id)
        if not course:
            raise ValueError("Course not found")

        enrollment = EnrollmentRepository.get_by_user_and_course(user_id, course_id)
        if not enrollment:
            raise ValueError("User is not enrolled in this course")

        raw_videos = _get_playlist_videos(course.youtube_playlist_id, course.total_videos)
        videos_dto = []
        for v in raw_videos:
            idx = v["index"]
            is_comp = (enrollment.watched_videos & (1 << idx)) != 0
            videos_dto.append(VideoResponseDto(
                index=idx,
                video_id=v["video_id"],
                title=v["title"],
                duration=v["duration"],
                is_completed=is_comp
            ))

        return CourseContentResponseDto(
            course_id=course.id,
            title=course.title,
            youtube_playlist_id=course.youtube_playlist_id,
            progress=enrollment.progress,
            is_completed=enrollment.is_completed,
            videos=videos_dto
        )

    @staticmethod
    def update_video_completion(course_id: int, user_id: int, video_index: int, completed: bool) -> CourseContentResponseDto:
        course = CourseRepository.get_by_id(course_id)
        if not course:
            raise ValueError("Course not found")

        enrollment = EnrollmentRepository.get_by_user_and_course(user_id, course_id)
        if not enrollment:
            raise ValueError("User is not enrolled in this course")

        if video_index < 0 or video_index >= course.total_videos:
            raise ValueError(f"Invalid video index. Course has {course.total_videos} videos (0 to {course.total_videos - 1}).")

        if completed:
            enrollment.watched_videos |= (1 << video_index)
        else:
            enrollment.watched_videos &= ~(1 << video_index)

        completed_count = bin(enrollment.watched_videos).count('1')

        if course.total_videos > 0:
            progress = int((completed_count / course.total_videos) * 100)
        else:
            progress = 0

        enrollment.progress = progress
        enrollment.is_completed = (completed_count == course.total_videos)

        EnrollmentRepository.save()

        return CourseServices.get_course_content(course_id, user_id)
