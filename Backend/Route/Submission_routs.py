import os
import shutil
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from services.cloud_db import get_db
from models.database_models import Assignment, Submission, User
from services.auth_service import get_current_user, require_role
from pydantic import BaseModel

router = APIRouter()
UPLOAD_DIR = os.getenv("STORAGE_DIR", "./uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

class GradeSubmissionRequest(BaseModel):
    marks: int
    feedback: str

@router.post("/assignments/{id}/submit")
def submit_assignment(
    id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("student"))
):
    assignment = db.query(Assignment).filter(Assignment.assignment_id == id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found.")

    # Validate file extension
    allowed_extensions = [".pdf", ".docx", ".zip"]
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file format. Allowed: .pdf, .docx, .zip")

    # Save file to cloud storage simulation directory
    storage_path = os.path.join(UPLOAD_DIR, f"assignment_{id}_student_{current_user.user_id}_{file.filename}")
    with open(storage_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Deadline validation
    current_time = datetime.utcnow()
    sub_status = "SUBMITTED" if current_time <= assignment.deadline else "LATE"

    # Check for existing submission (resubmission handling)
    existing_sub = db.query(Submission).filter(
        Submission.assignment_id == id,
        Submission.student_id == current_user.user_id
    ).first()

    if existing_sub:
        existing_sub.file_name = file.filename
        existing_sub.file_url = storage_path
        existing_sub.storage_path = storage_path
        existing_sub.submitted_at = current_time
        existing_sub.submission_status = sub_status
        db.commit()
        return {"message": "Assignment resubmitted successfully.", "submission_id": existing_sub.submission_id, "status": sub_status}

    new_submission = Submission(
        assignment_id=id,
        student_id=current_user.user_id,
        file_name=file.filename,
        file_url=storage_path,
        storage_path=storage_path,
        submission_status=sub_status
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)

    return {"message": "Assignment submitted successfully.", "submission_id": new_submission.submission_id, "status": sub_status}

@router.get("/submissions/me")
def get_my_submissions(db: Session = Depends(get_db), current_user: User = Depends(require_role("student"))):
    submissions = db.query(Submission).filter(Submission.student_id == current_user.user_id).all()
    return submissions

@router.get("/assignments/{id}/submissions")
def get_assignment_submissions(id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role("teacher"))):
    submissions = db.query(Submission).filter(Submission.assignment_id == id).all()
    return submissions

@router.post("/submissions/{id}/grade")
def grade_submission(
    id: int,
    grade_data: GradeSubmissionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("teacher"))
):
    submission = db.query(Submission).filter(Submission.submission_id == id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found.")

    assignment = db.query(Assignment).filter(Assignment.assignment_id == submission.assignment_id).first()
    if grade_data.marks > assignment.max_marks:
        raise HTTPException(status_code=400, detail=f"Marks cannot exceed maximum allowed ({assignment.max_marks}).")

    submission.marks = grade_data.marks
    submission.feedback = grade_data.feedback
    submission.submission_status = "GRADED"
    submission.graded_at = datetime.utcnow()
    db.commit()

    return {"message": "Submission graded successfully.", "submission_id": submission.submission_id}

@router.get("/submissions/{id}/download")
def download_submission(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    submission = db.query(Submission).filter(Submission.submission_id == id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found.")

    if current_user.role == "student" and submission.student_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Unauthorized to download this file.")

    if not os.path.exists(submission.storage_path):
        raise HTTPException(status_code=404, detail="File asset missing from cloud storage repository.")

    return FileResponse(submission.storage_path, filename=submission.file_name)
