def validate_policy(policy):
    for role, data in policy.items():
        for table, cfg in data.get("tables", {}).items():
            for rf in cfg.get("row_filters", []):
                if not isinstance(rf, dict):
                    raise Exception(f"Invalid policy in {role}.{table}: {rf}")
