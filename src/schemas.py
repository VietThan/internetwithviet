from attrs import define
from datetime import datetime, timezone


@define
class BaseResponse:
    ts: datetime = datetime.now(timezone.utc)
    """
    the timestamp in utc timezone
    """