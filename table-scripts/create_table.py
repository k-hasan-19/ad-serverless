import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')


table = dynamodb.create_table(
    TableName='inneedEap',
    KeySchema=[
        {
            'AttributeName': 'PK',
            'KeyType': 'HASH'  #Partition key
        },
        {
            'AttributeName': 'SK',
            'KeyType': 'RANGE'  #Sort key
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'PK',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'SK',
            'AttributeType': 'S'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

print("Table status:", table.table_status)