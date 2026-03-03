def extract_points(text: str, point_symbol: str, points_map: dict):
    if not text:
        return None

    count = len(text) - len(text.lstrip(point_symbol))
    return points_map.get(count)
