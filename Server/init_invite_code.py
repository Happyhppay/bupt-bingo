import os
os.environ.setdefault('DATABASE_URL', 'sqlite:////www/bupt-bingo/Server/bingo.db')

from database import SessionLocal, Base, engine

def init_invite_code():
    # 确保表已创建（通常由主应用执行一次）
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        print("开始初始化邀请码数据...")
        from crud.invite_code import create_invitecode
        from schemas.invite_code import InviteCodeCreate

        # 创建一些测试邀请码
        test_codes = [
            InviteCodeCreate(code="CLUB_TEST_001", role=1, club_id=1),
            InviteCodeCreate(code="CLUB_TEST_002", role=1, club_id=1),
            InviteCodeCreate(code="ADMIN_TEST_001", role=2, club_id=None),
        ]

        for invite in test_codes:
            try:
                create_invitecode(db, invite)
                print(f"已创建邀请码: {invite.code}")
            except Exception as e:
                print(f"创建邀请码失败或已存在: {e}")

    finally:
        db.close()
if __name__ == "__main__":
    init_invite_code()