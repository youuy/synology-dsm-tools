import requests

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/74.0.3729.169 Safari/537.36 '
})


def get_text():
    ip_query_service = "http://47.100.176.147"
    r = requests.post(url=ip_query_service)
    if r.status_code != 200:
        raise Exception('请求接口失败:%s(%s)' % (r.text, r.status_code))
    return r.text


def get_json():
    ip_query_service = "http://47.100.176.147/json"
    r = requests.post(url=ip_query_service)
    if r.status_code != 200:
        raise Exception('请求接口失败:%s(%s)' % (r.text, r.status_code))
    return r.json()
