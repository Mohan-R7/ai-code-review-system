# backend/app/static_analyzers/pylint_analyzer.py
import subprocess
import json
from typing import List
from app.schemas.review import Issue, Severity


def run_pylint(file_path: str) -> List[Issue]:
    """Run pylint and return list of Issue objects"""
    try:
        result = subprocess.run(
            ["pylint", "--output-format=json", file_path],
            capture_output=True,
            text=True,
            check=False
        )
        pylint_issues = json.loads(result.stdout) if result.stdout else []
    except Exception as e:
        print(f"Pylint error: {e}")
        return []

    issues = []
    severity_map = {
        "error": Severity.HIGH,
        "warning": Severity.MEDIUM,
        "convention": Severity.LOW,
        "refactor": Severity.LOW,
        "fatal": Severity.CRITICAL,
        "info": Severity.INFO
    }

    for item in pylint_issues:
        issues.append(Issue(
            id=f"pylint-{item['message-id']}-{item['line']}",
            severity=severity_map.get(item['type'], Severity.MEDIUM),
            title=item['symbol'],
            description=item['message'],
            file_path=item['path'],
            line_start=item['line'],
            line_end=item['line'],
            suggestion=None,  # Pylint doesn't give direct fixes
            source="pylint"
        ))
    return issues