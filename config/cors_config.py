import os

from fastapi.middleware.cors import CORSMiddleware

class CorsConfig:

    # 클래스 레벨에서 데이터를 처리하거나, 클래스의 상태를 수정할 때 사용 
    # self 객체를 첫번째 이자로 받음 
    @classmethod
    def middlewareConfig(self, app):
        origins = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_hearders=["*"],
        )