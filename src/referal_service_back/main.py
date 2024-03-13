from fastapi import FastAPI
import uvicorn
from auth.router import router
from referal.repository import CodeRepository, ReferalshipRepository


app = FastAPI()

@app.get('/')
async def ping_service():
    return {
        'Service': 'Referals'
    }


app.include_router(router=router, prefix='/auth', tags=['AUTH endpoints'])

@app.get('/codes/list')
async def get_all_ref():
    return await CodeRepository.get_all()

@app.get('/refers/list')
async def get_all_ref():
    return await ReferalshipRepository.get_all()


if __name__=='__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=8000)