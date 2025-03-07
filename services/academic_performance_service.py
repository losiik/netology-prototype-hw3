from fastapi_sqlalchemy import db

from services.db_operations import DBOperations

from models import AcademicPerformance

from schemas import AcademicPerformance as AcademicPerformanceSchema


class AcademicPerformanceService(DBOperations):
    @staticmethod
    async def __academic_performance_model_to_schema(academic_performance) -> AcademicPerformanceSchema:
        return AcademicPerformanceSchema(
            id=academic_performance.id,
            student_id=academic_performance.student_id,
            faculty_id=academic_performance.faculty_id,
            course_id=academic_performance.course_id,
            mark=academic_performance.mark
        )

    async def get_academic_performance(self, academic_performance_id: int):
        academic_performance = db.session.query(AcademicPerformance).filter(
            AcademicPerformance.id == academic_performance_id
        ).first()
        return await self.__academic_performance_model_to_schema(academic_performance=academic_performance)

    async def delete_academic_performance(self, academic_performance_id: int):
        academic_performance = db.session.query(AcademicPerformance).filter(
            AcademicPerformance.id == academic_performance_id
        ).first()
        await self.db_delete(entity=academic_performance)
        return await self.__academic_performance_model_to_schema(academic_performance=academic_performance)

    async def add_academic_performance(
            self,
            academic_performance: AcademicPerformanceSchema
    ) -> AcademicPerformanceSchema:
        academic_performance = AcademicPerformance(
            student_id=academic_performance.student_id,
            faculty_id=academic_performance.faculty_id,
            course_id=academic_performance.course_id,
            mark=academic_performance.mark
        )
        await self.db_write(academic_performance)
        return await self.__academic_performance_model_to_schema(academic_performance=academic_performance)

    async def update_academic_performance(
            self,
            academic_performance: AcademicPerformanceSchema
    ) -> AcademicPerformanceSchema:
        academic_performance_model = db.session.query(AcademicPerformance).filter(
            AcademicPerformance.id == academic_performance.id
        ).first()
        if academic_performance.student_id is not None:
            academic_performance_model.student_id = academic_performance.student_id
        if academic_performance.faculty_id is not None:
            academic_performance_model.faculty_id = academic_performance.faculty_id
        if academic_performance.course_id is not None:
            academic_performance_model.course_id = academic_performance.course_id
        if academic_performance.mark is not None:
            academic_performance_model.mark = academic_performance.mark

        await self.db_update()
        await self.refresh(academic_performance_model)

        return await self.__academic_performance_model_to_schema(academic_performance=academic_performance_model)
