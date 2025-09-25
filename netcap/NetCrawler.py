# TODO 网络测试 数据 从网络到内存

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common import *
from time import sleep as sp
import json
from . import config
from .DataIo import Txt, DyXlsx
from pprint import pprint


errors = [NoSuchElementException, ElementNotInteractableException]


class _Crawler:
    def __init__(self):
        # 配置
        self._option = webdriver.ChromeOptions()
        self._service = webdriver.ChromeService(service_args=['--append-log', '--readable-timestamp'], log_output = config.SELENIUM_CONFIG['log_output'].as_posix())

        self._option.set_capability('goog:loggingPrefs', config.SELENIUM_CONFIG['cap'])
        for i in config.SELENIUM_CONFIG['options']:
            self._option.add_argument(i)
        self._option.add_experimental_option("detach", False)
        self._option.binary_location = config.CHROME_.as_posix()
        self._service.path = config.CHROMEDRIVER_.as_posix()

    def _setup(self):
        return webdriver.Chrome(options=self._option, service=self._service)


class DyCrawler(_Crawler):
    def __init__(self,ti=2):
        super(DyCrawler,self).__init__()
        self.urls = Txt().get_urls()
        """获取待采集url"""
        self.keys = Txt().get_keys()
        # 获取关键词
        self._ti = ti
        '''设置暂停时间'''
        # self._option.add_experimental_option("detach", True)
        # self._option.add_argument('--headless')

    def _setup(self):
        return super(DyCrawler, self)._setup()

    @staticmethod
    def _click_login(driver):
        if (driver.find_elements(By.ID, 'RkbQLUok') or driver.find_elements(By.ID, 'b4kMZDrJ')) or driver.find_elements(
                By.ID, 'login-panel-news'):
            return True
        else:
            return False

    @staticmethod
    def _get_network_log(drivers, logs: [{}])->list:
        """
        获取网络日志中的粉丝关注列表
        :param drivers:
        :param logs:
        :return: list
        """
        fans_list = []
        for l in logs:
            nw = json.loads(l.get('message')).get('message')
            if nw.get('method') == 'Network.responseReceived':
                params = nw['params']
                request_url = params['response']['url']
                if 'user/follower/list' in request_url:
                    request_id = params['requestId']
                    response_body = drivers.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
                    fans_list += json.loads(response_body["body"])["followers"]
                if 'user/following/list' in request_url:
                    request_id = params['requestId']
                    response_body = drivers.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
                    fans_list += json.loads(response_body["body"])["followings"]
        return fans_list

    def _dy_activation(self) -> list:
        """
        抓取粉丝关注列表

        约定入口文件：
            待采集的主页链接：running/urls.txt

            筛选关键词：running/keys.txt

            完成采集的主页链接：running/complete_urls.txt
        :return:list 粉丝关注列表详细信息，还需进一步处理
        """
        test_temp = []

        _driver = self._setup()
        for url in self.urls:
            _driver.get(url)

            # 检测是否登录
            while self._click_login(_driver):
                print('请登录')
                sp(self._ti)
            wait = WebDriverWait(_driver, timeout=2, poll_frequency=.2, ignored_exceptions=errors)
            wait.until(lambda d: _driver.find_elements(by=By.CLASS_NAME, value="C1cxu0Vq") or True)
            box2 = [i for i in _driver.find_elements(By.CLASS_NAME, 'C1cxu0Vq')[:2] if i.text != '0']
            for i in box2:
                i.click()
                if _driver.find_elements(By.ID, value="toastContainer"):
                    print('隐私用户')
                    break
                # 滑动粉丝关注列表
                sp(self._ti)
                temp = 0
                while temp < len(_driver.find_elements(By.CLASS_NAME, value="i5U4dMnB")):
                    sp(self._ti - 1)
                    try:
                        ls = _driver.find_elements(By.CLASS_NAME, value="i5U4dMnB")
                        ActionChains(_driver).scroll_to_element(ls[-1]).perform()
                        print(len(ls))
                        temp = len(ls)
                    except:
                        print("关注粉丝列表为空，无法获取！")
                test_temp += self._get_network_log(_driver, _driver.get_log('performance'))
                if _driver.find_elements(By.CLASS_NAME, value="vc-captcha-close-btn"):
                    _driver.find_element(By.CLASS_NAME, value="vc-captcha-close-btn").click()
                _driver.find_element(by=By.CLASS_NAME, value='KArYflhI').click()
        return test_temp


    def _dy_setup(self):
        log = self._dy_activation()
        fans_list = []
        for i in log:
            if i['account_cert_info'] is None:
                is_biz_account = True
            else:
                is_biz_account = False
            # user_info = [i['nickname'], i['uid'], i['signature'], "https://www.douyin.com/user/" + i['sec_uid'],
            #              i['unique_id'], is_biz_account, i['follower_count'], i['following_count']]

            user_info = {"nickname": i['nickname'],
                         "uid": i['uid'],
                         "signature": i['signature'],
                         "sec_uid": "https://www.douyin.com/user/" + i['sec_uid'],
                         "unique_id": i['unique_id'],
                         "is_biz_account": is_biz_account,
                         "follower_count": i['follower_count'],
                         "following_count": i['following_count'],
                         }
            if user_info not in fans_list:
                fans_list.append(user_info)

        return fans_list


    def dy_fans_1(self):
        """
            抓取抖音粉丝列表
            保存数据到 OUTPUT \\ dy.xlsx
        :return:
        """
        x = DyXlsx()
        x.write_dict_list_to_excel(self._dy_setup())




