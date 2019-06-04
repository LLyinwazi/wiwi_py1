# 定义头
import itertools
import time

import requests
import json


def get_header(_cookies="") -> dict:
    """
    构建请求头

    :param _cookies: 可以指定cookies, 默认为空.
    :return: dict 格式的请求头.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Connection': 'keep-alive',
        'x-requested-with': 'XMLHttpRequest',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'cookie': _cookies,
        'upgrade-insecure-requests': '1'
    }
    return headers


def http_get(_host: str, _cookies: str):
    r"""
    查询域名是否已被注册, 注意此接口需要先查询一次前置接口, 以获取 token(cookies).

    :param _host:  所需校验的域名.
    :param _cookies:  前置 cookies, 用于身份校验.
    :return: 校验结果, 格式为 {"code":code, "msg":msg}, code=1000表示已有人注册, code=1001表示该域名无人注册,可用.
    """
    ts = int(time.time() * 1000)
    url = "https://whois.aliyun.com/whois/api_whois?host=" + _host \
          + "&umToken=whois-web-hichina-com%3A4d3df4e0523efcf4e288738fc972a257&_=" + str(ts)
    resp_data = requests.get(url, headers=get_header(_cookies))
    # 响应体
    resp_cont = str(resp_data.content, 'UTF-8')
    # print("响应体 >>> " + resp_cont)
    cont_json = json.loads(resp_cont)
    code_ = cont_json["code"]
    map_ = {"code": code_, "msg": cont_json["msg"]}
    return map_


def pre_step1_get_cookie(host) -> str:
    """
    输入域名, 获取 cookies, 用于后续查询该域名是否已被注册.
    :param host:
    :return: cookies
    """
    url = "https://whois.aliyun.com/whois/domain/" + host + "?spm=5334.whvccom.5.1"
    resp_data = requests.post(url, headers=get_header())
    json_cookies = json.loads(str(resp_data.headers).replace("\'", "\""))
    return json_cookies["Set-Cookie"]


if __name__ == '__main__':
    s_set = set()
    # 所需的域名从种子域名里取值并做遍历组合, 注意域名不区分大小写.
    seeds = {"pay", "u", "we", "ing", "me", "m", "v", "pal", "every"}
    for seed in itertools.combinations_with_replacement(seeds, 2):
        begin = time.time()
        combination = seed[0] + seed[1]
        host = combination + ".com"
        cookies = pre_step1_get_cookie(host)
        # print("cookies:" + cookies)
        resp = http_get(host, cookies)
        print("host:%s, response:%s" % (host, resp))
        if resp["code"] == "1001":
            print("获取到一个未注册的域名:" + host + " >>> " + resp["msg"])
            s_set.add(host)
        end = time.time()
        print("consume: %s ms" % str(int((end - begin) * 1000)))
    print("-------------divided line---------------------")
    if s_set.__sizeof__() > 0:
        print("total success:")
        print(s_set)
    else:
        print("未找到未注册的域名.")
