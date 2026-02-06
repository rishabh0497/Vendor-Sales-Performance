# Vendor Sales Performance (ETL + Power BI)

This project is an end-to-end vendor performance analytics solution built using Python, SQLite, and Power BI.  
It automates data ingestion, transformation, metric generation, and visual analysis using a real wholesale vendor dataset from Kaggle.

---

## 📊 Project Summary

The goal of this project is to provide insights into vendor and brand performance, profitability, inventory efficiency, and contribution patterns across a large sales and purchasing dataset.

It includes:

- Data ingestion and transformation scripts
- Exploratory Data Analysis
- Final analytical dataset
- Interactive Power BI dashboard
- Key insights and performance metrics

---

## 📌 Data Source

This project uses the Kaggle dataset:

👉 https://www.kaggle.com/datasets/vivekkumarkamat/vendor-performance-analysis

Due to size constraints (~2GB of raw CSVs), the raw files are **not included** in this repository.  
Instead, this repo includes the processed analytical dataset (`vendor_sales_summary.csv`) and all scripts needed to reproduce the full pipeline if you download the raw data.

---

## 🚀 Project Workflow

The project follows this sequence:

### 1) **Data Ingestion**
Script: `src/ingestion_db.py`

- Reads all CSV files from a local `Data/` folder
- Creates a SQLite database (`vendor_performance.db`)
- Saves each table into the database
- Keeps logs of table loads and timings

### 2) **Build Vendor Summary**
Script: `src/get_vendor_summary.py`

- Reads tables from the database
- Performs SQL joins: purchases, sales, purchase prices, vendor invoices
- Calculates business metrics like:
  - Gross Profit
  - Profit Margin
  - Stock Turnover
  - Unsold capital
- Saves the result back into the database as `vendor_sales_summary`

### 3) **Exploratory Data Analysis**
Notebook: `notebooks/Exploratory Data Analysis.ipynb`

- EDA of raw tables
- Distribution and missing value checks
- Patterns in vendor, brand, and sales data
- Helps decide which metrics to build

### 4) **Final Analysis and Export**
Notebook: `notebooks/Analysis.ipynb`

- Loads the vendor summary table
- Performs sanity checks and validations
- Explores trends and metrics
- Exports `vendor_sales_summary.csv`

### 5) **Power BI Dashboard**
File: `powerbi/Vendor Sales Performance.pbix`

- Loads `vendor_sales_summary.csv`
- Visualizes KPIs, trends and comparisons in an interactive layout

---

## 💻 How To Run This Project

### 1) Install dependencies

Make sure you have Python installed, then run:

```bash
pip install -r requirements.txt
```

---

### 2) Download Raw Data

Download the raw CSV files from Kaggle:

🔗 https://www.kaggle.com/datasets/vivekkumarkamat/vendor-performance-analysis

Extract all CSVs into a folder named:

```
Data/
```

So you should have:

```
Data/
  purchases.csv
  sales.csv
  vendor_invoice.csv
  purchase_prices.csv
  ...
```

---

### 3) Run the ETL Pipelines

```bash
python src/ingestion_db.py
python src/get_vendor_summary.py
```

This will build `vendor_performance.db` with all necessary tables.

---

### 4) View Notebooks (optional)

Open the notebooks in Jupyter:

- `Exploratory Data Analysis.ipynb`
- `Analysis.ipynb`

These explain the data, checks, and transformations in more detail.

---

### 5) Open the Power BI Dashboard

Open:

```
powerbi/Vendor Sales Performance.pbix
```

in Power BI Desktop to explore the interactive dashboard.

---

## 📊 Key Dashboard Features

The Power BI dashboard provides:

### 📈 High-level KPIs
- Total Sales  
- Total Purchases  
- Gross Profit  
- Profit Margin %  
- Unsold Capital  

### 🔝 Top Performers
- Top vendors by sales  
- Top brands by sales  

### 📊 Contribution Analysis
- Purchase contribution % of top vendors  
- Share of total procurement  

### 📉 Low Performing Segments
- Low-performing vendors  
- Low-performing brands  
- Scatter view: sales vs profit margin  

---

## 🔎 Key Insights from Analysis

Some of the main patterns and findings:

- **Vendor concentration:** Top 10 vendors contribute about **65.7%** of total purchases.
- **Profit variation:** Profit margins vary widely, and some items show **negative gross profit**, indicating potential loss lines.
- **Inventory issues:** Some products have purchase history but no sales, pointing to **slow or obsolete stock**.
- **Strong purchase–sales link:** Purchase quantity and sales quantity show **very strong correlation (~0.999)**.
- **Freight cost variance:** Freight costs differ notably across items and vendors, highlighting logistics differences.
