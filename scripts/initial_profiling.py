import pandas as pd

df = pd.read_csv("../data/raw_appeals_data.csv")

# This is the script performing initial profiling of raw appeals data
# It's role is to provide an overview of CSV structure, data types, missing values, and duplicate entries.
# Insights gained will help guide further data cleaning and analysis steps.

print ("--------------------------------------------------------------------")
print("INITIAL OBSERVATIONS")
print ("--------------------------------------------------------------------")

print("Shape:")
print(df.shape)
print("Info:")
df.info()

print("Columns in the DataFrame:")
print(df.columns)

print("Head of DataFrame:")
print(df.head())
print("Tail of DataFrame:")
print(df.tail())

print ("--------------------------------------------------------------------")
print ("DATA TYPES INFORMATION")
print ("--------------------------------------------------------------------")

print("Data types of DataFrame columns:")
print(df.dtypes)
print(f"Numeric columns statistics:")
print(df.select_dtypes(include=['number']).describe())

print ("--------------------------------------------------------------------")
print ("PER COLUMN MISSING/UNIQUE VALUES")
print ("--------------------------------------------------------------------")


print(f"Missing values per column (Max of {df.shape[0]} records):")
print(df.isna().sum().sort_values(ascending=False))
print("Unique values per column:")
print(df.nunique(dropna=False).sort_values(ascending=False))

print ("--------------------------------------------------------------------")
print ("UNIQUE AID/ID INFORMATION")
print ("--------------------------------------------------------------------")

print(f"Duplicate appeal AIDs ({df['aid'].duplicated().sum()}):")
print(df[df.duplicated(subset=['aid'], keep=False)])
print(f"Duplicate appeal IDs ({df['id'].duplicated().sum()}):")
print(df[df.duplicated(subset=['id'], keep=False)])

print ("--------------------------------------------------------------------")
print ("EVENT INFORMATION")
print ("--------------------------------------------------------------------")

print("Appeal records with no linked event:")
print(df["event_details.id"].isna().sum())

print("Distinct linked events:")
print(df["event_details.id"].nunique())

print("Appeal record count per event (top 10):")
print(df["event_details.id"].value_counts().head(10))

print ("--------------------------------------------------------------------")
print ("DUPLICATE RECORDS")
print ("--------------------------------------------------------------------")

print(f"Duplicate records ({df.duplicated().sum()})")
print(f"Remaining unique records ({df.drop_duplicates().shape[0]})")
print("Duplicate records:")

print("Duplicate full records:", df.duplicated().sum())
print("Duplicate AIDs:", df["aid"].duplicated().sum())
print("Duplicate IDs:", df["id"].duplicated().sum())

# Same duplicate rows for both AIDs and IDs?
aid_dupes = df["aid"].duplicated(keep=False)
id_dupes = df["id"].duplicated(keep=False)

print("Same duplicate rows:", aid_dupes.equals(id_dupes))

# Display duplicate IDs and AIDs side by side
print(
    df.loc[aid_dupes | id_dupes, ["id", "aid", "name"]]
    .sort_values(["id", "aid"])
    .to_string()
)

print ("--------------------------------------------------------------------")
print ("FINANCIAL AND BENEFICIARY INFORMATION")
print ("--------------------------------------------------------------------")
# Future analysis will be on financials and beneficiary information across appeal initiatives

financial_cols = [
    "amount_requested",
    "amount_funded",
    "num_beneficiaries"
]

print("Financial and beneficiary statistics:")
print(df[financial_cols].describe())

print("Missing critical values:")
print(df[financial_cols].isna().sum())

print("Negative financial values:")
print((df[["amount_requested", "amount_funded"]] < 0).sum())
