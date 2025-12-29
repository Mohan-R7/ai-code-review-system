# backend/app/static_analyzers/bandit_analyzer.py
import subprocess
import json
from typing import List
from app.schemas.review import Issue, Severity


def run_bandit(file_path: str) -> List[Issue]:
    """Run bandit and return list of Issue objects"""
    try:
        result = subprocess.run(
            ["bandit", "-f", "json", "-r", file_path],
            capture_output=True,
            text=True,
            check=False
        )
        data = json.loads(result.stdout) if result.stdout else {"results": []}
        bandit_issues = data.get("results", [])
    except Exception as e:
        print(f"Bandit error: {e}")
        return []

    issues = []
    severity_map = {
        "HIGH": Severity.HIGH,
        "MEDIUM": Severity.MEDIUM,
        "LOW": Severity.LOW
    }

    for item in bandit_issues:
        issues.append(Issue(
            id=f"bandit-{item['issue_confidence']}-{item['line_number']}",
            severity=severity_map.get(item['issue_severity'], Severity.MEDIUM),
            title=item['test_name'],
            description=item['issue_text'],
            file_path=item['filename'],
            line_start=item['line_number'],
            line_end=item['line_number'],
            suggestion=item.get('more_info', None),
            source="bandit"
        ))
    return issues 