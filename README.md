# InNeed Employee Advocacy Platform(AWS SAM+OpenAPI 3.0.0 )


## Deployment
```
sam deploy --stack-name inneed-eap --capabilities CAPABILITY_IAM
python ./table-scripts/create_table.py
python ./table-scripts/add_gsi.py
```
