import json
import numpy as np
import pandas as pd
import ast
import datetime

with open('task.json') as f:
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
        #data_entry=ast.literal_eval(data_entry)

#print(len(details_list[2]['data'][0]['salary'])) #[data_index]['data'][0]['salary']


bank_names = []
account_nos =[]
account_name =[]
opening_balances,closing_balances=[],[]
payment_categories = []
types = []
entities = []
narrations=[]
salary = []
final_user_ids=[]
dates = []

for data_index in range(len(data)):
    try:
        if 'data' in details_list[data_index]:
            for salary_index in range(len(details_list[data_index]['data'][0]['salary'])):
                dates.append(get_date(details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][0]['transactionDate']))
                salary.append(details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][0]['amount'])
                narrations.append(details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][0]['narration'])
                opening_balances.append(details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][0]['openingBalance'])
                closing_balances.append(details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][0]['closingBalance'])
                types.append(details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][0]['type'])
                payment_categories.append(details_list[data_index]['data'][0]['salary'][salary_index]['transactions'][0]['paymentCategory'])
                bank_names.append(details_list[data_index]['data'][0]['bankName'])
                account_nos.append(details_list[data_index]['data'][0]['accountNumber'])
                account_name.append(details_list[data_index]['data'][0]['accountName'])
                final_user_ids.append(users[data_index])
    except:
        continue
        print(f'### Exception at {data_index} ###')

print(narrations[0])
final_dataframe = pd.DataFrame({'User IDs':np.array(final_user_ids),'Bank-Name':np.array(bank_names),
                  'Account-Holder-Name':np.array(account_name),'Account-No':np.array(account_nos),
                  'Opening_Balance':np.array(opening_balances),'Closing_Balance':np.array(closing_balances),
                  'Narration':np.array(narrations),'PaymentCategories':np.array(payment_categories),
                  'Types' : np.array(types),
                  'Salary-Amount':np.array(salary),'Date of Transaction':np.array(dates)})

final_dataframe.to_csv('v7_final.csv',index=False)

print(final_dataframe) 