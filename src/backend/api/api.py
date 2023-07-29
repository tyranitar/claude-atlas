from fastapi import APIRouter

from api.endpoints import hello_world

api_router = APIRouter()
api_router.include_router(hello_world.router, tags=["hello_world"])
