# Case Study: {{PROJECT_TITLE}}

**Author:** {{YOUR_NAME}}
**Date:** {{DATE}}
**Tools:** {{TOOLS_USED}}

---

## Overview

{{OVERVIEW_PARAGRAPH}}

---

## Problem Statement

### Background
{{BACKGROUND}}

### Business Questions
1. {{BUSINESS_QUESTION_1}}
2. {{BUSINESS_QUESTION_2}}
3. {{BUSINESS_QUESTION_3}}

### Success Criteria
- {{SUCCESS_CRITERION_1}}
- {{SUCCESS_CRITERION_2}}

---

## Data Source

| Attribute | Detail |
|-----------|--------|
| **Dataset** | {{DATASET_NAME}} |
| **Source** | {{DATASET_SOURCE}} |
| **Rows** | {{ROW_COUNT}} |
| **Columns** | {{COLUMN_COUNT}} |
| **Date Range** | {{DATE_RANGE}} |

### Key Fields
| Column | Description | Data Type |
|--------|-------------|-----------|
| {{FIELD_1}} | {{FIELD_1_DESC}} | {{TYPE_1}} |
| {{FIELD_2}} | {{FIELD_2_DESC}} | {{TYPE_2}} |
| {{FIELD_3}} | {{FIELD_3_DESC}} | {{TYPE_3}} |

---

## Data Cleaning

### Issues Found
- {{ISSUE_1}}
- {{ISSUE_2}}
- {{ISSUE_3}}

### Steps Taken
```python
# Example cleaning steps
import pandas as pd

df = pd.read_csv("data/raw/{{RAW_FILE}}")

# Drop duplicates
df = df.drop_duplicates()

# Handle missing values
df["{{COLUMN}}"].fillna(df["{{COLUMN}}"].median(), inplace=True)

# Fix data types
df["{{DATE_COLUMN}}"] = pd.to_datetime(df["{{DATE_COLUMN}}"])

df.to_csv("data/cleaned/{{CLEAN_FILE}}", index=False)
```

### Final Dataset
- Rows after cleaning: **{{CLEAN_ROW_COUNT}}**
- Null values: **{{NULL_COUNT}}**
- Duplicate rows removed: **{{DUPLICATE_COUNT}}**

---

## Exploratory Analysis

### Key Statistics
{{EDA_SUMMARY}}

### Notable Findings from EDA
1. {{EDA_FINDING_1}}
2. {{EDA_FINDING_2}}
3. {{EDA_FINDING_3}}

### SQL Analysis

```sql
-- {{SQL_QUERY_DESCRIPTION}}
{{SQL_QUERY}}
```

---

## Dashboard Design

### KPIs Tracked
| KPI | Definition | Target |
|-----|-----------|--------|
| {{KPI_1}} | {{KPI_1_DEF}} | {{KPI_1_TARGET}} |
| {{KPI_2}} | {{KPI_2_DEF}} | {{KPI_2_TARGET}} |
| {{KPI_3}} | {{KPI_3_DEF}} | {{KPI_3_TARGET}} |

### Charts Included
- {{CHART_1}} — {{CHART_1_PURPOSE}}
- {{CHART_2}} — {{CHART_2_PURPOSE}}
- {{CHART_3}} — {{CHART_3_PURPOSE}}

### Design Decisions
{{DESIGN_RATIONALE}}

### Dashboard Screenshot
![Dashboard](assets/dashboard-preview.png)

> [View Live Dashboard]({{DASHBOARD_URL}})

---

## Insights

### Finding 1: {{INSIGHT_TITLE_1}}
{{INSIGHT_DETAIL_1}}

### Finding 2: {{INSIGHT_TITLE_2}}
{{INSIGHT_DETAIL_2}}

### Finding 3: {{INSIGHT_TITLE_3}}
{{INSIGHT_DETAIL_3}}

---

## Business Impact

| Impact Area | Before | After | Change |
|-------------|--------|-------|--------|
| {{IMPACT_1}} | {{BEFORE_1}} | {{AFTER_1}} | {{CHANGE_1}} |
| {{IMPACT_2}} | {{BEFORE_2}} | {{AFTER_2}} | {{CHANGE_2}} |

**Estimated value:** {{ESTIMATED_VALUE}}

---

## What I Learned

### Technical Skills
- {{TECHNICAL_SKILL_1}}
- {{TECHNICAL_SKILL_2}}

### Business Skills
- {{BUSINESS_SKILL_1}}
- {{BUSINESS_SKILL_2}}

### If I Did This Again
{{RETROSPECTIVE}}

---

*[Back to GitHub Repo](https://github.com/{{GITHUB_USERNAME}}/{{REPO_NAME}})*
