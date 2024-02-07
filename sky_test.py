import asyncio
import aiohttp
import BaseConfig
async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as response:
            return await response.text()

async def test():
    url1='http://'+BaseConfig.OWN_IP_OUT+':'+str(BaseConfig.OWN_PORT)+'/face/start'
    url2="http://"+BaseConfig.OWN_IP_OUT+':'+str(BaseConfig.OWN_PORT)+'/pose/start'

    tasks = [
        fetch(url1),
        fetch(url2)
    ]
    responses = await asyncio.gather(*tasks)
    print(responses)

asyncio.run(test())