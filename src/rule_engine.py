import json
from typing import Dict, Any, List


def load_rules(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        rules = json.load(f)
    return rules


def evaluate_rules(sensor_data: Dict, rules: List[Dict]) -> Dict:
    """Evaluate rule list against a single sensor sample.

    Each rule is expected to be a dict with 'conditions' and 'fault_type' and an optional 'severity'.
    Conditions are simple comparisons implemented here for demo.
    """
    explanations = []
    for rule in rules:
        conds = rule.get("conditions", [])
        matched = True
        for c in conds:
            field = c.get("field")
            op = c.get("op")
            val = c.get("value")
            if field not in sensor_data:
                matched = False
                break
            sd = sensor_data[field]
            if op == ">":
                matched = matched and (sd > val)
            elif op == "<":
                matched = matched and (sd < val)
            elif op == ">=":
                matched = matched and (sd >= val)
            elif op == "<=":
                matched = matched and (sd <= val)
            elif op == "==":
                matched = matched and (sd == val)
            else:
                matched = False
        if matched:
            explanations.append({"fault_type": rule.get("fault_type"), "severity": rule.get("severity", 1), "rule": rule})

    if explanations:
        # pick highest severity match
        explanations.sort(key=lambda x: x.get("severity", 1), reverse=True)
        top = explanations[0]
        return {"matched": True, "fault_type": top["fault_type"], "explanations": explanations}
    return {"matched": False, "fault_type": "Normal", "explanations": []}


def infer_fault_type(rule_eval: Dict) -> str:
    return rule_eval.get("fault_type", "Normal")


def combine_with_ai(ai_output: Dict, rule_output: Dict) -> Dict:
    # Simple combination: if rule matched, prefer rule; otherwise use AI
    if rule_output.get("matched"):
        return {"final": rule_output.get("fault_type"), "source": "rule", "explanation": rule_output}
    return {"final": ai_output.get("class"), "source": "ai", "explanation": ai_output}


def update_rules(rules: List[Dict], rule_id: str, new_thresholds: Dict) -> List[Dict]:
    for r in rules:
        if r.get("id") == rule_id:
            r.update(new_thresholds)
    return rules
