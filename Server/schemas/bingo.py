from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class BingoGridBase(BaseModel):
    user_id: int
    grid_row: int
    grid_col: int
    is_lit: Optional[int] = 0


class BingoGridCreate(BingoGridBase):
    pass


class BingoGridUpdate(BaseModel):
    grid_data: Optional[str] = None
    lit_time: Optional[datetime] = None


class BingoGrid(BingoGridBase):
    id: int
    lit_time: Optional[str]

    class Config:
        orm_mode = True


class BingoStatusResponse(BaseModel):
    code: int
    message: str
    data: dict


class LightBingoRequest(BaseModel):
    pointType: str  # normal 或 special
    # location 使用 1-based 索引：[row, col]，仅 special 时需要，范围均为 1..5
    location: Optional[List[int]] = None  # [row, col]


class LightBingoResponse(BaseModel):
    code: int
    message: str
    data: dict
