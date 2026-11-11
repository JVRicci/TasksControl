from pydantic import BaseModel, field_validator, model_validator


class TaskQuerySchema(BaseModel):
    user_id: int | None = None
    completed: bool | None = None

    @model_validator(mode="after")
    def require_user_for_status_filter(self):
        if self.completed is not None and self.user_id is None:
            raise ValueError("Informe user_id para filtrar por completed")

        return self

    @field_validator("completed", mode="before")
    @classmethod
    def parse_completed(cls, value: object) -> bool | None:
        if value is None or isinstance(value, bool):
            return value

        if isinstance(value, str):
            normalized_value = value.lower()
            if normalized_value == "true":
                return True
            if normalized_value == "false":
                return False

        raise ValueError("O parâmetro completed deve ser 'true' ou 'false'")
