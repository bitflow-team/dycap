# TODO 运行入口 数据 梦开始之地

from test import TsetDy

import fire,sys

# dy = Dy()
# driver = dy.setup()
# log = dy.fans_activation(driver=driver,url='https://www.douyin.com/user/MS4wLjABAAAAYmAOlqtM67sXnoOb5FfloEtW_sHcrpoy6a9ydyt9iYHFxvEzrRBY7s6_C0KUyXmp')
# # log = dy.fans_activation(driver, 'https://www.douyin.com/user/self?from_tab_name=main')
#
#
# print(DyHandler.handler_fans(driver=driver,log=log))

if __name__ == '__main__':
    fire.Fire(TsetDy)