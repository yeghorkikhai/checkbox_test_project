from pydantic import BaseModel, Field


class UserAccessTokenSchema(BaseModel):
    access_token: str
    """JWT Auth Token"""


class UserSchema(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    login: str = Field(min_length=1, max_length=32)
