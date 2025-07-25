from typing import Dict
from fastapi import Request

from api_if_test.repository.apiTest_repository import APITestRepository
from api_if_test.entity.humanResource_collection import APITestResponse


class APITestRepositoryImpl(APITestRepository):
    def __init__(self, httpRequest: Request):
        # self.api_client = api_client
        self.httpRequest = httpRequest
        self.vector_db =  self.httpRequest.app.state.vectorDBPool

    async def test_create(self, data: APITestResponse) -> None:
        # VectorDB 호출
        # print("******************************************************")
        # print(data)
        # print("******************************************************")

        vector_db = self.vector_db
        # Insert data into the humanResource collection
        collection = vector_db.humanResource
        for area in data:
            await collection.insert_one(area)


