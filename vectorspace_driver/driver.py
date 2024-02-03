from abc import ABC, abstractmethod

class VectorspaceDriver(ABC):
    @abstractmethod
    def insert(self, vectors):
        pass

    @abstractmethod
    def preprocess_vector(self, text, id, metadata=None):
        pass
