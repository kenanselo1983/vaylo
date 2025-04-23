import json

def evaluate_data(records, rules):
    results = []

    for entry in records:
        for rule in rules:
            column = rule["column"]
            raw_value = entry.get(column)

            # Try to parse JSON if value looks like JSON
            parsed_value = {}
            if isinstance(raw_value, str) and raw_value.strip().startswith("{"):
                try:
                    parsed_value = json.loads(raw_value)
                except json.JSONDecodeError:
                    pass

            # Rule: missing field entirely
            if rule["type"] == "missing" and not raw_value:
                results.append({
                    "rule": rule["name"],
                    "column": column,
                    "reason": "Field is missing or empty"
                })

            # Rule: consent_check
            if rule["type"] == "consent_check":
                if not parsed_value.get("consent_given", True):
                    results.append({
                        "rule": rule["name"],
                        "column": column,
                        "reason": "Consent not given"
                    })

            # Rule: email_check
            if rule["type"] == "email_check":
                email = parsed_value.get("email", "")
                if not email or "@" not in email:
                    results.append({
                        "rule": rule["name"],
                        "column": column,
                        "reason": "Missing or invalid email"
                    })

    return results
