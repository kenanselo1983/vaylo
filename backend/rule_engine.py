import json
from datetime import datetime, timedelta

def load_rules(path):
    with open(path, 'r') as f:
        return json.load(f)

def evaluate_data(data, rules):
    violations = []
    for entry in data:
        for rule in rules:
            if rule['id'] == "kvkk_001":
                if entry.get("consent_status") != "given":
                    violations.append({"rule": rule['name'], "field": "consent_status", "record": entry})

            elif rule['id'] == "kvkk_002":
                created_at_raw = entry.get("created_at")
                if isinstance(created_at_raw, str) and created_at_raw.strip():
                    try:
                        created_at = datetime.strptime(created_at_raw, "%Y-%m-%d")
                        if created_at < datetime.now() - timedelta(days=730):
                            violations.append({"rule": rule['name'], "field": "created_at", "record": entry})
                    except Exception as e:
                        violations.append({
                            "rule": rule['name'],
                            "field": "created_at",
                            "record": entry,
                            "error": f"Invalid date format: {e}"
                        })

            elif rule['id'] == "gdpr_001":
                if not entry.get("legal_basis"):
                    violations.append({"rule": rule['name'], "field": "legal_basis", "record": entry})

    return violations
