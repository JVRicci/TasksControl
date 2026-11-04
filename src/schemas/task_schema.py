from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class TaskCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = Field(..., description="Task name")
    description: str = Field(..., description="Task description")
    completed: bool = Field(False, description="Task status")

    user_id: int = Field(..., description="User identifier")


class TaskResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Task identifier")
    title: str = Field(..., description="Task name")
    description: str = Field(..., description="Task description")
    completed: bool = Field(False, description="Task status")

    user_id: int = Field(..., description="User identifier")
