from abc import ABC, abstractmethod

class ApiTestService(ABC):
    @abstractmethod
    def api_test(self, test_name: str) -> str:
        pass

    @abstractmethod
    def readCSV(self, file_path: str) -> list:
        pass

    @abstractmethod
    async def process_areas(self, area_data):
        pass

    @abstractmethod
    async def fetch_area_data(self, session, area_name):
        pass