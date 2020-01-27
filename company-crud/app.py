import os
import boto3
import json
import decimal
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
    PK, SK = _get_company_meta_keys(company_domain)
    print("Key: ", json.dumps({'PK':PK, 'SK':SK}, indent=4))

    try:
        data = table.get_item(Key={"PK":PK, "SK":SK}, ReturnConsumedCapacity='TOTAL')
        
        company_meta_info = _parse_company_details(data["Item"])
        
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
        
        
    
    return _response(200, company_meta_info)
    

def post_company_meta(event, context):
    
    table = __get_table_client()
    
    payload = json.loads(event['body'])
    
    item = _build_company_record(payload)
    
    print(PK, SK, name, domain, address, created_at, updated_at)

    try:
        table.put_item(Item=item, ReturnValues='ALL_OLD',
            ReturnConsumedCapacity='TOTAL'
        )
        payload['company_id'] = company_id
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
        
    if json.loads(event['body']).get('company_id'):
        return _response(200, payload)
    return _response(201, payload)

def put_company_meta(event, context):
    
    table = __get_table_client()
    
    payload = json.loads(event['body'])
    
    PK, SK, name, domain, address, company_id, created_at, updated_at = _get_company_meta(payload)
    
    print(PK, SK, name, domain, address, created_at, updated_at)

    try:
        table.update_item(
            Key={
                'PK': PK,
                'SK': SK
            },
            UpdateExpression='SET #company_name = :company_name, #company_domain = :company_domain, #company_address = :company_address, #company_id = :company_id, #created_at = :created_at, #updated_at = :updated_at',
            ExpressionAttributeNames={
                '#company_name': 'name',
                '#company_domain': 'company_domain',
                '#company_address': 'address',
                '#company_id': 'company_id',
                '#created_at':'created_at',
                '#updated_at':'updated_at'
            },
            ExpressionAttributeValues={
                ':company_name': name,
                ':company_domain': domain,
                ':company_address': address,
                ':company_id': company_id,
                ':created_at': created_at,
                ':updated_at': updated_at
            },
            ReturnConsumedCapacity='TOTAL'
        )
        payload['company_id'] = company_id
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
        
    if json.loads(event['body']).get('company_id'):
        return _response(200, payload)
    return _response(201, payload)
    
    
''' Company info cleaner'''

def _parse_company_details(item):
    item.pop('PK', None)
    item.pop('SK', None)
    return item

''' Company partition key generator '''

def _build_company_record(payload):
    
    PK = "COMPANY#" + payload['domain']
    SK = "#METADATA#" + payload['domain']
    name = payload['name']
    domain = payload['domain']
    address = payload['address']
    created_at = updated_at = _date_time_now()
    return {
        'PK':PK,
        'SK':SK,
        'name':name,
        'domain':domain,
        'address':address,
        'created_at':created_at,
        'updated_at':updated_at,
    }

def _get_company_meta_keys(company_domain):
    PK = "COMPANY#" + company_domain
    SK = "#METADATA#" + company_domain
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
