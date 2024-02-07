import uvicorn

import BaseConfig
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from GetPoseFast import service_angle
from GetFaceFast import service_face
from SkyLogger import get_current_time
from RMQ import rmq_send,rmq_recv
import time
app = FastAPI()
app.include_router(service_angle.router)
app.include_router(service_face.router)
origins = [
    "*",
]

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

if __name__ == '__main__':
    uvicorn.run("main:app",host=BaseConfig.OWN_IP,port=BaseConfig.OWN_PORT,reload=True)