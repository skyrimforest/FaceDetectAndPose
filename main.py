import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from GetPoseFast import service_angle
app = FastAPI()
app.include_router(service_angle.router)
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

if __name__ == '__main__':
    uvicorn.run("main:app",host="0.0.0.0",port=8000,reload=True)
