from DrissionPage.common import Settings
from DrissionPage import Chromium

Settings.set_language('zh_cn')  # 设置为中文时，填入'zh_cn'

tab = Chromium().latest_tab
tab.get('https://www.douyin.com/')
