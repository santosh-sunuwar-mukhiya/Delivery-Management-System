from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import jwt

from app.database.models import Seller
from app.utils import decode_access_token

from ..dependencies import SellerServiceDep, SessionDep
from ..schemas.seller import SellerCreate, SellerRead

from app.core.security import oauth2_scheme

router = APIRouter(prefix="/seller", tags=["Seller"])


### Register a seller
@router.post("/signup", response_model=SellerRead)
async def register_seller(
    seller: SellerCreate,
    service: SellerServiceDep
):
    return await service.add(seller)


@router.post("/token")
async def login_seller(
    request_form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: SellerServiceDep,
):
    token = await service.token(request_form.username, request_form.password)  # type: ignore
    return {
        "access_token": token,
        "type": "jwt",
    }
