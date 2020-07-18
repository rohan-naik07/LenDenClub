import json
import numpy as np
import pandas as pd
import ast
import datetime

with open('query_result_2020-07-10T11_59_14.080809Z.json') as f:
    data = json.load(f)

def get_date(input_date):
  your_dt = datetime.datetime.fromtimestamp(int(input_date)/1000).strftime("%Y-%m-%d")  #%H:%M:%S")
  return your_dt

users=[]
details_list = []
for index in range(len(data)):
    data_entry = data[index]['Response']
    user = data[index]['User ID']
    try:
        data_entry = data_entry.replace('u\'','\'')
        data_entry = data_entry.replace('\'','\"')
        data_entry = data_entry.replace('None','"None"')
        data_entry = data_entry.replace('True','"True"')
        data_entry = data_entry.replace('False','"False"')
        data_entry=json.loads(data_entry)
        users.append(user)
        details_list.append(data_entry)
    except:
        continue
        #print(f'### Exception at {index} ###')

narration_dict  = {
                    "lazypay" : "POS 405988XXXXXX3789 PAYU-LAZYPAY REP",
                    "bajaj" : "109869108846/CCABAJAJFINSERV",
                    "Zest" : "E5L9EFXJFQH7OB/RAZPZESTMONEY",
                    "Earlysalary" : "EW88GSRGJADGMO/RAZPEARLYSALARY",
                    "bajaj" : "CMS/000650117100/BAJAJ_AUTO_CD__4F50CD34 442335",
                    "cashe" : "UPI/017016955251/UPI Collect req/cashe@kotak/Kotak Mahindra/",
                    "kissht" : "TO TRANSFER- UPI/DR/015715788403/KISSHT /IDFB/kisshat@id/PAYM915-",
                    "lazypay" : "IMPS OUTWARD ORG UPI To lazypay.payu@hdfcbank,REF NO - 012505389088, Upi Transaction",
                    "kreditbee" : "UPI/kreditbee.r/016180632926/Kreditbee",
                    "bajaj" : "UPI-BAJAJFINANCELTD-BAJAJFINSERV@ABFSPAY-UTIB0000100-013311812828-COLLECT",
                    "razorpay" : "ACH D- CTRAZORPAY-CTTATAAIAAEMNEMW1Z7RDQ"
}

check_narration = ['lazypay', 'bajaj','zest','earlysalary','cashe','kissht','kreditbee','razorpay']

bank_names = []
account_nos =[]
account_name =[]
salary = []
final_users=[]
dates = []
narration = []
type=[]
opening_balance=[]
closing_balance=[]
payment_category=[]
entity = []


for data_index in range(len(data)):
    try:
        if 'data' in details_list[data_index]:
            for salary_index in range(len(details_list[data_index]['data'][0]['salary'])):
                for transaction_index in range(len(details_list[data_index]['data'][0]['salary'][salary_index]['transactions'])):
                    for item in check_narration:
                        if item in details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][transaction_index]['narration'].lower():
                            entity.append(item)
                            dates.append(get_date(details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][transaction_index]['transactionDate']))
                            salary.append(details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][transaction_index]['amount'])
                            closing_balance.append(details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][transaction_index]['closingBalance']) # closing_balance
                            opening_balance.append(details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][transaction_index]['openingBalance']) #opening_balance
                            payment_category.append(details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][transaction_index]['paymentCategory']) # payment_category
                            type.append(details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][transaction_index]['type']) # type
                            narration.append(details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][transaction_index]['narration']) # narration
                            bank_names.append(details_list[data_index]['data'][0]['bankName'])
                            account_nos.append(details_list[data_index]['data'][0]['accountNumber'])
                            account_name.append(details_list[data_index]['data'][0]['accountName'])
                            final_users.append(users[data_index])

    except:
        #print(f'### Exception at {data_index} ###')
        continue


final_dataframe = pd.DataFrame({'User IDs':np.array(final_users),'Account-No':np.array(account_nos),'Entity':np.array(entity),
                                'Salary-Amount':np.array(salary),'Date of Transaction':np.array(dates),'Narration':np.array(narration),
                                'Type':np.array(type),'Opening-Balance':np.array(opening_balance),'Closing-Balance':np.array(closing_balance),
                                'Payment-Category':np.array(payment_category)})

final_dataframe.to_csv('v2_narration.csv',index=False)

print(final_dataframe)
