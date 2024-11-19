from sms.models import *
from appauth.utils import fn_english_to_bangla_number
import datetime

NST_FREQ_LIST = {'W': 'সাপ্তাহিক', 'M': 'মাসিক', 'D': 'দৈনিক',
                 'Q': 'পাক্ষিক', 'H': 'অর্ধ বার্ষিক', 'Y': 'বার্ষিক'}


def fn_validate_phone(phone_number):
    try:
        if len(phone_number) < 11:
            return False

        return True
    except Exception as e:
        return False


def fn_send_tran_to_message_que(data):
    sms_require = True
    try:
        sms_temp = sms_template.objects.get(
            template_type=data["template_type"])
        message_text = sms_temp.template_text

        if sms_temp.is_messaging_enable:
            try:
                message_text = str.replace(
                    message_text, 'TRAN_AMOUNT', fn_english_to_bangla_number(data["TRAN_AMOUNT"]))
                if data["TRAN_AMOUNT"] < sms_temp.minimum_tran_amount:
                    sms_require = False
            except Exception as e:
                pass

            try:
                message_text = str.replace(
                    message_text, 'BALANCE', fn_english_to_bangla_number(data["BALANCE"]))
            except Exception as e:
                pass

            try:
                message_text = str.replace(
                    message_text, 'MEMBER_ID', fn_english_to_bangla_number(data["MEMBER_ID"]))
            except Exception as e:
                pass

            try:
                expire_date = datetime.datetime.strptime(
                    str(data["EXP_DATE"]), '%Y-%m-%d').strftime("%d-%m-%Y")
                message_text = str.replace(
                    message_text, 'EXP_DATE', fn_english_to_bangla_number(expire_date))
            except Exception as e:
                pass

            try:
                expire_date = datetime.datetime.strptime(
                    str(data["TRAN_DATE"]), '%Y-%m-%d').strftime("%d-%m-%Y")
                message_text = str.replace(
                    message_text, 'TRAN_DATE', fn_english_to_bangla_number(expire_date))
            except Exception as e:
                pass

            try:
                message_text = str.replace(
                    message_text, 'INSTALLMENT', fn_english_to_bangla_number(data["INSTALLMENT"]))
            except Exception as e:
                pass

            try:
                message_text = str.replace(
                    message_text, 'NST_FREQ', NST_FREQ_LIST[data["NST_FREQ"]])
            except Exception as e:
                pass

            try:
                message_text = str.replace(
                    message_text, 'PENALTY', fn_english_to_bangla_number(data["PENALTY"]))
            except Exception as e:
                pass

            if sms_require and fn_validate_phone(data["mobile_number"]):
                sent = sms_que(template_type=data["template_type"], mobile_number=data["mobile_number"],
                               text_message=message_text, app_user_id=data["app_user_id"])
                sent.save()

    except Exception as e:
        print(str(e))
