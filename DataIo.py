# TODO 文件数据 数据 内存与磁盘的相互转换
from config import RUNNING_CONFIG_KEYS,RUNNING_CONFIG_URLS,RUNNING_CONFIG_DIR

class Txt:
    def __init__(self):
        self._urls = RUNNING_CONFIG_URLS
        self._keys = RUNNING_CONFIG_KEYS
    
class Xlsx:
    def __init__(self):
        pass
    

class Db:
    def __init__(self):
        pass

class DyDB(Db):
    def __init__(self):
        super().__init__()


    
