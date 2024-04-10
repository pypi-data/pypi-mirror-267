from sqlalchemy import Column, Integer, String, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class V1HealthRecord(Base):
    __tablename__ = "v1_health"

    id = Column(Integer, primary_key=True)
    status = Column(String)


class V1DesktopRecord(Base):
    __tablename__ = "v1_desktops"

    id = Column(String, primary_key=True)
    name = Column(String)
    addr = Column(String)
    status = Column(String)
    created = Column(Float)
    cpu = Column(Integer, nullable=True)
    memory = Column(Integer, nullable=True)
    disk = Column(String, nullable=True)
    pid = Column(Integer, nullable=True)
    image = Column(String, nullable=True)
    provider = Column(String, nullable=True)
    requires_proxy = Column(Boolean, nullable=True)
    ssh_port = Column(Integer, nullable=True)
    reserved_ip = Column(Boolean, nullable=True)
    meta = Column(String, nullable=True)
    owner_id = Column(String, nullable=True)
    ssh_key = Column(String, nullable=True)
