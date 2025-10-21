from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class BingoStatusData(BaseModel):
    point: int
    specialPoint: int
    bingoGrid: List[List[int]]
    rewards: List[int]

class BingoStatusResponse(BaseModel):
    code: int
    message: str
    data: BingoStatusData


class LightBingoRequest(BaseModel):
    pointType: str
    location: Optional[List[int]] = None


class LightBingoResponse(BingoStatusResponse):
    pass
