# TODO 下载依赖
from pathlib import Path
from tqdm import tqdm
from sys import exit
import requests,zipfile



def unzip_file(zip_path, extract_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
    zip_ref.close()
    Path(zip_path.split('.')[0]).rename(zip_path.split('-')[0])

# chromedriver-linux64.zip
# chrome-linux64
# 下载浏览器及驱动
def get_driver_or_chrome(os_type:str, binary:str,source_dir:Path):
    def download_file(_url: str,zip_file_name): # zip_file_name: 绝对路径/**/*.zip
        response = requests.get(_url, stream=True)
        if response.status_code != 200:
            print(f"网络错误,无法下载,请手动下载:{_url}")
            exit(-1)
        total_size = int(response.headers.get('content-length', 0))
        with tqdm(desc=zip_file_name.as_posix(), total=total_size, unit='iB', unit_scale=True, unit_divisor=1024) as pbar:
            with open(zip_file_name.as_posix(), 'wb') as _f:
                for data in response.iter_content(chunk_size=1024):
                    _f.write(data)
                    pbar.update(len(data))
        try:
            unzip_file(zip_file_name.as_posix(), source_dir)
        except Exception as Error:
            print(Error)

    if os_type == 'nt':
        if binary == 'chrome':
            url = "https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.35/win64/chrome-win64.zip"
            download_file(url,source_dir/url.split('/')[-1])
        else:
            url = "https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.35/win64/chromedriver-win64.zip"
            download_file(url,source_dir / url.split('/')[-1])
    else:
        if binary == 'chrome':
            url = "https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.35/linux64/chrome-linux64.zip"
            download_file(url, source_dir / url.split('/')[-1])
        else:
            url = "https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.35/linux64/chromedriver-linux64.zip"
            download_file(url, source_dir / url.split('/')[-1])

