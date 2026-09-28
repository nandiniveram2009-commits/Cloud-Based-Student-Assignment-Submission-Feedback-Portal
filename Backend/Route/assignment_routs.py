from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from services.cloud_db import get_db
from models.database_models import Assignment, Course, User
from services.auth_service import get_current_user, require_role

router = APIRouter()

class AssignmentCreate(BaseModel):
    course_id: int
    title: str
    description: str
    deadline: datetime
    max_marks: int

class AssignmentResponse(BaseModel):
    assignment_id: int
    course_id: int
    title: str
    description: str
    deadline: datetime
    max_marks: int
    created_by: int

    class Config:
        orm_mode = True

@router.post("/assignments", status_code=status.HTTP_201_CREATED)
def create_assignment(
    assignment: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("teacher"))
):
    # Verify course exists
    course = db.query(Course).filter(Course.course_id == assignment.course_id).first()
    if not course:
        # Create default course if none exists for simplicity
        course = Course(course_id=assignment.course_id, course_name="Default Cloud Course", teacher_id=current_user.user_id)
        db.add(course)
        db.commit()

    new_assignment = Assignment(
        course_id=assignment.course_id,
        title=assignment.title,
        description=assignment.description,
        deadline=assignment.deadline,
        max_marks=assignment.max_marks,
        created_by=current_user.user_id
    )
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return {"message": "Assignment created successfully", "assignment_id": new_assignment.assignment_id}

@router.get("/assignments")
def get_assignments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    assignments = db.query(Assignment).all()
    return assignments

@router.get("/assignments/{id}")
def get_assignment_by_id(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    assignment = db.query(Assignment).filter(Assignment.assignment_id == id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found.")
    return assignment

@router.delete("/assignments/{id}")
def delete_assignment(id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role("teacher"))):
    assignment = db.query(Assignment).filter(Assignment.assignment_id == id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found.")
    db.delete(assignment)
    db.commit()
    return {"message": "Assignment deleted successfully."}
