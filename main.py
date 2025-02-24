import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware

from endpoints import student_router

app = FastAPI(openapi_prefix="/api/v1")
app.add_middleware(
    DBSessionMiddleware,
    db_url="sqlite:///./student.db",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(student_router)


if __name__ == "__main__":
    uvicorn.run(app, port=9000)
