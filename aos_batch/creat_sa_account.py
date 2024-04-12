import os
import sys
import boto3
import pandas as pd

aos_endpint = sys.argv[1]
dimension = sys.argv[2]
file_name = sys.argv[3]
action = sys.argv[4] if len(sys.argv)>4 else "create"

print(f"aos_endpint: {aos_endpint}")
print(f"dimension: {dimension}")
print(f"file_name: {file_name}")
print(f"action: {action}")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('chatbotFE_user')

def read_xlsx(file_name):
    df = pd.read_excel(file_name)
    df = df['Employee Login']
    return df

#iter each record in df
df = read_xlsx(file_name)

for tenant_idx in range(len(df)):
    tenant_name = df.iloc[tenant_idx]
    user_name = f"{tenant_name}"
    pwd = user_name
    item = {
        'username': user_name,
        'company': tenant_name,
        'groupname': 'normal',
        'password': pwd
    }

    if action == 'delete':
        print(f"delete tenant - {tenant_name}")
        os.system(f"sh teardown_knowledgebase.sh {aos_endpint} {dimension} {tenant_name}")
        table.delete_item(Key={
                'username': user_name
        })
    else:
        print(f"create tenant - {tenant_name}")
        os.system(f"sh setup_knowledgebase.sh {aos_endpint} {dimension} {tenant_name}")
        table.put_item(Item=item)

    print(f"success creating tenants for {tenant_name}")