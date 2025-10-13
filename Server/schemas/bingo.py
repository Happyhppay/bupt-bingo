from pydantic import BaseModel
from typing import List, Optional


class BingoGridBase(BaseModel):
    user_id: int
    grid_row: int
    grid_col: int
    is_lit: Optional[int] = 0


class BingoGridCreate(BingoGridBase):
    pass


class BingoGridUpdate(BaseModel):
    is_lit: Optional[int] = None
    lit_time: Optional[str] = None


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
    location: Optional[List[int]] = None  # [row, col]，仅 special 时需要


class LightBingoResponse(BaseModel):
    code: int
    message: str
    data: dict
