from app.schema.relationships import RELATIONSHIPS


def resolve_via_path(start_table, target_table):
    """
    Find path like:
    payments → orders
    """

    if start_table == target_table:
        return [start_table]

    visited = set()

    def dfs(current, path):
        if current == target_table:
            return path

        visited.add(current)

        for neighbor in RELATIONSHIPS.get(current, {}):
            if neighbor not in visited:
                result = dfs(neighbor, path + [neighbor])
                if result:
                    return result

        return None

    return dfs(start_table, [start_table])
