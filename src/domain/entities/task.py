class Task:
    def __init__(
        self,
        id: int | None,
        title: str,
        description: str,
        completed: bool,
        user_id: int,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
        self.user_id = user_id
