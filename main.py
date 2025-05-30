from NSE import NSE_bhav_copy_download
from BSE import BSE_bhav_copy_download
from MCX import MCX_bhav_copy_download
from datetime import datetime, timedelta

def download_bhav_copy():
    
    input_date = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')

    print("\nDownloading NSE Bhav copy...")
    NSE_bhav_copy_download(input_date)
    
    print("\nDownloading BSE Bhav copy...")
    BSE_bhav_copy_download(input_date)
    
    print("\nDownloading MCX Bhav copy...\n")
    MCX_bhav_copy_download(input_date)

    print(":)")

if __name__ == "__main__":
    download_bhav_copy()