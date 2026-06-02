# Data Portfolio System

A complete end-to-end system for creating, documenting, and showcasing data analytics projects — from raw CSV to published Tableau/Power BI dashboards and a live portfolio website.

---

## What's Included

| Folder | Purpose |
|--------|---------|
| `/projects/` | One folder per analytics project |
| `/portfolio-website/` | Next.js portfolio site (deploy to Vercel) |
| `/templates/` | Reusable README, case study, and dashboard doc templates |
| `/automation/` | Python scripts to generate and manage projects |
| `/assets/` | Shared images and branding |
| `requirements.txt` | Python dependencies |

---

## Quickstart

### Step 1 — Install Python dependencies

```bash
pip install -r requirements.txt
```

### Step 2 — Create your first project

```bash
python automation/create_project.py
```

Answer the prompts and the script will:
- Create the full folder structure under `/projects/<your-repo-name>/`
- Generate a filled `README.md`, `case-study.md`, and `dashboard-docs.md`
- Add your project card to the portfolio website's data file
- Optionally init a local git repo

### Step 3 — Add your data

```
projects/<your-repo-name>/data/raw/raw_data.csv
```

### Step 4 — Clean and explore

```bash
# Run the cleaning script
python projects/<your-repo-name>/src/clean_data.py

# Open the analysis notebook
jupyter notebook projects/<your-repo-name>/notebooks/analysis.ipynb
```

### Step 5 — Run SQL analysis

Using DuckDB (recommended — no server needed):
```bash
pip install duckdb
duckdb -c ".read projects/<your-repo-name>/sql/analysis.sql"
```

Or open the `.sql` file in any SQL editor connected to your database.

### Step 6 — Build dashboards

- **Tableau:** Open Tableau Desktop → Connect to `data/cleaned/cleaned_data.csv` → Build → Publish to Tableau Public → paste URL into `README.md`
- **Power BI:** Open Power BI Desktop → Get Data → CSV → Build → Publish to Power BI Service → paste embed URL into `README.md`

### Step 7 — Launch the portfolio website

```bash
cd portfolio-website
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

### Step 8 — Customize the website

Edit these two files to add your real information:

| File | What to edit |
|------|-------------|
| `portfolio-website/src/data/profile.json` | Your name, bio, skills, experience, links |
| `portfolio-website/src/data/projects.json` | Auto-updated by `create_project.py`, or edit manually |

### Step 9 — Deploy to Vercel (free)

```bash
# Install Vercel CLI
npm i -g vercel

cd portfolio-website
vercel
```

Or connect your GitHub repo at [vercel.com](https://vercel.com) for automatic deployments.

---

## Automation Scripts

### `create_project.py` — Start a new project
```bash
python automation/create_project.py
```

### `generate_readme.py` — Regenerate a project's README
```bash
python automation/generate_readme.py <repo-name>
```

### `generate_case_study.py` — Fill in a detailed case study
```bash
# Step 1: create a blank answers file
python automation/generate_case_study.py <repo-name> --init

# Step 2: edit projects/<repo-name>/case-study-answers.json

# Step 3: generate the case study
python automation/generate_case_study.py <repo-name>
```

### `update_portfolio.py` — Sync all projects to the website
```bash
python automation/update_portfolio.py
```

---

## Adding a New Project (Full Workflow)

```
1. python automation/create_project.py
2. Drop dataset into projects/<name>/data/raw/raw_data.csv
3. python projects/<name>/src/clean_data.py
4. jupyter notebook projects/<name>/notebooks/analysis.ipynb
5. Write SQL queries in projects/<name>/sql/analysis.sql
6. Build Tableau / Power BI dashboard
7. Take a screenshot → save as projects/<name>/assets/dashboard-preview.png
8. Update URLs in README.md and dashboard-docs.md
9. python automation/update_portfolio.py
10. git add . && git commit -m "Add <project-name>"
11. Push to GitHub + deploy Vercel
```

---

## GitHub Workflow

```bash
# Initialize repo for a project (if not done automatically)
cd projects/<repo-name>
git init
git add .
git commit -m "Initial project scaffold"
git remote add origin https://github.com/<username>/<repo-name>.git
git push -u origin main
```

---

## Template Placeholders

All templates use `{{PLACEHOLDER}}` syntax. The automation scripts fill them automatically. You can also search-and-replace manually in any text editor.

---

## Sample Project

A working example lives at `/projects/sample-sales-analysis/` with:
- Real SQL queries (10 analyses)
- A full Jupyter notebook EDA
- Filled README and case study
- Dashboard preview SVG

---

*Built with Python · Next.js · Tailwind CSS · Tableau · Power BI*
