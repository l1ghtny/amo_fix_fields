import re
from pprint import pprint

from fastapi import FastAPI, Request
from starlette.status import HTTP_200_OK

from api import add_info_from_ms, get_lead_by_id
from help_function import parse_the_cart_field, get_nested

app = FastAPI()


def insert_nested(data, keys, value):
    cur = data
    for k in keys[:-1]:
        if k not in cur:
            cur[k] = {}
        cur = cur[k]
    cur[keys[-1]] = value

@app.post("/lead_change")
async def lead_change(request: Request):
    form = await request.form()

    nested = {}
    for raw_key, value in form.items():
        # 'leads[update][0][id]' -> ['leads', 'update', '0', 'id']
        keys = re.findall(r'([^\[\]]+)', raw_key)
        insert_nested(nested, keys, value)

    ## parsing the specific lead_id

    goods = None
    delivery_type = None
    delivery_address = None

    lead_id = get_nested(nested, ["leads", "update", "0", "id"])
    if lead_id is None:
        lead_id = get_nested(nested, ["leads", "add", "0", "id"])

    print(f'LEAD_ID {lead_id}')

    if lead_id == '36334989':
        print('lead_id = 36334989')
        updates = get_nested(nested, ["leads", "update", "0", "custom_fields"])
        for updated_field in updates:
            info = updates[updated_field]
            if info['id'] == '576703':
                order_summary = info["values"]['0']['value']
                goods, delivery_type = await parse_the_cart_field(order_summary)
            if info['id'] == '576665':
                delivery_address = info["values"]['0']['value']
        # check if info is already correct
        current_info = await get_lead_by_id(lead_id)
        current_goods = get_nested(current_info, ["leads", "0", "custom_fields", "577313", "values"])
        current_delivery_type = get_nested(current_info, ["leads", "0", "custom_fields", "577315", "values"])
        current_delivery_address = get_nested(current_info, ["leads", "0", "custom_fields", "577311", "values"])
        if current_goods == goods and current_delivery_type == delivery_type and current_delivery_address == delivery_address:
            return HTTP_200_OK
        else:
            await add_info_from_ms(goods=goods, delivery_type=delivery_type, delivery_address=delivery_address, lead_id=lead_id)

            return HTTP_200_OK
    return HTTP_200_OK