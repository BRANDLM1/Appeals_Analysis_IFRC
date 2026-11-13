import requests
import pandas as pd

# This script is the initial and only direct link to official IFRC appeal reports, fetching publically available data from the IFRC appeals API
# It's role is to...
# 1. Fetch all appeal records from the API, accounting for pagination
# 2. Flatten fetched JSON to a tabular DataFrame,
# 3. Save everything to a CSV file for cleaning and validation before kpi selection and reports analysis

# This may be re-purposed for converting other IFRC GO API datasets to CSV by simply changing the URL and the output file name.
# Note for self and team: Future script enhancements may include batch processing and error handling for the capturing of multiple or exceptionally large datasets.

url = "https://goadmin.ifrc.org/api/v2/appeal/"
records = []
pages = 1
while url:
    try:
        print("Requesting:", url)

        response = requests.get(url, timeout= 10)
        response.raise_for_status()

        data = response.json()
        records.extend(data["results"])
        print(f"Fetched {len(data["results"])} records from page {pages}")

        url = data.get("next")
        if url:
            pages+=1
            print(f"Fetching page {pages}")

        
    #Error handling for the http request
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Other request error occurred: {err}")

print(f"Downloaded: {len(records)} records")

#Flattening JSON records to df, outputting to CSV
df = pd.json_normalize(records)
df.to_csv("data/raw_appeals_data.csv", index=False)
print("Records saved to data/raw_appeals_data.csv")
    