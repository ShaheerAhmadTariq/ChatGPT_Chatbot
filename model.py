from sqlalchemy.schema import Column, ForeignKey
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, JSON, ForeignKey, Date
from sqlalchemy.types import String, Integer, Text
from sqlalchemy.orm import relationship
from database import Base

class dataset(Base):
    __tablename__ = "dataset"
    __table_args__ = {'extend_existing': True}

    q_id = Column(Integer, primary_key=True)
    prompt = Column(String(150))
    completion = Column(String(250), unique=False, nullable=True)

    


