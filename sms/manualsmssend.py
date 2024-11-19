import DbConnection as db
import pandas as pd
from datetime import date, datetime, timedelta
import numpy as np
import requests
import time


sdb, scur, seng  = db.get_local_oracle_db()
tdb, tcur, teng = db.get_sms_db() 

sql_text ="SELECT PRODUCT_NAME, MOBILE_NUMBER, MESSAGE_TEXT FROM SMS_SEDN_QUE"

df = pd.read_sql(sql_text, con = sdb)

for i,row in df.iterrows():
    sql = "INSERT INTO sms_sms_que (template_type,mobile_number,text_message) VALUES ('" + str(row[0]) + "','" + str(row[1]) + "','" + str(row[2]) + "')"
    print(row[1])
    time.sleep(1)
    tcur.execute(sql)
    tdb.commit()
