"""
create_project.py
-----------------
Interactive project generator for the data portfolio system.

Run:
    python automation/create_project.py

What it does:
    1. Asks you a series of questions about your project
    2. Creates the full folder structure under /projects/<repo-name>/
    3. Generates README.md, case-study.md, and dashboard docs
    4. Adds a project card to portfolio-website/src/data/projects.json
    5. Optionally initializes a local git repo
"""

import os
import json
import shutil
import subprocess
from datetime import date
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
PROJECTS_DIR = ROOT / "projects"
TEMPLATES_DIR = ROOT / "templates"
PORTFOLIO_DATA = ROOT / "portfolio-website" / "src" / "data" / "projects.json"


# ── Helpers ────────────────────────────────────────────────────────────────────

def ask(prompt: str, default: str = "") -> str:
    """Prompt the user and return their answer (or the default)."""
    suffix = f" [{default}]" if default else ""
    answer = input(f"\n{prompt}{suffix}: ").strip()
    return answer if answer else default


def ask_multiline(prompt: str) -> str:
    """Allow the user to type multiple lines; end with a blank line."""
    print(f"\n{prompt} (press Enter twice to finish):")
    lines = []
    while True:
        line = input()
        if line == "" and lines:
            break
        lines.append(line)
    return "\n".join(lines)


def ask_list(prompt: str) -> list[str]:
    """Ask the user for comma-separated values; return as a list."""
    raw = ask(prompt)
    return [item.strip() for item in raw.split(",") if item.strip()]


def fill_template(template_path: Path, replacements: dict) -> str:
    """Read a template file and replace all {{PLACEHOLDERS}}."""
    content = template_path.read_text()
    for key, value in replacements.items():
        content = content.replace(f"{{{{{key}}}}}", str(value))
    return content


def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"  ✓  Created: {path.relative_to(ROOT)}")


def create_placeholder_image(path: Path):
    """Write a tiny SVG as a dashboard preview placeholder."""
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="800" height="450">
  <rect width="800" height="450" fill="#1e293b"/>
  <text x="400" y="210" font-family="sans-serif" font-size="28"
        fill="#64748b" text-anchor="middle">Dashboard Preview</text>
  <text x="400" y="255" font-family="sans-serif" font-size="16"
        fill="#475569" text-anchor="middle">Replace this with your actual screenshot</text>
</svg>"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg)
    print(f"  ✓  Created placeholder: {path.relative_to(ROOT)}")


# ── Interview ──────────────────────────────────────────────────────────────────

