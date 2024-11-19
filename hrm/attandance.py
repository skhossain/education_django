
import requests
import json

# url='http://localhost:3000/dataroot'
url='http://localhost:3000/'




# def getData():
#     response=requests.get(url=url)
#     data=response.json()
#     data_len=len(data['CHECKINOUT'])

#     att=dict()
#     for i in range(data_len):
#         # data=data['CHECKINOUT'][i]
#         userId=data['CHECKINOUT'][i]['USERID']
#         checkTime=data['CHECKINOUT'][i]['CHECKTIME']
#         checkType=data['CHECKINOUT'][i]['CHECKTYPE']
#         logId=data['CHECKINOUT'][i]['LOGID']
#         print(data)
#         return{
#             'userId':userId,
#             'logId':logId,
#             'checkTime':checkTime,
#             'checkType':checkType
#         }


def getData():
    api_req=requests.get(url)
    try:
        api_data=json.loads(api_req.content)
    except:
        api_data="error"
    data=api_data['CHECKINOUT']
    # userId=data['USERID']
    # checkTime=data['CHECKTIME']
    # checkType=data['CHECKTYPE']
    # logId=data['LOGID']
    # print(data)

    # return{
    #         'userId':userId,
    #         'logId':logId,
    #         'checkTime':checkTime,
    #         'checkType':checkType
    #     }
    return data
    
   

import pyodbc 
import re 


# # msa_driver =[x for x in pyodbc.drivers()if 'ACCESS' in x.upper ]
# msa_driver =[ pyodbc.drivers() ]

# print(f'Ms access driver: {msa_driver}')



def attandancelist():
    try:
        #cnxn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb)};Dbq=C:\\data\\mdb\\Jtk2002_Data.mdb;")
        conn_str = (r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Program Files (x86)\ZKTeco\ZKAccess3.5\access.mdb;')
        cnxn=pyodbc.connect(conn_str)
        print("connect data base")
        crsr = cnxn.cursor()
        crsr.execute("SELECT * from CHECKINOUT")
        rows = crsr.fetchall()
        cnxn.close()
        return rows
    except pyodbc.Error as e:
        print("error in connection",e)


def userlist():
    try:
        conn_str = (r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Program Files (x86)\ZKTeco\ZKAccess3.5\access.mdb;')
        cnxn=pyodbc.connect(conn_str)
        print("connect data base")
        crsr=cnxn.cursor()
        crsr.execute("select * from USERINFO")
        rows=crsr.fetchall()
        # print(rows)
        data=[]
        for row in rows:
              data.append(list(row))
        jsonData=json.dumps(data)
        response=requests.post(url,data=jsonData)
        data=response.json()
        # print(data)
        cnxn.close()


    except pyodbc.Error as e:
        print("error in connection",e)


# userlist()

        


      

