import json

import requests
from dns_record import DnsRecord
import logging
"""
https://api.cloudflare.com/#dns-records-for-a-zone-list-dns-records
"""

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/74.0.3729.169 Safari/537.36 ',
    'Content-Type': 'application/json'
})


class DNSApi:
    def __init__(self):
        self.configs = {
            'CF_Account_ID': None,
            'CF_Zone_ID': None,
            'CF_Api_Token': None,
            'CF_Api_Key': None,
        }

    def get_headers(self):
        if self.configs['CF_Zone_ID'] is None:
            raise Exception('CF_Zone_ID cannot be none')

        if self.configs['CF_Api_Token']:
            return {
                'Authorization': 'Bearer %s' % self.configs['CF_Api_Token']
            }
        elif self.configs['CF_Api_Key'] and self.configs['CF_Account_ID']:
            return {
                'X-Auth-Email': self.configs['CF_Account_ID'],
                'X-Auth-Key': self.configs['CF_Api_Key']
            }
        else:
            raise Exception('CF_Api_Key cannot be none or (X-Auth-Email and X-Auth-Key cannot be none)')

    def list(self, hostnames):
        logging.info('get dns record list...')
        api_url = "https://api.cloudflare.com/client/v4/zones/%s/dns_records" % self.configs["CF_Zone_ID"]

        r = requests.get(url=api_url, data="type=A&page=1&per_page=100&match=any", headers=self.get_headers())

        if r.status_code != 200:
            logging.info('get dns record list failed')
            raise Exception('request error:%s(%s)' % (r.text, r.status_code))
        r = r.json()
        records = []
        if r['success']:
            for record in r['result']:
                if record['name'] in hostnames:
                    records.append(
                        DnsRecord(id=record['id'], type=record['type'], name=record['name'], content=record['content'],
                                  ttl=record['ttl']))
            logging.info('get dns record list success, length = %s' % len(records))
            return records
        else:
            logging.info('get dns record list failed')
            raise Exception('request error: %s' % r)

    def edit(self, record):
        logging.info('edit dns record: %s' % json.dumps(record.__dict__))
        api_url = "https://api.cloudflare.com/client/v4/zones/%s/dns_records/%s" % (
            self.configs["CF_Zone_ID"], record.id)
        data = {
            'content': record.content
        }
        r = requests.patch(url=api_url, data=json.dumps(data), headers=self.get_headers())
        if r.status_code != 200:
            logging.info('edit dns record failed')
            raise Exception('request error:%s(%s)' % (r.text, r.status_code))
        r = r.json()
        if not r['success']:
            logging.info('edit dns record failed')
            raise Exception('request error: %s' % r)
        logging.info('edit dns record success')
