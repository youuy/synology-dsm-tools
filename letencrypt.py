import requests

"""
获取IP的服务
1.http://members.3322.org/dyndns/getip
2.http://ip-api.com/json/?lang=zh-CN
3.http://pv.sohu.com/cityjson
4.http://47.100.176.147/
"""

ip_query_service = "http://47.100.176.147"
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/74.0.3729.169 Safari/537.36 '
})


def main():
    r = requests.post(url=ip_query_service)
    if r.status_code != 200:
        raise Exception('请求接口失败:%s(%s)' % (r.text(), r.status_code))
    logging.info(r.text)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.info(e)
