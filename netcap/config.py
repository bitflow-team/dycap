# TODO 项目配置 数据 质变的初始
# from pathlib import Path
from .init import *
import os

# 公共目录
BASE_DIR = Path(__file__).resolve().parent

SOURCE_DIR = BASE_DIR / 'source'
CHROME_CACHED_DIR = SOURCE_DIR / 'cached_google'
DATABASE_DIR = SOURCE_DIR / 'db'

## 资源文件
if not os.path.exists(SOURCE_DIR):
    os.mkdir(SOURCE_DIR)
if not os.path.exists(CHROME_CACHED_DIR):
    os.mkdir(CHROME_CACHED_DIR)
if not os.path.exists(DATABASE_DIR):
    os.mkdir(DATABASE_DIR)

## 入口文件 urls.txt keys.txt *_already.txt
RUNNING_CONFIG_DIR = BASE_DIR / 'running'
if not os.path.isdir(RUNNING_CONFIG_DIR.as_posix()):
    os.mkdir(RUNNING_CONFIG_DIR.as_posix())
RUNNING_CONFIG_URLS = RUNNING_CONFIG_DIR / 'urls.txt'
if not os.path.isfile(RUNNING_CONFIG_URLS.as_posix()):
    with open(RUNNING_CONFIG_URLS.as_posix(), 'w') as f:
        pass
RUNNING_CONFIG_KEYS = RUNNING_CONFIG_DIR / 'keys.txt'
if not os.path.isfile(RUNNING_CONFIG_KEYS.as_posix()):
    with open(RUNNING_CONFIG_KEYS.as_posix(), 'w') as f:
        pass

## 出口文件 output/*.xlsx output/urls.txt
OUTPUT_DIR = BASE_DIR / 'output'
if not os.path.isdir(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR.as_posix())

if os.name == 'nt':
    CHROME_ = SOURCE_DIR / 'chrome/chrome.exe'
    CHROMEDRIVER_ = SOURCE_DIR / 'chromedriver/chromedriver.exe'
else:
    CHROME_ = SOURCE_DIR / 'chrome/chrome'
    CHROMEDRIVER_ = SOURCE_DIR / 'chromedriver/chromedriver'

if not os.path.isfile(CHROME_.as_posix()):
    get_driver_or_chrome(os.name, 'chrome', SOURCE_DIR)
if not os.path.isfile(CHROMEDRIVER_.as_posix()):
    get_driver_or_chrome(os.name, 'driver', SOURCE_DIR)

SELENIUM_CONFIG = {
    "cap": {"performance": "ALL"},
    "options": [
        f'--user-data-dir={CHROME_CACHED_DIR.as_posix()}',
        r'--disable-gpu-driver-bug-workarounds',
        r'--no-default-browser-check',
        r'--enable-unsafe-swiftshader',
        r'--disable-gpu',
        r'--no-sandbox',
        r'--disable-extensions',
        r'--disable-3d-apis',
        # r'--headless',
        # r'start-maximized',
        # r'disable-infobars',
        # r'--disable-background-network-ingestion',
        # r'--disable-background-networking'
    ],
    "log_output": SOURCE_DIR/'chromedriver.log'
}
