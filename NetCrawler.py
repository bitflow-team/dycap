# TODO 网络测试 数据 从网络到内存
from pprint import pprint

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common import *
import config, time

errors = [NoSuchElementException, ElementNotInteractableException]


class _Crawler:
    def __init__(self):
        # 配置
        self._option = webdriver.ChromeOptions()
        self._service = webdriver.ChromeService(service_args=['--append-log', '--readable-timestamp'],log_output = config.SELENIUM_CONFIG['log_output'].as_posix())

        self._option.set_capability('goog:loggingPrefs', config.SELENIUM_CONFIG['cap'])
        for i in config.SELENIUM_CONFIG['options']:
            self._option.add_argument(i)
        self._option.add_experimental_option("detach", False)
        self._option.binary_location = config.CHROME_.as_posix()
        self._service.path = config.CHROMEDRIVER_.as_posix()

    def _setup(self):
        return webdriver.Chrome(options=self._option, service=self._service)


class Dy(_Crawler):
    def __init__(self):
        super(_Crawler,self).__init__()
        self.cap_data_count = None
        self.pub_sleep_time = 2
        self.log = []
        self.user_status = True
        self.user_status_dict = {}

    def setup(self):
        return super()._setup()

    # get fans log
    def fans_activation(self, driver, url):
        c = 0
        while True:
            driver.get(url)
            time.sleep(self.pub_sleep_time)
            try:
                wait = WebDriverWait(driver, timeout=2, poll_frequency=.2, ignored_exceptions=errors)
                wait.until(lambda d: driver.find_elements(by=By.CLASS_NAME, value="C1cxu0Vq") or True)
                text_box = driver.find_elements(by=By.CLASS_NAME, value="C1cxu0Vq")
                if text_box != []:
                    for i in text_box[0:2]:
                        # 粉丝关注数量为0，就跳过
                        cap_data_total = int(i.text)
                        if cap_data_total == 0:
                            print("粉丝关注为0，跳过！")
                            continue
                        i.click()

                        time.sleep(self.pub_sleep_time)
                        if driver.find_elements(by=By.CLASS_NAME, value='i5U4dMnB') == []:
                            print("关注粉丝列表为空，无法获取！")
                            self.user_status_dict[url] = False
                            continue
                        self.user_status_dict[url] = True

                        _count = 0
                        self.cap_data_count = 0
                        while _count <= 1:
                            time.sleep(self.pub_sleep_time)
                            nodes = driver.find_elements(by=By.CLASS_NAME, value='i5U4dMnB')
                            if len(nodes) == self.cap_data_count:
                                _count += 1
                            self.cap_data_count = len(nodes)
                            try:
                                ActionChains(driver).scroll_to_element(nodes[-1]).perform()
                            except:
                                print("超出索引,粉丝关注列表不存在")
                                # 关闭粉丝关注弹窗面板
                                driver.find_element(by=By.CLASS_NAME, value='KArYflhI').click()
                                break
                            # self.log += driver.get_log('performance')
                            # print(len(self.log))
                        print(f"{driver.title}，跳出粉丝关注循环")
                        driver.find_element(by=By.CLASS_NAME, value='KArYflhI').click()
                    return driver.get_log('performance')
                else:
                    print("粉丝关注列表为空")
            except:
                # TODO 检测登录弹窗
                if driver.find_elements(by=By.CLASS_NAME, value='login-pannel-appear-done') != []:
                    time.sleep(60)
                    print("请登录！")
                    continue
                # TODO 反爬
                if driver.find_elements(by=By.CLASS_NAME, value='vc-captcha-close-btn') != []:  # 检测验证
                    driver.find_element(by=By.CLASS_NAME, value='vc-captcha-close-btn').click()
                if c >= 2:
                    return driver.get_log('performance')
                print(f"except:第{c}次出错")
                c += 1


if __name__ == "__main__":
    dy = Dy()
    driver = dy.setup()
    log = dy.fans_activation(driver=driver,
                             url='https://www.douyin.com/user/MS4wLjABAAAAYmAOlqtM67sXnoOb5FfloEtW_sHcrpoy6a9ydyt9iYHFxvEzrRBY7s6_C0KUyXmp')
    # log = dy.fans_activation(driver, 'https://www.douyin.com/user/self?from_tab_name=main')
    print(log)
