from fastapi import (
    Depends,
    APIRouter,
    HTTPException,
    Query,
)
from typing import Annotated, List

from opencredit.server.models import V1Principal
from opencredit.auth.transport import get_current_principal


router = APIRouter()


@router.post("/v1/credits")
async def create_credit(
    current_user: Annotated[V1Principal, Depends(get_current_principal)],
):
    pass
