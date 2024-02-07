import uvicorn

import BaseConfig
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from GetPoseFast import service_angle
from GetFaceFast import service_face
from SkyLogger import get_current_time,get_logger
from RMQ import rmq_send,rmq_recv
import time
import aiohttp
import asyncio

app = FastAPI()
app.include_router(service_angle.router)
app.include_router(service_face.router)
origins = [
    "*",
]

logger=get_logger('main')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class testModel(BaseModel):
    name:str
    age:int

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/mytest/")
async def mytest(test: testModel):
    print(test)
    return {"message": f"Hello {test.name}"}

@app.post("/skysendtest")
def skysendtest():
    print('send test start')
    cnt=0
    while True:
        time.sleep(1)
        rmq_send(get_current_time()+" this is "+str(cnt)+" times.")
        cnt=cnt+1

@app.post("/skyrecvtest")
def skysendtest():
    print('recv test start')
    rmq_recv()

# async def fetch(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.post(url) as response:
#             return await response.text()
# async def start_services():
#     url1='http://'+BaseConfig.OWN_IP_OUT+':'+str(BaseConfig.OWN_PORT)+'/face/start'
#     url2="http://"+BaseConfig.OWN_IP_OUT+':'+str(BaseConfig.OWN_PORT)+'/pose/start'
#     tasks = [
#         fetch(url1),
#         fetch(url2)
#     ]
#     responses = await asyncio.gather(*tasks)
#     print(responses)
#   asyncio.run(start_services())

if __name__ == '__main__':
    logger.info('start server...')
    uvicorn.run("main:app",host=BaseConfig.OWN_IP,port=BaseConfig.OWN_PORT,reload=True,)
    # logger.info('down server...')
