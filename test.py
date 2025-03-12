# TODO 测试
import time

import fire
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from NetCrawler import _Crawler, errors
from time import sleep as sp
from DataIo import Txt
import json
from multiprocessing import Queue, Process
import random
from queue import Empty

class _TestCrawler(_Crawler):
    def __init__(self):
        super(_TestCrawler, self).__init__()
        # self._option.add_experimental_option("detach", True)
        self._option.add_argument('--headless')

    def _test_setup(self):
        return super(_TestCrawler, self)._setup()


class TsetDy(_TestCrawler):
    def __init__(self,ti=2):
        super(TsetDy, self).__init__()
        self.urls = Txt().get_urls()
        """获取待采集url"""
        self.keys = Txt().get_keys()
        # 获取关键词
        self._ti = ti
        '''设置暂停时间'''

    def _test_setup(self):
        return super(TsetDy, self)._test_setup()

    @staticmethod
    def _click_login(driver):
        if (driver.find_elements(By.ID, 'RkbQLUok') or driver.find_elements(By.ID, 'b4kMZDrJ')) or driver.find_elements(
                By.ID, 'login-panel-news'):
            return True
        else:
            return False

    @staticmethod
    def _get_network_log(drivers,logs: [{}]):
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

    def test_fans_activation(self) -> list:
        """
        抓取粉丝关注列表

        约定入口文件：
            待采集的主页链接：running/urls.txt

            筛选关键词：running/keys.txt

            完成采集的主页链接：running/complete_urls.txt

        约定出口文件：
            经关键词筛选后未采集的主页链接：output/urls.txt

            输出采集结果：output/result.xlsx

        :return:list
        """
        test_temp = []

        _driver = self._test_setup()
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
                test_temp +=self._get_network_log(_driver, _driver.get_log('performance'))
                if _driver.find_elements(By.CLASS_NAME, value="vc-captcha-close-btn"):
                    _driver.find_element(By.CLASS_NAME, value="vc-captcha-close-btn").click()
                _driver.find_element(by=By.CLASS_NAME, value='KArYflhI').click()
        return test_temp




class TestDataHandler:
    def getter(self,name, qu, q):
        print('子进程： %s' % name)
        while True:
            try:
                fans_list = []
                values = qu.get(block=True, timeout=15)
                # block为True,就是如果队列中无数据了。
                #   |—————— 若timeout默认是None，那么会一直等待下去。
                #   |—————— 若timeout设置了时间，那么会等待timeout秒后才会抛出Queue.Empty异常
                # block 为False，如果队列中无数据，就抛出Queue.Empty异常
                for i in values:
                    is_biz_account = False
                    if i['account_cert_info'] is None:
                        is_biz_account = True
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
                    print(user_info)
                    print(time.time() - q)
                    # fans_list.append(user_info)
                # print(fans_list)
            except Empty:
                break





# 任务调度
class TaskPipeline(object):
    def __init__(self):
        pass

    def _fans_work(self,qu):
        self._test_dy = 0
        qu.put(TsetDy().test_fans_activation())

    def _getter_work(self,name, qu, q):
        self._test_data_handler = 0
        TestDataHandler().getter(name, qu, q)

    def run(self):
        t = time.time()

        queue = Queue()
        putter_process = Process(target=self._fans_work, args=(queue,))
        getter_process = Process(target=self._getter_work, args=("Getter", queue, t))

        putter_process.start()
        getter_process.start()

        putter_process.join()
        getter_process.join()


if __name__ == '__main__':
    fire.Fire(TaskPipeline)

