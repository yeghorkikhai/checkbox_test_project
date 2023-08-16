from pydantic import BaseModel


class UserAccessTokenSchema(BaseModel):
    access_token: str


class UserSchema(BaseModel):
    name: str
    login: str
