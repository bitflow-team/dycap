# TODO 文件数据 数据 内存与磁盘的相互转换
from .config import RUNNING_CONFIG_KEYS,RUNNING_CONFIG_URLS,DATABASE_DIR,OUTPUT_DIR
from openpyxl import Workbook, load_workbook


class _DataIo:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        self.database_dir = DATABASE_DIR
        self.db_file = self.database_dir.joinpath('dy.db')



class Txt:
    def __init__(self):
        self._urls_file = RUNNING_CONFIG_URLS.as_posix()
        self._keys_file = RUNNING_CONFIG_KEYS.as_posix()
        self._urls =None
        self._keys =None

    def get_urls(self):
        try:
            with open(self._urls_file,'r',encoding='utf-8') as f:
                self._urls = f.readlines()
            self._urls = [u.strip('\n') for u in self._urls]
            return self._urls
        except FileNotFoundError as e:
            raise e

    def get_keys(self):
        try:
            with open(self._keys_file,'r',encoding='utf-8') as f:
                self._keys = f.readlines()
            self._keys = [u.strip('\n') for u in self._keys]
            return self._keys
        except FileNotFoundError as e:
            raise e

class _Xlsx(_DataIo):
    def __init__(self):
        super().__init__()

class DyXlsx(_Xlsx):
    def __init__(self):
        super().__init__()
        self.xlsx_file = self.output_dir.joinpath('dy.xlsx')

    def get(self,data):
        pass

    def test(self):
        print('test','*'*50)
        print(self.database_dir,self.db_file,self.xlsx_file)

class Db(_DataIo):
    def __init__(self):
        self._db_file = DATABASE_DIR.as_posix()
        pass

class DyDB(Db):
    def __init__(self):
        super().__init__()



if __name__ == '__main__':
    a = Txt()
    print(a.get_urls())
