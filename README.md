📊 EDA-Pipeline

An end-to-end ETL + EDA pipeline built on the Telco Customer Churn dataset.
This project performs data extraction, cleaning, feature engineering, database loading, validation, and exploratory analysis.

🚀 What This Project Does

This project has two main components:

1️⃣ ETL Pipeline (Automated Scripts)
✔ Extract

Load the raw Telco churn CSV

Save it into a structured data/raw/ directory

✔ Transform

Fix data types (TotalCharges → numeric)

Fill missing values

Engineer new features

Drop unwanted columns

✔ Load

Insert cleaned data into Supabase (PostgreSQL backend)

Use batch upsert for reliable loading

✔ Validate

Checks data quality:

Row counts

Missing values

Feature-engineered segments

Contract codes

Supabase row match

2️⃣ EDA Notebook (Data Analysis)

A separate Jupyter/Colab notebook that analyzes churn patterns such as:

Churn distribution

Tenure & charges trends

Contract type impact

Internet service patterns

Customer segmentation

📘 Dataset Summary

The Telco Customer Churn dataset contains 7,043 telecom customers, including:

Demographic details

Services subscribed

Monthly & total charges

Contract types

Churn status

This dataset is widely used for churn prediction, retention analysis, and customer behavior studies.

📁 Folder Structure 
EDA-Pipeline/
│
├── data/
│   ├── raw/                 # raw telco_raw.csv
│   └── staged/              # cleaned telco_transformed.csv
│
├── scripts/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── validate.py
│
└── etl_analysis_tele.ipynb  # EDA Notebook

🛠 Technologies Used

Python

Pandas / NumPy

Supabase

dotenv

Matplotlib / Seaborn (for EDA)

🎯 Purpose

This project demonstrates:

ETL pipeline development

Data cleaning & preprocessing

Feature engineering

Cloud database loading

Data validation

Exploratory data analysis

Ideal for learning, portfolios, and demonstrating full data engineering + analytics workflow.
