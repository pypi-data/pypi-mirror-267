from abc import ABC, abstractmethod


class BaseCutter(ABC):
    @abstractmethod
    def __call__(self, text, max_chunk_length):
        pass
