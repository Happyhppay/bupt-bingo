from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from crud.user_scan import get_by_user_id_and_club_id, record_user_scan
from database import get_db
from schemas.club import QrcodeRefreshResponse, ScanQrcodeRequest, ScanQrcodeResponse
from crud.qrcode_token import create_qrcode_token, get_valid_unused_token, update_qrcode_token_status
from crud.club import get_club
from crud.user import update_user_points
from dependencies import get_current_club_member, get_current_user
from utils import generate_club_qrcode_token, limiter

router = APIRouter(
    prefix="/clubs",
    tags=["clubs"]
)


@router.get("/qrcode", response_model=QrcodeRefreshResponse)
@limiter.limit("1/second")
def refresh_club_qrcode(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_club_member)
):
    """刷新社团二维码（社团成员）"""
    # 检查用户是否关联了社团
    if not current_user.club_id:
        raise HTTPException(status_code=400, detail="User not associated with any club")

    # 获取社团信息
    club = get_club(db, club_id=current_user.club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")

    # 生成新的二维码token
    token = generate_club_qrcode_token(club.id)
    create_qrcode_token(db, token=token, club_id=club.id)

    return {
        "code": 200,
        "message": "Success",
        "data": {
            "qrcodeToken": token
        }
    }


@router.post("/scan", response_model=ScanQrcodeResponse)
@limiter.limit("5/minute")
def scan_club_qrcode(
        scan_request: ScanQrcodeRequest,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    """扫描社团二维码获取积分（普通用户）"""
    token = scan_request.qrcodeToken

    # 验证token有效性
    qrcode_token = get_valid_unused_token(db, token=token)
    if not qrcode_token:
        raise HTTPException(status_code=400, detail="Invalid or expired QR code")

    # 获取社团信息
    club = get_club(db, club_id=qrcode_token.club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")

    user_scan = get_by_user_id_and_club_id(db, current_user.id, qrcode_token.club_id)
    if user_scan:
        raise HTTPException(status_code=400, detail="User already scanned")

    # 确定增加的积分类型
    added_point = 0
    added_special_point = 0

    if club.club_type == 1:  # 特殊社团
        added_special_point = 1
    else:  # 普通社团
        added_point = 1

    # 更新用户积分
    update_user_points(db, user_id=current_user.id, add_points=added_point, add_special=added_special_point)

    # 标记token为已使用
    update_qrcode_token_status(db, token_id=qrcode_token.id, is_used=1)

    # 记录用户扫描行为
    record_user_scan(db, user_id=current_user.id, club_id=qrcode_token.club_id)

    return {
        "code": 200,
        "message": "Success",
        "data": {
            "addedPoint": added_point,
            "addedSpecialPoint": added_special_point
        }
    }
