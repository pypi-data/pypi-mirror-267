import datetime
from pydantic import BaseModel


class Prompt(BaseModel):
    title: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    author_id: int
    upvotes: int
    version: int

    def __str__(self):
        return self.title


class PromptUpvote(BaseModel):
    prompt_id: int
    user_id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class PromptShare(BaseModel):
    prompt_id: int
    user_id: int
    created_at: datetime.datetime


class PromptCreation(BaseModel):
    prompt_id: int
    user_id: int
    creation: str
    created_at: datetime.datetime


class PromptFork(BaseModel):
    original_prompt_id: int
    forked_prompt_id: int
    user_id: int
    created_at: datetime.datetime
