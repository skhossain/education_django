from sms.models import *
import requests
import json
import time

def fn_get_sms_balance():
    balance = None
    try:
        app_set = SMS_Application_Settings.objects.get()
        if app_set.sms_api=='3':
            balance_url = app_set.balance_url+app_set.client_id
            res = requests.get(balance_url)
            balance = res.json()["Balance"]
        elif app_set.sms_api=='2':
            balance_url = app_set.balance_url
            res = requests.get(balance_url)
            balance = res.text
        return balance
    except Exception as e:
        return balance