from fastapi import APIRouter

router = APIRouter(prefix="/dishes", tags=["dishes"])


@router.get("")
def list_dishes():
    return []
