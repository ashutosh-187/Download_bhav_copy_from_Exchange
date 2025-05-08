import requests
import pandas as pd
from datetime import datetime
import zipfile
import io
import os

def NSE_bhav_copy_download(date):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
        'Upgrade-Insecure-Requests': "1",
        "DNT": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }

    # Initialize session
    session = requests.Session()
    session.get("http://nseindia.com", headers=headers)
    
    # Format date properly
    input_date = datetime.strptime(date, "%Y%m%d")
    formatted_date = input_date.strftime("%Y%m%d")
    
    root_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Download and extract FnO data
    fno_url = f"https://nsearchives.nseindia.com/content/fo/BhavCopy_NSE_FO_0_0_0_{date}_F_0000.csv.zip"
    print(f"Downloading FnO data from: {fno_url}")
    
    fno_response = requests.get(fno_url, headers=headers)
    
    # Extract CSV from zip data in memory (no zip file saved)
    with zipfile.ZipFile(io.BytesIO(fno_response.content)) as zip_ref:
        for file_info in zip_ref.infolist():
            if file_info.filename.endswith('.csv'):
                # Extract the CSV content
                csv_content = zip_ref.read(file_info.filename)
                
                # Save only the CSV file
                csv_path = os.path.join(root_directory, f"NSE_FnO_BhavCopy_{formatted_date}.csv")
                with open(csv_path, 'wb') as f:
                    f.write(csv_content)
                print(f"Saved FnO CSV file to: {csv_path}")
    
    # Download and extract Equity data
    equity_url = f"https://nsearchives.nseindia.com/content/cm/BhavCopy_NSE_CM_0_0_0_{date}_F_0000.csv.zip"
    print(f"Downloading Equity data from: {equity_url}")
    
    equity_response = requests.get(equity_url, headers=headers)
    
    # Extract CSV from zip data in memory (no zip file saved)
    with zipfile.ZipFile(io.BytesIO(equity_response.content)) as zip_ref:
        for file_info in zip_ref.infolist():
            if file_info.filename.endswith('.csv'):
                # Extract the CSV content
                csv_content = zip_ref.read(file_info.filename)
                
                # Save only the CSV file
                csv_path = os.path.join(root_directory, f"NSE_Equity_BhavCopy_{formatted_date}.csv")
                with open(csv_path, 'wb') as f:
                    f.write(csv_content)
                print(f"Saved Equity CSV file to: {csv_path}")
    
    print("Successfully downloaded and extracted NSE bhav copy data")
    return "Successfully downloaded and extracted NSE bhav copy data."

if __name__ == "__main__":
    NSE_bhav_copy_download("20250505")