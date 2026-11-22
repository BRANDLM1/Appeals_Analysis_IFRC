# IFRC Appeals Analysis Repository
##### Contributors: Miles Brandl

## Project Overview
The purpose of the IFRC Appeals Analysis Tool is to assist with the extracting, processing, and analysis of appeal data for operations of the International Federation of Red Cross (IFRC), leveraging Python, Excel, Power BI, and IFRC GO's Appeals API.

## Project Objectives

* Extract appeals data to CSV from IFRC Appeals API
* Validate and clean appeal records CSV
* Formulate key indicators from polished CSV 
* Justify key indicators against established report questions and methodologies. 
* Pull relevant data fields and indicators into Excel and Power BI Dashboard
* Formulate Power BI Dash for high level observation, filtering results by disaster type, country, region, etc...

 Ultimately gain familiarity with Red Cross data extraction workflows, IFRC GO Wiki structure, and general Red Cross operations analysis.

## Questions for Reporting
1. Where are the largest gaps in IFRC funding?
2. Are there patterns in funding across different types of operations?
3. How reliable is IFRC GO appeal data?

## Tools & Technologies
#### Data Processing and Validation

Python (pandas) for profiling, cleaning, validation, and indicator calculations.

#### Analysis and Reporting

Excel Online for PivotTables and cross-checking totals. Power BI Desktop for interactive reporting, regional comparisons, and disaster-type filters.

## Data Sources

This project uses public appeal records from the [IFRC GO Appeals API](https://goadmin.ifrc.org/api/v2/appeal/). The [IFRC GO Wiki](https://go-wiki.ifrc.org/en/go-api/data_dictionary_appeal) provides definitions for the fields used in the analysis.

The source includes appeal types, dates, statuses, disaster categories, requested and funded amounts (CHF), beneficiary estimates, and geographic references. Python retrieves the API records and converts them to a working CSV.

The current reporting scope is **Emergency Appeals beginning January 1, 2022 through November 17, 2026**. Funding amounts are the values available when the data was extracted, not necessarily money received during that date range.

See [methodologies.md](documentation/methodologies.md) for the selection and calculation rules, and [data_dictionary.md](documentation/data_dictionary.md) for field definitions.


## Project Structure

```text
Appeals_Analysis_IFRC/
├── README.md
├── data/
│   ├── raw_appeals_data.csv
│   ├── cleaned_appeals_data.csv
│   ├── post_clean_validation_report.csv
│   ├── final_appeals_data.csv
│   └── final_indicators_report.csv
├── documentation/
│   ├── methodologies.md
│   └── data_dictionary.md
└── scripts/
    ├── json_to_csv.py
    ├── initial_profiling.py
    ├── validate.py
    ├── clean.py
    └── report_creation.py
```

The Python programs save their output under `data/`. 
The final appeal-level CSV is used for Excel and Power BI, while the indicator report provides a separate reference for checking overall totals.

## Steps for Reproduction

1. Install Python and the required libraries: `pip install pandas requests`.
2. Run `json_to_csv.py` to retrieve the paginated GO Appeals API results and produce `raw_appeals_data.csv`.
3. Run `initial_profiling.py` and `validate.py` to inspect the records and check data quality.
4. Run `clean.py` to standardize selected columns and produce `cleaned_appeals_data.csv` and `post_clean_validation_report.csv`.
5. Run `report_creation.py` to filter the reporting scope, calculate the financial indicators, and export `final_appeals_data.csv` and `final_indicators_report.csv`.
6. In Excel, import `final_appeals_data.csv`, create a regional PivotTable for requested and funded amounts, and filter for `eligible_for_analysis = TRUE`. Compare totals with the indicator report.
7. In Power BI, load the same appeal-level CSV, calculate funding measures, and build the dashboard with regional comparisons and disaster-type filters. Check the unfiltered results against the Python and Excel totals.

The scripts currently use paths relative to the `scripts/` folder, so run them from that directory. GO data can change between downloads, and running the extraction again may produce different figures.

## Results and Visualizations

For the 2022–present Emergency Appeal selection, the three reporting tools produced matching results:

| Indicator                       |        Result |
| --------------------------------|---------------|
| Appeals analyzed                |            92 |
| Eligible for financial analysis |            87 |
| Incomplete or ineligible        |             5 |
| Total requested (CHF)           | 2,785,900,000 |
| Total funded (CHF)              | 1,305,330,484 |
| Net funding gap (CHF)           | 1,480,569,515 |
| Funding coverage                |        46.85% |

### Excel analysis

The Excel worksheet uses a PivotTable and slicers to compare requested and funded amounts by IFRC region, appeal start year, and status, to check the totals against Python. A second pivot table allows for granular filtering of specific appeal records based on region, disaster, amd status.

[Excel regional funding analysis with slicers](documentation/excel_analysis_v2.png)
[Excel appeal record lookup by filters](documentation/excel_analysis_v2p2.png)

### Power BI dashboard

The Power BI dashboard summarizes requested and funded amounts, funding coverage, and the net funding gap. Regional comparisons via clustered column chart display requested vs funded financial sums. Disaster-type filters allow further investigation of the same records.

New version capable of slicing by region, country, and disaster type. Additionally investigate countries ranked by appeal count and a world map of appeals. Adaptive key takeaways cater to granular selections.

[Power BI appeal funding dashboard](documentation/bi_dashboard_v2.png)

## Limitations and Future Work

This report shows **funding progress across emergency appeals**, with comparisons by disaster type and IFRC region. It does not show how the funding was allocated, what assistance was delivered, or the humanitarian impact of an operation. Funding coverage alone also cannot explain differences in need, operating conditions, or appeal performance.

The reporting period is based on appeal start dates, while financial amounts reflect the data available at extraction. Some records have incomplete financial information and are excluded from comparable funding calculations; those exclusions are counted in the results.

I plan to expand the Excel and Power BI analysis and explore other IFRC operational datasets to add context on program activities, resource allocation, and outcomes where those data are available and comparable.

This is an independent analysis using IFRC public data, not an official IFRC or ICRC report.
