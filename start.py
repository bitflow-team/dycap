# TODO 运行入口 数据 梦开始之地

from NetCrawler import Dy
from DataHandler import DyHandler

import fire

# dy = Dy()
# driver = dy.setup()
# log = dy.fans_activation(driver=driver,url='https://www.douyin.com/user/MS4wLjABAAAAYmAOlqtM67sXnoOb5FfloEtW_sHcrpoy6a9ydyt9iYHFxvEzrRBY7s6_C0KUyXmp')
# # log = dy.fans_activation(driver, 'https://www.douyin.com/user/self?from_tab_name=main')
#
#
# print(DyHandler.handler_fans(driver=driver,log=log))
what = 'who'
if __name__ == '__main__':
    fire.Fire(Dy)