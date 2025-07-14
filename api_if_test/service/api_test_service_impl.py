from fastapi import Request, HTTPException
from datetime import datetime

import json
import requests
import xmltodict
import json

from aiomysql import Pool
from typing import List, Dict

from api_if_test.service.api_test_service import ApiTestService

import aiohttp
import asyncio
import logging
import pandas as pd


# ✅ 로깅 설정
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)

class ApiTestServiceImpl(ApiTestService):

    # 생성자
    def __init__(self, httpRequest: Request, db_pool: Pool):
        self.httpRequest = httpRequest
        

    async def readCSV(self, file_path: str) -> list:
        try:
            # CSV 파일 읽기
            df = pd.read_csv(file_path)
            
            # DataFrame을 JSON 형식으로 변환
            data = df.to_dict(orient='records')
            
            return data

        except Exception as e:
            print(f"❌ ApiTestServiceImpl Error in readCSV(): {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))


    async def process_areas(self, area_data: List[Dict]) -> List[Dict]:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for area in area_data:
                area_name = area['AREA_NM']
                tasks.append(self.fetch_area_data(session, area_name))
            
            # asyncio.gather는 모든 비동기 작업을 동시에 실행하고 결과를 기다립니다.
            # 실행 결과의 순서는 tasks에 추가된 순서와 동일합니다.
            results = await asyncio.gather(*tasks)
            return results


    async def fetch_area_data(self, session, area_name):
        url = f"http://openapi.seoul.go.kr:8088/704c465755686b533130384c656a6654/xml/citydata_ppltn/1/5/{area_name}"

        async with session.get(url) as response:
            response_text = await response.text()
            response_dict = xmltodict.parse(response_text)
            return response_dict


    async def api_test(self,test_name: str) -> str:
        try:
            csv_file_path = "csv/seoulAreaList.csv"
            area_data = await self.readCSV(csv_file_path)

            start_time = datetime.now()
            # process_areaas 함수로 기준 정보를 모두 불러오기 위해 await 대기
            result = await self.process_areas(area_data)

            # 비동기 함수 확인을 위함             
            # area_nm = result[100]["Map"]["SeoulRtd.citydata_ppltn"]["AREA_NM"]

            # logging.info("** area_nm ****************************************")
            # logging.info(f"[api-test] First area name: {area_nm}")
            # logging.info("***************************************************")
                        
            end_time = datetime.now()
            totalTime = end_time - start_time
            
            logging.info(f"[api test] Total processing time: {totalTime} seconds")


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
        


