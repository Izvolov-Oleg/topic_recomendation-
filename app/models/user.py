from pydantic import BaseModel
from typing import List


class UserPreferences(BaseModel):
    active_skills: List[List[str]]
    cobot_topics: List[List[str]]
