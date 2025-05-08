from NSE import NSE_bhav_copy_download
from BSE import BSE_bhav_copy_download
from MCX import MCX_bhav_copy_download

def download_bhv_copy():
    input_day = input("Enter day: ")
    input_month = input("Enter month: ")
    input_year = input("Enter year: ")

    input_date = f"{input_year}{input_month}{input_day}"

    print("\nDownloading NSE Bhav copy...")
    NSE_bhav_copy_download(input_date)
    
    print("\nDownloading BSE Bhav copy...")
    BSE_bhav_copy_download(input_date)
    
    print("\nDownloading MCX Bhav copy...\n")
    MCX_bhav_copy_download(input_date)

    print(":)")

if __name__ == "__main__":
    download_bhv_copy()