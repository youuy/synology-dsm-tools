import json
import logging
import os
import time

import whatsmyip
from dns_cf import DNSApi
from util import read_from_file

# var
last_ip = None

dns_api = DNSApi()

logging.basicConfig(format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    filename=os.path.join(
                        os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "."), 'ddns.log'),
                    level=logging.INFO)


# var end

def read_config(config_path):
    config = {
        "hostnames": [],
        "configs": {
            "CF_Account_ID": None,
            "CF_Zone_ID": None,
            "CF_Api_Token": None,
            "CF_Api_Key": None
        },
        "query_interval_seconds": 30
    }
    try:
        config_bytes = read_from_file(config_path, 'rb')
        config.update(json.loads(config_bytes))
    except:
        pass
    return config


def main(hostnames):
    my_ip = whatsmyip.get_text()
    global last_ip
    logging.info('current ip address is %s, last ip address is %s' % (my_ip, last_ip))
    if my_ip == last_ip:
        return
    try:
        for record in dns_api.list(hostnames):
            if record.content != my_ip:
                record.content = my_ip
                logging.info('dns record(%s): current(%s) is not the same as last ip address(%s), modifying...' % (
                    record.name, my_ip, last_ip))
                try:
                    dns_api.edit(record)
                except Exception as e:
                    logging.info(e)
            else:
                logging.info('dns record(%s)(%s) - current(%s) is the same as last ip address(%s), pass.' % (
                    record.name, record.content, my_ip, last_ip))
        last_ip = my_ip
    except Exception as e:
        logging.info(e)


def get_app_path():
    current_path = os.path.realpath(__file__)
    return os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")


def get_log_path():
    return


def get_config_path():
    return os.path.join(get_app_path(), 'ddns.json')


if __name__ == '__main__':
    app_path = get_app_path()
    config_path = get_config_path()
    if os.path.isfile(config_path):
        config = read_config(config_path)
        dnsapi_cf = config['dnsapi_cf']
        dns_api.configs.update({
            'CF_Account_ID': dnsapi_cf['CF_Account_ID'],
            'CF_Zone_ID': dnsapi_cf['CF_Zone_ID'],
            'CF_Api_Token': dnsapi_cf['CF_Api_Token'],
            'CF_Api_Key': dnsapi_cf['CF_Api_Key'],
        })
        query_interval_seconds = config['query_interval_seconds']
        if not isinstance(query_interval_seconds, int) or query_interval_seconds < 10:
            query_interval_seconds = 10
        hostnames = config['hostnames']
        while True:
            logging.info('start to listen public ip address...')
            try:
                main(hostnames)
            except Exception as e:
                logging.info(e)
            time.sleep(query_interval_seconds)
