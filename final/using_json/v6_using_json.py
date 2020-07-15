import json
import os
import numpy as np
import pandas as pd
import requests
import ast

with open('query_result_2020-07-10T11_59_14.080809Z.json') as f:
    data = json.load(f)

users=[]
details_list = []
for index in range(len(data)):
    #print(index)
    data_dict = data[index]
    s = data_dict['Response']
    user = data_dict['User ID']
    #print(type(s))
    try:
        s = s.replace('u\'','\'')
        s = s.replace('\'','\"')
        s = s.replace('None','"None"')
        s = s.replace('True','"True"')
        s = s.replace('False','"False"')
        s=json.loads(s)
        users.append(user)
        details_list.append(s)
        #print(users)
    except:
        print(f'### Exception at {index} ###')
        #s=ast.literal_eval(s)
    #s = json.loads(s)
    #print(type(s))


print(len(users))
print(len(details_list))
print(len(data))

"""s = details_list[2]

print(details_list[2]['data'][0]['bankName'])
print(s['data'][0]['accountNumber'])
print(s['data'][0]['accountName'])
print(s['data'][0]['salary'][-1]['totalSalary'])"""

users=np.array(users)

#print(f"First user : {users[0]} , Second : {users[1]} , Third : {users[2]} ")


bank_names = []
account_nos =[]
account_name =[]
salary = []
final_users=[]

for data_index in range(len(data)):
    #print(data_index)
    try:
        if 'data' in details_list[data_index]:
            #print(data_index)
            #print(f"User : {users[data_index]}")
            bank_names.append(details_list[data_index]['data'][0]['bankName'])
            account_nos.append(details_list[data_index]['data'][0]['accountNumber'])
            account_name.append(details_list[data_index]['data'][0]['accountName'])
            if details_list[data_index]['data'][0]['salary']:
                salary.append(details_list[data_index]['data'][0]['salary'][-1]['totalSalary'])
            else:
                salary.append(-1)
            final_users.append(users[data_index])
    except:
        print(f"### Exception at {data_index} ###")

final_dataframe = pd.DataFrame({'User IDs':np.array(final_users),'Bank-Name':np.array(bank_names),'Account-Holder-Name':np.array(account_name),'Account-No':np.array(account_nos),'Recent-Salary':np.array(salary)})
final_dataframe.to_csv('v6_final.csv',index=False)

print(final_dataframe)
