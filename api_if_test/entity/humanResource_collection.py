from pydantic import BaseModel, field_validator, Field
from typing import List, Dict
from datetime import datetime


# Pydantic models matching the shared document format
class ForecastPpltn(BaseModel):
    FCST_TIME: datetime
    FCST_CONGEST_LVL: str
    FCST_PPLTN_MIN: int
    FCST_PPLTN_MAX: int


class CityDataPpltn(BaseModel):
    AREA_NM: str
    AREA_CD: str
    AREA_CONGEST_LVL: str
    AREA_CONGEST_MSG: str
    AREA_PPLTN_MIN: int
    AREA_PPLTN_MAX: int
    MALE_PPLTN_RATE: float
    FEMALE_PPLTN_RATE: float
    PPLTN_RATE_0: float
    PPLTN_RATE_10: float
    PPLTN_RATE_20: float
    PPLTN_RATE_30: float
    PPLTN_RATE_40: float
    PPLTN_RATE_50: float
    PPLTN_RATE_60: float
    PPLTN_RATE_70: float
    RESNT_PPLTN_RATE: float
    NON_RESNT_PPLTN_RATE: float
    REPLACE_YN: str
    PPLTN_TIME: datetime
    FCST_YN: str
    FCST_PPLTN: Dict[str, List[ForecastPpltn]]

    # 검증 로직을 테스트 형식으로 추가해봄
    @field_validator('AREA_NM', mode='before')
    @classmethod
    def parse_area_nm(cls, v):
        if v is None:
            raise ValueError("AREA_NM cannot be None")
        if not isinstance(v, str):
            raise TypeError("AREA_NM must be a string")
        return v.strip()

class ResultStatus(BaseModel):
    RESULT_CODE: str = Field(..., alias="RESULT.CODE")
    RESULT_MESSAGE: str = Field(..., alias="RESULT.MESSAGE")


class CityDataMap(BaseModel):
    SeoulRtd_citydata_ppltn: CityDataPpltn = Field(..., alias="SeoulRtd.citydata.ppltn")
    RESULT: ResultStatus


class APITestResponse(BaseModel):
    Map: CityDataMap

