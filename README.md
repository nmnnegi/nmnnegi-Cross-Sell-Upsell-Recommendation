# 🧠 LangGraph Cross-Sell / Upsell Recommendation System

This project builds a modular LangGraph agent system that analyzes customer purchase data to generate personalized **cross-sell** and **upsell** recommendations, along with a detailed **natural language research report**. The data is stored in a **PostgreSQL** database hosted on **Render**.

---

## 🚀 Features

- Modular agent-based analysis using LangGraph
- Cross-sell & upsell recommendations based on:
  - Purchase patterns
  - Product affinity
  - Industry trends
- Clean and structured API via FastAPI
- Live research report generation in plain English
- **PostgreSQL** integration (hosted on Render – Free Tier)

---

## 📂 Project Structure

```
langgraph_crosssell/
🔾️ agents/                  # LangGraph sub-agents
🏢 customer_context.py
🏢 purchase_pattern.py
🏢 product_affinity.py
🏢 opportunity_scoring.py
🏢 report_generator.py
📆 db/                      # SQL schema and sample data
🏢 schema.sql
🏢 sample_data.sql
🏢 db_utils.py              # PostgreSQL connection and data fetch
🏢 graph_builder.py         # LangGraph pipeline
🏢 main.py                  # FastAPI API definition
🏢 requirements.txt
🏢 README.md                # You're here
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/langgraph_crosssell.git
cd langgraph_crosssell
```

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🛠️ PostgreSQL Setup (via Render)

1. Go to [https://render.com](https://render.com) and sign in.
2. Create a new **PostgreSQL database** (Free Tier).
3. Go to your **Database Dashboard → Connection Details**.
4. Run the schema and insert data via `psql` or Render's SQL Shell:
   - Upload and execute `db/schema.sql`
   - Then execute `db/sample_data.sql`
5. Update `db_utils.py` with your connection values:

```python
def get_connection():
    return psycopg2.connect(
        dbname="your_db",
        user="your_user",
        password="your_password",
        host="your_host",  # e.g., dpg-xyz.render.com
        port="5432"
    )
```

---

## ▶️ Run the API

```bash
uvicorn main:app --reload
```

Then open in your browser or Postman:

```
http://127.0.0.1:8000/recommendation?customer_id=C003
```

### 📅 Sample Response

```json
{
  "customer_id": "C003",
  "report": "Cross-Sell and Upsell Opportunities for Pyramid Construction Inc.\n\nIndustry: Construction...",
  "recommendations": [
    {
      "product": "Backup Batteries",
      "score": 60,
      "rationale": "commonly purchased by peers"
    },
    {
      "product": "Safety Gear",
      "score": 40,
      "rationale": "frequently bought with existing products"
    }
  ]
}
```

---

## 📌 Agents Summary

| Agent                   | Purpose                                                   |
| ----------------------- | --------------------------------------------------------- |
| CustomerContextAgent    | Extracts customer profile from PostgreSQL                 |
| PurchasePatternAgent    | Analyzes frequent vs missing purchases vs industry trends |
| ProductAffinityAgent    | Suggests co-purchased/related products                    |
| OpportunityScoringAgent | Scores opportunities based on synergy and relevance       |
| ReportGeneratorAgent    | Converts scores into a natural-language research report   |

---

## 💪 Example Customer IDs (from `sample_data.sql`)

- `C001` – Edge Communications
- `C002` – Burlington Textiles Corp
- `C003` – Pyramid Construction Inc.
- `C004` – Grand Hotels & Resorts
- `C005` – United Oil & Gas Corp.

---

## ✅ TODO (Optional Enhancements)

- Add Dockerfile and PostgreSQL container
- Deploy FastAPI backend on Render or Railway
- Implement ML-based affinity prediction
- Add authentication layer

---

## 📄 License

MIT License – free to use, modify, and distribute.

---

## 🤝 Contributing

PRs and feedback welcome. Let's make B2B AI smarter together!
