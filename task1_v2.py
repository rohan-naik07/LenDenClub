
path = 'Users\me\Desktop'

import json
import os
import numpy as np
import pandas as pd

with open('task.json') as f:
    data = json.load(f)

#user_ids = data['User ID']
details_list = []
i=0
for index in range(25):
    if index==29 or index==52 or index==77:
        continue
    data_dict = data[index]
    s = data_dict['Response']
    s = s.replace('u\'','\'')
    s = s.replace('\'','\"')
    s = s.replace('None','"None"')
    s = s.replace('True','"True"')
    s = s.replace('False','"False"')
    s = json.loads(s)
    details_list.append(s)
    print(i)
    i=i+1



s = details_list[2]

print(details_list[2]['data'][0]['bankName'])
print(s['data'][0]['accountNumber'])
print(s['data'][0]['accountName'])
print(s['data'][0]['salary'][-1]['totalSalary'])


bank_names = []
account_nos =[]
account_name =[]
salary = []

for data_index in range(25):
    if 'data' in details_list[data_index]:
        bank_names.append(details_list[data_index]['data'][0]['bankName'])
        account_nos.append(details_list[data_index]['data'][0]['accountNumber'])
        account_name.append(details_list[data_index]['data'][0]['accountName'])
        if details_list[data_index]['data'][0]['salary']:
            salary.append(details_list[data_index]['data'][0]['salary'][-1]['totalSalary'])
        else:
            salary.append(-1)
  
final_dataframe = pd.DataFrame({'Bank-Name':np.array(bank_names),
     'Account-Holder-Name':np.array(account_name),'Account-No':np.array(account_nos),'Recent-Salary':np.array(salary)})
final_dataframe.to_csv('v6_final.csv',index=False)