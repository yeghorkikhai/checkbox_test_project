from pydantic import BaseModel


class UserAccessTokenSchema(BaseModel):
    access_token: str
