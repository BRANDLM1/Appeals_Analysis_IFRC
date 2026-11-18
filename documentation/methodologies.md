# Reporting Methodology

This document explains how I prepared the IFRC GO Appeals data and calculated the figures used in Excel and Power BI.

## Data source and extraction

- **Source:** [IFRC GO Appeals API](https://goadmin.ifrc.org/api/v2/appeal/)
- **Field reference:** [IFRC GO Appeal Data Dictionary](https://go-wiki.ifrc.org/en/go-api/data_dictionary_appeal)
- **Extraction timestamp:** November 13, 2026 at approximately 5:20 PM EST
- **Working export:** `data/raw_appeals_data.csv`

`json_to_csv.py` requests API pages, collects each page's records, and flattens the JSON fields into a CSV. During testing, downloads without explicit ordering repeated some appeal IDs across page boundaries. Using larger pages and requesting `ordering=id` eliminated the duplicates observed in a later export. I checked record counts and duplicate IDs before continuing.

## Reporting scope

- **Appeal type:** Emergency Appeal (`atype = 1`).
- **Start dates:** January 1, 2022 through November 17, 2026, inclusive (`start_date >= 2022-01-01` and `start_date < 2026-11-18`).
- **Status:** No status restriction in the overall reporting selection.
- **Geography:** All represented IFRC regions, with no additional regional restriction.

This selects appeals **started** during the period. Funding values reflect the API's state at the extraction date; the figures do not represent funding transactions made specifically between 2022 and 2026.

## Assessment, cleaning, and validation

1. `initial_profiling.py` reviews column types, sample records, missing values, duplicates, and numerical distributions.
2. `validate.py` checks the raw CSV for issues that may affect later analysis.
3. `clean.py` selects 19 fields, converts dates to UTC, converts numeric columns, and trims text values. It also flags records for post-clean validation.
4. Post_clean validation checks within `clean.py` write to `post_clean_validation_report.csv`, with each warning, count, and a list of affected appeal IDs.

Checks include missing or duplicate identifiers, failed conversions, unexpected appeal type or status codes, dates out of order, negative amounts, zero requested amounts, and cases where funded amounts exceed requested amounts. Not every warning is an error. For example, funding can be missing, and funding exceeding the requested amount may be legitimate.

The post-clean validation report applies to **all cleaned appeals**, not just the final 2022–present Emergency Appeal subset. A single appeal can have multiple warnings, so summing warning counts does not give the number of distinct affected appeals.

## Financial indicators

`report_creation.py` applies the reporting scope and checks which appeals are eligible for comparable financial calculations.

An appeal is `eligible_for_analysis` when its requested amount is present and greater than zero, and its funded amount is present and at least zero. Missing funding is not assumed to equal zero. Appeals failing the rule remain counted in the report but are excluded from financial totals.

| Indicator | Calculation |
| --- | --- |
| `total_appeals` | Number of appeals in scope |
| `eligible_for_analysis` | Count meeting the financial eligibility rule |
| `incomplete_or_ineligible_for_analysis` | In-scope appeals minus eligible appeals |
| `total_requested_chf` | Sum of requested amounts for eligible appeals |
| `total_funded_chf` | Sum of funded amounts for eligible appeals |
| `total_funding_gap_chf` | Requested total minus funded total (**net gap**) |
| `funding_pct` | Funded total ÷ requested total × 100 |
| `appeals_below_50_pct` | Count of eligible appeals whose individual funded/requested ratio is below 50% |
| Status counts | Number of appeals by Active, Closed, Frozen, or Archived status |

The overall funding percentage is calculated from **total amounts**, not by averaging individual appeal percentages. The net funding gap can differ from a sum of individual positive shortfalls when some appeals are overfunded.

## Current results and verification

For the selected 2022–present Emergency Appeals:

| Result | Value |
| --- | ---: |
| Appeals | 92 |
| Eligible for financial analysis | 87 |
| Incomplete or ineligible | 5 |
| Requested funding | CHF 2,785,900,000 |
| Funded amount | CHF 1,305,330,484 |
| Net funding gap | CHF 1,480,569,515 |
| Funding coverage | 46.85% |

`final_appeals_data.csv` holds the appeal-level records for investigation. `final_indicators_report.csv` holds the aggregate results. I compared the unfiltered Excel PivotTable and Power BI measures with the Python summary, using the same eligibility rule, and the results matched.

## Limits of the analysis

The findings describe the financing status of appeals, not how funds were spent or what was achieved. The data alone cannot establish the distribution of aid, the number of people actually reached, or improvements in humanitarian conditions. Disaster type and IFRC region provide useful breakdowns, but they do not account for all differences in operational needs or circumstances.

`sector` refers to the submitting IFRC office or cluster, not a humanitarian program sector. Geographic labels should not automatically be treated as the locations of all beneficiaries. The available `num_beneficiaries` field is not evidence of people actually reached.

This first version focuses on appeal financing. Future work may incorporate other IFRC operational datasets to examine program activities, allocation of resources, and outcome indicators where the source definitions allow valid comparisons.

The project is an independent analysis using public IFRC data, not an official IFRC or ICRC report.