def interview() -> dict:
    print("\n" + "=" * 60)
    print("  DATA PORTFOLIO PROJECT GENERATOR")
    print("=" * 60)
    print("Answer each question. Press Enter to accept the default.\n")

    data = {}

    data["PROJECT_TITLE"]   = ask("Project title", "Sales Performance Analysis")
    data["REPO_NAME"]       = ask("GitHub repo / folder name (no spaces)",
                                   data["PROJECT_TITLE"].lower().replace(" ", "-"))
    data["YOUR_NAME"]       = ask("Your full name", "Your Name")
    data["GITHUB_USERNAME"] = ask("GitHub username", "yourusername")
    data["SHORT_DESCRIPTION"] = ask("One-sentence description",
                                     "Analyzing sales trends to identify growth opportunities")
    data["BUSINESS_PROBLEM"] = ask_multiline("Describe the business problem")
    data["DATASET_SOURCE"]  = ask("Dataset source or file name", "Kaggle — Superstore Sales Dataset")
    data["DATASET_SIZE"]    = ask("Approx. dataset size", "~10,000 rows")
    data["TIME_PERIOD"]     = ask("Time period covered", "2020–2023")
    data["DATA_FORMAT"]     = ask("Data format", "CSV")

    tools_raw = ask("Tools used (comma-separated)",
                    "Python, SQL, Tableau, Power BI, Excel")
    data["TOOLS_LIST"]  = [t.strip() for t in tools_raw.split(",")]
    data["TOOLS_USED"]  = "\n".join(f"- {t}" for t in data["TOOLS_LIST"])

    kpis_raw = ask("Key KPIs (comma-separated)", "Revenue, Profit Margin, Sales Growth, Customer Count")
    data["KPIS"]     = [k.strip() for k in kpis_raw.split(",")]

    dashboard_choice = ask("Dashboard type (tableau / powerbi / both)", "both").lower()
    data["USE_TABLEAU"] = "tableau" in dashboard_choice or "both" in dashboard_choice
    data["USE_POWERBI"] = "powerbi" in dashboard_choice or "both" in dashboard_choice

    data["PORTFOLIO_DESCRIPTION"] = ask(
        "Portfolio card description (2-3 sentences)",
        "Built an end-to-end analytics solution exploring sales trends. "
        "Created interactive dashboards in Tableau and Power BI."
    )
    data["TAGS"] = ask_list("Portfolio tags (comma-separated)", "Python, SQL, Tableau, Power BI")

    data["DATE"]    = str(date.today())
    data["YEAR"]    = str(date.today().year)

    # Sensible defaults for template placeholders not asked interactively
    defaults = {
        "TABLEAU_URL": "https://public.tableau.com/views/your-workbook",
        "POWERBI_URL": "https://app.powerbi.com/view?r=your-report-id",
        "DASHBOARD_URL": "https://public.tableau.com/views/your-workbook",
        "DASHBOARD_TOOL": "Tableau / Power BI",
        "DATA_COLLECTION_STEP": "Downloaded dataset from source and loaded into pandas",
        "DATA_CLEANING_STEP": "Removed duplicates, handled nulls, fixed data types",
        "EDA_STEP": "Explored distributions, trends, and correlations",
        "DASHBOARD_STEP": "Designed KPI cards, bar charts, line trends, and filters",
        "INSIGHTS_STEP": "Summarized findings and wrote business recommendations",
        "INSIGHT_1": "Add your first key finding here",
        "INSIGHT_2": "Add your second key finding here",
        "INSIGHT_3": "Add your third key finding here",
        "FINAL_RECOMMENDATION": "Add your final business recommendation here",
        "OVERVIEW_PARAGRAPH": "Provide a 2-3 sentence overview of the project.",
        "BACKGROUND": "Describe the business context.",
        "BUSINESS_QUESTION_1": "What are the top-performing products by revenue?",
        "BUSINESS_QUESTION_2": "Which regions drive the most profit?",
        "BUSINESS_QUESTION_3": "What seasonal patterns affect sales?",
        "SUCCESS_CRITERION_1": "Dashboard accessible to business stakeholders",
        "SUCCESS_CRITERION_2": "Key KPIs visible at a glance",
        "DATASET_NAME": data["DATASET_SOURCE"],
        "ROW_COUNT": data["DATASET_SIZE"],
        "COLUMN_COUNT": "~20",
        "DATE_RANGE": data["TIME_PERIOD"],
        "FIELD_1": "date", "FIELD_1_DESC": "Transaction date", "TYPE_1": "DATE",
        "FIELD_2": "sales", "FIELD_2_DESC": "Sale amount in USD", "TYPE_2": "FLOAT",
        "FIELD_3": "category", "FIELD_3_DESC": "Product category", "TYPE_3": "VARCHAR",
        "ISSUE_1": "Missing values in key columns",
        "ISSUE_2": "Inconsistent date formats",
        "ISSUE_3": "Duplicate transaction IDs",
        "RAW_FILE": "raw_data.csv",
        "CLEAN_FILE": "cleaned_data.csv",
        "COLUMN": "sales",
        "DATE_COLUMN": "date",
        "CLEAN_ROW_COUNT": "~9,800",
        "NULL_COUNT": "0",
        "DUPLICATE_COUNT": "~200",
        "EDA_SUMMARY": "Distribution of sales is right-skewed. Top 20% of customers drive 80% of revenue.",
        "EDA_FINDING_1": "Q4 consistently outperforms other quarters by 30%",
        "EDA_FINDING_2": "Technology category has the highest profit margin",
        "EDA_FINDING_3": "West region leads in total revenue",
        "SQL_QUERY_DESCRIPTION": "Top 10 products by revenue",
        "SQL_QUERY": "SELECT product_name, SUM(sales) AS total_revenue\nFROM sales\nGROUP BY product_name\nORDER BY total_revenue DESC\nLIMIT 10;",
        "KPI_1": data["KPIS"][0] if data["KPIS"] else "Revenue",
        "KPI_1_DEF": "Total sales amount", "KPI_1_TARGET": "$1M",
        "KPI_2": data["KPIS"][1] if len(data["KPIS"]) > 1 else "Profit Margin",
        "KPI_2_DEF": "Profit / Revenue", "KPI_2_TARGET": "25%",
        "KPI_3": data["KPIS"][2] if len(data["KPIS"]) > 2 else "Growth",
        "KPI_3_DEF": "YoY revenue growth", "KPI_3_TARGET": "10%",
        "CHART_TYPE_1": "Bar Chart", "CHART_TITLE_1": "Revenue by Category",
        "X_1": "Category", "Y_1": "Revenue", "FILTERS_1": "Date, Region",
        "PURPOSE_1": "Compare revenue across product categories",
        "CHART_TYPE_2": "Line Chart", "CHART_TITLE_2": "Monthly Sales Trend",
        "X_2": "Month", "Y_2": "Sales", "FILTERS_2": "Year, Category",
        "PURPOSE_2": "Show sales trend over time",
        "CHART_TYPE_3": "Map", "CHART_TITLE_3": "Sales by Region",
        "X_3": "Region", "Y_3": "Sales", "FILTERS_3": "Date",
        "PURPOSE_3": "Geographic breakdown of performance",
        "CHART_TYPE_4": "Scatter Plot", "CHART_TITLE_4": "Profit vs. Discount",
        "X_4": "Discount", "Y_4": "Profit", "FILTERS_4": "Category",
        "PURPOSE_4": "Identify discount impact on profitability",
        "DATE_FIELD": "order_date",
        "FILTER_2": "Category", "FIELD_2": "category",
        "AFFECTED_CHARTS_2": "Revenue, Profit charts",
        "FILTER_3": "Region", "FIELD_3": "region",
        "AFFECTED_CHARTS_3": "Map, KPI cards",
        "COLOR_1": "Navy Blue", "HEX_1": "#1E3A5F",
        "COLOR_2": "Teal", "HEX_2": "#0D9488",
        "DATA_SOURCE": data["DATASET_SOURCE"],
        "CONNECTION_TYPE": "CSV",
        "REFRESH_SCHEDULE": "Manual",
        "LAST_REFRESH": data["DATE"],
        "CALC_FIELD_1": "Profit Ratio",
        "FORMULA_1": "SUM([Profit]) / SUM([Sales])",
        "FIELD_PURPOSE_1": "Calculate profit margin percentage",
        "CALC_FIELD_2": "Sales YoY Growth",
        "FORMULA_2": "(SUM([Sales]) - LOOKUP(SUM([Sales]), -1)) / ABS(LOOKUP(SUM([Sales]), -1))",
        "FIELD_PURPOSE_2": "Year-over-year growth rate",
        "PARAMETER_1": "Top N", "PARAM_PURPOSE_1": "Filter top N products dynamically",
        "PARAMETER_2": "Metric Selector", "PARAM_PURPOSE_2": "Switch between Sales and Profit",
        "MEASURE_NAME_1": "Total Revenue",
        "DAX_FORMULA_1": "SUM(Sales[SalesAmount])",
        "MEASURE_NAME_2": "Profit Margin %",
        "DAX_FORMULA_2": "DIVIDE(SUM(Sales[Profit]), SUM(Sales[SalesAmount]), 0)",
        "TABLE_A": "Sales", "KEY_A": "ProductID",
        "TABLE_B": "Products", "KEY_B": "ProductID",
        "INSIGHT_TITLE_1": "Q4 Seasonality",
        "INSIGHT_DETAIL_1": "Sales spike 30% in Q4, driven by holiday demand.",
        "INSIGHT_TITLE_2": "Regional Disparity",
        "INSIGHT_DETAIL_2": "The West region generates 40% of total revenue despite having 25% of customers.",
        "INSIGHT_TITLE_3": "Discount Risk",
        "INSIGHT_DETAIL_3": "Discounts above 20% consistently produce negative profit margins.",
        "IMPACT_1": "Reporting time", "BEFORE_1": "2 hours/week", "AFTER_1": "15 min/week", "CHANGE_1": "-87%",
        "IMPACT_2": "Decision speed", "BEFORE_2": "Days", "AFTER_2": "Real-time", "CHANGE_2": "Immediate",
        "ESTIMATED_VALUE": "$50K/year in analyst time saved",
        "TECHNICAL_SKILL_1": "Advanced SQL window functions",
        "TECHNICAL_SKILL_2": "Power BI DAX calculated measures",
        "BUSINESS_SKILL_1": "Translating business questions into metrics",
        "BUSINESS_SKILL_2": "Storytelling with data",
        "RETROSPECTIVE": "I would gather stakeholder requirements earlier and test dashboard prototypes before building final version.",
        "QUESTION_1": "Which product categories generate the most revenue?",
        "QUESTION_2": "How have sales trended over time?",
        "QUESTION_3": "Which regions are underperforming?",
        "QUESTION_4": "What is the relationship between discounts and profitability?",
    }

    # Merge — only fill keys not already set by the interview
    for k, v in defaults.items():
        data.setdefault(k, v)

    return data


