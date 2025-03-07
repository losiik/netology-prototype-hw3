from typing import List

from fastapi_sqlalchemy import db

from services.db_operations import DBOperations

from models import Course

from schemas import Course as CourseSchema


class CourseService(DBOperations):
    @staticmethod
    async def __courses_model_to_schema(courses) -> List[CourseSchema]:
        return [CourseSchema(id=course.id, course_name=course.course_name) for course in courses]

    @staticmethod
    async def __course_model_to_schema(course) -> CourseSchema:
        return CourseSchema(id=course.id, course_name=course.course_name)

    async def get_courses(self) -> List[CourseSchema]:
        courses = db.session.query(Course).all()
        return await self.__courses_model_to_schema(courses=courses)

    async def get_course(self, course_id: int) -> CourseSchema:
        course = db.session.query(Course).filter(Course.id == course_id).first()
        return await self.__course_model_to_schema(course=course)

    async def delete_course(self, course_id: int) -> CourseSchema:
        course = db.session.query(Course).filter(Course.id == course_id).first()
        await self.db_delete(entity=course)
        return await self.__course_model_to_schema(course=course)

    async def add_course(self, course: CourseSchema) -> CourseSchema:
        course = Course(
            course_name=course.course_name
        )
        await self.db_write(course)
        return await self.__course_model_to_schema(course=course)

    async def update_course(self, course: CourseSchema) -> CourseSchema:
        course_model = db.session.query(Course).filter(Course.id == course.id).first()
        course_model.course_name = course.course_name

        await self.db_update()
        await self.refresh(course_model)

        return await self.__course_model_to_schema(course=course_model)
