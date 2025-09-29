# TODO 数据处理 数据 内存中发生质变
import json


class Handler:
    def __init__(self):
        pass

class DyHandler(Handler):
    def __init__(self):
        super().__init__()

    @staticmethod
    def handler_fans(driver, log) -> list[dict]:
        def following_or_follower(input):
            if 'user/follower/list' in input:
                return 'follower'
            if 'user/following/list' in input:
                return 'following'
            return 'following'

        fans_list = []
        for i in log:
            logjson = json.loads(i['message'])['message']
            if logjson['method'] != 'Network.responseReceived':
                break
            params = logjson['params']
            # 粉丝和关注
            if 'user/follower/list' in params['response']['url'] or 'user/following/list' in params['response']['url']:
                for i in json.loads(
                        driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': params['requestId']})["body"])[
                    following_or_follower(params['response']['url'])]:
                    # user_info = [i['nickname'], i['uid'], i['signature'], "https://www.douyin.com/user/" + i['sec_uid'],
                    #              i['unique_id'], is_biz_account, i['follower_count'], i['following_count']]
                    user_info = {"nickname": i['nickname'],
                                 "uid": i['uid'],
                                 "signature": i['signature'],
                                 "sec_uid": "https://www.douyin.com/user/" + i['sec_uid'],
                                 "unique_id": i['unique_id'],
                                 "is_biz_account": i['account_cert_info'] is None,
                                 "follower_count": i['follower_count'],
                                 "following_count": i['following_count'],
                                 }
                    if following_or_follower(params['response']['url']) == 'followings':
                        fans_list.append(user_info)
        if fans_list:
            return fans_list