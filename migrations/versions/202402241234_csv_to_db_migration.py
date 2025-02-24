import csv
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = '202402241234'
down_revision = '7cffd7471f42'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    # Чтение данных из CSV
    with open("students.csv", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Пропускаем заголовок

        students = {}
        faculties = {}
        courses = {}

        for last_name, first_name, faculty_name, course_name, mark in reader:
            mark = int(mark)

            # Добавление факультета, если его нет
            if faculty_name not in faculties:
                session.execute(text("INSERT INTO faculty (faculty_name) VALUES (:name)"), {"name": faculty_name})
                faculty_id = session.execute(text("SELECT last_insert_rowid()")).scalar()
                faculties[faculty_name] = faculty_id
            else:
                faculty_id = faculties[faculty_name]

            # Добавление курса, если его нет
            if course_name not in courses:
                result = session.execute(text("INSERT INTO course (course_name) VALUES (:name) RETURNING id"),
                                         {"name": course_name})
                course_id = result.scalar()
                courses[course_name] = course_id
            else:
                course_id = courses[course_name]

            # Добавление студента, если его нет
            student_key = (first_name, last_name)
            if student_key not in students:
                result = session.execute(
                    text("INSERT INTO student (first_name, last_name) VALUES (:first_name, :last_name) RETURNING id"),
                    {"first_name": first_name, "last_name": last_name})
                student_id = result.scalar()
                students[student_key] = student_id
            else:
                student_id = students[student_key]

            # Добавление оценки
            session.execute(text(
                "INSERT INTO academic_performance (student_id, faculty_id, course_id, mark) VALUES (:student_id, :faculty_id, :course_id, :mark)"),
                            {"student_id": student_id, "faculty_id": faculty_id, "course_id": course_id, "mark": mark})

    session.commit()


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)
    session.execute(text("DELETE FROM academic_performance"))
    session.execute(text("DELETE FROM student"))
    session.execute(text("DELETE FROM faculty"))
    session.execute(text("DELETE FROM course"))
    session.commit()
