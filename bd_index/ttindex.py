from urllib.parse import urlencode
import queue
from datetime import datetime
from datetime import timedelta
import json
import requests
import pandas as pd
import numpy as np
from requests.api import get
from tqdm import tqdm
import browsercookie

class ttindex():

    def __init__(self, keyword, starttime, endtime):
        self.body1 = {
            "keyword_list": [
                keyword
            ],
            "start_date": starttime,
            "end_date": endtime,
            "app_name": ""
        }
        self.body2 = {
            "param": {
                "keyword": keyword,
                "start_date": starttime,
                "end_date": endtime,
                "app_name": ""
            }
        }
        self.header = {
            'Host': 'trendinsight.oceanengine.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'Connection': 'keep-alive',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': 'https://trendinsight.oceanengine.com/index/analysis?keyword=%E7%8A%AC%E5%A4%9C%E5%8F%89',
            'Content-Type': 'application/json;charset=UTF-8',
        }
        self.dyattr = {}
        self.ttattr = {}
        self.ava = False
        self.get_tt_atr()
        self.get_dy_atr()
        self.is_ava()
    
    def get_dy_index(self):
        if self.ava:
            body = self.body1.copy()
            body['app_name'] = 'aweme'
            url = 'https://trendinsight.oceanengine.com/api/open/index/get_multi_keyword_hot_trend'
            response = requests.post(url, headers=self.header, data=json.dumps(body))
            if response.status_code != 200:
                return None
            else:
                dic = {}
                wbdata = json.loads(response.text)
                for item in wbdata['data']['hot_list'][0]['hot_list']:
                    dic[item['datetime']] = int(item['index'])
                return dic
        else:
            return 'No Record'

    def get_tt_index(self):
        if self.ava:
            body = self.body1.copy()
            body['app_name'] = 'toutiao'
            url = 'https://trendinsight.oceanengine.com/api/open/index/get_multi_keyword_hot_trend'
            response = requests.post(url, headers=self.header, data=json.dumps(body))
            if response.status_code != 200:
                return None
            else:
                dic = {}
                wbdata = json.loads(response.text)
                for item in wbdata['data']['hot_list'][0]['hot_list']:
                    dic[item['datetime']] = int(item['index'])
                return dic
        else:
            return 'No Record'


    def get_tt_atr(self):
        url = 'https://trendinsight.oceanengine.com/api/open/index/get_portrait'
        body = self.body2.copy()
        body['param']['app_name'] = 'toutiao'
        response = requests.post(url, headers=self.header, data=json.dumps(body))
        if response.status_code != 200:
            return None
        else:
            wbdata = json.loads(response.text)
            self.ttattr = wbdata['data']['data']

    def get_dy_atr(self):
        url = 'https://trendinsight.oceanengine.com/api/open/index/get_portrait'
        body = self.body2.copy()
        body['param']['app_name'] = 'aweme'
        response = requests.post(url, headers=self.header, data=json.dumps(body))
        if response.status_code != 200:
            return None
        else:
            wbdata = json.loads(response.text)
            self.dyattr = wbdata['data']['data']

    def is_ava(self):
        try:
            woman = self.ttattr[1]['label_list'][1]['value']
            man = self.ttattr[1]['label_list'][0]['value']
            if man == 0 and woman == 0:
                return None
            else:
                self.ava = True
        except:
            return None

    def get_dy_age(self):
        if self.ava:
            dic = {}
            for item in self.dyattr[0]['label_list']:
                dic[item['name_zh']] = item['value']
            return dic
        else:
            return None

    def get_tt_age(self):
        if self.ava:
            dic = {}
            for item in self.ttattr[0]['label_list']:
                dic[item['name_zh']] = item['value']
            return dic
        else:
            return None

    def get_dy_sex(self):
        if self.ava:
            dic = {}
            for item in self.dyattr[1]['label_list']:
                dic[item['name_zh']] = item['value']
            return dic
        else:
            return None

    def get_tt_sex(self):
        if self.ava:
            dic = {}
            for item in self.ttattr[1]['label_list']:
                dic[item['name_zh']] = item['value']
            return dic
        else:
            return None
