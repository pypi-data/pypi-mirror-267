from abc import ABC, abstractmethod


class BaseJoiner(ABC):
    @abstractmethod
    def __call__(self, chunks, separators):
        pass
