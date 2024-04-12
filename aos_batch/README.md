# 用法
1. 需要先aws configure，配置AK/SK
2. 拷贝创建/删除 AOS Index的脚本文件
curl -LJO https://raw.githubusercontent.com/aws-samples/private-llm-qa-bot/main/deploy/setup_knowledgebase.sh
curl -LJO https://raw.githubusercontent.com/aws-samples/private-llm-qa-bot/main/deploy/teardown_knowledgebase.sh
3. python3 manage_tenant.py {aos_endpoint} {dimension} {tenant_name} {tenant_cnt} {action}

# example
- 删除租户
python3 manage_tenant.py vpc-domain66ac69e0-0qtb5cahmu4a-czex64vkosnktpwhwbut2i7nay.us-west-2.es.amazonaws.com 1024 test 1 delete

- 创建租户
python3 manage_tenant.py vpc-domain66ac69e0-0qtb5cahmu4a-czex64vkosnktpwhwbut2i7nay.us-west-2.es.amazonaws.com 1024 test 1