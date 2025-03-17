from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, Date
from sqlalchemy.orm import relationship
from BASE.database import Base
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), nullable=False)

    targets = relationship("Target", back_populates="site", cascade="all, delete-orphan", lazy="joined")


class Target(Base):
    __tablename__ = "targets"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(255), nullable=False)
    title = Column(String(255), nullable=True)  # Fixed nullable issue
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)

    site = relationship("Site", back_populates="targets", lazy="joined")
    price_history = relationship("PriceHistory", back_populates="target", cascade="all, delete-orphan", lazy="joined")


class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    target_id = Column(Integer, ForeignKey("targets.id"), nullable=False)
    price_date = Column(Date, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)

    target = relationship("Target", back_populates="price_history", lazy="joined")


class SiteBase(BaseModel):
    name: str

class SiteCreate(SiteBase):
    pass

class SiteResponse(SiteBase):
    id: int
    targets: List["TargetResponse"] = []

    class Config:
        from_attributes = True


class TargetBase(BaseModel):
    site_id: int
    url: str
    title: Optional[str] = None

class TargetCreate(TargetBase):
    pass

class TargetResponse(TargetBase):
    id: int
    price_history: List["PriceHistoryResponse"] = []

    class Config:
        from_attributes = True


class PriceHistoryBase(BaseModel):
    target_id: int
    price_date: Optional[date]
    price: float

class PriceHistoryCreate(PriceHistoryBase):
    pass

class PriceHistoryResponse(PriceHistoryBase):
    id: int

    class Config:
        from_attributes = True
