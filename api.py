import os
from pprint import pprint

from dotenv import load_dotenv
import httpx

load_dotenv()

integration_id = os.environ.get('INTEGRATION_ID')
secret_key = os.getenv('SECRET_KEY')


current_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjI2NjA2YjFiYjA3NDdmYzgyMmYwMzEzZTNiOGJjMzRmYzkyNTM2ZDBiZGRlNGEzN2E2MDYxYTgyYmZkOTUzNGEwZGJjOTFkOGFlNzRmMWZjIn0.eyJhdWQiOiJlOTJhMzIzMC05ZDhmLTRmZjEtOGM0ZS00YTVmYjNhMjUwYmEiLCJqdGkiOiIyNjYwNmIxYmIwNzQ3ZmM4MjJmMDMxM2UzYjhiYzM0ZmM5MjUzNmQwYmRkZTRhMzdhNjA2MWE4MmJmZDk1MzRhMGRiYzkxZDhhZTc0ZjFmYyIsImlhdCI6MTc2NDU5NTc0NCwibmJmIjoxNzY0NTk1NzQ0LCJleHAiOjE3NjcyMjU2MDAsInN1YiI6IjEzMDA5MTIyIiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjE3NjMxNzA2LCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJjcm0iLCJmaWxlcyIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiLCJwdXNoX25vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiNTIzMWQ2NzEtYzQ4Ni00Njc0LTljMzUtMzMyNDBmNjA3OTdhIiwidXNlcl9mbGFncyI6MCwiYXBpX2RvbWFpbiI6ImFwaS1iLmFtb2NybS5ydSJ9.er482wjD6HlBaWyvw9IY_IUsORucgLeaOy-zv29byGzHNO0_xFajzCV-yQzCGGYZNMTQbBC_aSvh__XVkZOru_HxivK6cKCR6XIcskxJQki-HBbmxJ-yXG-b3pCaDQ7_nBzQNmwlzwdmVyyiQTo_YFoNbhccNbXAO827n_S4GVy2KNqpJk15yq4QPAu9ei_rj_T9SAtp587ugV93GYJeZYdaxS1uHRjoYaZG15wdsvJCjv5p4XhO6dUkfBi-c7aCEG-h0gdb8ewuF4QlR_ob1hgrhrI5gjmvDSacQC4jfBRtBP73ebEbnjqT9pv5EwKr7CKifjPfpITijLGtX_p2hg"

headers = {
    f'Authorization': f'Bearer {current_token}'
 }

