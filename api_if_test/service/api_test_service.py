from abc import ABC, abstractmethod

class ApiTestService(ABC):
    @abstractmethod
    def api_test(self, test_name: str) -> str:
        pass