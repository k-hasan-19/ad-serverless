import os
import boto3
import json
import decimal

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from encoder_class import DecimalEncoder


def crud_handler(event, context):
    if event['httpMethod']=='GET':
        response = get_post_meta(event, context)
        return response
    if event['httpMethod']=='PUT':
        response = put_post_meta(event, context)
        return response




def get_post_meta(event, context):
    
    table = __get_table_client()
    company_id = event["queryStringParameters"]["company_id"]
    post_id = event["queryStringParameters"]["post_id"]
    PK, SK = _get_post_meta_keys(company_id, post_id)
    print("Key: ", json.dumps({'PK':PK, 'SK':SK}, indent=4))

    try:
        data = table.get_item(Key={"PK":PK, "SK":SK}, ReturnConsumedCapacity='TOTAL')
        
        post_info = _parse_post_details(data["Item"])
        
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
        
        
    
    return _response(200, post_info)
    

def put_post_meta(event, context):
    
    table = __get_table_client()
    
    payload = json.loads(event['body'])
    
    PK, SK, company_id, user_id, post_id, post_title, post_content, can_share_on, points_map, created_at, updated_at = _get_post_meta(payload)
    
    print(PK, SK, company_id, user_id, post_id, post_title, post_content, can_share_on, points_map, created_at, updated_at)

    try:
        table.update_item(
            Key={
                'PK': PK,
                'SK': SK
            },
            UpdateExpression='SET #company_id = :company_id, #user_id = :user_id, #post_id = :post_id, #post_title = :post_title, #post_content = :post_content, #can_share_on = :can_share_on, #points_map = :points_map, #created_at = if_not_exists(#created_at, :created_at), #updated_at = :updated_at',
            ExpressionAttributeNames={
                '#company_id': 'company_id',
                '#user_id': 'user_id',
                '#post_id': 'post_id',
                '#post_title': 'post_title',
                '#post_content': 'post_content',
                '#can_share_on': 'can_share_on',
                '#points_map': 'points_map',
                '#created_at':'created_at',
                '#updated_at':'updated_at'
            },
            ExpressionAttributeValues={
                ':company_id': company_id,
                ':user_id': user_id,
                ':post_id': post_id,
                ':post_title': post_title,
                ':post_content': post_content,
                ':can_share_on': can_share_on,
                ':points_map': points_map,
                ':created_at':created_at,
                ':updated_at':updated_at
            },
            ReturnConsumedCapacity='TOTAL'
        )
        payload['post_id'] = post_id

    except ClientError as e:
        print(e.response['Error']['Message'])
        return _response(500, {'status':"DynamoDB Client Error"})
    except KeyError as e:
        print(e)
        return _response(404, {'status':"ITEM NOT FOUND"})
    else:
        print("PutItem succeeded:")
        print(json.dumps(payload, indent=4, cls=DecimalEncoder))
        
    if json.loads(event['body']).get('post_id'):
        return _response(200, payload)
    return _response(201, payload)
    
    
''' Post info cleaner'''

def _parse_post_details(item):
    item.pop('PK', None)
    item.pop('SK', None)
    return item

''' Post partition key generator '''

def _get_post_meta(payload):
    import uuid
    time_now_rfc = _date_time_now()
    if not payload.get('post_id'):
        post_id = str(uuid.uuid4())
        created_at = time_now_rfc
        updated_at = time_now_rfc
    else:
        post_id = payload['post_id']
        updated_at = time_now_rfc
        created_at = payload.get('created_at')
    company_id = payload['company_id']
    user_id = payload['user_id']
    PK = "COMPANY#" + company_id
    SK = "POST#" + post_id
    post_title = payload['post_title']
    post_content = payload['post_content']
    can_share_on = payload.get('can_share_on')
    points_map = payload.get('points_map')
    
    
    return (PK, SK, company_id, user_id, post_id, post_title, post_content, can_share_on, points_map, created_at, updated_at,)

def _get_post_meta_keys(company_id, post_id):
    PK = "COMPANY#" + company_id
    SK = "POST#" + post_id
    return (
        PK,
        SK
        )
        
def _date_time_now():
    import datetime
    return str(datetime.datetime.utcnow().isoformat('T'))+'Z'
# Http response builder

def _response(status_code, json_body):
    body = json.dumps(json_body, cls=DecimalEncoder)

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
