import os
import asyncio
import warnings
import aiomysql

from fastapi import FastAPI
from config.cors_config import CorsConfig # 설정 파일 보안 등 
from config.initializer import lifespan   # app의 생명 주기 관리


app = FastAPI(lifespan=lifespan)

print(123)