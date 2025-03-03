# TODO 数据处理 数据 内存中发生质变
import json


class Handler:
    def __init__(self):
        pass



class DyHandler(Handler):
    def __init__(self):
        super().__init__()

    def handler_fans(driver,log):
        fans_list = []
        for i in log:
            logjson = json.loads(i['message'])['message']
            if logjson['method'] == 'Network.responseReceived':
                params = logjson['params']
                requestUrl = params['response']['url']
                # 粉丝
                if 'user/follower/list' in requestUrl:
                    requestId = params['requestId']
                    response_body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
                    body_data = response_body["body"]
                    for i in json.loads(body_data)["followers"]:
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
                        fans_list.append(user_info)

                # 关注
                if 'user/following/list' in requestUrl:
                    requestId = params['requestId']
                    response_body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
                    body_data = response_body["body"]
                    for i in json.loads(body_data)["followings"]:
                        is_biz_account = False
                        if i['account_cert_info'] is None:
                            is_biz_account = True
                        # user_info = [i['nickname'], i['uid'], i['signature'], "https://www.douyin.com/user/" + i['sec_uid'],
                        #              i['unique_id'], is_biz_account, i['follower_count'], i['following_count']]
                        # pprint(user_info)
                        user_info = {"nickname": i['nickname'],
                                     "uid": i['uid'],
                                     "signature": i['signature'],
                                     "sec_uid": "https://www.douyin.com/user/" + i['sec_uid'],
                                     "unique_id": i['unique_id'],
                                     "is_biz_account": is_biz_account,
                                     "follower_count": i['follower_count'],
                                     "following_count": i['following_count'],
                                     }
                        fans_list.append(user_info)
        if fans_list:
            return fans_list



