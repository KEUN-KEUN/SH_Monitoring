from fastapi import Request, HTTPException
from datetime import datetime

import json
import requests
import xmltodict
import json

from aiomysql import Pool

from api_if_test.service.api_test_service import ApiTestService

class ApiTestServiceImpl(ApiTestService):

    # 생성자
    def __init__(self, httpRequest: Request, db_pool: Pool):
        self.httpRequest = httpRequest
        

    async def api_test(self,test_name: str) -> str:
        try:

            # api 
            # http://openapi.seoul.go.kr:8088/704c465755686b533130384c656a6654/xml/citydata_ppltn/1/5/%EA%B4%91%ED%99%94%EB%AC%B8%C2%B7%EB%8D%95%EC%88%98%EA%B6%81
            url = f"http://openapi.seoul.go.kr:8088/704c465755686b533130384c656a6654/xml/citydata_ppltn/1/5/%EA%B4%91%ED%99%94%EB%AC%B8%C2%B7%EB%8D%95%EC%88%98%EA%B6%81"
            
            response = requests.get(url)
            response_dict = xmltodict.parse(response.content)
            data = response_dict
            print(json.dumps(data, indent=2, ensure_ascii=False))  # JSON 형식으로 출력
            

            # 현재 시간 가져오기
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 테스트 이름과 현재 시간을 JSON 형식으로 반환
            response_data = {
                "test_name": test_name,
                "timestamp": current_time
            }
            
            return json.dumps(response_data, ensure_ascii=False)

        except Exception as e:
            print(f"❌ ApiTestServiceImpl Error in api_test(): {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        

"url 호출 결과 값에 대해 response를 json 형식으로 받아서 print 해보고 싶다"