{"filter":false,"title":"app.py","tooltip":"/admin-posts-crud/app.py","undoManager":{"mark":84,"position":84,"stack":[[{"start":{"row":10,"column":0},"end":{"row":19,"column":0},"action":"remove","lines":["def crud_handler(event, context):","    if event['httpMethod']=='GET':","        response = get_post_meta(event, context)","        return response","    if event['httpMethod']=='PUT':","        response = put_post_meta(event, context)","        return response","","",""],"id":2},{"start":{"row":10,"column":0},"end":{"row":11,"column":0},"action":"remove","lines":["",""]}],[{"start":{"row":42,"column":0},"end":{"row":100,"column":4},"action":"remove","lines":["def put_post_meta(event, context):","    ","    table = __get_table_client()","    ","    payload = json.loads(event['body'])","    ","    PK, SK, company_id, user_id, post_id, post_title, post_content, can_share_on, points_map, created_at, updated_at = _get_post_meta(payload)","    ","    print(PK, SK, company_id, user_id, post_id, post_title, post_content, can_share_on, points_map, created_at, updated_at)","","    try:","        table.update_item(","            Key={","                'PK': PK,","                'SK': SK","            },","            UpdateExpression='SET #company_id = :company_id, #user_id = :user_id, #post_id = :post_id, #post_title = :post_title, #post_content = :post_content, #can_share_on = :can_share_on, #points_map = :points_map, #created_at = if_not_exists(#created_at, :created_at), #post_created_at = if_not_exists(#created_at, :created_at), #updated_at = :updated_at',","            ExpressionAttributeNames={","                '#company_id': 'company_id',","                '#user_id': 'user_id',","                '#post_id': 'post_id',","                '#post_title': 'post_title',","                '#post_content': 'post_content',","                '#can_share_on': 'can_share_on',","                '#points_map': 'points_map',","                '#post_created_at':'post_created_at',","                '#created_at':'created_at',","                '#updated_at':'updated_at'","            },","            ExpressionAttributeValues={","                ':company_id': company_id,","                ':user_id': user_id,","                ':post_id': post_id,","                ':post_title': post_title,","                ':post_content': post_content,","                ':can_share_on': can_share_on,","                ':points_map': points_map,","                ':created_at':created_at,","                ':updated_at':updated_at","            },","            ReturnConsumedCapacity='TOTAL'","        )","        payload['post_id'] = post_id","","    except ClientError as e:","        print(e.response['Error']['Message'])","        return _response(500, {'status':\"DynamoDB Client Error\"})","    except KeyError as e:","        print(e)","        return _response(404, {'status':\"ITEM NOT FOUND\"})","    else:","        print(\"PutItem succeeded:\")","        print(json.dumps(payload, indent=4, cls=DecimalEncoder))","        ","    if json.loads(event['body']).get('post_id'):","        return _response(200, payload)","    return _response(201, payload)","    ","    "],"id":3}],[{"start":{"row":42,"column":0},"end":{"row":43,"column":0},"action":"remove","lines":["",""],"id":4}],[{"start":{"row":11,"column":4},"end":{"row":11,"column":17},"action":"remove","lines":["get_post_meta"],"id":5},{"start":{"row":11,"column":4},"end":{"row":11,"column":18},"action":"insert","lines":["get_posts_meta"]}],[{"start":{"row":15,"column":46},"end":{"row":15,"column":50},"action":"remove","lines":["post"],"id":6},{"start":{"row":15,"column":46},"end":{"row":15,"column":47},"action":"insert","lines":["u"]},{"start":{"row":15,"column":47},"end":{"row":15,"column":48},"action":"insert","lines":["s"]},{"start":{"row":15,"column":48},"end":{"row":15,"column":49},"action":"insert","lines":["e"]},{"start":{"row":15,"column":49},"end":{"row":15,"column":50},"action":"insert","lines":["r"]}],[{"start":{"row":74,"column":13},"end":{"row":74,"column":14},"action":"insert","lines":["s"],"id":7}],[{"start":{"row":76,"column":4},"end":{"row":76,"column":6},"action":"remove","lines":["SK"],"id":8},{"start":{"row":76,"column":4},"end":{"row":76,"column":19},"action":"insert","lines":["post_created_at"]}],[{"start":{"row":78,"column":11},"end":{"row":79,"column":10},"action":"remove","lines":["","        SK"],"id":10}],[{"start":{"row":77,"column":12},"end":{"row":78,"column":0},"action":"remove","lines":["",""],"id":12},{"start":{"row":77,"column":12},"end":{"row":77,"column":16},"action":"remove","lines":["    "]},{"start":{"row":77,"column":12},"end":{"row":77,"column":16},"action":"remove","lines":["    "]}],[{"start":{"row":77,"column":15},"end":{"row":78,"column":0},"action":"remove","lines":["",""],"id":13},{"start":{"row":77,"column":15},"end":{"row":77,"column":16},"action":"remove","lines":[" "]},{"start":{"row":77,"column":15},"end":{"row":77,"column":16},"action":"remove","lines":[" "]},{"start":{"row":77,"column":15},"end":{"row":77,"column":16},"action":"remove","lines":[" "]},{"start":{"row":77,"column":15},"end":{"row":77,"column":16},"action":"remove","lines":[" "]},{"start":{"row":77,"column":15},"end":{"row":77,"column":16},"action":"remove","lines":[" "]},{"start":{"row":77,"column":15},"end":{"row":77,"column":16},"action":"remove","lines":[" "]}],[{"start":{"row":77,"column":15},"end":{"row":77,"column":16},"action":"remove","lines":[" "],"id":14},{"start":{"row":77,"column":15},"end":{"row":77,"column":16},"action":"remove","lines":[" "]}],[{"start":{"row":75,"column":32},"end":{"row":76,"column":39},"action":"remove","lines":["","    post_created_at = \"POST#\" + post_id"],"id":15}],[{"start":{"row":16,"column":13},"end":{"row":16,"column":32},"action":"remove","lines":["_get_post_meta_keys"],"id":16},{"start":{"row":16,"column":13},"end":{"row":16,"column":33},"action":"insert","lines":["_get_posts_meta_keys"]}],[{"start":{"row":16,"column":6},"end":{"row":16,"column":10},"action":"remove","lines":[", SK"],"id":17}],[{"start":{"row":17,"column":38},"end":{"row":17,"column":47},"action":"remove","lines":[", 'SK':SK"],"id":18}],[{"start":{"row":17,"column":51},"end":{"row":18,"column":0},"action":"insert","lines":["",""],"id":19},{"start":{"row":18,"column":0},"end":{"row":18,"column":4},"action":"insert","lines":["    "]},{"start":{"row":18,"column":4},"end":{"row":19,"column":0},"action":"insert","lines":["",""]},{"start":{"row":19,"column":0},"end":{"row":19,"column":4},"action":"insert","lines":["    "]}],[{"start":{"row":19,"column":4},"end":{"row":33,"column":65},"action":"insert","lines":["","try:","    response = table.query(","            KeyConditionExpression=Key('user_id').eq(user_id),# & Key('shared_on').eq(shared_on),","            IndexName='user_id-shared_on-index',","            ReturnConsumedCapacity='TOTAL'","    )","except ClientError as e:","    print(e.response['Error']['Message'])","else:","    items = response['Items']","    consumed_cap = response['ConsumedCapacity']","    print(\"GetItem succeeded:\")","    print(json.dumps(items, indent=4, cls=DecimalEncoder))","    print(json.dumps(consumed_cap, indent=4, cls=DecimalEncoder))"],"id":20}],[{"start":{"row":20,"column":0},"end":{"row":20,"column":4},"action":"insert","lines":["    "],"id":21},{"start":{"row":21,"column":0},"end":{"row":21,"column":4},"action":"insert","lines":["    "]},{"start":{"row":22,"column":0},"end":{"row":22,"column":4},"action":"insert","lines":["    "]},{"start":{"row":23,"column":0},"end":{"row":23,"column":4},"action":"insert","lines":["    "]},{"start":{"row":24,"column":0},"end":{"row":24,"column":4},"action":"insert","lines":["    "]},{"start":{"row":25,"column":0},"end":{"row":25,"column":4},"action":"insert","lines":["    "]},{"start":{"row":26,"column":0},"end":{"row":26,"column":4},"action":"insert","lines":["    "]},{"start":{"row":27,"column":0},"end":{"row":27,"column":4},"action":"insert","lines":["    "]},{"start":{"row":28,"column":0},"end":{"row":28,"column":4},"action":"insert","lines":["    "]},{"start":{"row":29,"column":0},"end":{"row":29,"column":4},"action":"insert","lines":["    "]},{"start":{"row":30,"column":0},"end":{"row":30,"column":4},"action":"insert","lines":["    "]},{"start":{"row":31,"column":0},"end":{"row":31,"column":4},"action":"insert","lines":["    "]},{"start":{"row":32,"column":0},"end":{"row":32,"column":4},"action":"insert","lines":["    "]},{"start":{"row":33,"column":0},"end":{"row":33,"column":4},"action":"insert","lines":["    "]}],[{"start":{"row":22,"column":44},"end":{"row":22,"column":51},"action":"remove","lines":["user_id"],"id":22},{"start":{"row":22,"column":44},"end":{"row":22,"column":45},"action":"insert","lines":["P"]},{"start":{"row":22,"column":45},"end":{"row":22,"column":46},"action":"insert","lines":["K"]}],[{"start":{"row":22,"column":52},"end":{"row":22,"column":59},"action":"remove","lines":["user_id"],"id":23},{"start":{"row":22,"column":52},"end":{"row":22,"column":53},"action":"insert","lines":["P"]},{"start":{"row":22,"column":53},"end":{"row":22,"column":54},"action":"insert","lines":["K"]}],[{"start":{"row":8,"column":0},"end":{"row":9,"column":0},"action":"insert","lines":["",""],"id":24},{"start":{"row":9,"column":0},"end":{"row":9,"column":1},"action":"insert","lines":["I"]},{"start":{"row":9,"column":1},"end":{"row":9,"column":2},"action":"insert","lines":["N"]},{"start":{"row":9,"column":2},"end":{"row":9,"column":3},"action":"insert","lines":["D"]},{"start":{"row":9,"column":3},"end":{"row":9,"column":4},"action":"insert","lines":["E"]}],[{"start":{"row":9,"column":4},"end":{"row":9,"column":5},"action":"insert","lines":["X"],"id":25},{"start":{"row":9,"column":5},"end":{"row":9,"column":6},"action":"insert","lines":["_"]},{"start":{"row":9,"column":6},"end":{"row":9,"column":7},"action":"insert","lines":["N"]},{"start":{"row":9,"column":7},"end":{"row":9,"column":8},"action":"insert","lines":["A"]}],[{"start":{"row":9,"column":8},"end":{"row":9,"column":9},"action":"insert","lines":["M"],"id":26},{"start":{"row":9,"column":9},"end":{"row":9,"column":10},"action":"insert","lines":["E"]}],[{"start":{"row":9,"column":10},"end":{"row":9,"column":11},"action":"insert","lines":[" "],"id":27},{"start":{"row":9,"column":11},"end":{"row":9,"column":12},"action":"insert","lines":["="]}],[{"start":{"row":9,"column":12},"end":{"row":9,"column":13},"action":"insert","lines":[" "],"id":28}],[{"start":{"row":9,"column":13},"end":{"row":9,"column":15},"action":"insert","lines":["''"],"id":29}],[{"start":{"row":9,"column":14},"end":{"row":9,"column":38},"action":"insert","lines":["PK-post_created_at-index"],"id":30}],[{"start":{"row":24,"column":26},"end":{"row":24,"column":51},"action":"remove","lines":["'user_id-shared_on-index'"],"id":31},{"start":{"row":24,"column":26},"end":{"row":24,"column":36},"action":"insert","lines":["INDEX_NAME"]}],[{"start":{"row":24,"column":37},"end":{"row":25,"column":0},"action":"insert","lines":["",""],"id":32},{"start":{"row":25,"column":0},"end":{"row":25,"column":16},"action":"insert","lines":["                "]}],[{"start":{"row":25,"column":16},"end":{"row":25,"column":17},"action":"insert","lines":["S"],"id":33},{"start":{"row":25,"column":17},"end":{"row":25,"column":18},"action":"insert","lines":["c"]},{"start":{"row":25,"column":18},"end":{"row":25,"column":19},"action":"insert","lines":["a"]},{"start":{"row":25,"column":19},"end":{"row":25,"column":20},"action":"insert","lines":["n"]}],[{"start":{"row":25,"column":20},"end":{"row":25,"column":21},"action":"insert","lines":["I"],"id":34},{"start":{"row":25,"column":21},"end":{"row":25,"column":22},"action":"insert","lines":["n"]},{"start":{"row":25,"column":22},"end":{"row":25,"column":23},"action":"insert","lines":["d"]},{"start":{"row":25,"column":23},"end":{"row":25,"column":24},"action":"insert","lines":["e"]},{"start":{"row":25,"column":24},"end":{"row":25,"column":25},"action":"insert","lines":["x"]},{"start":{"row":25,"column":25},"end":{"row":25,"column":26},"action":"insert","lines":["F"]}],[{"start":{"row":25,"column":26},"end":{"row":25,"column":27},"action":"insert","lines":["o"],"id":35},{"start":{"row":25,"column":27},"end":{"row":25,"column":28},"action":"insert","lines":["r"]},{"start":{"row":25,"column":28},"end":{"row":25,"column":29},"action":"insert","lines":["w"]},{"start":{"row":25,"column":29},"end":{"row":25,"column":30},"action":"insert","lines":["a"]},{"start":{"row":25,"column":30},"end":{"row":25,"column":31},"action":"insert","lines":["r"]},{"start":{"row":25,"column":31},"end":{"row":25,"column":32},"action":"insert","lines":["d"]}],[{"start":{"row":25,"column":32},"end":{"row":25,"column":33},"action":"insert","lines":["="],"id":36},{"start":{"row":25,"column":33},"end":{"row":25,"column":34},"action":"insert","lines":["F"]},{"start":{"row":25,"column":34},"end":{"row":25,"column":35},"action":"insert","lines":["a"]},{"start":{"row":25,"column":35},"end":{"row":25,"column":36},"action":"insert","lines":["l"]}],[{"start":{"row":25,"column":36},"end":{"row":25,"column":37},"action":"insert","lines":["s"],"id":37},{"start":{"row":25,"column":37},"end":{"row":25,"column":38},"action":"insert","lines":["e"]},{"start":{"row":25,"column":38},"end":{"row":25,"column":39},"action":"insert","lines":[","]}],[{"start":{"row":29,"column":45},"end":{"row":30,"column":0},"action":"insert","lines":["",""],"id":38},{"start":{"row":30,"column":0},"end":{"row":30,"column":8},"action":"insert","lines":["        "]}],[{"start":{"row":30,"column":8},"end":{"row":30,"column":65},"action":"insert","lines":["return _response(500, {'status':\"DynamoDB Client Error\"})"],"id":39}],[{"start":{"row":34,"column":22},"end":{"row":34,"column":23},"action":"insert","lines":["s"],"id":40}],[{"start":{"row":9,"column":39},"end":{"row":10,"column":0},"action":"insert","lines":["",""],"id":41}],[{"start":{"row":10,"column":0},"end":{"row":10,"column":5},"action":"insert","lines":["Limit"],"id":42}],[{"start":{"row":10,"column":5},"end":{"row":10,"column":6},"action":"insert","lines":[" "],"id":43},{"start":{"row":10,"column":6},"end":{"row":10,"column":7},"action":"insert","lines":["="]}],[{"start":{"row":10,"column":7},"end":{"row":10,"column":8},"action":"insert","lines":[" "],"id":44}],[{"start":{"row":10,"column":0},"end":{"row":10,"column":8},"action":"remove","lines":["Limit = "],"id":45},{"start":{"row":10,"column":0},"end":{"row":10,"column":1},"action":"insert","lines":["L"]},{"start":{"row":10,"column":1},"end":{"row":10,"column":2},"action":"insert","lines":["I"]},{"start":{"row":10,"column":2},"end":{"row":10,"column":3},"action":"insert","lines":["M"]},{"start":{"row":10,"column":3},"end":{"row":10,"column":4},"action":"insert","lines":["I"]},{"start":{"row":10,"column":4},"end":{"row":10,"column":5},"action":"insert","lines":["T"]}],[{"start":{"row":10,"column":5},"end":{"row":10,"column":6},"action":"insert","lines":[" "],"id":46},{"start":{"row":10,"column":6},"end":{"row":10,"column":7},"action":"insert","lines":["="]}],[{"start":{"row":10,"column":7},"end":{"row":10,"column":8},"action":"insert","lines":[" "],"id":47},{"start":{"row":10,"column":8},"end":{"row":10,"column":9},"action":"insert","lines":["1"]},{"start":{"row":10,"column":9},"end":{"row":10,"column":10},"action":"insert","lines":["0"]}],[{"start":{"row":26,"column":39},"end":{"row":27,"column":0},"action":"insert","lines":["",""],"id":48},{"start":{"row":27,"column":0},"end":{"row":27,"column":16},"action":"insert","lines":["                "]}],[{"start":{"row":27,"column":16},"end":{"row":27,"column":21},"action":"insert","lines":["Limit"],"id":49}],[{"start":{"row":27,"column":21},"end":{"row":27,"column":22},"action":"insert","lines":["="],"id":50},{"start":{"row":27,"column":22},"end":{"row":27,"column":23},"action":"insert","lines":["L"]},{"start":{"row":27,"column":23},"end":{"row":27,"column":24},"action":"insert","lines":["I"]},{"start":{"row":27,"column":24},"end":{"row":27,"column":25},"action":"insert","lines":["M"]},{"start":{"row":27,"column":25},"end":{"row":27,"column":26},"action":"insert","lines":["i"]}],[{"start":{"row":27,"column":26},"end":{"row":27,"column":28},"action":"insert","lines":["  "],"id":51}],[{"start":{"row":27,"column":27},"end":{"row":27,"column":28},"action":"remove","lines":[" "],"id":52},{"start":{"row":27,"column":26},"end":{"row":27,"column":27},"action":"remove","lines":[" "]},{"start":{"row":27,"column":25},"end":{"row":27,"column":26},"action":"remove","lines":["i"]}],[{"start":{"row":27,"column":25},"end":{"row":27,"column":26},"action":"insert","lines":["i"],"id":53}],[{"start":{"row":27,"column":25},"end":{"row":27,"column":26},"action":"remove","lines":["i"],"id":54}],[{"start":{"row":27,"column":25},"end":{"row":27,"column":26},"action":"insert","lines":["I"],"id":55}],[{"start":{"row":27,"column":22},"end":{"row":27,"column":26},"action":"remove","lines":["LIMI"],"id":56},{"start":{"row":27,"column":22},"end":{"row":27,"column":27},"action":"insert","lines":["LIMIT"]}],[{"start":{"row":27,"column":27},"end":{"row":27,"column":28},"action":"insert","lines":[","],"id":57}],[{"start":{"row":17,"column":55},"end":{"row":18,"column":0},"action":"insert","lines":["",""],"id":58},{"start":{"row":18,"column":0},"end":{"row":18,"column":4},"action":"insert","lines":["    "]},{"start":{"row":18,"column":4},"end":{"row":18,"column":5},"action":"insert","lines":["i"]}],[{"start":{"row":18,"column":5},"end":{"row":18,"column":6},"action":"insert","lines":["f"],"id":59}],[{"start":{"row":18,"column":6},"end":{"row":18,"column":7},"action":"insert","lines":[" "],"id":60}],[{"start":{"row":18,"column":7},"end":{"row":18,"column":48},"action":"insert","lines":["event[\"queryStringParameters\"][\"user_id\"]"],"id":61}],[{"start":{"row":18,"column":37},"end":{"row":18,"column":38},"action":"insert","lines":["."],"id":62},{"start":{"row":18,"column":38},"end":{"row":18,"column":39},"action":"insert","lines":["g"]},{"start":{"row":18,"column":39},"end":{"row":18,"column":40},"action":"insert","lines":["e"]},{"start":{"row":18,"column":40},"end":{"row":18,"column":41},"action":"insert","lines":["t"]}],[{"start":{"row":18,"column":41},"end":{"row":18,"column":42},"action":"remove","lines":["["],"id":63}],[{"start":{"row":18,"column":41},"end":{"row":18,"column":42},"action":"insert","lines":["("],"id":64}],[{"start":{"row":18,"column":51},"end":{"row":18,"column":52},"action":"remove","lines":["]"],"id":65}],[{"start":{"row":18,"column":51},"end":{"row":18,"column":52},"action":"insert","lines":[")"],"id":66},{"start":{"row":18,"column":52},"end":{"row":18,"column":53},"action":"insert","lines":[":"]}],[{"start":{"row":18,"column":43},"end":{"row":18,"column":50},"action":"remove","lines":["user_id"],"id":67},{"start":{"row":18,"column":43},"end":{"row":18,"column":44},"action":"insert","lines":["l"]},{"start":{"row":18,"column":44},"end":{"row":18,"column":45},"action":"insert","lines":["i"]},{"start":{"row":18,"column":45},"end":{"row":18,"column":46},"action":"insert","lines":["m"]},{"start":{"row":18,"column":46},"end":{"row":18,"column":47},"action":"insert","lines":["i"]},{"start":{"row":18,"column":47},"end":{"row":18,"column":48},"action":"insert","lines":["t"]}],[{"start":{"row":18,"column":51},"end":{"row":19,"column":0},"action":"insert","lines":["",""],"id":68},{"start":{"row":19,"column":0},"end":{"row":19,"column":8},"action":"insert","lines":["        "]}],[{"start":{"row":19,"column":8},"end":{"row":19,"column":9},"action":"insert","lines":["L"],"id":69},{"start":{"row":19,"column":9},"end":{"row":19,"column":10},"action":"insert","lines":["I"]},{"start":{"row":19,"column":10},"end":{"row":19,"column":11},"action":"insert","lines":["M"]}],[{"start":{"row":19,"column":8},"end":{"row":19,"column":11},"action":"remove","lines":["LIM"],"id":70},{"start":{"row":19,"column":8},"end":{"row":19,"column":13},"action":"insert","lines":["LIMIT"]}],[{"start":{"row":19,"column":13},"end":{"row":19,"column":14},"action":"insert","lines":[" "],"id":71},{"start":{"row":19,"column":14},"end":{"row":19,"column":15},"action":"insert","lines":["="]}],[{"start":{"row":19,"column":15},"end":{"row":19,"column":16},"action":"insert","lines":[" "],"id":72}],[{"start":{"row":19,"column":16},"end":{"row":19,"column":59},"action":"insert","lines":["event[\"queryStringParameters\"].get(\"limit\")"],"id":73}],[{"start":{"row":40,"column":69},"end":{"row":41,"column":0},"action":"insert","lines":["",""],"id":75},{"start":{"row":41,"column":0},"end":{"row":41,"column":8},"action":"insert","lines":["        "]}],[{"start":{"row":41,"column":4},"end":{"row":41,"column":8},"action":"remove","lines":["    "],"id":76}],[{"start":{"row":41,"column":4},"end":{"row":41,"column":5},"action":"insert","lines":["r"],"id":77},{"start":{"row":41,"column":5},"end":{"row":41,"column":6},"action":"insert","lines":["e"]},{"start":{"row":41,"column":6},"end":{"row":41,"column":7},"action":"insert","lines":["t"]},{"start":{"row":41,"column":7},"end":{"row":41,"column":8},"action":"insert","lines":["u"]},{"start":{"row":41,"column":8},"end":{"row":41,"column":9},"action":"insert","lines":["r"]},{"start":{"row":41,"column":9},"end":{"row":41,"column":10},"action":"insert","lines":["n"]}],[{"start":{"row":41,"column":10},"end":{"row":41,"column":11},"action":"insert","lines":[" "],"id":78}],[{"start":{"row":41,"column":11},"end":{"row":41,"column":12},"action":"insert","lines":["_"],"id":79},{"start":{"row":41,"column":12},"end":{"row":41,"column":13},"action":"insert","lines":["r"]},{"start":{"row":41,"column":13},"end":{"row":41,"column":14},"action":"insert","lines":["e"]},{"start":{"row":41,"column":14},"end":{"row":41,"column":15},"action":"insert","lines":["s"]}],[{"start":{"row":41,"column":11},"end":{"row":41,"column":15},"action":"remove","lines":["_res"],"id":80},{"start":{"row":41,"column":11},"end":{"row":41,"column":22},"action":"insert","lines":["_response()"]}],[{"start":{"row":41,"column":21},"end":{"row":41,"column":22},"action":"insert","lines":["2"],"id":81},{"start":{"row":41,"column":22},"end":{"row":41,"column":23},"action":"insert","lines":["0"]},{"start":{"row":41,"column":23},"end":{"row":41,"column":24},"action":"insert","lines":["0"]},{"start":{"row":41,"column":24},"end":{"row":41,"column":25},"action":"insert","lines":[","]}],[{"start":{"row":41,"column":25},"end":{"row":41,"column":26},"action":"insert","lines":[" "],"id":82},{"start":{"row":41,"column":26},"end":{"row":41,"column":27},"action":"insert","lines":["i"]},{"start":{"row":41,"column":27},"end":{"row":41,"column":28},"action":"insert","lines":["t"]}],[{"start":{"row":41,"column":26},"end":{"row":41,"column":28},"action":"remove","lines":["it"],"id":83},{"start":{"row":41,"column":26},"end":{"row":41,"column":31},"action":"insert","lines":["items"]}],[{"start":{"row":43,"column":4},"end":{"row":60,"column":4},"action":"remove","lines":["try:","        data = table.get_item(Key={\"PK\":PK, \"SK\":SK}, ReturnConsumedCapacity='TOTAL')","        ","        post_info = _parse_post_details(data[\"Item\"])","        ","        # response = table.get_item(Key={\"PK\":\"COMPANY#8fd4728b-89b6-40aa-a57a-85a4672ec9a0\", \"SK\":\"#METADATA#8fd4728b-89b6-40aa-a57a-85a4672ec9a0\"}, ReturnConsumedCapacity='TOTAL')","","    except ClientError as e:","        print(e.response['Error']['Message'])","        return _response(500, {'status':\"DynamoDB Client Error\"})","    except KeyError as e:","        print(e)","        return _response(404, {'status':\"ITEM NOT FOUND\"})","    else:","        consumed_cap = data[\"ConsumedCapacity\"]","        print(\"GetItem succeeded:\")","        print(json.dumps(data, indent=4, cls=DecimalEncoder))","    "],"id":84}],[{"start":{"row":43,"column":4},"end":{"row":47,"column":4},"action":"remove","lines":["    ","        ","    ","    return _response(200, post_info)","    "],"id":85},{"start":{"row":43,"column":0},"end":{"row":43,"column":4},"action":"remove","lines":["    "]},{"start":{"row":42,"column":0},"end":{"row":43,"column":0},"action":"remove","lines":["",""]}],[{"start":{"row":41,"column":32},"end":{"row":42,"column":0},"action":"remove","lines":["",""],"id":86}],[{"start":{"row":48,"column":15},"end":{"row":73,"column":126},"action":"remove","lines":["","","''' Post partition key generator '''","","def _get_post_meta(payload):","    import uuid","    time_now_rfc = _date_time_now()","    if not payload.get('post_id'):","        post_id = str(uuid.uuid4())","        created_at = time_now_rfc","        updated_at = time_now_rfc","    else:","        post_id = payload['post_id']","        updated_at = time_now_rfc","        created_at = payload.get('created_at')","    company_id = payload['company_id']","    user_id = payload['user_id']","    PK = \"COMPANY#\" + company_id","    SK = \"POST#\" + post_id","    post_title = payload['post_title']","    post_content = payload['post_content']","    can_share_on = payload.get('can_share_on')","    points_map = payload.get('points_map')","    ","    ","    return (PK, SK, company_id, user_id, post_id, post_title, post_content, can_share_on, points_map, created_at, updated_at,)"],"id":87}],[{"start":{"row":52,"column":16},"end":{"row":56,"column":61},"action":"remove","lines":["","        ","def _date_time_now():","    import datetime","    return str(datetime.datetime.utcnow().isoformat('T'))+'Z'"],"id":88}],[{"start":{"row":52,"column":16},"end":{"row":53,"column":0},"action":"insert","lines":["",""],"id":89},{"start":{"row":53,"column":0},"end":{"row":53,"column":4},"action":"insert","lines":["    "]}]]},"ace":{"folds":[],"scrolltop":180,"scrollleft":0,"selection":{"start":{"row":53,"column":4},"end":{"row":53,"column":4},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":{"row":12,"state":"start","mode":"ace/mode/python"}},"timestamp":1579491121392,"hash":"48ff8282f6592cd17c4ce8d523293506c532bf56"}