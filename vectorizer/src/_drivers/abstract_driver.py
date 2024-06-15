from abc import ABC, abstractmethod

class IVectorspaceDriver(ABC):
    RECOMMENDED_BATCH_SIZE = None

    @abstractmethod
    def insert(self, vectors: list, vectorspace: str):
        """
        Inserts a list of vectors to the vector db in a specific vectorspace.
        :param vectors: The list of vectors to insert to the database.
        :param vectorspace: A string that identifies the vectorspace the vectors should enter. 
                            A vectorspace allows for distinction between different-purpose vectors.
        """
        pass

    @abstractmethod
    def create_vector(self, text: str, id: str, metadata: dict = None) -> dict:
        """
        Takes text and creates a preprocessed vector embedding from it.
        :param text: The string to create a text vector embedding from.
        :param id: A unique identifier for the vector embedding inside the vector db.
        :param metadata: Optional additional metadata to be stored inside the vector db.
        :returns: A preprocessed vector embedding object, ready to be inserted into the db.
        """
        pass
