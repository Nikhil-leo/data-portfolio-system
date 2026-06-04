# Tableau Dashboard Build Guide
## E-Commerce Operations Analytics — Olist Brazil

Follow these steps exactly to build a 3-page interactive Tableau dashboard.

---

## SETUP

1. Open **Tableau Desktop**
2. Connect → **Text File** → select `data/cleaned/master.csv`
3. Go to **Sheet** view

---

## PAGE 1: EXECUTIVE OVERVIEW

### KPI Cards (create 5 BANs)

For each KPI, create a new sheet:

#### KPI 1 — Total Revenue
- Drag `Total Revenue` to **Text**
- Calculation: `SUM([Total Revenue])`
- Format: Currency, 0 decimal places
- Title: "Total Revenue"
- Sheet name: `KPI_Revenue`

#### KPI 2 — Total Orders
- Calculation: `COUNTD([Order Id])`
- Format: Number, comma separated
- Title: "Total Orders"
- Sheet name: `KPI_Orders`

#### KPI 3 — Avg Order Value
- Calculation: `SUM([Total Revenue]) / COUNTD([Order Id])`
- Format: Currency, 2 decimal places
- Title: "Avg Order Value"
- Sheet name: `KPI_AOV`

#### KPI 4 — Avg Review Score
- Calculation: `AVG([Review Score])`
- Format: Number, 2 decimal places
- Title: "Avg Review Score"
- Sheet name: `KPI_Review`

#### KPI 5 — On-Time Delivery %
- Calculation: `AVG([On Time Delivery]) * 100`
- Format: Number, 1 decimal + "%" suffix
- Title: "On-Time Delivery %"
- Sheet name: `KPI_OnTime`

---

### Chart 1 — Monthly Revenue Trend (Line Chart)
**Sheet name:** `Revenue_Trend`

1. Drag `Order Purchase Timestamp` → **Columns** (set to **Month**)
2. Drag `Total Revenue` → **Rows** → SUM
3. Drag `Total Revenue` again to **Color** (creates gradient)
4. Change mark type to **Line**
5. Add `Total Revenue` to **Label** → show at end of line
6. Filter: `Order Status = delivered`
7. Title: "Monthly Revenue Trend"
8. Add **Reference Line** → Average → dashed gray

---

### Chart 2 — Orders by Day of Week (Bar Chart)
**Sheet name:** `Orders_DOW`

1. Create Calculated Field → `Day of Week`:
   ```
   DATENAME('weekday', [Order Purchase Timestamp])
   ```
2. Drag `Day of Week` → **Columns**
3. Drag `Order Id` → **Rows** → COUNTD
4. Sort: Custom order (Mon→Sun)
5. Color: Blue gradient
6. Title: "Orders by Day of Week"

---

### Chart 3 — Payment Type Breakdown (Donut Chart)
**Sheet name:** `Payment_Types`

1. Drag `Payment Type` → **Color**
2. Drag `Order Id` → **Angle** → COUNTD
3. Change to **Pie** mark
4. Duplicate the sheet, set size to 1 (inner circle trick for donut)
5. Put both on dashboard with inner circle on top
6. Title: "Payment Method Mix"

---

### Chart 4 — Order Status Funnel (Bar Chart)
**Sheet name:** `Order_Status`

1. Drag `Order Status` → **Rows**
2. Drag `Order Id` → **Columns** → COUNTD
3. Sort descending
4. Color each bar differently
5. Add labels
6. Title: "Order Status Breakdown"

---

## PAGE 2: DELIVERY & OPERATIONS

### Chart 5 — Brazil State Map (Filled Map)
**Sheet name:** `State_Map`

1. Drag `Customer State` → **Detail**
2. Tableau auto-detects → set **Geographic Role** = State/Province → Brazil
3. Drag `Total Revenue` → **Color** → SUM → Blue gradient
4. Drag `On Time Delivery` → **Tooltip** → AVG → format as %
5. Drag `Avg Review Score` → **Tooltip** → AVG
6. Drag `Order Id` → **Tooltip** → COUNTD
7. Title: "Revenue & Performance by State"

---

### Chart 6 — Delivery Days Distribution (Histogram)
**Sheet name:** `Delivery_Histogram`

