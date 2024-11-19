# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 14:54:33 2022

@author: rajib.pradhan
"""

import requests

url='https://portal.adnsms.com/api/v1/secure/check-balance'

url_data={"api_key":"KEY-loxbhx6rhyds14trr7ysehck5ldxztv4", "api_secret":"bEmflqq9uZCHqqK$"}

rep = requests.post(url, data=url_data)

rep_dict = rep.json()


url='https://portal.adnsms.com/api/v1/secure/send-sms'

url_data={"api_key":"KEY-loxbhx6rhyds14trr7ysehck5ldxztv4", "api_secret":"bEmflqq9uZCHqqK$",
          "request_type":"SINGLE_SMS","message_type": "UNICODE",
          "mobile":"01749195756", "message_body":"টেস্ট এডিন এস এম এস "}

rep = requests.post(url, data=url_data)

rep_dict = rep.json()