import json

import pandas as pd

# Clean and transform IFRC GO appeals data by selecting relevant fields, standardizing data types, and normalizing text values
# Preserve records with missing or anomalous values for investigation
# Generates a post-clean validation report containing warning categories and affected appeal ids

df = pd.read_csv("../data/raw_appeals_data.csv")

#Select relevant columns to proceed with analysis
selected_columns = [
    "id", "aid", "code", "name",
    "atype", "atype_display",
    "status", "status_display",
    "sector", "num_beneficiaries",
    "amount_requested", "amount_funded",
    "start_date", "end_date",
    "dtype.id", "dtype.name",
    "country.name", "country.record_type_display",
    "region.region_name",
]

missing_columns = [
    col for col in selected_columns if col not in df.columns
]
if missing_columns:
    raise ValueError(f"Missing expected columns: {missing_columns}")

cleaned_df = df[selected_columns].copy()
# Preserve original values to distinguish invalid formats
# from values that were already missing.
original_df = cleaned_df.copy()

# Convert dates to datetime format
for col in ["start_date", "end_date"]:
    cleaned_df[col] = pd.to_datetime(cleaned_df[col], errors="coerce", utc=True)

numeric_columns = ["id", "atype", "status", "dtype.id", "num_beneficiaries", "amount_requested", "amount_funded"]
categorical_columns = ["aid", "code", "name", "atype_display","status_display", "sector", "dtype.name",
                       "country.name", "country.record_type_display","region.region_name"]

# Numeric columns to proper numeric types
for col in numeric_columns:
    cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors="coerce")

# Standardize categorical fields
for col in categorical_columns:
    cleaned_df[col] = cleaned_df[col].astype("string").str.strip()
    cleaned_df.loc[cleaned_df[col] == "", col] = pd.NA

# -- Validation Stage --

warnings = {}

# Missing values for each column
for col in selected_columns:
    mask = cleaned_df[col].isna()
    warnings[f"missing_{col}"] = (cleaned_df.loc[mask, "id"].tolist())

# If ID is missing, use row index as reference
warnings["missing_id"] = (cleaned_df.index[cleaned_df["id"].isna()].tolist())

for col in ["start_date", "end_date"]:
    mask = (original_df[col].notna() & cleaned_df[col].isna())
    warnings[f"invalid_{col}"] = (cleaned_df.loc[mask, "id"].tolist())

# Invalid numeric fields
for col in numeric_columns:
    mask = (original_df[col].notna() & cleaned_df[col].isna())

    warnings[f"invalid_{col}"] = (
        cleaned_df.loc[mask, "id"].tolist()
    )

# Duplicate ids and aids
warnings["duplicate_id"] = cleaned_df.loc[
    cleaned_df["id"].notna()
    & cleaned_df["id"].duplicated(keep=False),
    "id"
].tolist()

warnings["duplicate_aid"] = cleaned_df.loc[
    cleaned_df["aid"].notna()
    & cleaned_df["aid"].duplicated(keep=False),
    "id"
].tolist()

# Unexpected categorical values
warnings["invalid_status_code"] = cleaned_df.loc[
    cleaned_df["status"].notna()
    & ~cleaned_df["status"].isin([0, 1, 2, 3]),
    "id"
].tolist()

warnings["invalid_atype_code"] = cleaned_df.loc[
    cleaned_df["atype"].notna()
    & ~cleaned_df["atype"].isin([0, 1, 2, 3]),
    "id"
].tolist()

warnings["end_before_start"] = cleaned_df.loc[
    cleaned_df["end_date"] < cleaned_df["start_date"],
    "id"
].tolist()

warnings["negative_amount_requested"] = cleaned_df.loc[
    cleaned_df["amount_requested"] < 0, "id"
].tolist()

warnings["negative_amount_funded"] = cleaned_df.loc[
    cleaned_df["amount_funded"] < 0, "id"
].tolist()

warnings["funding_exceeds_requested"] = cleaned_df.loc[
    cleaned_df["amount_funded"] > cleaned_df["amount_requested"],
    "id"
].tolist()

warnings["zero_amount_requested"] = cleaned_df.loc[
    cleaned_df["amount_requested"] == 0, "id"
].tolist()

warnings["negative_beneficiaries"] = cleaned_df.loc[
    cleaned_df["num_beneficiaries"] < 0, "id"
].tolist()


# Save cleaned data
cleaned_df.to_csv("../data/cleaned_appeals_data.csv", index=False)

# Save post-clean validation report
post_clean_validation_report = pd.DataFrame([
    {
        "warning": category,
        "count": len(ids),
        "appeal_ids": json.dumps([str(i) for i in ids])
    }
    for category, ids in warnings.items()])

post_clean_validation_report.to_csv("../data/post_clean_validation_report.csv", index=False)

print("Post-clean validation summary:")
print(post_clean_validation_report[["warning", "count"]].to_string(index=False))
# Sum of all warning occurrences across categories, may have reccuring appeal ids across categories
print("Total warning occurrences:", post_clean_validation_report["count"].sum())
print("Cleaned records:", len(cleaned_df))