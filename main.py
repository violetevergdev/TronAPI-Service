from fastapi import FastAPI

from app.api.tron_routes import router
from app.lifespan import lifespan

app = FastAPI(lifespan=lifespan)

@app.get('/')
async def root():
    return {'msg': 'Tron API Is Running'}

app.include_router(router)

if __name__ == '__main__':
    import uvicorn

    uvi_conf = uvicorn.Config(
        app='main:app',
        host='127.0.0.1',
        port=8000,
        reload=True,
        timeout_graceful_shutdown=10
    )
    server = uvicorn.Server(uvi_conf)
    server.run()
