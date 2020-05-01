import logging
import os
import time

import requests

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    filename=os.path.join(
                        os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "."),
                        'netcheck.log'),
                    level=logging.INFO)

websites_for_check = [
    'https://www.baidu.com',
    'https://wx.qq.com',
    'https://www.alipay.com'
]

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/74.0.3729.169 Safari/537.36 ',
    'Content-Type': 'text/html;charset=utf-8'
})

if __name__ == '__main__':
    query_interval_seconds = 60
    error_counter = 0
    restart_wan_counter = 0
    # 先休眠一段时间，等待首次启动联网成功再检查网络状况
    logging.info('start to listen network state...')
    time.sleep(60)
    reboot = False
    while True:
        logging.info('error_counter : %s' % error_counter)
        logging.info('restart_wan_counter : %s' % restart_wan_counter)
        try:
            for website in websites_for_check:
                try:
                    r = session.get(website, timeout=(5, 5))
                    if r.status_code != 200:
                        error_counter += 1
                except:
                    error_counter += 1

            if restart_wan_counter >= 5:
                logging.info('network is not ok, restarting router...')
                reboot = True
                restart_wan_counter += 1
                os.system('reboot -f')
            if error_counter >= 3:
                if not reboot:
                    logging.info('network is not ok, restarting wan...')
                    restart_wan_counter += 1
                    os.system('/sbin/service restart_wan')
            else:
                logging.info('network is ok')
            error_counter = 0
        except Exception as e:
            logging.info(e)
        time.sleep(query_interval_seconds)
