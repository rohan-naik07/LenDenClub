import json
import numpy as np
import pandas as pd
import ast
import datetime

with open('query_result_2020-07-10T11_59_14.080809Z.json') as f:
    data = json.load(f)

def get_date(input_date):
  your_dt = datetime.datetime.fromtimestamp(int(input_date)/1000).strftime("%Y-%m-%d")  #%H:%M:%S")
  #print(your_dt)
  #print(type(your_dt))
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
        #data_entry=ast.literal_eval(data_entry)

#print(len(details_list[2]['data'][0]['salary'])) #[data_index]['data'][0]['salary']


bank_names = []
account_nos =[]
account_name =[]
salary = []
final_users=[]
dates = []

for data_index in range(len(data)):
    try:
        if 'data' in details_list[data_index]:
            for salary_index in range(len(details_list[data_index]['data'][0]['salary'])):
                dates.append(get_date(details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][0]['transactionDate']))
                salary.append(details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][0]['amount'])
                bank_names.append(details_list[data_index]['data'][0]['bankName'])
                account_nos.append(details_list[data_index]['data'][0]['accountNumber'])
                account_name.append(details_list[data_index]['data'][0]['accountName'])
                final_users.append(users[data_index])
    except:
        continue
        #print(f'### Exception at {data_index} ###')

final_dataframe = pd.DataFrame({'User IDs':np.array(final_users),'Bank-Name':np.array(bank_names),'Account-Holder-Name':np.array(account_name),'Account-No':np.array(account_nos),'Salary-Amount':np.array(salary),'Date of Transaction':np.array(dates)})
final_dataframe.to_csv('v7_final.csv',index=False)

print(final_dataframe)
