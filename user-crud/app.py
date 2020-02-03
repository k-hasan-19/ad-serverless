import os
import boto3
import json
import decimal
from entities.user import UserMeta
from pprint import pprint as pp

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from encoder_class import DecimalEncoder


def crud_handler(event, context):
       
    if event['httpMethod']=='GET':
        response = get_user_meta(event, context)
        return response
    if event['httpMethod']=='POST':
        response = post_user_meta(event, context)
        return response
    if event['httpMethod']=='PUT':
        response = put_user_meta(event, context)
        return response




def get_user_meta(event, context):
    
    table = __get_table_client()
    company_id = event["queryStringParameters"]["company_id"]
    user_id = event["queryStringParameters"]["user_id"]
    
    PK, SK = UserMeta.keys_from_ids(company_id, user_id)
    print("Key: ", json.dumps({'PK':PK, 'SK':SK}, indent=4))

    try:
        data = table.get_item(Key={"PK":PK, "SK":SK}, ReturnConsumedCapacity='TOTAL')
        
        user = UserMeta(data["Item"])

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
        
        
    
    return _response(200, user.get_item())
    
def post_user_meta(event, context):
    
    table = __get_table_client()
    
    payload = json.loads(event['body'])
    user = UserMeta(payload)
    keys = user.get_keys()
    PK, SK = keys['PK'], keys['SK']
    print("Key: ", json.dumps({'PK':PK, 'SK':SK}, indent=4))
    table_record = user.get_record()
    

    try:
        table.put_item(Item=table_record, ConditionExpression='attribute_not_exists(PK) and attribute_not_exists(SK)' ,ReturnConsumedCapacity='TOTAL')
    except ClientError as e:
        if e.response['Error']['Code']=='ConditionalCheckFailedException':
            return _response(409, {'status':"Item already exists"})
        print(e.response['Error']['Message'])
        return _response(500, {'status':"DynamoDB Client Error"})
    else:
        print("PutItem succeeded:")
        print(json.dumps(table_record, indent=4, cls=DecimalEncoder))
    item = user.get_item()
    return _response(201, item)
    

def put_user_meta(event, context):
    
    table = __get_table_client()
    
    payload = json.loads(event['body'])
    
    user = UserMeta(payload)
    table_record = user.get_record()
    PK = table_record['PK']
    SK = table_record['SK']
    try:
        response = table.update_item(
            Key={
                'PK': PK,
                'SK': SK
            },
            ConditionExpression='attribute_exists(PK) and attribute_exists(SK)',
            UpdateExpression='SET #company_id = :company_id, #first_name = :first_name, #last_name = :last_name, #address = :address, #updated_at = :updated_at',
            ExpressionAttributeNames={
                '#company_id': 'company_id',
                '#first_name': 'first_name',
                '#last_name': 'last_name',
                '#address': 'address',
                '#updated_at':'updated_at'
            },
            ExpressionAttributeValues={
                ':first_name': table_record['first_name'],
                ':last_name': table_record['last_name'],
                ':address': table_record['address'],
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
    item = UserMeta(response['Attributes']).get_item()
    return _response(200, item)
    
# Http response builder

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
