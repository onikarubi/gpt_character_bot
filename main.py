from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
import pydantic

class SamplePost(pydantic.BaseModel):
    x: int
    y: int

app = FastAPI()

@app.get('/')
def root():
    return {'message': 'hello'}


@app.post('/')
def calc(data: SamplePost):
    result = data.x * data.y
    return JSONResponse(result)


