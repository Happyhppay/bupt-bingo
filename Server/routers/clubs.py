# routers/clubs.py
from fastapi import APIRouter, Depends
from schemas import QrcodeTokenResponse, ScanResponse
from utils import generate_hash_token
from database import SessionLocal
from models import QrcodeToken, Club, ScanRecord, User
from dependencies import require_role

router = APIRouter(prefix="/clubs", tags=["社团"])

@router.get("/qrcode", response_model=QrcodeTokenResponse, dependencies=[Depends(require_role("club"))])
def refresh_qrcode():
    db = SessionLocal()
    # 假设当前社团名为“动漫社”（实际从 session 获取）
    club_name = "动漫社"
    token_str = generate_hash_token("club", club_name)

    # 失效旧 token
    db.query(QrcodeToken).filter(QrcodeToken.club_name == club_name).update({"used": True})
    new_token = QrcodeToken(token=token_str, club_name=club_name, used=False)
    db.add(new_token)
    db.commit()

    db.close()
    return {
        "code": 200,
        "msg": "二维码生成成功",
        "data": {"qrcodeToken": token_str}
    }

@router.post("/scan", response_model=ScanResponse)
def scan_qrcode(body: dict, current_user=Depends(get_current_user)):
    token = body.get("qrcodeToken")
    db = SessionLocal()

    user_id = current_user["sub"]
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    qtoken = db.query(QrcodeToken).filter(QrcodeToken.token == token).first()
    if not qtoken or qtoken.used:
        raise HTTPException(status_code=400, detail="二维码无效或已使用")

    # 检查是否重复扫描
    exists = db.query(ScanRecord).filter(
        ScanRecord.user_id == user.id,
        ScanRecord.club_name == qtoken.club_name
    ).first()

    if exists:
        db.close()
        return {
            "code": 200,
            "msg": "积分获取成功",
            "data": {"addedPoint": 0, "addedSpecialPoint": 0, "isDuplicate": True}
        }

    # 新增积分
    added_point = 1
    added_special = 1 if qtoken.club_name == "神秘社团" else 0  # 特殊社团示例

    user.point += added_point
    user.special_point += added_special
    db.add(ScanRecord(user_id=user.id, club_name=qtoken.club_name))
    qtoken.used = True

    db.commit()
    db.refresh(user)

    db.close()
    return {
        "code": 200,
        "msg": "积分获取成功",
        "data": {
            "addedPoint": added_point,
            "addedSpecialPoint": added_special,
            "isDuplicate": False
        }
    }