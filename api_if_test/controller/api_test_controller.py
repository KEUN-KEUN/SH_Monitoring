from fastapi import APIRouter, Depends, HTTPException, status, Request, Body
from fastapi.responses import JSONResponse

from aiomysql import Pool

from async_db.database import getMySqlPool
#from api_if_test.service.api_test_service_impl import api_test
from api_if_test.service.api_test_service_impl import ApiTestServiceImpl

testingRouter = APIRouter()

# api 
# http://openapi.seoul.go.kr:8088/704c465755686b533130384c656a6654/xml/citydata_ppltn/1/5/%EA%B4%91%ED%99%94%EB%AC%B8%C2%B7%EB%8D%95%EC%88%98%EA%B6%81


# 의존성 주입
async def injectApiTest(httpRequest: Request, db_pool: Pool = Depends(getMySqlPool)) -> ApiTestServiceImpl:
    return ApiTestServiceImpl(httpRequest, db_pool)


@testingRouter.get("/apitest")
async def apiTestRead(
    apiService: ApiTestServiceImpl = Depends(injectApiTest),
):
    try:
        print("api_test 호출")

        await ApiTestServiceImpl.api_test(apiService, "api_test")

    except Exception as e:
        print(f"❌ Error in generateMarketingData(): {str(e)}")
        raise HTTPException(status_code=500, detail="서버 내부 오류 발생")
    
