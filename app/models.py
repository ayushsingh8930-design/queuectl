from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime

from app.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True)
    command = Column(String, nullable=False)
    state = Column(String, default="pending")
    attempts = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)