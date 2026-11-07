from abc import ABC, abstractmethod


class ITask(ABC):
    @abstractmethod
    def create(self, task):
        pass

    @abstractmethod
    def get_by_id(self, task_id: int):
        pass

    @abstractmethod
    def update(self, task):
        pass

    @abstractmethod
    def delete(self, task_id: int):
        pass
