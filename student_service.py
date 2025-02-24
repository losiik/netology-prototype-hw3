from fastapi_sqlalchemy import db
from sqlalchemy import select, func

from db_operations import DBOperations

from models import Student, AcademicPerformance, Faculty, Course
from schemas import Student as StudentSchema
from schemas import Course as CourseSchema


class StudentService(DBOperations):
    @staticmethod
    async def __student_model_to_schema(students):
        return [StudentSchema(id=row.id, first_name=row.first_name, last_name=row.last_name) for row in students]

    @staticmethod
    async def __course_model_to_schema(courses):
        return [CourseSchema(id=course.id, course_name=course.course_name) for course in courses]

    async def get_students_list(self, faculty_name: str = None, course_name: str = None):
        if course_name is not None:
            stmt = (
                select(Student.id, Student.first_name, Student.last_name)
                .join(AcademicPerformance, Student.id == AcademicPerformance.student_id)
                .join(Course, AcademicPerformance.course_id == Course.id)
                .where(
                    Course.course_name == course_name,
                    AcademicPerformance.mark >= 30
                )
                .distinct()
            )
        elif faculty_name is not None:
            stmt = (
                select(Student.id, Student.first_name, Student.last_name)
                .join(AcademicPerformance, Student.id == AcademicPerformance.student_id)
                .join(Faculty, AcademicPerformance.faculty_id == Faculty.id)
                .where(Faculty.faculty_name == faculty_name)
                .distinct()
            )
        else:
            return None

        students = db.session.execute(stmt)
        return await self.__student_model_to_schema(students=students)

    async def get_courses(self):
        courses = db.session.query(Course).all()
        return await self.__course_model_to_schema(courses=courses)

    @staticmethod
    async def get_average_mark_by_faculty(faculty_name: str):
        average_mark = db.session.query(
            func.avg(AcademicPerformance.mark).label('average_mark')
        ).join(Faculty, AcademicPerformance.faculty_id == Faculty.id) \
            .filter(Faculty.faculty_name == faculty_name) \
            .scalar()

        return average_mark
