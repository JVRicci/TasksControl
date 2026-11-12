from abc import ABC, abstractmethod


class IRepository(ABC):
    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def get_by_id(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass
