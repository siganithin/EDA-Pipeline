📊 EDA-Pipeline

An end-to-end ETL + EDA pipeline built on the Telco Customer Churn dataset.
It includes data extraction, cleaning, feature engineering, Supabase loading, validation, and exploratory analysis.

🚀 What This Project Does
This project has two parts:

1️⃣ ETL Pipeline (Automated Scripts)
Extract raw Telco churn CSV
Transform
fix data types
fill missing values
engineer new features
drop unwanted columns
Load cleaned data into Supabase (cloud database)
Validate final data quality
row counts
missing values
feature segments
contract codes
Supabase match

2️⃣ EDA Notebook (Data Analysis)
A separate Jupyter/Colab notebook that explores churn patterns:
churn distribution
tenure & charges behavior
contract type impact
internet service patterns
customer segments

📘 Dataset Summary
The Telco Customer Churn dataset contains 7,043 telecom customers with:
demographics
services subscribed
billing details
contract type
churn status
Used widely for customer retention, churn prediction, and behavior analysis.

EDA-Pipeline/
│
├── data/
│   ├── raw/          # raw telco_raw.csv
│   └── staged/       # cleaned telco_transformed.csv
│
├── scripts/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── validate.py
│
└── etl_analysis_tele.ipynb   # EDA Notebook

🛠 Technologies Used
Python
Pandas / NumPy
Supabase
dotenv
Matplotlib / Seaborn (EDA)

🎯 Purpose
This project demonstrates:
ETL pipeline building
Data cleaning & feature engineering
Database loading
Validation logic
Churn analysis & visualization
Perfect for portfolio and learning.
