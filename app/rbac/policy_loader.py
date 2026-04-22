# app/rbac/policy_loader.py

import json
import os


def load_policy():
    base_path = os.path.dirname(os.path.dirname(__file__))
    policy_path = os.path.join(base_path, "policies", "rbac.json")

    with open(policy_path) as f:
        return json.load(f)
