from abc import ABC, abstractmethod


class IUser(ABC):
    @abstractmethod
    def create(self, user):
        pass

    @abstractmethod
    def get_by_id(self, user_id: int):
        pass

    @abstractmethod
    def get_by_email(self, user_email: str):
        pass

    @abstractmethod
    def delete(self, user_id: int):
        pass

    @abstractmethod
    def update(self, user):
        pass
