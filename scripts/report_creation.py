import pandas as pd

# Final stage of the processing pipeline for the IFRC appeals dataset
# This program outputs key performance and data integrity indicators into final_indicators and final_appeals_data CSV files, for analysis in Power BI and Excel

df = pd.read_csv("../data/cleaned_appeals_data.csv")

df['start_date'] = pd.to_datetime(df["start_date"], errors="coerce", utc=True)

# Filter to emergency appeals from Jan. 2022 - present
report_df = df[
    (df["atype"] == 1) & (df["start_date"] >= "2022-01-01") & (df["start_date"] < "2026-11-18")
].copy()

# Establish reqs for report eligibility flag
requested = pd.to_numeric(report_df["amount_requested"], errors="coerce")
funded = pd.to_numeric(report_df["amount_funded"], errors="coerce")

eligible = (requested.notna() & funded.notna() & (requested > 0) & (funded >=0))
report_df['eligible_for_analysis'] = eligible

# Derived analytical indicators for reporting
total_requested = requested.where(eligible).sum()
total_funded = funded.where(eligible).sum()
funding_percentage = (total_funded / total_requested * 100)
total_funding_gap_chf = (total_requested - total_funded)

appeals_below_50_pct = int((eligible & ((funded / requested) < 0.5)).sum())

report_summary = {
    'total_appeals': len(report_df),
    'eligible_for_analysis': int(eligible.sum()),
    "incomplete_or_ineligible_for_analysis": int((~eligible).sum()),
    'total_requested_chf': total_requested,
    'total_funded_chf': total_funded,
    'total_funding_gap_chf': total_funding_gap_chf,
    'funding_pct': funding_percentage,
    'appeals_below_50_pct': appeals_below_50_pct,
    "active_appeals": int((report_df["status"] == 0).sum()),
    "closed_appeals": int((report_df["status"] == 1).sum()),
    "frozen_appeals": int((report_df["status"] == 2).sum()),
    "archived_appeals": int((report_df["status"] == 3).sum()),
}

report_df.to_csv("../data/final_appeals_data.csv", index=False)

report_summary_df = pd.DataFrame(list(report_summary.items()), columns = ["indicator", "value"])
report_summary_df.to_csv("../data/final_indicators_report.csv", index=False)

print(report_summary_df.to_string(index=False, float_format= lambda x: f"{x:,.2f}"))