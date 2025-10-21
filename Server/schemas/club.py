from pydantic import BaseModel
from typing import Optional


class RefreshClubQrcodeData(BaseModel):
    qrcodeToken: str

class RefreshClubQrcodeResponse(BaseModel):
    code: int
    message: str
    data: RefreshClubQrcodeData


class ScanQrcodeRequest(BaseModel):
    qrcodeToken: str

class ScanClubQrcodeData(BaseModel):
    addedPoint: int
    addedSpecialPoint: int

class ScanClubQrcodeResponse(BaseModel):
    code: int
    message: str
    data: ScanClubQrcodeData
