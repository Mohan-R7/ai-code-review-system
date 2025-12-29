# backend/app/api/v1/endpoints/review.py
import uuid
import os
from fastapi import APIRouter, File, UploadFile
from typing import List
from datetime import datetime

from app.schemas.review import ReviewResponse, Issue, Severity
from app.static_analyzers.pylint_analyzer import run_pylint
from app.static_analyzers.bandit_analyzer import run_bandit
from app.ai_review.real_codet5 import add_ai_suggestions   

router = APIRouter()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", response_model=ReviewResponse)
async def review_upload(file: UploadFile = File(...)):


    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # ←←← ADD THIS BLOCK
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        full_code_content = f.read()

    # Static analysis
    pylint_issues = run_pylint(file_path)
    bandit_issues = run_bandit(file_path)
    all_issues = pylint_issues + bandit_issues

    # ←←← CHANGE THIS LINE
    final_issues = add_ai_suggestions(all_issues, full_code_content)

   
    summary = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for issue in final_issues:
        summary[issue.severity.value] += 1

    return ReviewResponse(
        review_id=str(uuid.uuid4()),
        total_issues=len(final_issues),
        summary=summary,
        issues=final_issues
    ) 