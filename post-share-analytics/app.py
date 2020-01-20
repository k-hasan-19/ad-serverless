import os
import boto3
import json
import decimal

from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from encoder_class import DecimalEncoder



def post_share_analytics(event, context):
    
    table = __get_table_client()
    company_id = event["queryStringParameters"]["company_id"]
    post_id = event["queryStringParameters"]["post_id"]
    
    PK, SK_sub = _get_posts_meta_key(company_id, post_id)
    
    print("Key: ", json.dumps({'PK':PK, 'SK_sub':SK_sub}, indent=4))
    
    
    try:
        response = table.query(
                KeyConditionExpression=Key('PK').eq(PK) & Key('SK').begins_with(SK_sub),
                ProjectionExpression='post_id, shared_on',
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
    if items==[]:
        return _response(404, {})
    parsed_share_analytics = parse_share_analytics(items, post_id)
    return _response(200, parsed_share_analytics)

def parse_share_analytics(items, post_id):
    SOCIAL_ENUMS = _get_social_enums()
    analytics_dict = dict(post_id=post_id)
    elements = []
    for item in items:
        # assert item['shared_on'] in SOCIAL_ENUMS
        elements.append(item['shared_on'])
    for social_media in SOCIAL_ENUMS:
        share_count = elements.count(social_media)
        analytics_dict[social_media] = share_count
    return analytics_dict

def _get_posts_meta_key(company_id, post_id):
    PK = "COMPANY#" + company_id
    SK_sub = "POST_SHARE#"+post_id
    return (PK, SK_sub)
    
def _get_social_enums():
    return (
        'TWITTER',
        'FACEBOOK',
        'LINKEDIN'
        )
    
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
