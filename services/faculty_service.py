from fastapi_sqlalchemy import db

from services.db_operations import DBOperations

from models import Faculty

from schemas import Faculty as FacultySchema


class FacultyService(DBOperations):
    @staticmethod
    async def __faculty_model_to_schema(faculty) -> FacultySchema:
        return FacultySchema(id=faculty.id, faculty_name=faculty.faculty_name)

    async def delete_faculty(self, faculty_id: int) -> FacultySchema:
        faculty = db.session.query(Faculty).filter(Faculty.id == faculty_id).first()
        await self.db_delete(entity=faculty)
        return await self.__faculty_model_to_schema(faculty=faculty)

    async def add_faculty(self, faculty: FacultySchema) -> FacultySchema:
        faculty = Faculty(
            faculty_name=faculty.faculty_name
        )
        await self.db_write(faculty)
        return await self.__faculty_model_to_schema(faculty=faculty)

    async def update_faculty(self, faculty: FacultySchema) -> FacultySchema:
        faculty_model = db.session.query(Faculty).filter(Faculty.id == faculty.id).first()
        faculty_model.faculty_name = faculty.faculty_name

        await self.db_update()
        await self.refresh(faculty_model)

        return await self.__faculty_model_to_schema(faculty=faculty_model)

    async def get_faculty(self, faculty_id: int) -> FacultySchema:
        faculty = db.session.query(Faculty).filter(Faculty.id == faculty_id).first()
        return await self.__faculty_model_to_schema(faculty=faculty)
