from abc import ABC, abstractmethod
from typing import List
from executors.base import Executor

class Provider(ABC):
    @abstractmethod
    def get_executors(self) -> List[Executor]:
        pass
