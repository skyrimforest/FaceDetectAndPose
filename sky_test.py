import asyncio
import aiohttp

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as response:
            return await response.text()

async def test():
    url1 = 'http://192.168.0.107:8000/skysendtest'
    url2 = 'http://192.168.0.107:8000/skyrecvtest'

    tasks = [
        fetch(url1),
        fetch(url2)
    ]
    responses = await asyncio.gather(*tasks)
    print(responses)

asyncio.run(test())