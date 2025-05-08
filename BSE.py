from datetime import datetime
from model import connect_with_database
import requests
import pandas as pd
import io

def download_and_parse(url, headers, session):
    resp = session.get(url, headers=headers)
    resp.raise_for_status()
    csv_data = io.StringIO(resp.text)
    output = pd.read_csv(csv_data)
    return output

def BSE_bhav_copy_download(date):
    collection = connect_with_database()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Referer': 'https://www.bseindia.com/markets/equity/EQReports/BhavCopyDebt.aspx'
    }

    session = requests.Session()
    
    # Initialize session with BSE domain - combine into one request
    session.get("https://www.bseindia.com/markets/equity/EQReports/BhavCopyDebt.aspx", headers=headers)
    
    # Define download information
    download_urls = [
        {
            'url': f"https://www.bseindia.com/download/Bhavcopy/Derivative/MS_{date}-01.csv",
            'filename': f"BSE_FnO_BhavCopy_{date}.csv",
            'type': 'F&O'
        },
        {
            'url': f"https://www.bseindia.com/download/BhavCopy/Equity/BhavCopy_BSE_CM_0_0_0_{date}_F_0000.CSV",
            'filename': f"BSE_Equity_BhavCopy_{date}.csv",
            'type': 'Equity'
        }
    ]

    for url in download_urls:
        downloaded_bhav_copy = download_and_parse(url.get("url"), headers, session)
        collection.insert_many(downloaded_bhav_copy.to_dict(orient="records"))
        
    return ":)"

if __name__ == "__main__":
    NSE_bhav_copy = BSE_bhav_copy_download("20250505")
    # print(NSE_bhav_copy)
