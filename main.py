
import csv
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Student Data API")

# Allow GET requests from any origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
    allow_credentials=False,
)

CSV_FILE = Path(__file__).parent / "q-fastapi.csv"


def load_students():
    students = []

    with CSV_FILE.open(
        mode="r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            students.append({
                "studentId": int(row["studentId"]),
                "class": row["class"],
            })

    return students


@app.get("/api")
async def get_students(
    class_: Optional[list[str]] = Query(default=None, alias="class")
):
    students = load_students()

    # Filter without changing the original CSV row order.
    if class_:
        requested_classes = set(class_)
        students = [
            student
            for student in students
            if student["class"] in requested_classes
        ]

    return {"students": students}


@app.get("/")
async def root():
    return {"message": "Student Data API is running"}
