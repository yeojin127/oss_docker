from pydantic import BaseModel, Field
from typing import List, Literal

class Course(BaseModel):
    course_code: str = Field(..., description="과목 코드")
    course_name: str = Field(..., description="과목명")
    credits: int = Field(..., gt=0, description="학점 (양수)")
    grade: Literal["A+", "A", "B+", "B", "C+", "C", "D+", "D", "F"] = Field(..., description="성적")

class StudentRequest(BaseModel):
    student_id: str = Field(..., description="학번")
    name: str = Field(..., description="학생 이름")
    courses: List[Course] = Field(..., min_items=1, description="수강한 과목 리스트")

    class Config:
        extra = "forbid"  # 예상치 못한 필드가 들어오면 에러 발생

class StudentSummary(BaseModel):
    student_id: str
    name: str
    gpa: float
    total_credits: int

class StudentResponse(BaseModel):
    student_summary: StudentSummary
