# Static product affinities (could be dynamic with market data or ML in real use)

affinity_map = {
    "Drills": ["Drill Bits", "Protective Gloves"],
    "Generators": ["Backup Batteries", "Safety Gear"],
    "Advanced Analytics": ["API Integrations", "Workflow Automation"],
    "Collaboration Suite": ["Advanced Analytics", "Workflow Automation"],
    "Reporting Dashboard": ["API Integrations", "Safety Gear"]
}

def suggest_related_products(products):
    related = set()
    for prod in products:
        if prod in affinity_map:
            related.update(affinity_map[prod])
    return list(related)
