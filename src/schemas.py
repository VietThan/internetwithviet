from attrs import define
from datetime import datetime


@define
class BaseResponse:
    ts: datetime = datetime.utcnow()