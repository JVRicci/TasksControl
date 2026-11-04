from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., description="Username")
    email: EmailStr = Field(..., description="User e-mail")
    password: str = Field(..., description="User password")


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="User identifier")
    name: str = Field(..., description="Username")
    email: EmailStr = Field(..., description="User e-mail")
    password: str = Field(..., description="User password")
