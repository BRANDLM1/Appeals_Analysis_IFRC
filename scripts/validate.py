import json

import pandas as pd

# This program may be used to validate working CSV data along early stages of the data pipeline, prior to further processing and analysis. 
# The goal is to ensure that the data meets the expected quality standards and is suitable for use in subsequent steps of the pipeline.

# Generates validation report to document results and any data integrity issues
# Data checks here include...
# Missing values
# Duplicate values
# Invalid formats and values

csv = "../data/raw_appeals_data.csv"

df = pd.read_csv(csv)

requested = pd.to_numeric(df["amount_requested"], errors="coerce")
funded = pd.to_numeric(df["amount_funded"], errors="coerce")
start_dates = pd.to_datetime(df["start_date"], errors="coerce", utc=True)
end_dates = pd.to_datetime(df["end_date"], errors="coerce", utc=True)

quality_report = {

    "Total Records": len(df),
    "Duplicate Records": df.duplicated().sum(),

    "Start dates missing": df["start_date"].isna().sum(),
    "Start dates invalid": (df["start_date"].notna() & start_dates.isna()).sum(),
    
    "End dates missing": end_dates.isna().sum(),
    "End dates invalid": (df["end_date"].notna() & end_dates.isna()).sum(),
    "Start dates after end dates": ((start_dates > end_dates) & start_dates.notna() & end_dates.notna()).sum(),
    
    "Duplicate IDs": df["id"].dropna().duplicated().sum(),
    "Duplicate AIDs": df["aid"].dropna().duplicated().sum(),

    "Missing IDs": df["id"].isna().sum(),
    "Missing AIDs": df["aid"].isna().sum(),
    
    "Invalid IDs": (df["id"].notna() & df["id"].apply(lambda x: not str(x).isdigit())).sum(),
    "Invalid AIDs": (df["aid"].notna() & df["aid"].apply(lambda x: not str(x).isdigit())).sum(),

    "Missing Amount Requested": df["amount_requested"].isna().sum(),
    "Missing Amount Funded": df["amount_funded"].isna().sum(),

    "Invalid Amount Requested": (df["amount_requested"].notna() & requested.isna()).sum(),
    "Invalid Amount Funded": (df["amount_funded"].notna() & funded.isna()).sum(),

    "Amount Requested is 0": ((requested == 0)).sum(),
    "Amount Funded is 0": ((funded == 0)).sum(),

    "Amount Requested is missing": df["amount_requested"].isna().sum(),
    "Amount Funded is missing": df["amount_funded"].isna().sum(),
    
    "Negative Requested Amounts": (requested < 0).sum(),
    "Negative Funded Amounts": (funded < 0).sum(),
    "Funding Exceeds Requested": (funded > requested).sum()
}

print(pd.Series(quality_report))

with open("../data/validation_report.txt", "w") as f:
    json.dump(quality_report, f, indent=4)