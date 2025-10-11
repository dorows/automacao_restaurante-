from dataclasses import dataclass
from typing import Any, Optional, Literal

Status = Literal["ok", "invalid", "not_found", "conflict", "error"]

@dataclass
class Result:
    status: Status
    data: Any = None
    message_key: Optional[str] = None
    error: Optional[str] = None