1. Drag `Delivery Days Actual` → **Columns**
2. Right-click → **Create Bins** → Bin size = 2
3. Drag count → **Rows**
4. Color: conditional
   - Create Calculated Field `Delivery Color`:
     ```
     IF [Delivery Days Actual] <= 7 THEN "Fast (≤7d)"
     ELSEIF [Delivery Days Actual] <= 14 THEN "Normal (8-14d)"
     ELSEIF [Delivery Days Actual] <= 21 THEN "Slow (15-21d)"
     ELSE "Critical (21d+)"
     END
     ```
5. Drag `Delivery Color` → **Color**
6. Set colors: Green, Blue, Orange, Red
7. Add Reference Line at mean
8. Title: "Delivery Time Distribution"

---

### Chart 7 — On-Time Delivery Rate by State (Bar Chart)
**Sheet name:** `OnTime_State`

1. Drag `Customer State` → **Rows**
2. Create Calculated Field `On Time %`:
   ```
   AVG([On Time Delivery]) * 100
   ```
3. Drag `On Time %` → **Columns**
4. Color by value:
   - Create Calculated Field `OT Color`:
     ```
     IF AVG([On Time Delivery])*100 >= 90 THEN "On Target"
     ELSEIF AVG([On Time Delivery])*100 >= 80 THEN "Near Target"
     ELSE "Below Target"
     END
     ```
5. Set colors: Green, Yellow, Red
6. Sort descending
7. Add Reference Line at 90%
8. Title: "On-Time Delivery Rate by State"

---

### Chart 8 — Delivery vs Review Score (Scatter Plot)
**Sheet name:** `Delivery_vs_Review`

1. Drag `Delivery Days Actual` → **Columns** → AVG
2. Drag `Review Score` → **Rows** → AVG
3. Drag `Category` → **Detail**
4. Drag `Total Revenue` → **Size** → SUM
5. Drag `Category` → **Color**
6. Add **Trend Line** (Analysis → Trend Lines → Show Trend Lines)
7. Title: "Delivery Time vs Customer Satisfaction"

---

### Chart 9 — Late Delivery Impact (Side-by-Side Bar)
**Sheet name:** `Late_Impact`

1. Create Calculated Field `Delivery Status`:
   ```
   IF [On Time Delivery] = 1 THEN "On Time" ELSE "Late" END
   ```
2. Drag `Delivery Status` → **Columns**
3. Drag `Review Score` → **Rows** → AVG
4. Drag `Delivery Status` → **Color**
5. Set: Green = On Time, Red = Late
6. Add labels
7. Title: "Review Score: On-Time vs Late Deliveries"

---

## PAGE 3: PRODUCTS & SELLERS

### Chart 10 — Top 15 Categories by Revenue (Bar Chart)
**Sheet name:** `Category_Revenue`

1. Drag `Category` → **Rows**
2. Drag `Total Revenue` → **Columns** → SUM
3. Sort descending, show top 15 (right-click Category → Filter → Top 15 by SUM Revenue)
4. Drag `Total Revenue` → **Color**
5. Add `Total Revenue` to labels
6. Title: "Top 15 Product Categories by Revenue"

---

### Chart 11 — Category Review Heatmap (Highlight Table)
**Sheet name:** `Category_Heatmap`

1. Drag `Category` → **Rows**
2. Create calculated fields:
   - `Avg Review` = `AVG([Review Score])`
   - `On Time %` = `AVG([On Time Delivery])*100`
   - `Avg Delivery Days` = `AVG([Delivery Days Actual])`
3. Drag each measure to **Columns** (creates multi-measure view)
4. Change mark type to **Square**
5. Color by `Avg Review`
6. This creates a performance heatmap across categories
7. Title: "Category Performance Heatmap"

---

### Chart 12 — Top Sellers Performance (Bar Chart)
**Sheet name:** `Top_Sellers`

1. Drag `Seller Id` → **Rows**
2. Drag `Total Revenue` → **Columns** → SUM
3. Filter: Top 20 sellers by SUM(Total Revenue)
4. Drag `On Time %` → **Color**
5. Add `Avg Review Score` to tooltip
6. Title: "Top 20 Sellers by Revenue"

---

### Chart 13 — Revenue by Quarter (Grouped Bar)
**Sheet name:** `Quarterly_Revenue`

1. Drag `Purchase Quarter` → **Columns**
2. Drag `Purchase Year` → **Color**
3. Drag `Total Revenue` → **Rows** → SUM
4. Mark type: **Bar**
5. Title: "Quarterly Revenue by Year"

