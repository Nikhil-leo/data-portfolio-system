"""
generate_case_study.py
----------------------
Regenerate a project's case-study.md from an answers JSON file
(so you can fill in the detailed answers without re-running the full
create_project wizard).

Usage:
    # Step 1: generate a blank answers file
    python automation/generate_case_study.py <repo-name> --init

    # Step 2: fill in your answers in projects/<repo>/case-study-answers.json

    # Step 3: regenerate the case study
    python automation/generate_case_study.py <repo-name>
"""

import json
import sys
from pathlib import Path

ROOT          = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"
PROJECTS_DIR  = ROOT / "projects"

# All placeholder keys that appear in the case study template
BLANK_ANSWERS = {
    "PROJECT_TITLE": "My Project Title",
    "YOUR_NAME": "Your Name",
    "DATE": "2025-01-01",
    "TOOLS_USED": "Python, SQL, Tableau",
    "OVERVIEW_PARAGRAPH": "Write 2-3 sentences summarising the project here.",
    "BACKGROUND": "Describe the business context and why this analysis was needed.",
    "BUSINESS_QUESTION_1": "What are the top-performing products?",
    "BUSINESS_QUESTION_2": "Which regions drive the most profit?",
    "BUSINESS_QUESTION_3": "What seasonal patterns affect sales?",
    "SUCCESS_CRITERION_1": "Dashboard accessible to business stakeholders",
    "SUCCESS_CRITERION_2": "Key KPIs visible at a glance",
    "DATASET_NAME": "Superstore Sales Dataset",
    "DATASET_SOURCE": "Kaggle",
    "ROW_COUNT": "10,000",
    "COLUMN_COUNT": "20",
    "DATE_RANGE": "2020-2023",
    "FIELD_1": "order_date", "FIELD_1_DESC": "Date of order", "TYPE_1": "DATE",
    "FIELD_2": "sales", "FIELD_2_DESC": "Sale amount USD", "TYPE_2": "FLOAT",
    "FIELD_3": "category", "FIELD_3_DESC": "Product category", "TYPE_3": "VARCHAR",
    "ISSUE_1": "Missing values in profit column",
    "ISSUE_2": "Inconsistent date formats",
    "ISSUE_3": "Duplicate order IDs",
    "RAW_FILE": "raw_data.csv",
    "COLUMN": "profit",
    "DATE_COLUMN": "order_date",
    "CLEAN_FILE": "cleaned_data.csv",
    "CLEAN_ROW_COUNT": "9,800",
    "NULL_COUNT": "0",
    "DUPLICATE_COUNT": "200",
    "EDA_SUMMARY": "Distribution is right-skewed; top 20% of customers drive 80% of revenue.",
    "EDA_FINDING_1": "Q4 consistently outperforms by 30%",
    "EDA_FINDING_2": "Technology category has highest margin",
    "EDA_FINDING_3": "West region leads in revenue",
    "SQL_QUERY_DESCRIPTION": "Top 10 products by revenue",
    "SQL_QUERY": "SELECT product_name, SUM(sales) AS total_revenue\nFROM sales\nGROUP BY product_name\nORDER BY total_revenue DESC\nLIMIT 10;",
    "KPI_1": "Revenue", "KPI_1_DEF": "Total sales", "KPI_1_TARGET": "$1M",
    "KPI_2": "Profit Margin", "KPI_2_DEF": "Profit / Revenue", "KPI_2_TARGET": "25%",
    "KPI_3": "Growth Rate", "KPI_3_DEF": "YoY revenue growth", "KPI_3_TARGET": "10%",
    "CHART_1": "Bar chart — Revenue by Category", "CHART_1_PURPOSE": "Compare performance",
    "CHART_2": "Line chart — Monthly Trend", "CHART_2_PURPOSE": "Show seasonality",
    "CHART_3": "Map — Sales by Region", "CHART_3_PURPOSE": "Geographic breakdown",
    "DESIGN_RATIONALE": "Chose blue tones for trust; KPI cards at top for executive summary.",
    "DASHBOARD_URL": "https://public.tableau.com/views/your-workbook",
    "INSIGHT_TITLE_1": "Seasonal Demand Spike",
    "INSIGHT_DETAIL_1": "Q4 demand peaks 30% above annual average due to holiday shopping.",
    "INSIGHT_TITLE_2": "Regional Disparity",
    "INSIGHT_DETAIL_2": "West region generates 40% of revenue with 25% of customers.",
    "INSIGHT_TITLE_3": "Discount Risk",
    "INSIGHT_DETAIL_3": "Discounts above 20% produce negative profit margins.",
    "IMPACT_1": "Reporting time", "BEFORE_1": "2 hrs/week", "AFTER_1": "15 min/week", "CHANGE_1": "-87%",
    "IMPACT_2": "Decision speed", "BEFORE_2": "Days", "AFTER_2": "Real-time", "CHANGE_2": "Instant",
    "ESTIMATED_VALUE": "$50K/year in analyst time saved",
    "TECHNICAL_SKILL_1": "SQL window functions",
    "TECHNICAL_SKILL_2": "Power BI DAX measures",
    "BUSINESS_SKILL_1": "Translating questions into metrics",
    "BUSINESS_SKILL_2": "Storytelling with data",
    "RETROSPECTIVE": "Gather stakeholder requirements earlier and prototype before full build.",
    "GITHUB_USERNAME": "yourusername",
    "REPO_NAME": "your-repo-name",
}


def fill_template(template_path: Path, answers: dict) -> str:
    content = template_path.read_text()
    for key, value in answers.items():
        content = content.replace(f"{{{{{key}}}}}", str(value))
    return content


def init_answers(project_dir: Path, repo_name: str):
    answers_path = project_dir / "case-study-answers.json"
    blank = {**BLANK_ANSWERS, "REPO_NAME": repo_name}
    answers_path.write_text(json.dumps(blank, indent=2))
    print(f"✓ Blank answers file created: {answers_path.relative_to(ROOT)}")
    print("  Fill in your answers, then re-run without --init to generate the case study.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python automation/generate_case_study.py <repo-name> [--init]")
        sys.exit(1)

    repo_name   = sys.argv[1]
    init_mode   = "--init" in sys.argv
    project_dir = PROJECTS_DIR / repo_name

    if not project_dir.exists():
        print(f"Error: Project folder not found: {project_dir}")
        sys.exit(1)

    if init_mode:
        init_answers(project_dir, repo_name)
        return

    answers_path = project_dir / "case-study-answers.json"
    if not answers_path.exists():
        print(f"Answers file not found. Run with --init first:")
        print(f"  python automation/generate_case_study.py {repo_name} --init")
        sys.exit(1)

    with open(answers_path) as f:
        answers = json.load(f)

    template = TEMPLATES_DIR / "case-study-template.md"
    content  = fill_template(template, answers)
    out_path = project_dir / "case-study.md"
    out_path.write_text(content)
    print(f"✓ Case study generated: {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
