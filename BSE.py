import requests
import os
import concurrent.futures

def download_file(session, url, filename, headers):
    """Download a single file and save it to disk"""
    response = session.get(url, headers=headers, allow_redirects=True)
    
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return f"Successfully downloaded to {filename}"
    else:
        return f"Failed to download {filename}, status code: {response.status_code}"

def BSE_bhav_copy_download(date_str):
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
    download_info = [
        {
            'url': f"https://www.bseindia.com/download/Bhavcopy/Derivative/MS_{date_str}-01.csv",
            'filename': f"BSE_FnO_BhavCopy_{date_str}.csv",
            'type': 'F&O'
        },
        {
            'url': f"https://www.bseindia.com/download/BhavCopy/Equity/BhavCopy_BSE_CM_0_0_0_{date_str}_F_0000.CSV",
            'filename': f"BSE_Equity_BhavCopy_{date_str}.csv",
            'type': 'Equity'
        }
    ]
    
    results = []
    
    # Download files in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(download_file, session, info['url'], info['filename'], headers)
            for info in download_info
        ]
        
        for future, info in zip(concurrent.futures.as_completed(futures), download_info):
            try:
                result = future.result()
                print(result)
                results.append(result)
            except Exception as e:
                print(f"Error downloading {info['type']} bhav copy: {str(e)}")
                results.append(f"Failed to download {info['type']} bhav copy: {str(e)}")
    
    return "BSE bhav copy download process completed."

if __name__ == "__main__":
    # Use the date from your example
    date = "20250502"
    BSE_bhav_copy_download(date)