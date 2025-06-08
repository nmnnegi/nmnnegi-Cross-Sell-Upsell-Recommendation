def generate_report(profile, recommendations):
    report = f"Cross-Sell and Upsell Opportunities for {profile['name']}\n\n"
    report += f"Industry: {profile['industry']}, Revenue: ${profile['annual_revenue']}, "
    report += f"Employees: {profile['employee_count']}, Location: {profile['location']}\n"
    report += f"Current Products: {', '.join(profile['current_products'])}\n\n"
    
    report += "Recommended Opportunities:\n"
    for item in recommendations[:5]:
        report += f"- {item['product']}: {item['rationale']} (Score: {item['score']})\n"
    
    report += "\nConclusion:\n"
    report += "Implementing targeted campaigns based on these insights can increase customer retention and revenue."
    return report
