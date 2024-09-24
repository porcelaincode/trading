import os
import shutil
import requests
import logging
from datetime import datetime
from pathlib import Path
import zipfile
import pandas as pd

def todays_date():
    '''
    Returns todays date in format YYYY-MM-DD
    '''
    return datetime.date(datetime.now()).isoformat()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a file handler to store logs
handler = logging.FileHandler('instruments.log')
handler.setLevel(logging.INFO)

# Define the log format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Stream logs in console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Connection': 'keep-alive',
    'DNT': '1',  # Do Not Track request header
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://www.google.com/',
}

def download_kotak_files():
    local_dir = './temp/kotak/'
    os.makedirs(local_dir, exist_ok=True)
    
    response_eq = requests.get(f"https://lapi.kotaksecurities.com/wso2-scripmaster/v1/prod/{todays_date()}/transformed/nse_cm.csv", headers=headers)
    logger.info(f'Kotak EQ request returned with status code {response_eq.status_code}')
    with open('./data/kotak/nse_eq.csv', 'wb') as f:
            f.write(response_eq.content)

    response_fo = requests.get(f"https://lapi.kotaksecurities.com/wso2-scripmaster/v1/prod/{todays_date()}/transformed/nse_fo.csv", headers=headers)
    logger.info(f'Kotak FO request returned with status code {response_fo.status_code}')
    with open('./data/kotak/nse_fo.csv', 'wb') as f:
            f.write(response_fo.content)
    pass

def download_icici_files():
    local_dir = './temp/icici/'
    local_zip_file = f'{local_dir}SecurityMaster_{todays_date()}.zip'

    # Ensure the directory exists
    os.makedirs(local_dir, exist_ok=True)

    if Path(local_zip_file).is_file():
        logger.info('Loading instruments from downloaded scripts...')
        pass
    else:
        url = 'https://directlink.icicidirect.com/NewSecurityMaster/SecurityMaster.zip'
        response = requests.get(url)
        logger.info(f'ICICI Security Master request returned with status code {response.status_code}')
        with open(local_zip_file, 'wb') as f:
            f.write(response.content)
        with zipfile.ZipFile(local_zip_file, 'r') as zip_ref:
            zip_ref.extractall('./temp/icici')
        logger.info('Imported and stored instrument scripts in dir /data')


    with open('./temp/icici/NSEScripMaster.txt', 'r') as src_file:
        with open('./data/icici/nse_eq.csv', 'w') as dest_file:
            dest_file.write(src_file.read())

    with open('./temp/icici/FONSEScripMaster.txt', 'r') as src_file:
        with open('./data/icici/nse_fo.csv', 'w') as dest_file:
            dest_file.write(src_file.read())

    return True

def reconcile_files():
    pass


def delete_temp_files():
    temp_dir = './temp/'
    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        logger.info(f'Deleting {file_path} and its contents')
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            logger.error(f'Failed to delete {file_path}. Reason: {e}')
    logger.info('Done clearing all instruments...')

if __name__ == "__main__":
    logger.info('Downloading instrument files from kotak')
    download_kotak_files()
    
    logger.info('Downloading instrument files from icici')
    download_icici_files()

    logger.info('Reconciling downloaded files for instruments collection')
    reconcile_files()

    logger.info('Deleting temp files from /temp dir')
    delete_temp_files()