---

## FILTERS (Apply to All Sheets)

Create these as **Dashboard Filters** visible to all sheets:

1. **Date Range Filter**
   - Field: `Order Purchase Timestamp`
   - Type: Relative Date or Range of Dates
   - Apply to all worksheets

2. **State Filter**
   - Field: `Customer State`
   - Type: Multi-select dropdown
   - Apply to all worksheets

3. **Category Filter**
   - Field: `Category`
   - Type: Multi-select dropdown
   - Apply to relevant worksheets

4. **Order Status Filter**
   - Field: `Order Status`
   - Default: Select "delivered"
   - Apply to all worksheets

---

## DASHBOARD ASSEMBLY

### Dashboard 1: Executive Overview
- Size: **1366 × 768** (Desktop)
- Layout:
  ```
  ┌─────────────────────────────────────────────────┐
  │  KPI: Revenue | Orders | AOV | Review | OnTime  │ ← Row of 5 KPI cards
  ├────────────────────────┬────────────────────────┤
  │                        │                        │
  │   Revenue_Trend        │   Orders_DOW           │
  │   (line chart)         │   (bar chart)          │
  │                        │                        │
  ├────────────────────────┼────────────────────────┤
  │                        │                        │
  │   Payment_Types        │   Order_Status         │
  │   (donut)              │   (bar)                │
  │                        │                        │
  └────────────────────────┴────────────────────────┘
  ```
- Add Date Range filter at top right

### Dashboard 2: Delivery & Operations
```
┌─────────────────────────────────────────────────┐
│  KPI: OnTime% | Avg Delivery Days | Late Orders  │
├────────────────────────┬────────────────────────┤
│                        │                        │
│   State_Map            │   OnTime_State         │
│   (Brazil map)         │   (bar chart)          │
│                        │                        │
├────────────────────────┼────────────────────────┤
│                        │                        │
│   Delivery_Histogram   │   Late_Impact          │
│   (histogram)          │   (bar chart)          │
│                        │                        │
└────────────────────────┴────────────────────────┘
```

### Dashboard 3: Products & Sellers
```
┌─────────────────────────────────────────────────┐
│   Filters: Category | State | Date              │
├────────────────────────┬────────────────────────┤
│                        │                        │
│   Category_Revenue     │   Quarterly_Revenue    │
│   (horiz bar)          │   (grouped bar)        │
│                        │                        │
├────────────────────────┼────────────────────────┤
│                        │                        │
│   Category_Heatmap     │   Top_Sellers          │
│   (highlight table)    │   (bar chart)          │
│                        │                        │
└────────────────────────┴────────────────────────┘
```

---

## INTERACTIVITY SETTINGS

1. **Use as Filter** — click each chart → Use as Filter (funnel icon)
   - State Map filters all other charts on Dashboard 2
   - Category bar filters all charts on Dashboard 3
   - Revenue Trend filters by selected time period

2. **Actions** — Dashboard → Actions → Add Action → Filter
   - Source: State_Map → Target: all sheets on Dashboard 2
   - Source: Category_Revenue → Target: Category_Heatmap, Top_Sellers

3. **Highlight Actions**
   - Dashboard → Actions → Highlight
   - Source: any sheet → Target: all sheets
   - Fields: Customer State, Category

---

## COLOR PALETTE

| Use | Color | Hex |
|-----|-------|-----|
| Primary | Blue | #3b82f6 |
| Positive | Green | #22c55e |
| Warning | Amber | #f59e0b |
| Negative | Red | #ef4444 |
| Neutral | Gray | #94a3b8 |
| Background | Dark | #0f172a |

Apply dark background:
- Format → Shading → Worksheet → Dark gray (#1e293b)
- Format → Font → All → White

---

## PUBLISHING

1. File → Save As → save `.twbx` to `tableau/` folder
2. Server → Tableau Public → Sign In → Save to Public
3. Copy the share URL
4. Update the URL in `README.md`

---

## FINAL CHECKLIST

- [ ] All 13 charts created
- [ ] 3 dashboards assembled
- [ ] Filters applied to all sheets
- [ ] Use-as-filter interactivity on all charts
- [ ] Dark theme applied
- [ ] KPI cards show correct numbers
- [ ] Map shows Brazil states correctly
- [ ] Published to Tableau Public
- [ ] URL added to README.md
