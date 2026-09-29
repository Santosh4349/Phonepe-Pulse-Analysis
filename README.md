# Phonepe-Pulse-Analysis
Exploratory analysis of PhonePe Pulse transaction, user, and device data across Indian states and districts (2018–2021), using Python to find what actually drives digital payment adoption.

## Overview

This project explores PhonePe Pulse's public dataset to understand how digital payment adoption varies across India, which factors actually drive transaction volume, and where the biggest growth opportunities are. The analysis moves through data cleaning and validation, metric engineering, correlation analysis, and visualization.

## Datasets Used

- State and district-level transaction data
- State and district-level registered user data
- Transaction type breakdown
- Device brand usage
- District-level demographics (population, area, density)

Data spans **2018 Q1 to 2021 Q2**.

## What This Analysis Does

- **Data quality checks** — reconciles district-level totals against state-level figures to catch inconsistencies before drawing conclusions; flags missing values and incomplete records rather than silently dropping them.
- **Metric engineering** — derives average transaction value, user-to-population ratio, and spend per user to make states and districts comparable on a level footing.
- **Correlation analysis** — merges transaction data with demographics and runs Pearson and Spearman correlation to test what actually predicts usage: population, population density, or area. Population turns out to be the dominant driver, not density or geography.
- **Visualization** — charts quarterly growth, top and bottom performing states, and device brand share to surface adoption trends.
- **Business recommendations** — translates the findings into two concrete actions: prioritize user acquisition in low-penetration states, and deepen merchant/bill-payment usage in states that already have high transaction volume.

## Tech Stack

- Python
- Pandas, NumPy — data cleaning, aggregation, merging
- Matplotlib, Seaborn — visualization
- SciPy (Pearson/Spearman correlation)

## Key Finding

Population size is the primary driver of PhonePe transaction volume at the district level — not population density or geographic area. This suggests growth strategy should weight raw addressable population more heavily than urban-density assumptions when prioritizing markets.

## Files

- `PhonePay.py` — full analysis script (data loading, cleaning, metric calculation, correlation testing, and charts)

## How to Run

```bash
pip install pandas numpy matplotlib seaborn scipy
python PhonePay.py
```

## Data Source

[PhonePe Pulse](https://www.phonepe.com/pulse/) — publicly available transaction, user, and insurance data released by PhonePe.
