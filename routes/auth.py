from fastapi import APIRouter

auth_router = APIRouter()


@auth_router.post(path="/login")
async def login():
    pass


@auth_router.post("/register")
async def register():
    pass
