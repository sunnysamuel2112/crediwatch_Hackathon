import csv

# Rule class
class Rule:
    def __init__(self, rule_code, rule_description, conditions, calculations, alert_category):
        self.rule_code = rule_code
        self.rule_description = rule_description
        self.conditions = conditions
        self.calculations = calculations
        self.alert_category = alert_category

    def apply(self, insurance_entry):
        # Evaluate conditions with insurance_entry as a local variable
        conditions_met = eval(self.conditions, locals())
        if not conditions_met:
            return False

        # Calculate values
        for key, expression in self.calculations.items():
            insurance_entry[key] = eval(expression, locals())

        return True

# BusinessRulesEngine class
class BusinessRulesEngine:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def generate_alerts(self, insurance_data):
        alerts = []

        for insurance_entry in insurance_data:
            for rule in self.rules:
                if rule.apply(insurance_entry):
                    # Generate alert
                    alert = {
                        'customer_name': insurance_entry['customer_name'],
                        'customer_number': insurance_entry['customer_number'],
                        'reporting_date': insurance_entry['reporting_date'],
                        'date_of_alert': 'current_date',
                        'category': rule.alert_category,
                        'rule_desc': rule.rule_description,
                        'rule_code': rule.rule_code
                    }
                    alerts.append(alert)

        return alerts

# Read insurance data from CSV file
insurance_data = []
with open('data.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        insurance_data.append(row)

# Create rule instances
rules_json = {
    "signal_1": {
        "rule": "Overinsured inventory",
        "class": "signal_1",
        "conditions": "float(insurance_entry['amount_of_insurance']) > float(insurance_entry['value_of_security']) and insurance_entry['expiry_date'] > insurance_entry['reporting_date']",
        "calculate": {
            "insurance_percentage": "float(insurance_entry['amount_of_insurance']) / float(insurance_entry['value_of_security']) * 100"
        },
        "category": {
            "high": "over_insurance_percentage > 150",
            "medium": "120 < over_insurance_percentage <= 150",
            "low": "110 < over_insurance_percentage <= 120"
        }
    },
    "signal_2": {
        "rule": "Underinsured inventory",
        "class": "signal_2",
        "conditions": "float(insurance_entry['amount_of_insurance']) < float(insurance_entry['value_of_security']) and insurance_entry['expiry_date'] > insurance_entry['reporting_date']",
        "calculate": {
            "insurance_percentage": "float(insurance_entry['amount_of_insurance']) / float(insurance_entry['value_of_security']) * 100"
        },
        "category": {
            "high": "under_insurance_percentage < 70",
            "medium": "70 <= under_insurance_percentage < 80",
            "low": "80 <= under_insurance_percentage < 90"
        }
    }
}

rules_engine = BusinessRulesEngine()

for signal, rule_json in rules_json.items():
    rule = Rule(
        rule_code=signal,
        rule_description=rule_json['rule'],
        conditions=rule_json['conditions'],
        calculations=rule_json['calculate'],
        alert_category=rule_json['category']
    )
    rules_engine.add_rule(rule)

# Generate alerts
alerts = rules_engine.generate_alerts(insurance_data)

# Print alerts
for alert in alerts:
    print(alert)
