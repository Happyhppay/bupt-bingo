from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from database import Base


class BingoGrid(Base):
    __tablename__ = "bingo_grid"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    grid_row = Column(Integer, nullable=False)  # 1-5
    grid_col = Column(Integer, nullable=False)  # 1-5
    is_lit = Column(Integer, default=0)  # 0-未点亮，1-已点亮
    lit_time = Column(DateTime(timezone=True))

    # 唯一约束：同一用户的同一格子仅一条记录
    __table_args__ = (
        UniqueConstraint('user_id', 'grid_row', 'grid_col', name='unique_user_grid'),
    )
