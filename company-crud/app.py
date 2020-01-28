import os
import boto3
import json
import decimal
from entities.company import CompanyMeta
from pprint import pprint as pp

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from encoder_class import DecimalEncoder


def crud_handler(event, context):
    if event['httpMethod']=='GET':
        response = get_company_meta(event, context)
        return response
    if event['httpMethod']=='POST':
        response = post_company_meta(event, context)
        return response
    if event['httpMethod']=='PUT':
        response = put_company_meta(event, context)
        return response




def get_company_meta(event, context):
    
    table = __get_table_client()
    company_domain = event["queryStringParameters"]["domain"]
    PK, SK = CompanyMeta.keys_from_domain(company_domain)
    print("Key: ", json.dumps({'PK':PK, 'SK':SK}, indent=4))

    try:
        data = table.get_item(Key={"PK":PK, "SK":SK}, ReturnConsumedCapacity='TOTAL')
        company = CompanyMeta(data["Item"])

    except ClientError as e:
        print(e.response['Error']['Message'])
        return _response(500, {'status':"DynamoDB Client Error"})
    except KeyError as e:
        print(e)
        return _response(404, {'status':"ITEM NOT FOUND"})
    else:
        consumed_cap = data["ConsumedCapacity"]
        print("GetItem succeeded:")
        print(json.dumps(data, indent=4, cls=DecimalEncoder))
        
        
    
    return _response(200, company.get_item())
    

def post_company_meta(event, context):
    
    table = __get_table_client()
    
    payload = json.loads(event['body'])
    company = CompanyMeta(payload)
    keys = company.get_keys()
    PK, SK = keys['PK'], keys['SK']
    print("Key: ", json.dumps({'PK':PK, 'SK':SK}, indent=4))

    # try:
    #     data = table.get_item(Key={"PK":PK, "SK":SK}, ReturnConsumedCapacity='TOTAL')
        
    # except ClientError as e:
    #     print(e.response['Error']['Message'])
    #     return _response(500, {'status':"DynamoDB Client Error"})
    # if data.get('Item'):
    #     return _response(409, {'status':"Item already exists"})
    
    table_record = company.get_record()
    # pp(table_record)
    
    

    try:
        table.put_item(Item=table_record, ConditionExpression='attribute_not_exists(PK)' ,ReturnConsumedCapacity='TOTAL')
    except ClientError as e:
        if e.response['Error']['Code']=='ConditionalCheckFailedException':
            return _response(409, {'status':"Item already exists"})
        print(e.response['Error']['Message'])
        return _response(500, {'status':"DynamoDB Client Error"})
    else:
        print("PutItem succeeded:")
        print(json.dumps(table_record, indent=4, cls=DecimalEncoder))
    item = company.get_item()
    return _response(201, item)

def put_company_meta(event, context):
    
    table = __get_table_client()
    
    payload = json.loads(event['body'])
    
    company = CompanyMeta(payload)
    table_record = company.get_record()
    PK = table_record['PK']
    SK = table_record['SK']
    try:
        response = table.update_item(
            Key={
                'PK': PK,
                'SK': SK
            },
            UpdateExpression='SET #company_name = :company_name, #company_address = :company_address, #updated_at = :updated_at',
            ConditionExpression= 'attribute_exists(PK)',
            ExpressionAttributeNames={
                '#company_name': 'name',
                '#company_address': 'address',
                '#updated_at':'updated_at'
            },
            ExpressionAttributeValues={
                ':company_name': table_record['name'],
                ':company_address': table_record['address'],
                ':updated_at': table_record['updated_at']
            },
            ReturnValues='ALL_NEW',
            ReturnConsumedCapacity='TOTAL'
        )

    except ClientError as e:
        if e.response['Error']['Code']=='ConditionalCheckFailedException':
            return _response(404, {'status':"ITEM NOT FOUND"})
            
        print(e.response['Error']['Message'])
        return _response(500, {'status':"DynamoDB Client Error"})
    else:
        print("PutItem succeeded:")
        print(json.dumps(table_record, indent=4, cls=DecimalEncoder))
    print('Item update response: ',response)
    if not response.get('Attributes'):
        return _response(404, {'status':"ITEM NOT FOUND"})
    item = CompanyMeta(response['Attributes']).get_item()
    return _response(200, item)

def _response(status_code, json_body):
    body = json.dumps(json_body)

    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            # "Access-Control-Allow-Origin": "*"
        },
        "body": body,
    }


def __get_table_client():
    TABLE_NAME = os.getenv("TABLE_NAME")
    AWS_REGION_DYNAMODB = os.getenv('AWS_REGION_DYNAMODB')
    dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION_DYNAMODB)
    table = dynamodb.Table(TABLE_NAME)
    return table
