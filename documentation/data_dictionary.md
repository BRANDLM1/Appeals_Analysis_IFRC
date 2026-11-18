# Data Dictionary

Definitions for the fields retained from the [IFRC GO Appeals API](https://goadmin.ifrc.org/api/v2/appeal/) and the indicators calculated in the reporting script. Source definitions can also be checked against the [IFRC GO Wiki](https://go-wiki.ifrc.org/en/go-api/data_dictionary_appeal).

## Selected fields

These are the 19 fields retained in `cleaned_appeals_data.csv`. Nested API properties appear as flattened column names in the CSV.

| Column | Format | Description |
| --- | --- | --- |
| `id` | Integer | IFRC GO appeal record ID; used for tracking and validation warnings |
| `aid` | Text | Appeal identifier from the source system; treated as an identifier, not a number for analysis |
| `code` | Text | Appeal reference code |
| `name` | Text | Name of the appeal |
| `atype` | Integer code | Appeal type; `1` identifies Emergency Appeals |
| `atype_display` | Text | Readable appeal type, such as Emergency Appeal |
| `status` | Integer code | Appeal status |
| `status_display` | Text | Readable appeal status, such as Active or Closed |
| `sector` | Text | IFRC office or country cluster submitting the appeal, **not** an assistance sector |
| `num_beneficiaries` | Numeric | Beneficiary estimate; not necessarily the number of people actually reached |
| `amount_requested` | Numeric, CHF | Funding requested for the appeal |
| `amount_funded` | Numeric, CHF | Funding recorded against the appeal; can be missing |
| `start_date` | Date/time (UTC) | Appeal start date; used to select the reporting period |
| `end_date` | Date/time (UTC) | Appeal end date, where available |
| `dtype.id` | Integer code | Identifier for the linked disaster type |
| `dtype.name` | Text | Disaster type, such as Flood, Earthquake, or Epidemic |
| `country.name` | Text | Country or geographic entity associated with the appeal/submitting cluster |
| `country.record_type_display` | Text | Type of geographic record, such as Country or Region |

### Appeal categories and statuses

| `atype` | `atype_display` | `status` | `status_display` |
| --- | --- | --- | --- |
| 0 | DREF | 0 | Active |
| 1 | Emergency Appeal | 1 | Closed |
| 2 | International Appeal | 2 | Frozen |
| 3 | Forecast Based Action | 3 | Archived |

These are two **separate** sets of codes; columns in the same table row are not linked to each other.

## Derived reporting fields and indicators

| Name | Level | Meaning or calculation |
| --- | --- | --- |
| `eligible_for_analysis` | Appeal record | True when requested is present and > 0, and funded is present and >= 0 |
| `total_appeals` | Summary | Number of selected Emergency Appeals |
| `eligible_for_analysis` (summary) | Summary | Number of financially eligible appeals |
| `incomplete_or_ineligible_for_analysis` | Summary | Selected appeals not meeting the financial eligibility rule |
| `total_requested_chf` | Summary, CHF | Sum of eligible requested amounts |
| `total_funded_chf` | Summary, CHF | Sum of eligible funded amounts |
| `total_funding_gap_chf` | Summary, CHF | Requested total minus funded total; **net** financing difference |
| `funding_pct` | Summary, % | Funded total divided by requested total, multiplied by 100 |
| `appeals_below_50_pct` | Summary, count | Number of eligible appeals with funding below half of the requested amount; despite the name, this is a **count**, not a percentage |
| `active_appeals`, `closed_appeals`, `frozen_appeals`, `archived_appeals` | Summary, counts | Number of in-scope appeals in each status |

The financial summary uses only eligible appeals, but `total_appeals` includes all in-scope records. Funding coverage should be calculated from the aggregated funded and requested amounts, not the average of individual appeal ratios.

## Validation report fields

The `post_clean_validation_report.csv` file contains:

| Column | Description |
| --- | --- |
| `warning` | Name of a data-quality check or flagged condition |
| `count` | Number of records or references flagged for that condition |
| `appeal_ids` | List of associated appeal IDs, saved as JSON text; a row index can be used when an ID is missing |

The validation report covers the cleaned source records as a whole, not only the final Emergency Appeal selection. Warning categories may overlap.

## Interpretation notes

- Financial figures are in CHF and reflect values available in the extracted data, not necessarily funding received during the appeal start-date range.
- Missing funded amounts are not treated as confirmed zero funding. A zero requested amount cannot be used as a denominator for funding coverage.
- A beneficiary estimate does not establish humanitarian impact or people actually served.
- Region and country-related fields describe IFRC reporting/geographic references, not population demographics or precise locations of all aid recipients.
- Definitions can be extended as additional IFRC datasets are incorporated into the project.