from fastapi import FastAPI
from models import StudentRequest, StudentResponse, StudentSummary, Course
from typing import List
from decimal import Decimal, ROUND_HALF_UP

app = FastAPI(title="학생 성적 처리 API")

# 성적 점수 매핑표: 성적 문자랑 숫자 점수를 연결해 둔 거야
grade_mapping = {
    "A+": 4.5, "A": 4.0,
    "B+": 3.5, "B": 3.0,
    "C+": 2.5, "C": 2.0,
    "D+": 1.5, "D": 1.0,
    "F": 0.0
}

# GPA 계산 함수: 과목들 받아서 평점 계산해
def calculate_gpa(courses: List[Course]) -> (float, int):
    total_points = Decimal("0.0")
    total_credits = 0
    for course in courses:
        points = Decimal(str(grade_mapping[course.grade]))  # 성적 -> 숫자 점수
        total_points += points * course.credits
        total_credits += course.credits

    if total_credits == 0:
        return 0.0, 0

    gpa = (total_points / total_credits).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)  # 소수 둘째 자리까지
    return float(gpa), total_credits

# 기본 페이지: 서버가 살아있나 확인용
@app.get("/")
async def root():
    return {"message": "학생 성적 처리 API가 실행 중입니다!"}

# /score 에 POST 요청 오면 처리해주는 함수
@app.post("/score", response_model=StudentResponse)
async def calculate_student_score(student_data: StudentRequest):
    gpa, total_credits = calculate_gpa(student_data.courses)
    summary = StudentSummary(
        student_id=student_data.student_id,
        name=student_data.name,
        gpa=gpa,
        total_credits=total_credits
    )
    return StudentResponse(student_summary=summary)