# ── Folder structure ───────────────────────────────────────────────────────────

SUBFOLDERS = ["data/raw", "data/cleaned", "notebooks", "sql", "src",
              "tableau", "powerbi", "assets"]

STUB_FILES = {
    "notebooks/analysis.ipynb": '''{
 "cells": [
  {"cell_type": "markdown", "metadata": {},
   "source": ["# {title}\\n\\nExploratory Data Analysis"]},
  {"cell_type": "code", "execution_count": null, "metadata": {}, "outputs": [],
   "source": [
    "import pandas as pd\\n",
    "import matplotlib.pyplot as plt\\n",
    "import seaborn as sns\\n\\n",
    "# Load cleaned data\\n",
    "df = pd.read_csv(\\"../data/cleaned/cleaned_data.csv\\")\\n",
    "df.head()"
   ]},
  {"cell_type": "code", "execution_count": null, "metadata": {}, "outputs": [],
   "source": ["df.describe()"]},
  {"cell_type": "code", "execution_count": null, "metadata": {}, "outputs": [],
   "source": ["df.info()"]}
 ],
 "metadata": {
  "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
  "language_info": {"name": "python", "version": "3.10.0"}
 },
 "nbformat": 4, "nbformat_minor": 5
}''',

    "src/clean_data.py": '''"""
clean_data.py — Data cleaning script for {title}
Run: python src/clean_data.py
"""
import pandas as pd
from pathlib import Path

RAW  = Path("data/raw/raw_data.csv")
OUT  = Path("data/cleaned/cleaned_data.csv")

def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates()
    # TODO: add your cleaning steps here
    return df

if __name__ == "__main__":
    df = pd.read_csv(RAW)
    print(f"Loaded {{len(df)}} rows")
    df = clean(df)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"Saved {{len(df)}} cleaned rows → {{OUT}}")
''',

    "sql/analysis.sql": '''-- ============================================================
-- {title} — SQL Analysis Queries
-- ============================================================

-- 1. Overview: total records
SELECT COUNT(*) AS total_records
FROM your_table;

-- 2. Revenue by category
SELECT
    category,
    SUM(sales)   AS total_revenue,
    SUM(profit)  AS total_profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2) AS profit_margin_pct
FROM your_table
GROUP BY category
ORDER BY total_revenue DESC;

-- 3. Monthly trend
SELECT
    DATE_TRUNC(\'month\', order_date) AS month,
    SUM(sales) AS monthly_revenue
FROM your_table
GROUP BY 1
ORDER BY 1;

-- 4. Top 10 customers
SELECT
    customer_id,
    customer_name,
    SUM(sales) AS lifetime_value
FROM your_table
GROUP BY customer_id, customer_name
ORDER BY lifetime_value DESC
LIMIT 10;
''',

    "tableau/README.md": '''# Tableau Workbook

Place your `.twbx` file in this folder.

## Instructions
1. Open Tableau Desktop
2. Connect to `data/cleaned/cleaned_data.csv`
3. Build your visualizations
4. File → Save As → save `.twbx` here
5. Publish to Tableau Public and update the URL in README.md
''',

    "powerbi/README.md": '''# Power BI Report

Place your `.pbix` file in this folder.

## Instructions
1. Open Power BI Desktop
2. Get Data → Text/CSV → select `data/cleaned/cleaned_data.csv`
3. Build your report
4. File → Save As → save `.pbix` here
5. Publish to Power BI Service and update the URL in README.md
''',

    "data/raw/.gitkeep": "",
    "data/cleaned/.gitkeep": "",
}


