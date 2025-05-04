from fastapi import FastAPI
from app.api.tron_routes import router
from app.core.deps import db

import uvicorn


app = FastAPI()


@app.on_event("startup")
async def startup():
    await db.initialize()

@app.get('/')
async def root():
    return {'msg': 'Tron API Is Running'}

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
