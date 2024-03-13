from fastapi import FastAPI
import uvicorn
from auth.router import router

app = FastAPI()

@app.get('/')
async def ping_service():
    return {
        'Service': 'Referals'
    }


app.include_router(router=router, prefix='/auth', tags=['AUTH endpoints'])


if __name__=='__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=8000)