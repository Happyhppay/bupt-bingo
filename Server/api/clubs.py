from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from crud.user_scan import get_by_user_id_and_club_id, record_user_scan
from database import get_db
from schemas.club import RefreshClubQrcodeResponse, ScanQrcodeRequest, ScanClubQrcodeResponse
from crud.qrcode_token import create_qrcode_token, get_valid_unused_token, update_qrcode_token_status
from crud.club import get_club_by_id
from crud.user import get_user_by_student_id, update_user_points
from dependencies import get_current_club_member, get_current_user_id
from utils import generate_club_qrcode_token, limiter

router = APIRouter(
    prefix="/clubs",
    tags=["clubs"]
)


@router.get("/qrcode", response_model=RefreshClubQrcodeResponse)
@limiter.limit("1/second")
def refresh_club_qrcode(
        request: Request,
        db: Session = Depends(get_db),
        user_id=Depends(get_current_club_member)
):
    """刷新社团二维码（社团成员）"""
    # 检查用户是否关联了社团
    user = get_user_by_student_id(db, user_id)
    club_id = user.club_id
    if not club_id:
        raise HTTPException(status_code=400, detail="User not associated with any club")

    # 生成新的二维码token
    token = generate_club_qrcode_token(club_id)
    create_qrcode_token(db, token=token, club_id=club_id)

    return {
        "code": 200,
        "message": "Success",
        "data": {
            "qrcodeToken": token
        }
    }


@router.post("/scan", response_model=ScanClubQrcodeResponse)
@limiter.limit("3/minute")
def scan_club_qrcode(
        request: Request, 
        scan: ScanQrcodeRequest,
        db: Session = Depends(get_db),
        user_id=Depends(get_current_user_id)
):
    """扫描社团二维码获取积分（普通用户）"""
    token = scan.qrcodeToken

    # 验证token有效性
    qrcode_token = get_valid_unused_token(db, token)
    if not qrcode_token:
        raise HTTPException(status_code=400, detail="Invalid or expired QR code")
    club_id = qrcode_token.club_id
    qrcode_id = qrcode_token.id

    user_scan = get_by_user_id_and_club_id(db, user_id, club_id)
    if user_scan:
        raise HTTPException(status_code=400, detail="User already scanned")

    # 获取社团信息
    club = get_club_by_id(db, club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")

    # 确定增加的积分类型
    added_point = 0
    added_special_point = 0

    if club.club_type == 1:  # 特殊社团
        added_special_point = 1
    else:  # 普通社团
        added_point = 1

    # 更新用户积分
    update_user_points(db, user_id, added_point, added_special_point)

    # 标记token为已使用
    update_qrcode_token_status(db, qrcode_id)

    # 记录用户扫描行为
    record_user_scan(db, user_id, club_id)

    return {
        "code": 200,
        "message": "Success",
        "data": {
            "addedPoint": added_point,
            "addedSpecialPoint": added_special_point
        }
    }
