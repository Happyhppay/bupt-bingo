from sqlalchemy.orm import Session
from models.bingo_grid import BingoGrid
from datetime import datetime
from typing import List


def get_bingo_grid_by_grid_id(db: Session, grid_id: int):
    return db.query(BingoGrid).filter(BingoGrid.id == grid_id).first()


def get_bingo_grid_by_user_and_position(db: Session, user_id: int, row: int, col: int):
    """按用户和位置查找格子。row/col 应为 0-based（0..4）。"""
    return db.query(BingoGrid).filter(
        BingoGrid.user_id == user_id,
        BingoGrid.grid_row == row,
        BingoGrid.grid_col == col
    ).first()


def get_bingo_grids_by_user(db: Session, user_id: int):
    return db.query(BingoGrid).filter(BingoGrid.user_id == user_id).all()


def create_bingo_grid(db: Session, user_id: int, row: int, col: int, is_lit: int = 0):
    if row < 0 or row > 4 or col < 0 or col > 4:
        raise ValueError("row and col must be in range 0..4")

    db_grid = BingoGrid(
        user_id=user_id,
        grid_row=row,
        grid_col=col,
        is_lit=is_lit
    )
    db.add(db_grid)
    db.commit()
    db.refresh(db_grid)
    return db_grid


def update_bingo_grid(db: Session, grid_id: int, is_lit: int, lit_time: datetime = None):
    db_grid = db.query(BingoGrid).filter(BingoGrid.id == grid_id).first()
    if db_grid:
        db_grid.is_lit = is_lit
        if lit_time:
            db_grid.lit_time = lit_time
        db.commit()
        db.refresh(db_grid)
    return db_grid


def initialize_user_bingo_grid(db: Session, user_id: int):
    """初始化用户的5x5 Bingo格子"""
    for row in range(5):
        for col in range(5):
            create_bingo_grid(db,
                user_id,
                row,
                col,
                0
            )


def set_bingo_grid_lit(db: Session, user_id: int, row: int, col: int, is_lit: int = 1):
    """设置指定格子的点亮状态"""
    if row < 0 or row > 4 or col < 0 or col > 4:
        raise ValueError("row and col must be in range 0..4")

    grid = get_bingo_grid_by_user_and_position(db, user_id, row, col)
    if not grid:
        grid = create_bingo_grid(db,
            user_id,
            row,
            col,
            is_lit
        )
    else:
        grid = update_bingo_grid(db,
            grid.id, 
            is_lit=is_lit,
            lit_time=datetime.now()
        )
    return grid


def get_user_bingo_status(db: Session, user_id: int) -> List[List[int]]:
    """获取用户的Bingo格子状态，返回5x5矩阵"""
    grids = get_bingo_grids_by_user(db, user_id)

    # 初始化5x5矩阵
    status = [[0 for _ in range(5)] for _ in range(5)]

    for grid in grids:
        # 转换为0-based索引
        row_idx = grid.grid_row
        col_idx = grid.grid_col
        if 0 <= row_idx < 5 and 0 <= col_idx < 5:
            status[row_idx][col_idx] = grid.is_lit

    return status
