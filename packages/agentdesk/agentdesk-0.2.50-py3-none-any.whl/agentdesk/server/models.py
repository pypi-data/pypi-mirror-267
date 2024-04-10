from typing import List, Optional

from pydantic import BaseModel


class V1Health(BaseModel):
    status: Optional[str] = None


class V1Info(BaseModel):
    version: Optional[str] = None


class V1DesktopReqeust(BaseModel):
    name: Optional[str] = None
    memory: Optional[str] = None
    cpu: Optional[int] = None
    disk: Optional[str] = None


class V1DesktopRegistration(BaseModel):
    name: Optional[str] = None
    addr: Optional[str] = None


class V1ProviderData(BaseModel):
    type: Optional[str] = None
    args: Optional[dict] = None


class V1Desktop(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    addr: Optional[str] = None
    status: Optional[str] = None
    created: Optional[float] = None
    image: Optional[str] = None
    memory: Optional[int] = None
    cpu: Optional[int] = None
    disk: Optional[str] = None
    memory_usage: Optional[float] = None
    cpu_usage: Optional[float] = None
    disk_usage: Optional[float] = None
    reserved_ip: Optional[bool] = None
    provider: Optional[V1ProviderData] = None
    meta: Optional[dict] = None
    owner_id: Optional[str] = None


class V1Desktops(BaseModel):
    desktops: List[V1Desktop]
