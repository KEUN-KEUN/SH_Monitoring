from abc import ABC, abstractmethod
from typing import List, Dict
from api_if_test.entity.humanResource_collection import APITestResponse

class APITestRepository(ABC):

    @abstractmethod
    def test_create(selft, data: APITestResponse) -> None:
        pass

    @abstractmethod
    def test_findAll(self) -> List[APITestResponse]:
        pass

    @abstractmethod
    def test_findById(self, id: str) -> APITestResponse:
        pass

    @abstractmethod
    def test_update(self, id: str, data: APITestResponse) -> None:
        pass

    @abstractmethod
    def test_delete(self, id: str) -> None:
        pass

    @abstractmethod
    def test_deleteByAreaNm(self, area_nm: str) -> None:
        pass