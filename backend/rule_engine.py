import json

def load_rules(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def evaluate_data(records, rules):
    results = []

    for entry in records:
        for rule in rules:
            column = rule["column"]
            raw_value = entry.get(column)

            # Try to parse JSON if value is a JSON-like string
            parsed_value = {}
            if isinstance(raw_value, str) and raw_value.strip().startswith("{"):
                try:
                    parsed_value = json.loads(raw_value)
                except json.JSONDecodeError:
                    pass

            # Rule: Field is missing or empty
            if rule["type"] == "missing":
                if not raw_value:
                    results.append({
                        "rule": rule["name"],
                        "column": column,
                        "reason": "Field is missing or empty"
                    })

            # Rule: Consent not given
            elif rule["type"] == "consent_check":
                if isinstance(parsed_value, dict) and not parsed_value.get("consent_given", True):
                    results.append({
                        "rule": rule["name"],
                        "column": column,
                        "reason": "Consent not given"
                    })

            # Rule: Email missing or invalid
            elif rule["type"] == "email_check":
                email = parsed_value.get("email", "") if isinstance(parsed_value, dict) else ""
                if not email or "@" not in email:
                    results.append({
                        "rule": rule["name"],
                        "column": column,
                        "reason": "Missing or invalid email"
                    })

    return results
