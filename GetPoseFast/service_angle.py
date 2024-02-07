from fastapi import APIRouter

router = APIRouter(
    prefix="/pose",
    tags=["pose"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/me")
async def read_user_me():
    return {"username": "fakecurrentuser"}
