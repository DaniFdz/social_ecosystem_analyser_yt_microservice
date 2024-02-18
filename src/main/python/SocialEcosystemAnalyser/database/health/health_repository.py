from abc import ABC, abstractmethod


class HealthRepository(ABC):
    @abstractmethod
    def check_health(self) -> bool:
        pass
