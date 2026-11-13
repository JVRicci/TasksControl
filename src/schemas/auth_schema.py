from pydantic import BaseModel, ConfigDict, Field


class AuthSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: str = Field(..., description="User email for login")
    password: str = Field(..., description="User password for login")
