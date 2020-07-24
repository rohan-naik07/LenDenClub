import boto3
import json
import numpy as np
import pandas as pd
import datetime

s3_client = boto3.client('s3')

def get_date(input_date):
  your_dt = datetime.datetime.fromtimestamp(int(input_date)/1000).strftime("%Y-%m-%d")  # YYYY-MM-DD
  return your_dt


def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']
    json_object = s3_client.get_object(Bucket=bucket_name,Key=file_name)
    
    print('Done-1')
    
    json_file = json_object['Body'].read()
    
    data = json.loads(json_file)
    
    print('Done-2')
    
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

    check_narration = ['lazypay','bajaj','zest','earlysalary','cashe','kissht','kreditbee','razorpay']
    
    print('Done-3')

    bank_names = []
    account_nos =[]
    account_name =[]
    salary = []
    final_users=[]
    dates = []
    narrations = []
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
                        for bank_narration in check_narration:
                            if bank_narration in details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][transaction_index]['narration'].lower():
                                entity.append(bank_narration)
                                dates.append(get_date(details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][transaction_index]['transactionDate'])) #transactionDate
                                salary.append(details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][transaction_index]['amount']) #amount
                                closing_balance.append(details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][transaction_index]['closingBalance']) # closing_balance
                                opening_balance.append(details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][transaction_index]['openingBalance']) #opening_balance
                                payment_category.append(details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][transaction_index]['paymentCategory']) # payment_category
                                type.append(details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][transaction_index]['type']) # type
                                narrations.append(details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][transaction_index]['narration']) # narration
                                bank_names.append(details_list[data_index]['data'][0]['bankName']) #bankName
                                account_nos.append(details_list[data_index]['data'][0]['accountNumber']) #accountno
                                account_name.append(details_list[data_index]['data'][0]['accountName']) #accountName
                                final_users.append(users[data_index]) #user-id

        except:
            continue
        
    print('Done-4')


    final_dataframe = pd.DataFrame({'User IDs':np.array(final_users),'Account-No':np.array(account_nos),'Entity':np.array(entity),
                                    'Salary-Amount':np.array(salary),'Date of Transaction':np.array(dates),'Narration':np.array(narrations),
                                    'Type':np.array(type),'Opening-Balance':np.array(opening_balance),'Closing-Balance':np.array(closing_balance),
                                    'Payment-Category':np.array(payment_category)})

    ##final_dataframe.to_csv('v1_narrationT4.csv',index=False)

    print(final_dataframe)
    
    print('Done-5')   
    
    return "Done-6"
