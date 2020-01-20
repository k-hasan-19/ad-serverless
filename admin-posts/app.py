import os
import boto3
import json
import decimal

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from encoder_class import DecimalEncoder

INDEX_NAME = 'PK-post_created_at-index'
LIMIT = 10


def get_admin_posts(event, context):
    
    table = __get_table_client()
    company_id = event["queryStringParameters"]["company_id"]
    user_id = event["queryStringParameters"]["user_id"]
    if event["queryStringParameters"].get("limit"):
        global LIMIT
        LIMIT = event["queryStringParameters"].get("limit")
    PK = _get_posts_key(company_id, user_id)
    print("Key: ", json.dumps({'PK':PK}, indent=4))
    
    
    try:
        response = table.query(
                KeyConditionExpression=Key('PK').eq(PK),
                FilterExpression=Attr('user_id').eq(user_id),
                IndexName=INDEX_NAME,
                ProjectionExpression='post_id, post_title, post_content, points_map, can_share_on, created_at, updated_at',
                ScanIndexForward=False,
                Limit=LIMIT,
                ReturnConsumedCapacity='TOTAL'
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return _response(500, {'status':"DynamoDB Client Error"})
    else:
        items = response['Items']
        consumed_cap = response['ConsumedCapacity']
        print("GetItems succeeded:")
        print(json.dumps(items, indent=4, cls=DecimalEncoder))
        print(json.dumps(consumed_cap, indent=4, cls=DecimalEncoder))
    return _response(200, items)



def _get_posts_key(company_id, user_id):
    PK = "COMPANY#" + company_id
    return PK
    
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
