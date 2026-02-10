from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional, Any


class CallKind(Enum):
    FUNCTION = "function"
    TOOL = "tool"


@dataclass
class CallDescriptor:
    kind: CallKind
    name: str
    arguments: Optional[Any]
    tool_call_id: Optional[str] = None