async def auth():
    body = {
        'client_id': integration_id,
        'client_secret': secret_key,
        'grant_type': 'authorization_code',
        'code': 'def5020093463e984c956d5b3258cfad73c1387473a85cd733b384576db0555198b3f674efacec89407f4a055d619eee71b693c80a3ae045e05418a0ef2a098ebbf43f9f0405c56ac3c419bd9e3479d0f6fca16146fdf7b0ca844a3563bed928d79dfcfb2e0445314bea6d470b5c36aaeb146bb58647078e7829cb190ef600f1072dd36ecd7230cd7e6ae4830bf0e251d5321f7f5d564d77f2cd597e2508423fb391f05760d10f4c88d1d4ba783c62852b489510dba58e0e2540ba54e93afcafda77a7b0a29d1b35c20d1c6da55fcb4733224d1b0e66e2f2caea774071d6efd717403e17906a0e48af31ca1e5e3a50246a64070cdea3b48417b719a060b8cc4a44cd6736cf82d207c4c1288c3d3ecf20b93e413fa138d243b542c6db85e154aa606a0a3066b675e6e0d882832e7ccbfbceea0e6d417438f08bfbdd79b198f144c59127b62164395a1bf152ed19415a6a3cb7bf0a354e7e84e16bbe7549cf0bbf3815403bcbb7ee56ac16f1efff5318ae529758ca8c15b91ccdef1f636f46f532aff17bc2573005a4a7997846b36ffb6988badaefa6b5c46606d6efc80d2ce796a5f6ade82be70998ecc9c082cd5af915cffaefa422db2ba94edda6cc5d98f6066a2dd446980c9449fc5c75299a60a889737aa15f7924fffd2fc1fe3846bdae55ceede77e0b8fdba81f5fa3ae6c9031d76a26ac',
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



if __name__ == '__main__':
    import asyncio
    asyncio.run(get_lead_by_id(36334989))
    # asyncio.run(auth())


old_info = '''
{'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImVmZTllNTA0NjFmOTM4NzNjZjNhNzE0OTg0NzI2ZmUzNjU3ZGU4Zjc5MTkzM2U0NmU2YTkxODVmNzAyYmY5YTY5NWEzMGVkN2ZjODI1N2RkIn0.eyJhdWQiOiJlOTJhMzIzMC05ZDhmLTRmZjEtOGM0ZS00YTVmYjNhMjUwYmEiLCJqdGkiOiJlZmU5ZTUwNDYxZjkzODczY2YzYTcxNDk4NDcyNmZlMzY1N2RlOGY3OTE5MzNlNDZlNmE5MTg1ZjcwMmJmOWE2OTVhMzBlZDdmYzgyNTdkZCIsImlhdCI6MTc2NDU5NDcyNSwibmJmIjoxNzY0NTk0NzI1LCJleHAiOjE3NjQ2ODExMjUsInN1YiI6IjEzMDA5MTIyIiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjE3NjMxNzA2LCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJwdXNoX25vdGlmaWNhdGlvbnMiLCJmaWxlcyIsImNybSIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiYjIzYmQwYTctMmUwYS00ZDM0LTgyYTgtOWVmZmQ2YzA2YjQ0IiwidXNlcl9mbGFncyI6MCwiYXBpX2RvbWFpbiI6ImFwaS1iLmFtb2NybS5ydSJ9.E5JqzNU7ox0q1Fha-5wJAjRVpbG_NvVcvH3DNgEi16zyxg9dMJVs-ng2dfAkCyX9Vtsq2P6o0TdHL5UrdT9bRw60rDfc9w4JsmA6xpAzRksjHeBn3Y4ZNqGflq9Oig1LyJ6GKLA3-Utuay0y-zyMn5OwZWl8RVfkgiaFwfEgcbuPbDrwYnqX8fmLqr_3mPxgpnI4TVIar0ILavyvc6_tAyuX59w0--GxbpuDEGKRv125amSqvDqisrI-iE-bfuiJDVSPo0Q_Tmy2fLoncVXTKclTiobpVop9pcwjvGKMULWj5iaUP1p9dc_gXcc_PNmrPTmEwW4se9fNeWDUu4oY_w',
 'expires_in': 86400,
 'refresh_token': 'def50200b9e44364474379a03ebf00bb8d6e8678c9b59331a01431b29819315a26181f2dbad129f35bac3df9d54298589f63e4d138a825ff08410511ae90164bffb54b361aeecff38cf436da4a41812c5bc8ced23773851c640cb212a03a2b21dc31c3831d38534ce6d8aafc970e07ccc2185714931d9684dfb574bf27e4ebfa7a099e4fb56bf35512162b2ff8cbee1c7293786c73d1ac88435f330cc51d5f63ab85cd7706d91ce26b7294cd1d2a47ac77a737e281ef32b8f8fcde756ccb8d20c1823a73087f273e24ab82d89709f25cc87397f6137d0ccfe1ca0db138df133f6274bbeca017d53ea39fc640c04ed3b97c35b5ebde8b858c81f533b08976dc9d5656625d5ac96212711abbe91dd90568747ec1e4d3383392957eb1e25a145ee6a0982c5d757deb9b731192818e8f81cabe27c82f5e0173e56bf09572ff28e6f5265f6a2ef0c3f8a88cf85f0305480cf29b1355bb9c0508e5243638eaf59f3d35af5d130762ef7eaaed800bdf27d888653f46b755349b1200a967869c0e9dc6bbac127af372468ee03187aa321f3d07bc10b58cce7d69300380b294ac99767461d9980a481dba7d0644f9987f02f6645c6c6d4b1640bf7f608aaa2039fb380bbbddc96013feca1dce44d17e299a0bd78797bacd0c38c9b5180b3ce578a2ea85e4745f4e6d661a00459c504c6104a2',
 'server_time': 1764594725,
 'token_type': 'Bearer'}

Process finished with exit code 0'''
