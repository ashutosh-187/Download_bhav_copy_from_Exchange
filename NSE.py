from datetime import datetime
from model import connect_with_database
import requests
import pandas as pd
import zipfile
import io

def download_and_parse(url, headers, session):
    resp = session.get(url, headers=headers)
    resp.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
        # find the one .csv in the archive
        name = next(f for f in z.namelist() if f.endswith('.csv'))
        # read it directly into pandas
        with z.open(name) as csvfile:
            # if it’s bytes, pandas.read_csv can consume it directly
            return pd.read_csv(csvfile)
    # in case something goes wrong
    raise RuntimeError(f"No CSV found in {url}")

def NSE_bhav_copy_download(date):
    collection = connect_with_database()

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Upgrade-Insecure-Requests': "1",
        "DNT": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }

    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers)

    # Ensure date is in YYYYMMDD
    input_date = datetime.strptime(date, "%Y%m%d")
    formatted_date = input_date.strftime("%Y%m%d")

    download_urls = {
        "FnO":  (
            f"https://nsearchives.nseindia.com/content/fo/"
            f"BhavCopy_NSE_FO_0_0_0_{formatted_date}_F_0000.csv.zip"
        ),
        "Equity": (
            f"https://nsearchives.nseindia.com/content/cm/"
            f"BhavCopy_NSE_CM_0_0_0_{formatted_date}_F_0000.csv.zip"
        )
    }

    for segment, url in download_urls.items():
        downloaded_bhav_copy = download_and_parse(url, headers, session)
        collection.insert_many(downloaded_bhav_copy.to_dict(orient="records"))

    return ":)"

if __name__ == "__main__":
    NSE_bhav_copy = NSE_bhav_copy_download("20250505")
    # print(NSE_bhav_copy)
