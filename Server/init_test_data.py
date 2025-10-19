"""初始化测试数据脚本。

将用于在开发或测试环境中创建一些示例社团和用户。
在命令行运行：
    python3 Server/init_test_data.py
"""
import os

# 确保使用 Server 目录下的 bingo.db（绝对路径），必须在导入 database 之前设置
# sqlite 绝对路径格式使用 4 个斜杠: sqlite:////absolute/path/dbfile
os.environ.setdefault('DATABASE_URL', 'sqlite:////www/bupt-bingo/Server/bingo.db')

from database import SessionLocal, Base, engine
from crud.club import create_club
from crud.user import create_user, update_user_role, update_user_points


def init_data():
    # 确保表已创建（通常由主应用执行一次）
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        print(db)
        print("开始初始化测试数据...")
        # 1) 创建或获取测试社团
        from crud.club import get_club_by_name, create_club as crud_create_club
        test_club_name = "Test Club"
        club = get_club_by_name(db, club_name=test_club_name)
        if not club:
            club = crud_create_club(db, club_name=test_club_name, club_type=1)
            print(f"创建社团: id={club.id}, name={club.club_name}")
        else:
            print(f"社团已存在: id={club.id}, name={club.club_name}")

        # 2) 创建普通用户（带 100 普通积分与 100 特殊积分）
        from crud.user import get_user, create_user as crud_create_user

        normal_user_id = 1001
        normal_user = get_user(db, user_id=normal_user_id)
        if not normal_user:
            normal_user = crud_create_user(db, student_id=normal_user_id, name="normal_user")
            print(f"创建普通用户: id={normal_user.id}, name={normal_user.name}")
        else:
            print(f"普通用户已存在: id={normal_user.id}, name={normal_user.name}")

        # 确保普通用户拥有 100 普通与 100 特殊积分
        update_user_points(db, user_id=normal_user.id, add_points=100 - (normal_user.points or 0), add_special=100 - (normal_user.special_points or 0))
        print(f"普通用户积分已设置: id={normal_user.id}")

        # 3) 创建社团成员用户并关联到测试社团
        club_user_id = 1002
        club_user = get_user(db, user_id=club_user_id)
        if not club_user:
            club_user = crud_create_user(db, student_id=club_user_id, name="club_member")
            print(f"创建社团用户: id={club_user.id}, name={club_user.name}")
        else:
            print(f"社团用户已存在: id={club_user.id}, name={club_user.name}")

        # 设置为社团成员 (role=1)
        update_user_role(db, user_id=club_user.id, role=1, club_id=club.id)
        print(f"社团用户角色已设置: id={club_user.id}, club_id={club.id}")

        # 4) 创建管理员用户
        admin_user_id = 1003
        admin_user = get_user(db, user_id=admin_user_id)
        if not admin_user:
            admin_user = crud_create_user(db, student_id=admin_user_id, name="admin_user")
            print(f"创建管理员用户: id={admin_user.id}, name={admin_user.name}")
        else:
            print(f"管理员用户已存在: id={admin_user.id}, name={admin_user.name}")

        # 设置为管理员 (role=2)
        update_user_role(db, user_id=admin_user.id, role=2)
        print(f"管理员用户角色已设置: id={admin_user.id}")

        print("测试数据初始化完成。")
    except Exception as e:
        print("初始化测试数据时发生错误:", e)
    finally:
        db.close()


if __name__ == '__main__':
    init_data()
