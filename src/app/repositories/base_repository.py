import abc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generic, TypeVar, Type, Optional
T = TypeVar("T")


class BaseRepository(abc.ABC,Generic[T]):
    """
    Abstract base class for repositories.
    Defines the interface for basic CRUD operations.
    """

    def __init__(self, model: Type[T], session: AsyncSession):
        """
        Initialize the repository with a model and a database session.

        Args:
            session (AsyncSession): SQLAlchemy async session.
        """
        self.model = model
        self.session = session


    @abc.abstractmethod
    def get_one(self, item_id: int):
        """
        Retrieve a single item by its ID.

        Args:
            item_id (int): The ID of the item to retrieve.

        Returns:
            The item instance.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_many(self, limit: int, offset: int):
        """
        Retrieve multiple items with pagination.

        Args:
            limit (int): Maximum number of items to retrieve.
            offset (int): Number of items to skip.

        Returns:
            List of item instances.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, item):
        """
        Add a new item to the repository.

        Args:
            item: The item instance to add.

        Returns:
            The result of the add operation.
        """
        raise NotImplementedError
    
    # @abc.abstractmethod
    # def add_user(self, item):
    #     """
    #     Add a new item to the repository.

    #     Args:
    #         item: The item instance to add.

    #     Returns:
    #         The result of the add operation.
    #     """
    #     raise NotImplementedError
        