def create_project_structure(data: dict) -> Path:
    project_dir = PROJECTS_DIR / data["REPO_NAME"]

    if project_dir.exists():
        overwrite = ask(f"\n'{data['REPO_NAME']}' already exists. Overwrite? (yes/no)", "no")
        if overwrite.lower() != "yes":
            print("Aborted.")
            raise SystemExit(0)
        shutil.rmtree(project_dir)

    print(f"\n📁 Creating project: {project_dir.relative_to(ROOT)}")

    # Sub-folders
    for folder in SUBFOLDERS:
        (project_dir / folder).mkdir(parents=True, exist_ok=True)

    # Stub files
    for rel_path, content in STUB_FILES.items():
        write_file(project_dir / rel_path,
                   content.replace("{title}", data["PROJECT_TITLE"]))

    # Templates → filled docs
    readme_content = fill_template(TEMPLATES_DIR / "README-template.md", data)
    write_file(project_dir / "README.md", readme_content)

    case_study_content = fill_template(TEMPLATES_DIR / "case-study-template.md", data)
    write_file(project_dir / "case-study.md", case_study_content)

    dashboard_content = fill_template(TEMPLATES_DIR / "dashboard-template.md", data)
    write_file(project_dir / "dashboard-docs.md", dashboard_content)

    # Placeholder image
    create_placeholder_image(project_dir / "assets" / "dashboard-preview.svg")

    return project_dir


