# Marketing Campaign Data Pipeline

## End-to-End Analysis of Operations, Quality Assurance, Sales Tracking & Forecasting

---

## Project Overview

This project was developed as part of a Data technical assessment designed to evaluate end-to-end analytical capabilities including:

* Data Understanding
* Data Cleaning & Wrangling
* Exploratory Data Analysis (EDA)
* Business Intelligence & KPI Analysis
* Time-Series Forecasting
* Interactive Dashboard Development

The dataset contains operational, quality assurance, and sales records for a marketing campaign. The objective is to transform raw campaign data into actionable business insights and forecast future performance.

---

## Business Problem

Marketing and sales teams need visibility into campaign performance, quality assurance processes, sales conversion rates, and future lead generation trends.

This project aims to answer key business questions:

* How effective is the sales funnel?
* Which products generate the highest sales?
* Which team leaders and closers perform best?
* How does quality assurance impact operational performance?
* Which states generate the most revenue?
* What are the expected lead and revenue trends in the coming weeks?

---

## Dataset Information

The dataset contains:

* Operations records
* Quality Assurance reviews
* Sales transactions
* Customer information
* Product information
* Payment information

### Dataset Size

| Metric             | Value |
| ------------------ | ----- |
| Rows               | 1,184 |
| Columns            | 26    |
| Final Cleaned Rows | 1,183 |
| Final Features     | 31    |

---

# Project Structure

```text
Marketing-Campaign-Analysis/
│
├── data/
│   ├── sample_data.csv
│   └── cleaned_data.csv
│
├── notebooks/
│   └── Marketing_Campaign_Analysis.ipynb
│
├── models/
│   ├── lead_prophet.pkl
│   └── revenue_prophet.pkl
│
├── images/
│   ├── sales_funnel.png
│   ├── qa_analysis.png
│   ├── state_analysis.png
│   ├── product_analysis.png
│   ├── team_performance.png
│   └── forecast.png
│
├── app.py
├── requirements.txt
├── environment.yml
├── README.md
└── .gitignore
```

---

# Phase 1 — Data Understanding & Cleaning

## Data Quality Assessment

The dataset contained:

* Mixed data types
* Missing values
* Inconsistent date formats
* Duplicate records
* Excel-generated formatting artifacts
* Text-based pricing information

## Cleaning Steps

### Date Standardization

Converted all date columns into proper datetime format:

* Assign Date
* Finish Date
* Validation Date
* Date of Sale
* Creation Date
* Date of Payment
* DOB

---

### Quality Score Correction

Excel incorrectly converted some percentage values into dates.

Examples:

| Incorrect Value | Correct Value |
| --------------- | ------------- |
| 10-Aug          | 80            |
| 10-Sep          | 90            |
| 10-Oct          | 100           |

Custom cleaning logic was implemented to recover original quality scores.

---

### Missing Value Handling

#### QA Fields

QA-related missing values were intentionally preserved because they represent records that were never reviewed.

#### Customer Information

Missing values in:

* Gender
* City
* Customer attributes

were replaced with:

```text
Unknown
```

---

### Feature Engineering

The following business features were created:

| Feature          | Description                              |
| ---------------- | ---------------------------------------- |
| QA Reviewed      | Indicates if a record received QA review |
| Sale Made        | Indicates if a sale occurred             |
| Payment Received | Indicates if payment was received        |
| Monthly Price    | Numeric extraction from pricing text     |
| Days To Payment  | Time between sale and payment            |

---

### Duplicate Handling

Duplicate records were identified and removed only after verification.

Result:

```text
1 duplicate removed
```

---

# Phase 2 — Exploratory Data Analysis

## Sales Funnel Analysis

Evaluated customer progression through:

```text
Lead
↓
Transferred
↓
Approved
↓
Paid
```

Analysis highlighted conversion bottlenecks and sales performance opportunities.

---

## Quality Assurance Analysis

Investigated:

* QA completion rates
* Quality score distributions
* Review coverage
* Validation performance

---

## Product Performance

Analyzed:

* Sales by product
* Revenue contribution
* Product popularity
* Conversion efficiency

---

## Team Leader Performance

Compared:

* Sales generated
* Approval rates
* Revenue contribution
* Operational effectiveness

---

## Closer Performance

Evaluated:

* Individual sales performance
* Revenue generated
* Closing efficiency

---

## Geographic Analysis

State-level analysis included:

* Revenue distribution
* Lead generation
* Sales concentration
* Market performance

---

## Payment Analysis

Investigated:

* Payment completion rates
* Revenue collection
* Payment delays
* Days-to-payment trends

---

# Phase 3 — Time-Series Forecasting

## Forecasting Objective

Predict future campaign performance using historical campaign activity.

---

## Forecasted Metrics

### Lead Forecasting

Forecast future daily lead generation.

### Revenue Forecasting

Forecast expected future revenue.

---

## Forecasting Model

Model Used:

```text
Facebook Prophet
```

Features:

* Trend Detection
* Weekly Seasonality
* Changepoint Detection
* Confidence Intervals

---

## Forecast Outputs

Generated:

* Daily Forecast
* Weekly Trend Analysis
* Seasonal Components
* Future Performance Estimates

---

# Key Forecast Insights

### Lead Trend

The campaign demonstrates an overall positive growth trajectory.

Average lead volume increased significantly throughout the campaign period, indicating improved operational performance and market engagement.

### Weekly Seasonality

The strongest performance occurs during weekdays, particularly Thursdays.

Weekend performance is consistently lower.

### Operational Recommendation

Staffing and QA resources should be concentrated on peak weekday periods to maximize conversion opportunities and prevent operational bottlenecks.

---

# Phase 4 — Interactive Dashboard

An interactive Streamlit dashboard was developed to present business insights and forecasting results.

## Dashboard Features

### KPI Cards

* Total Leads
* Approved Sales
* Approval Rate
* Total Revenue
* Payments Received
* Payment Rate

### Interactive Filters

* Date Range
* Product
* State
* Team Leader

### Analysis Pages

* Executive Overview
* Sales Analysis
* QA Analysis
* Geographic Insights
* Forecasting Dashboard

---

# Technologies Used

## Data Processing

* Python
* Pandas
* NumPy

## Visualization

* Matplotlib
* Seaborn
* Plotly

## Forecasting

* Prophet
* Scikit-Learn

## Dashboard

* Streamlit

---

# Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/end-to-end-TimeSeries-forecasting

cd end-to-end-TimeSeries-forecasting
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Run the Notebook

```bash
jupyter notebook
```

Open:

```text
Understanding-Cleaning-EDA-CompaignData.ipynb
```

---

# Run the Dashboard

```bash
streamlit run app.py
```

Dashboard URL:

```text
http://localhost:8501
```
or can see it in publish:
```text
https://end-to-end-timeseries-forecasting-mfrk3kfsg3hd7pvi5hbkw9.streamlit.app/
```

---

# Main Business Takeaways

## 1. Sales Funnel Efficiency

The sales funnel reveals clear conversion opportunities that can significantly improve campaign revenue through targeted optimization.

---

## 2. Team Performance Differences

Performance varies substantially across team leaders and closers, highlighting opportunities for coaching and process standardization.

---

## 3. Forecasted Growth

Forecasting results indicate continued campaign growth, with strong weekday seasonality patterns that should guide staffing and operational planning.

---

# Author

Youssef Bassiony

Data Scientist | Business Analytics | Machine Learning
