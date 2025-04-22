from backend.scanner import fetch_data_from_db
from backend.rule_engine import evaluate_data, load_rules

data = fetch_data_from_db()
rules = load_rules("backend/rules/kvkk_rules.json") + load_rules("backend/rules/gdpr_rules.json")
violations = evaluate_data(data, rules)

for v in violations:
    print(f"❌ {v['rule']} - Field: {v['field']} - Name: {v['record'].get('name')}")
