## Employee Advocacy Platform(AWS SAM+OpenAPI 3.0.2 )


`Warning`: We are still at development stage. It's not stable yet

## Deployment

```
sam deploy --stack-name inneed-eap --capabilities CAPABILITY_IAM
python ./table-scripts/create_table.py
python ./table-scripts/add_gsi.py
```
[API endpoint details](./eap-openapi.yaml)
### TODO

- [ ] Integrate existing front end 
- [ ] POST endpoints for CRUD
- [ ] Social Media credential GET/POST end points
- [ ] Top score endpoint
