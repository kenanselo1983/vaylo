import json

def load_rules(path):
    with open(path, "r") as f:
        return json.load(f)

def evaluate_data(data, rules):
    results = []
    for row in data:
        for rule in rules:
            # Validate that required keys exist
            if "column" not in rule or "condition" not in rule or "name" not in rule or "message" not in rule:
                print(f"⚠️ Skipping malformed rule: {rule}")
                continue

            column = rule["column"]
            condition = rule["condition"]
            try:
                value = row.get(column)
                context = {"value": value}
                if eval(condition, {}, context):
                    results.append({
                        "rule": rule["name"],
                        "column": column,
                        "value": value,
                        "message": rule["message"]
                    })
            except Exception as e:
                print(f"❌ Rule error: {e} | Rule: {rule}")
    return results
