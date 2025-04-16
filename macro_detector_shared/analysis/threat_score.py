def calculate_threat_score(static_result):
    keywords = static_result.get("suspicious_keywords", [])
    score = min(len(keywords) * 20, 100)  # Simple scoring: 20 pts per keyword
    return score
