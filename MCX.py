import requests
import os
from bs4 import BeautifulSoup
import re
import json
import csv

def fetch_vbc(html_response):
    soup = BeautifulSoup(html_response, 'html.parser')
    # Find the first <script> that mentions "vBC"
    script = soup.find('script', string=re.compile(r'vBC'))
    if not script:
        raise RuntimeError('script tag with vBC variable not found')

    # Extract the JS object literal
    m = re.search(r'vBC\s*=\s*([\s\S]*?);', script.string)
    if not m:
        raise RuntimeError('vBC assignment not found')

    return m.group(1)


def MCX_bhav_copy_download(date):
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json; charset=UTF-8",
        "Origin": "https://www.mcxindia.com",
        "Referer": "https://www.mcxindia.com/market-data/bhavcopy",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
        ),
        "X-Requested-With": "XMLHttpRequest"
    }

    # Start a session to capture cookies
    session = requests.Session()
    session.get("https://www.mcxindia.com", headers=headers)

    payload = {
        "Date": date,
        "InstrumentName": "ALL"
    }

    # Fetch the bhav copy script
    response = session.post(
        "https://www.mcxindia.com/market-data/bhavcopy",
        headers=headers,
        json=payload
    )
    response.raise_for_status()

    # Extract the JS literal string
    bhav_copy_str = fetch_vbc(response.text)

    # Attempt to parse directly as JSON
    try:
        data = json.loads(bhav_copy_str)
    except json.JSONDecodeError:
        # Fallback: replace single quotes with double quotes
        bhav_copy_clean = bhav_copy_str.replace("'", '"')
        data = json.loads(bhav_copy_clean)

    # Define output filename
    filename = f"BhavCopy_MCX_FO_{date}.csv"

    # Write to CSV
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        if not data:
            raise RuntimeError('No data to write to CSV')
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print(f"Successfully saved Bhav Copy to {filename}")
    return filename


if __name__ == "__main__":
    # Example usage: download for May 5, 2025
    MCX_bhav_copy_download("20250505")
