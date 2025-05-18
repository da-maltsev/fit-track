from typing import Annotated, TypeVar

from app.core.security import verify_token
from app.db.session import get_db
from app.models.models import User
from app.services import user as user_service
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession


__all__ = ["form_or_json", "get_current_user", "get_db"]

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/users/login",
    auto_error=False,
)

_TModel = TypeVar("_TModel", bound=BaseModel)


def form_or_json(model: type[_TModel]) -> _TModel:
    async def form_or_json_inner(request: Request) -> _TModel:
        type_ = request.headers["Content-Type"].split(";", 1)[0]
        if type_ == "application/json":
            data = await request.json()
        elif type_ == "application/x-www-form-urlencoded":
            data = await request.form()
        else:
            raise HTTPException(400)
        return model.model_validate(data)

    return Depends(form_or_json_inner)


async def get_current_user(
    token: Annotated[str | None, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    """Get the current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = verify_token(token)
    if user_id is None:
        raise credentials_exception

    user = await user_service.get_user(db, int(user_id))
    if user is None:
        raise credentials_exception

    return user
