from fastapi import APIRouter

from api.endpoints import hello_world, predict

api_router = APIRouter()
api_router.include_router(hello_world.router)
api_router.include_router(predict.router)
