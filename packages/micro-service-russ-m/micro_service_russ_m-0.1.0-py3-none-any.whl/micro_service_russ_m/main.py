from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def check_health():
    return {"status": "server is up; ok"}


@app.get('/greet/{name}')
async def greet(name: str):
    return {'message': f'Hello, {name}!'}