import asyncio
import json
import time
import aiohttp
import logging

headers = {
        'token': '************************',
        'Content-Type': 'application/json'
    }


async def create_order(phone_number):
    url = "Указываем API"

    payload = json.dumps({
        "expired_at": "2022-12-12 23:59:59",
        "order_type": 3,
        "pharmacy_id": 1490,
        "stock_id": 718649,
        "phone": phone_number,
        "products": [
            {
                "count": 1,
                "price": 40,
                "product_id": "321235"
            }
        ],
        "source": "kassa"
    })

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.post(url, headers=headers, data=payload) as resp:
            return await resp.json()


async def set_status(order_number, status):
    url = "Указываем API" + order_number

    payload = json.dumps({
        "status": status,
        "expired_at": "2022-09-11 01:01:01",
        "comment": "string"
    })
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.put(url, headers=headers, data=payload) as resp:
            return await resp.json()


async def main():
    order_number = (await create_order(PHONE)).get('order_number')
    if order_number:
        for status in [2, 3, 5]:
            resp_status = (await set_status(order_number, status)).get('status')
            time.sleep(10)
            if resp_status == status:
                print(f'status is set {resp_status}')
            else:
                print(f'status setting error {status}')
    else:
        print('NO ORDER NUMBER')


if __name__ == "__main__":
    logger = logging.getLogger('logger')
    logger.propagate = False
    PHONE = "Указываем номер"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
