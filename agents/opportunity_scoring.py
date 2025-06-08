def score_opportunities(frequent, missing, related):
    combined = set(missing + related)
    results = []

    for product in combined:
        score = 0
        reasons = []
        if product in missing:
            score += 60
            reasons.append("commonly purchased by peers")
        if product in related:
            score += 40
            reasons.append("frequently bought with existing products")
        
        results.append({
            "product": product,
            "score": score,
            "rationale": ", ".join(reasons)
        })
    return sorted(results, key=lambda x: x["score"], reverse=True)
