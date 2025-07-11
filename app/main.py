import os
import asyncio
import warnings
import aiomysql

from dotenv import load_dotenv
from fastapi import FastAPI

from config.cors_config import CorsConfig # 설정 파일 보안 등 
from config.initializer import lifespan   # app의 생명 주기 관리

from api_if_test.controller.api_test_controller import testingRouter  # API 테스트 컨트롤러

# 초기 설정
warnings.filterwarnings("ignore", category=aiomysql.Warning)
load_dotenv()

# FastAPI 앱 초기화
app = FastAPI(lifespan=lifespan)

# CORS 설정
CorsConfig.middlewareConfig(app)

# 웹소켓 연결 상태 저장소
app.state.connections = set()

# 라우터 등록
app.include_router(testingRouter)
 
# 앱 실행
if __name__ == "__main__":
    import uvicorn

    host = os.getenv("APP_HOST")
    port = int(os.getenv("APP_PORT"))

    print("********************** app 실행 **********************")    
    print(f"Starting FastAPI app on {host}:{port}")

    uvicorn.run(app, host=host, port=port)

