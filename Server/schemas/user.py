from pydantic import BaseModel

class UserLoginRequest(BaseModel):
    student_id: int

class userInfo(BaseModel):
    studentId: int
    firstEnterTime: str
    role: str

class UserLoginData(BaseModel):
    userToken: str
    userInfo: userInfo

class UserLoginResponse(BaseModel):
    code: int
    message: str
    data: UserLoginData


class VerifyInviteCodeRequest(BaseModel):
    inviteCode: str

class VerifyInviteCodeData(BaseModel):
    role: str
    clubName: str
    newToken: str

class VerifyInviteCodeResponse(BaseModel):
    code: int
    message: str
    data: VerifyInviteCodeData