# ── Portfolio data ─────────────────────────────────────────────────────────────

def update_portfolio_json(data: dict):
    """Append or update the project card in projects.json."""
    PORTFOLIO_DATA.parent.mkdir(parents=True, exist_ok=True)

    if PORTFOLIO_DATA.exists():
        with open(PORTFOLIO_DATA) as f:
            projects = json.load(f)
    else:
        projects = []

    # Remove existing entry with same repo name
    projects = [p for p in projects if p.get("repoName") != data["REPO_NAME"]]

    card = {
        "id": data["REPO_NAME"],
        "title": data["PROJECT_TITLE"],
        "description": data["PORTFOLIO_DESCRIPTION"],
        "tags": data["TAGS"],
        "tools": data["TOOLS_LIST"],
        "kpis": data["KPIS"],
        "dashboards": {
            "tableau": data["USE_TABLEAU"],
            "powerbi": data["USE_POWERBI"],
        },
        "repoName": data["REPO_NAME"],
        "githubUrl": f"https://github.com/{data['GITHUB_USERNAME']}/{data['REPO_NAME']}",
        "tableauUrl": data.get("TABLEAU_URL", ""),
        "powerbiUrl": data.get("POWERBI_URL", ""),
        "image": f"/projects/{data['REPO_NAME']}-preview.png",
        "featured": len(projects) == 0,  # first project is featured
        "date": data["DATE"],
    }

    projects.append(card)

    with open(PORTFOLIO_DATA, "w") as f:
        json.dump(projects, f, indent=2)

    print(f"  ✓  Updated portfolio data: {PORTFOLIO_DATA.relative_to(ROOT)}")


# ── Git init ───────────────────────────────────────────────────────────────────

def git_init(project_dir: Path, data: dict):
    """Optionally initialize a git repo and make a first commit."""
    do_git = ask("\nInitialize a local git repo for this project? (yes/no)", "yes")
    if do_git.lower() != "yes":
        return

    gitignore = """# Python
__pycache__/
*.pyc
.env
venv/

# Data (large files)
data/raw/*.csv
data/raw/*.xlsx

# Jupyter checkpoints
.ipynb_checkpoints/

# OS
.DS_Store
"""
    write_file(project_dir / ".gitignore", gitignore)

    cmds = [
        ["git", "init"],
        ["git", "add", "."],
        ["git", "commit", "-m",
         f"Initial commit: {data['PROJECT_TITLE']} project scaffold"],
    ]

    for cmd in cmds:
        result = subprocess.run(cmd, cwd=project_dir, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✓  git {cmd[1]}")
        else:
            print(f"  ✗  git {cmd[1]} failed: {result.stderr.strip()}")

    remote = ask(
        f"\nEnter GitHub remote URL to add (or press Enter to skip)",
        f"https://github.com/{data['GITHUB_USERNAME']}/{data['REPO_NAME']}.git"
    )
    if remote:
        subprocess.run(["git", "remote", "add", "origin", remote], cwd=project_dir)
        print(f"  ✓  Remote set to {remote}")
        print(f"\n  To push: cd projects/{data['REPO_NAME']} && git push -u origin main")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    try:
        data = interview()
        project_dir = create_project_structure(data)
        update_portfolio_json(data)
        git_init(project_dir, data)

        print("\n" + "=" * 60)
        print("  PROJECT CREATED SUCCESSFULLY")
        print("=" * 60)
        print(f"\n  📂 Location : projects/{data['REPO_NAME']}/")
        print(f"  📄 README   : projects/{data['REPO_NAME']}/README.md")
        print(f"  📋 Case study: projects/{data['REPO_NAME']}/case-study.md")
        print(f"  📊 Dashboard docs: projects/{data['REPO_NAME']}/dashboard-docs.md")
        print(f"\n  Next steps:")
        print(f"  1. Drop your dataset into:  projects/{data['REPO_NAME']}/data/raw/")
        print(f"  2. Run the cleaning script: python projects/{data['REPO_NAME']}/src/clean_data.py")
        print(f"  3. Open the notebook:       projects/{data['REPO_NAME']}/notebooks/analysis.ipynb")
        print(f"  4. Build your dashboard and replace the preview image in assets/")
        print(f"  5. Run: python automation/update_portfolio.py to refresh the website\n")

    except KeyboardInterrupt:
        print("\n\nCancelled.")


if __name__ == "__main__":
    main()
