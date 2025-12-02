import os
from pprint import pprint

from dotenv import load_dotenv
import httpx

load_dotenv()

integration_id = os.environ.get('INTEGRATION_ID')
secret_key = os.getenv('SECRET_KEY')


current_token = os.getenv("TOKEN")
headers = {
    f'Authorization': f'Bearer {current_token}'
 }

async def auth():
    body = {
        'client_id': integration_id,
        'client_secret': secret_key,
        'grant_type': 'authorization_code',
        'code': '',
        'redirect_uri': 'https://new5a2e8ea7b16b4.amocrm.ru'
    }
    async with httpx.AsyncClient() as client:
        response = (await client.post('https://new5a2e8ea7b16b4.amocrm.ru/oauth2/access_token', data=body)).json()


async def get_lead_by_id(lead_id):
    async with httpx.AsyncClient() as client:
        response = (await client.get(f'https://new5a2e8ea7b16b4.amocrm.ru/api/v4/leads/{lead_id}', headers=headers)).json()
        return response


async def add_info_from_ms(goods, delivery_type, delivery_address, lead_id):

    custom_fields = []
    if goods:
        custom_fields.append(await create_custom_field(goods, 577313))
    if delivery_type:
        custom_fields.append(await create_custom_field(delivery_type, 577315))
    if delivery_address:
        custom_fields.append(await create_custom_field(delivery_address, 577311))




    body = {
        'id': lead_id,
        'custom_fields_values': custom_fields
    }
    async with httpx.AsyncClient() as client:
        response = await client.patch(f'https://new5a2e8ea7b16b4.amocrm.ru/api/v4/leads/{lead_id}', headers=headers, json=body)
        print(f'RESPONSE: {response}', f'RESPONSE JSON: {response.json()}')


async def create_custom_field(value, id):
    new_field = {
            'field_id': id,
            'values': [
                {
                    'value': value
                }
            ]
        }
    return new_field
