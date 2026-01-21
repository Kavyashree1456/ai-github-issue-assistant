import json

REQUIRED_FIELDS = [
    "summary",
    "type",
    "priority_score",
    "suggested_labels",
    "potential_impact"
]

import re

def clean_json_text(text):
    text = re.sub(r"```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```", "", text)
    return text.strip()

def validate_ai_json(ai_text):
    try:
        cleaned = clean_json_text(ai_text)
        data = json.loads(cleaned)

        for field in REQUIRED_FIELDS:
            if field not in data:
                raise ValueError(f"Missing field: {field}")

        return data, None

    except Exception as e:
        return None, str(e)
