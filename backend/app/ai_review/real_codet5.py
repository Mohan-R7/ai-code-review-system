# backend/app/ai_review/real_codet5.py
# ←←← Rename the file to real_codet5.py or just overwrite mock_generator.py

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from typing import List
from app.schemas.review import Issue, Severity

# Load the model once at startup (fast on CPU)
print("Loading CodeT5+ 220m model... (first time only)")
tokenizer = AutoTokenizer.from_pretrained("Salesforce/codet5p-220m")
model = AutoModelForSeq2SeqLM.from_pretrained("Salesforce/codet5p-220m")
print("CodeT5 loaded!")

def generate_ai_suggestion(code_snippet: str, problem_description: str) -> str:
    prompt = f"""Review this Python code and give a helpful suggestion:

Code:
{code_snippet}

Problem: {problem_description}

Suggestion:"""

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=128,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

    suggestion = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Extract only the suggestion part
    if "Suggestion:" in suggestion:
        suggestion = suggestion.split("Suggestion:", 1)[1].strip()
    return suggestion.strip() or "Consider refactoring this code for better readability and safety."


def add_ai_suggestions(issues: List[Issue], full_code: str) -> List[Issue]:
    enhanced = issues.copy()

    # Only add AI suggestions for medium+ severity issues to avoid spam
    for issue in issues:
        if issue.severity in (Severity.HIGH, Severity.CRITICAL, Severity.MEDIUM):
            # Extract context around the line
            lines = full_code.splitlines()
            start = max(0, (issue.line_start or 1) - 6)
            end = min(len(lines), (issue.line_end or issue.line_start or issue.line_start or 1) + 10)
            context = "\n".join(lines[start:end])

            suggestion = generate_ai_suggestion(context, issue.description)

            ai_issue = Issue(
                id=f"ai-{issue.id}",
                severity=Severity.INFO,
                title="AI-Powered Suggestion",
                description=suggestion,
                file_path=issue.file_path,
                line_start=issue.line_start,
                line_end=issue.line_end,
                suggestion=None,
                source="codet5"
            )
            enhanced.append(ai_issue)

    return enhanced