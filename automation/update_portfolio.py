"""
update_portfolio.py
-------------------
Scan all projects and sync their metadata into the portfolio website's
data file (portfolio-website/src/data/projects.json).

Run this any time you:
  - Add a new project manually
  - Update a project's README or case-study
  - Change URLs after publishing dashboards

Usage:
    python automation/update_portfolio.py
"""

import json
import re
from datetime import date
from pathlib import Path

ROOT           = Path(__file__).resolve().parent.parent
PROJECTS_DIR   = ROOT / "projects"
PORTFOLIO_DATA = ROOT / "portfolio-website" / "src" / "data" / "projects.json"


def parse_readme(readme_path: Path) -> dict:
    """Extract key fields from a project README.md via simple regex."""
    if not readme_path.exists():
        return {}

    text = readme_path.read_text()
    data = {}

    # Title
    title_match = re.search(r"^# (.+)$", text, re.MULTILINE)
    data["title"] = title_match.group(1).strip() if title_match else readme_path.parent.name

    # Short description (blockquote after title)
    desc_match = re.search(r"^> (.+)$", text, re.MULTILINE)
    data["description"] = desc_match.group(1).strip() if desc_match else ""

    # Tools (bullet list under "## Tools Used")
    tools_match = re.search(r"## Tools Used\n((?:- .+\n?)+)", text)
    if tools_match:
        data["tools"] = re.findall(r"- (.+)", tools_match.group(1))
    else:
        data["tools"] = []

    # Dashboard URLs
    tableau_match = re.search(r"\[View on Tableau Public\]\((.+?)\)", text)
    data["tableauUrl"] = tableau_match.group(1) if tableau_match else ""

    powerbi_match = re.search(r"\[View Report\]\((.+?)\)", text)
    data["powerbiUrl"] = powerbi_match.group(1) if powerbi_match else ""

    # GitHub URL
    github_match = re.search(r"git clone (https://github\.com/\S+)", text)
    if github_match:
        data["githubUrl"] = github_match.group(1).replace(".git", "")
    else:
        data["githubUrl"] = ""

    return data


def build_card(project_dir: Path, existing_card: dict = None) -> dict:
    """Build a portfolio project card from the project folder."""
    readme_data = parse_readme(project_dir / "README.md")
    repo_name   = project_dir.name

    # Start from existing card so user-edited fields aren't overwritten
    card = existing_card.copy() if existing_card else {}

    card.setdefault("id",          repo_name)
    card.setdefault("repoName",    repo_name)
    card.setdefault("featured",    False)
    card.setdefault("date",        str(date.today()))
    card.setdefault("tags",        readme_data.get("tools", []))
    card.setdefault("kpis",        [])
    card.setdefault("dashboards",  {
        "tableau": bool(readme_data.get("tableauUrl")),
        "powerbi": bool(readme_data.get("powerbiUrl")),
    })
    card.setdefault("image", f"/projects/{repo_name}-preview.png")

    # Always update these from the README (they may have changed)
    if readme_data.get("title"):
        card["title"] = readme_data["title"]
    if readme_data.get("description"):
        card["description"] = readme_data["description"]
    if readme_data.get("tools"):
        card["tools"] = readme_data["tools"]
    if readme_data.get("tableauUrl"):
        card["tableauUrl"] = readme_data["tableauUrl"]
    if readme_data.get("powerbiUrl"):
        card["powerbiUrl"] = readme_data["powerbiUrl"]
    if readme_data.get("githubUrl"):
        card["githubUrl"] = readme_data["githubUrl"]

    return card


def main():
    PORTFOLIO_DATA.parent.mkdir(parents=True, exist_ok=True)

    # Load existing portfolio data
    existing = {}
    if PORTFOLIO_DATA.exists():
        with open(PORTFOLIO_DATA) as f:
            for card in json.load(f):
                existing[card.get("repoName", card.get("id", ""))] = card

    # Scan projects directory
    project_dirs = [d for d in PROJECTS_DIR.iterdir() if d.is_dir()
                    and not d.name.startswith(".")]

    if not project_dirs:
        print("No projects found. Run create_project.py first.")
        return

    cards = []
    for project_dir in sorted(project_dirs):
        print(f"  Scanning: {project_dir.name}")
        card = build_card(project_dir, existing.get(project_dir.name))
        cards.append(card)
        print(f"    ✓ {card['title']}")

    with open(PORTFOLIO_DATA, "w") as f:
        json.dump(cards, f, indent=2)

    print(f"\n✓ Portfolio data updated: {PORTFOLIO_DATA.relative_to(ROOT)}")
    print(f"  {len(cards)} project(s) synced")
    print(f"\n  Next: cd portfolio-website && npm run dev")


if __name__ == "__main__":
    main()
