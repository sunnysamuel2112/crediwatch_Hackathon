import rules
from rules import BusinessRulesEngine

# Instantiate BusinessRulesEngine
engine = BusinessRulesEngine()

# Add rules
rule1 = Rule('RULE001', 'Rule 1 description')
engine.add_rule(rule1)

rule2 = Rule('RULE002', 'Rule 2 description')
engine.add_rule(rule2)

# Generate alerts
data = {
    'customer_name': 'John Doe',
    'customer_number': '123456',
    'reporting_date': '2023-07-18',
    'date_of_alert': '2023-07-18'
}
alerts = engine.generate_alerts(data)

# Print the alerts
for alert in alerts:
    print(alert)
