import threading
from sms.models import *
import requests
import json
import time


def fn_get_token():
    token = None
    try:
        app_set = SMS_Application_Settings.objects.get()
        if app_set.api_key or app_set.api_key is not None:
            return app_set.api_key
        else:
            auth_url = app_set.messaging_auth_url
            if app_set.total_message_limit > 0:
                app_data = {'username': app_set.messaging_username,
                            'password': app_set.messaging_password}
                headers = {'content-type': 'application/json'}
                res = requests.post(auth_url, data=json.dumps(
                    app_data), headers=headers)
                res_dict = res.json()
                try:
                    token = res_dict['access']
                except Exception as e:
                    token = None
            return token

    except Exception as e:
        return token

def fn_smanager_send_sms():
    error_message = None
    try:
        app_set = SMS_Application_Settings.objects.get()
        post_url = app_set.messaging_url
        if app_set.total_message_limit > 0:
            sms_list = sms_que.objects.filter(message_error__isnull=True).values('id', 'mobile_number', 'text_message', 'template_type',
                                                                                 'app_user_id').order_by('-app_data_time')
            for sms in sms_list:
                sms_temp = sms_template.objects.get(
                    template_type=sms["template_type"])
                app_data = {'api_key': app_set.api_key,
                            'type': sms_temp.message_type,
                            'contacts': sms['mobile_number'],
                            'msg': sms['text_message'],
                            'senderid': app_set.senderid
                            }
                headers = {'content-type': 'application/json',
                           'Authorization': 'Bearer '+fn_get_token()}
                if app_set.is_headers_require:
                    res = requests.post(post_url, data=json.dumps(
                        app_data), headers=headers)
                else:
                    res = requests.post(post_url, data=json.dumps(
                        app_data), headers=headers)

                #res_dict = res.json()
                if res.status_code == 200:
                    sms_que.objects.filter(id=sms['id']).delete()
                    sent = sms_sent(template_type=sms["template_type"], mobile_number=sms['mobile_number'],
                                    text_message=sms['text_message'], app_user_id=sms["app_user_id"])
                    sent.save()
                else:
                    sms_que.objects.get(id=sms['id'])
                    sms_que.message_error = res.json()
                    sms_que.save()
                    app_set.messaging_error = res.json()
                    app_set.save()

        return True, error_message
    except Exception as e:
        app_set = SMS_Application_Settings.objects.get()
        app_set.messaging_error = str(e)
        app_set.save()
        return False, error_message


def fn_adn_send_sms():
    error_message = None
    try:
        app_set = SMS_Application_Settings.objects.get()
        post_url = app_set.messaging_url
        
        if app_set.total_message_limit > 0:
            sms_list = sms_que.objects.filter(message_error__isnull=True).values('id', 'mobile_number', 'text_message', 'template_type',
                                                                                 'app_user_id').order_by('-app_data_time')
            for sms in sms_list:
                try:
                    sms_temp = sms_template.objects.get(
                        template_type=sms["template_type"])
                    app_data = {'api_key': app_set.api_key,
                                'api_secret':app_set.api_secret,
                                'request_type': 'SINGLE_SMS',
                                'message_type': 'UNICODE',
                                'mobile': sms['mobile_number'],
                                'message_body': sms['text_message']
                                }
                    res = requests.post(post_url, data=app_data)
                    if res.json()["api_response_code"] == 200:
                        sms_que.objects.filter(id=sms['id']).delete()
                        sent = sms_sent(template_type=sms["template_type"], mobile_number=sms['mobile_number'],
                                        text_message=sms['text_message'], sms_uid=res.json()['sms_uid'], app_user_id=sms["app_user_id"])
                        sent.save()
                    else:
                        app_set.messaging_error = res.json()['error']
                        app_set.save()
                except Exception as e:
                    print(str(e))

        return True, error_message
    except Exception as e:
        app_set = SMS_Application_Settings.objects.get()
        app_set.messaging_error = str(e)
        app_set.save()
        return False, error_message


def fn_reve_send_sms():
    error_message = None
    try:
        app_set = SMS_Application_Settings.objects.get()
        if app_set.total_message_limit > 0:
            sms_list = sms_que.objects.filter(message_error__isnull=True).values('id', 'mobile_number', 'text_message', 'template_type',
                                                                                 'app_user_id').order_by('-app_data_time')
            for sms in sms_list:
                try:
                    post_url = app_set.messaging_url+'apikey='+app_set.api_key+'&secretkey='+app_set.api_secret+'&callerID='+app_set.senderid
                    post_url=post_url+'&toUser='+sms['mobile_number']+'&messageContent='+ sms['text_message']
                    res = requests.get(post_url)
                    if res.json()["Text"] == 'ACCEPTD':
                        sms_que.objects.filter(id=sms['id']).delete()
                        sent = sms_sent(template_type=sms["template_type"], mobile_number=sms['mobile_number'],
                                        text_message=sms['text_message'], sms_uid=res.json()['Message_ID'], app_user_id=sms["app_user_id"])
                        sent.save()
                    else:
                        app_set.messaging_error = res.json()['error']
                        app_set.save()
                except Exception as e:
                    print(str(e))

        return True, error_message
    except Exception as e:
        app_set = SMS_Application_Settings.objects.get()
        app_set.messaging_error = str(e)
        app_set.save()
        print( str(e))
        return False, error_message


def fn_start_sms_sending():
    error_message = None
    try:
        token = fn_get_token()
        while (True):
            app_set = SMS_Application_Settings.objects.get()
            if app_set.total_message_limit > 0 and token is not None and app_set.is_messaging_on:
                if app_set.sms_api=='1':
                    fn_adn_send_sms()
                elif app_set.sms_api=='2':
                    fn_smanager_send_sms()
                elif app_set.sms_api=='3':
                    fn_reve_send_sms()
            time.sleep(2)
    except Exception as e:
        print(str(e))


def fn_start_sms_job():
    try:
        print('Job Started')
        sms_thread = threading.Thread(target=fn_start_sms_sending())
        sms_thread.start()
        return True
    except Exception as e:
        print(str(e))
        return True
