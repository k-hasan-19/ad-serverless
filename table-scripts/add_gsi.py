import boto3

dynamodb = boto3.client('dynamodb', region_name='us-west-2')

try:
    dynamodb.update_table(
        TableName='inneedEap',
        AttributeDefinitions=[
            {
                "AttributeName": "PK",
                "AttributeType": "S"
            },
            {
                "AttributeName": "post_created_at",
                "AttributeType": "N"
            }
        ],
        GlobalSecondaryIndexUpdates=[
            {
                "Create": {
                    "IndexName": "PK-post_created_at-index",
                    "KeySchema": [
                        {
                            "AttributeName": "PK",
                            "KeyType": "HASH"
                        },
                        {
                            "AttributeName": "post_created_at",
                            "KeyType": "RANGE"
                        }
                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    },
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 5,
                        "WriteCapacityUnits": 5
                    }
                }
            }
        ],
    )
    print("Table updated successfully.")
except Exception as e:
    print("Could not update table. Error:")
    print(e)