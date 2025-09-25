# TODO 运行入口

# from test import TsetDy
from netcap.NetCrawler import _get_exposed_objects
import fire




if __name__ == "__main__":
    fire.Fire(_get_exposed_objects())  # 自动传入过滤后的对象