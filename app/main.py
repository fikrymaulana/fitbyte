from fastapi import FastAPI
from fastapi.responses import JSONResponse

#bikin istance utama FastApi
app=FastAPI()


@app.get("/",tags=['misc'], include_in_schema=True)
def hello_world():
    return JSONResponse({"message": "hello World tommy"})