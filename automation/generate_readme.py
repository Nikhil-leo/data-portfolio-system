"""
generate_readme.py
------------------
Regenerate a project's README.md from its saved project.json metadata.

Usage:
    python automation/generate_readme.py <repo-name>

Example:
    python automation/generate_readme.py sales-performance-analysis
"""

import json
import sys
from pathlib import Path

ROOT          = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"
PROJECTS_DIR  = ROOT / "projects"
PORTFOLIO_DATA = ROOT / "portfolio-website" / "src" / "data" / "projects.json"


def fill_template(template_path: Path, replacements: dict) -> str:
    content = template_path.read_text()
    for key, value in replacements.items():
        content = content.replace(f"{{{{{key}}}}}", str(value))
    return content


def load_project_card(repo_name: str) -> dict:
    """Load the project's metadata from the portfolio JSON file."""
    if not PORTFOLIO_DATA.exists():
        raise FileNotFoundError(f"Portfolio data not found: {PORTFOLIO_DATA}")

    with open(PORTFOLIO_DATA) as f:
        projects = json.load(f)

    for project in projects:
        if project.get("id") == repo_name or project.get("repoName") == repo_name:
            return project

    raise ValueError(f"Project '{repo_name}' not found in {PORTFOLIO_DATA}")


def build_replacements(card: dict) -> dict:
    """Map portfolio card fields to README template placeholders."""
    tools_list = card.get("tools", [])
    kpis_list  = card.get("kpis", [])

    return {
        "PROJECT_TITLE":       card.get("title", ""),
        "SHORT_DESCRIPTION":   card.get("description", ""),
        "BUSINESS_PROBLEM":    card.get("description", ""),
        "DATASET_SOURCE":      "See case-study.md for details",
        "DATASET_SIZE":        "See data/",
        "TIME_PERIOD":         "See case-study.md",
        "DATA_FORMAT":         "CSV",
        "TOOLS_USED":          "\n".join(f"- {t}" for t in tools_list),
        "DATA_COLLECTION_STEP": "Sourced and downloaded dataset",
        "DATA_CLEANING_STEP":  "Cleaned with Python (src/clean_data.py)",
        "EDA_STEP":            "Explored patterns in notebooks/analysis.ipynb",
        "DASHBOARD_STEP":      "Built in " + (
            "Tableau and Power BI" if card.get("dashboards", {}).get("tableau")
            and card.get("dashboards", {}).get("powerbi")
            else "Tableau" if card.get("dashboards", {}).get("tableau")
            else "Power BI"
        ),
        "INSIGHTS_STEP":       "Summarized in case-study.md",
        "INSIGHT_1":           kpis_list[0] + " analysis" if kpis_list else "Key finding 1",
        "INSIGHT_2":           kpis_list[1] + " trends"   if len(kpis_list) > 1 else "Key finding 2",
        "INSIGHT_3":           "Business recommendation — see case-study.md",
        "TABLEAU_URL":         card.get("tableauUrl", "#"),
        "POWERBI_URL":         card.get("powerbiUrl", "#"),
        "GITHUB_USERNAME":     card.get("githubUrl", "").split("/")[-2] or "yourusername",
        "REPO_NAME":           card.get("repoName", ""),
        "FINAL_RECOMMENDATION": "See the full case study for detailed recommendations.",
        "YOUR_NAME":           "Your Name",
        "YEAR":                card.get("date", "")[:4] if card.get("date") else "2025",
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python automation/generate_readme.py <repo-name>")
        print("Example: python automation/generate_readme.py sales-performance-analysis")
        sys.exit(1)

    repo_name   = sys.argv[1]
    project_dir = PROJECTS_DIR / repo_name

    if not project_dir.exists():
        print(f"Error: Project folder not found: {project_dir}")
        sys.exit(1)

    print(f"Loading metadata for '{repo_name}'...")
    card         = load_project_card(repo_name)
    replacements = build_replacements(card)

    template  = TEMPLATES_DIR / "README-template.md"
    content   = fill_template(template, replacements)
    out_path  = project_dir / "README.md"

    out_path.write_text(content)
    print(f"✓ README regenerated: {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
