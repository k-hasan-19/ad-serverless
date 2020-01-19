import os
import boto3
import json
import decimal

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from encoder_class import DecimalEncoder


def crud_handler(event, context):
    if event['httpMethod']=='GET':
        response = get_user_meta(event, context)
        return response
    if event['httpMethod']=='PUT':
        response = put_user_meta(event, context)
        return response




def get_user_meta(event, context):
    
    table = __get_table_client()
    company_id = event["queryStringParameters"]["company_id"]
    user_id = event["queryStringParameters"]["user_id"]
    PK, SK = _get_user_meta_keys(company_id, user_id)
    print("Key: ", json.dumps({'PK':PK, 'SK':SK}, indent=4))

    try:
        data = table.get_item(Key={"PK":PK, "SK":SK}, ReturnConsumedCapacity='TOTAL')
        
        company_user_info = _parse_user_details(data["Item"])
        
        # response = table.get_item(Key={"PK":"COMPANY#8fd4728b-89b6-40aa-a57a-85a4672ec9a0", "SK":"#METADATA#8fd4728b-89b6-40aa-a57a-85a4672ec9a0"}, ReturnConsumedCapacity='TOTAL')

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
        
        
    
    return _response(200, company_user_info)
    

def put_user_meta(event, context):
    
    table = __get_table_client()
    
    payload = json.loads(event['body'])
    
    PK, SK, company_id, user_id, email, first_name, last_name, address, is_admin, created_at, updated_at = _get_user_meta(payload)
    
    print(PK, SK, company_id, user_id, email, first_name, last_name, address, is_admin, created_at, updated_at)

    try:
        table.update_item(
            Key={
                'PK': PK,
                'SK': SK
            },
            UpdateExpression='SET #company_id = :company_id, #user_id = :user_id, #email = :email, #first_name = :first_name, #last_name = :last_name, #address = :address, #is_admin = :is_admin, #created_at = if_not_exists(#created_at, :created_at), #updated_at = :updated_at',
            ExpressionAttributeNames={
                '#company_id': 'company_id',
                '#user_id': 'user_id',
                '#email': 'email',
                '#first_name': 'first_name',
                '#last_name': 'last_name',
                '#address': 'address',
                '#is_admin': 'is_admin',
                '#created_at':'created_at',
                '#updated_at':'updated_at'
            },
            ExpressionAttributeValues={
                ':company_id': company_id,
                ':user_id': user_id,
                ':email': email,
                ':first_name': first_name,
                ':last_name': last_name,
                ':address': address,
                ':is_admin': is_admin,
                ':created_at': created_at,
                ':updated_at': updated_at
            },
            ReturnConsumedCapacity='TOTAL'
        )
        payload['user_id'] = user_id
        # response = table.get_item(Key={"PK":"COMPANY#8fd4728b-89b6-40aa-a57a-85a4672ec9a0", "SK":"#METADATA#8fd4728b-89b6-40aa-a57a-85a4672ec9a0"}, ReturnConsumedCapacity='TOTAL')

    except ClientError as e:
        print(e.response['Error']['Message'])
        return _response(500, {'status':"DynamoDB Client Error"})
    except KeyError as e:
        print(e)
        return _response(404, {'status':"ITEM NOT FOUND"})
    else:
        print("PutItem succeeded:")
        print(json.dumps(payload, indent=4, cls=DecimalEncoder))
        
    if json.loads(event['body']).get('user_id'):
        return _response(200, payload)
    return _response(201, payload)
    
    
''' User info cleaner'''

def _parse_user_details(item):
    item.pop('PK', None)
    item.pop('SK', None)
    return item

''' User partition key generator '''

def _get_user_meta(payload):
    import uuid
    time_now_rfc = _date_time_now()
    if not payload.get('user_id'):
        user_id = str(uuid.uuid4())
        created_at = time_now_rfc
        updated_at = time_now_rfc
    else:
        user_id = payload['user_id']
        updated_at = time_now_rfc
        created_at = payload.get('created_at')
    company_id = payload['company_id']
    PK = "COMPANY#" + company_id
    SK = "USER#" + company_id
    email = payload['email']
    first_name = payload['first_name']
    last_name = payload['last_name']
    address = payload.get('address')
    is_admin = payload['is_admin']
    
    
    return (PK, SK, company_id, user_id, email, first_name, last_name, address, is_admin, created_at, updated_at,)

def _get_user_meta_keys(company_id, user_id):
    PK = "COMPANY#" + company_id
    SK = "USER#" + user_id
    return (
        PK,
        SK
        )
        
def _date_time_now():
    import datetime
    return str(datetime.datetime.utcnow().isoformat('T'))+'Z'
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
