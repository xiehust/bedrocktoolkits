import os
import sys
import boto3

aos_endpint = sys.argv[1]
dimension = sys.argv[2]
tenant_parent = sys.argv[3]
tenant_cnt = int(sys.argv[4])
action = sys.argv[5] if len(sys.argv)>5 else "create"

print(f"aos_endpint: {aos_endpint}")
print(f"dimension: {dimension}")
print(f"tenant_parent: {tenant_parent}")
print(f"tenant_cnt: {tenant_cnt}")
print(f"action: {action}")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('chatbotFE_user')

for tenant_idx in range(tenant_cnt):
        tenant_name = f"{tenant_parent}-{tenant_idx}"

        user_name = f"{tenant_parent}-user-{tenant_idx}"
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

print(f"finish creating tenants for {tenant_parent}")