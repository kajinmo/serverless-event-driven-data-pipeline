import boto3

# Boto3 Configuration (Pointing to Floci)
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

# Table names match the previously applied Terraform resources
tb_profile = dynamodb.Table('tb_user_profile')
tb_activity = dynamodb.Table('tb_user_activity')
