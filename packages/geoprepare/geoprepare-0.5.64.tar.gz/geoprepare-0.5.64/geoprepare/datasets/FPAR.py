########################################################################################################################
# Ritvik Sahajpal, Joanne Hall
# ritvik@umd.edu
#
# The original data is in zipped/unzipped tiff format at 0.05 degree resolution (zipped for final products and unzipped
# for preliminary product in recent years). The naming convention is in year, month, day and to match the other datasets
# the data has to be renamed into year, julian day.
#
# Final Tiffs
# Step 1: Unzip, rename the original tiff files, and convert the floating point (unit: mm) data into integer by scaling
# by 100. This speeds up step 2 and the Weighted Average Extraction code.
# Step 2: Convert the data into a global extent to match the crop masks.
#
# Preliminary Tiffs
# Step 1: Rename the original tiff files. Convert the floating point (unit: mm) data into integer by scaling by 100.
# This speeds up step 2 and the Weighted Average Extraction code.
# Step 2: Convert the data into a global extent to match the crop masks.
########################################################################################################################
import os
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor


def download_file(url):
    """
    Downloads a file from the given URL and saves it in the current directory.
    Shows a progress bar for the download.
    """
    local_filename = url.split('/')[-1]

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size_in_bytes = int(r.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True, desc=local_filename)

        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(block_size):
                progress_bar.update(len(chunk))
                f.write(chunk)
        progress_bar.close()

    return local_filename


def get_file_urls(url):
    """
    Scrapes the given directory URL for .tif file links and returns their URLs.
    """
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError if the response code was unsuccessful
    soup = BeautifulSoup(response.text, 'html.parser')

    return [url + a['href'] for a in soup.find_all('a') if a['href'].endswith('.tif')]


def download_FPAR(params):
    file_urls = get_file_urls(params.data_dir)
    breakpoint()
    # Download files in parallel using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=5) as executor:
        list(tqdm(executor.map(download_file, file_urls), total=len(file_urls), desc="Downloading files"))

def run(params):
    """

    Args:
        params ():

    Returns:

    """

    import itertools

    download_FPAR(params)

    # all_params = []
    # for year in range(params.start_year, params.end_year + 1):
    #     for jd in range(start_jd, end_jd, 1):
    #         all_params.extend(list(itertools.product([params], [year], [jd])))
    #
    # if False and params.parallel_process:
    #     with multiprocessing.Pool(
    #         int(multiprocessing.cpu_count() * params.fraction_cpus)
    #     ) as p:
    #         with tqdm(total=len(all_params)) as pbar:
    #             for i, _ in tqdm(enumerate(p.imap_unordered(lst_tiff_qa, all_params))):
    #                 pbar.update()
    # else:
    #     for val in all_params:
    #         lst_tiff_qa(val)
    #
    # download_FPAR(params)


if __name__ == "__main__":
    run()
    pass
