# backend/app/schemas/review.py
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class Issue(BaseModel):
    id: str
    severity: Severity
    title: str
    description: str
    file_path: Optional[str] = None
    line_start: Optional[int] = None
    line_end: Optional[int] = None
    suggestion: Optional[str] = None
    source: str  # "pylint" | "bandit" | "ai"


class ReviewResponse(BaseModel):
    review_id: str
    total_issues: int
    summary: dict
    issues: List[Issue]