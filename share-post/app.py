import os
import boto3
import json
import decimal

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from encoder_class import DecimalEncoder




def post_share(event, context):
    
    table = __get_table_client()

    payload = json.loads(event['body'])
    
    PK, SK = _get_share_keys(payload)
    created_at = _date_time_now()
    print(PK, SK, created_at, payload)
    
    item = dict(payload)
    item['PK'] = PK
    item['SK'] = SK
    item['created_at'] = created_at
    try:
        table.put_item(
           Item=item,
           ReturnConsumedCapacity='TOTAL'
        )

    except ClientError as e:
        print(e.response['Error']['Message'])
        return _response(500, {'status':"DynamoDB Client Error"})
    else:
        print("PutItem succeeded:")
        print(json.dumps(payload, indent=4, cls=DecimalEncoder))
    return _response(201, payload)
    
    

''' Share event partition key generator '''

def _get_share_keys(payload):
    # company_id, user_id, post_id, shared_on
    PK = "COMPANY#" + payload['company_id']
    SK = "POST_RELATION#"+payload['post_id']+"#"+payload['shared_on']+"#"+payload['user_id']
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
