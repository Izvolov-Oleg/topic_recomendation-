from typing import List

from fastapi import APIRouter

from app.models.user import UserPreferences
from app.services.recommendation import handler

router = APIRouter()


@router.post('/respond', response_model=List[List[str]])
async def respond(
        user_prefer: UserPreferences
):
    return handler(user_prefer)
