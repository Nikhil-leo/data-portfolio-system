# Dashboard Documentation: {{PROJECT_TITLE}}

**Tool:** {{DASHBOARD_TOOL}}  (Tableau / Power BI)
**Author:** {{YOUR_NAME}}
**Last Updated:** {{DATE}}

---

## Business Questions Answered

1. {{QUESTION_1}}
2. {{QUESTION_2}}
3. {{QUESTION_3}}
4. {{QUESTION_4}}

---

## KPI List

| KPI Name | Calculation | Data Source Field | Target | Color Code |
|----------|-------------|-------------------|--------|-----------|
| {{KPI_1}} | {{CALC_1}} | {{FIELD_1}} | {{TARGET_1}} | Green > target |
| {{KPI_2}} | {{CALC_2}} | {{FIELD_2}} | {{TARGET_2}} | Red < target |
| {{KPI_3}} | {{CALC_3}} | {{FIELD_3}} | {{TARGET_3}} | Amber ±5% |

---

## Chart List

| # | Chart Type | Title | X-Axis | Y-Axis | Filters Applied | Purpose |
|---|-----------|-------|--------|--------|-----------------|---------|
| 1 | {{CHART_TYPE_1}} | {{CHART_TITLE_1}} | {{X_1}} | {{Y_1}} | {{FILTERS_1}} | {{PURPOSE_1}} |
| 2 | {{CHART_TYPE_2}} | {{CHART_TITLE_2}} | {{X_2}} | {{Y_2}} | {{FILTERS_2}} | {{PURPOSE_2}} |
| 3 | {{CHART_TYPE_3}} | {{CHART_TITLE_3}} | {{X_3}} | {{Y_3}} | {{FILTERS_3}} | {{PURPOSE_3}} |
| 4 | {{CHART_TYPE_4}} | {{CHART_TITLE_4}} | {{X_4}} | {{Y_4}} | {{FILTERS_4}} | {{PURPOSE_4}} |

---

## Filters & Interactivity

| Filter | Type | Field | Default Value | Affects |
|--------|------|-------|---------------|---------|
| Date Range | Date Picker | {{DATE_FIELD}} | Last 12 months | All charts |
| {{FILTER_2}} | Dropdown | {{FIELD_2}} | All | {{AFFECTED_CHARTS_2}} |
| {{FILTER_3}} | Multi-select | {{FIELD_3}} | All | {{AFFECTED_CHARTS_3}} |

---

## Color Palette

| Use | Color | Hex |
|-----|-------|-----|
| Primary | {{COLOR_1}} | {{HEX_1}} |
| Secondary | {{COLOR_2}} | {{HEX_2}} |
| Positive trend | Green | #2ECC71 |
| Negative trend | Red | #E74C3C |
| Neutral | Gray | #95A5A6 |

---

## Data Connection

**Source:** {{DATA_SOURCE}}
**Connection Type:** {{CONNECTION_TYPE}}  (CSV / SQL / API / Live)
**Refresh Schedule:** {{REFRESH_SCHEDULE}}
**Last Refresh:** {{LAST_REFRESH}}

---

## Dashboard Screenshot

![Dashboard Preview](assets/dashboard-preview.png)

*Add your screenshot above by saving it as `assets/dashboard-preview.png`*

---

## Publishing Instructions

### Tableau Public
```
1. Open Tableau Desktop
2. File → Save to Tableau Public As...
3. Sign in with your Tableau Public account
4. Name: "{{PROJECT_TITLE}}"
5. Copy the share URL and paste into README.md
```

### Power BI Service
```
1. Open Power BI Desktop
2. File → Publish → Publish to Power BI
3. Select your workspace
4. Go to app.powerbi.com → find your report
5. Click Share → copy link → paste into README.md
```

---

## Tableau-Specific Notes

### Calculated Fields
| Field Name | Formula | Purpose |
|-----------|---------|---------|
| {{CALC_FIELD_1}} | `{{FORMULA_1}}` | {{FIELD_PURPOSE_1}} |
| {{CALC_FIELD_2}} | `{{FORMULA_2}}` | {{FIELD_PURPOSE_2}} |

### Parameters Used
- {{PARAMETER_1}}: {{PARAM_PURPOSE_1}}
- {{PARAMETER_2}}: {{PARAM_PURPOSE_2}}

---

## Power BI-Specific Notes

### DAX Measures
```dax
-- {{MEASURE_NAME_1}}
{{MEASURE_NAME_1}} = {{DAX_FORMULA_1}}

-- {{MEASURE_NAME_2}}
{{MEASURE_NAME_2}} = {{DAX_FORMULA_2}}
```

### Relationships
| Table A | Key | Table B | Key | Type |
|---------|-----|---------|-----|------|
| {{TABLE_A}} | {{KEY_A}} | {{TABLE_B}} | {{KEY_B}} | Many-to-One |

---

*Dashboard documentation for [{{PROJECT_TITLE}}](../README.md)*
