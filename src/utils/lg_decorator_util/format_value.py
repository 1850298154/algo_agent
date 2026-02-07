import pprint
import json
from functools import wraps
from typing import Callable, Optional, Dict, Any, Union, get_type_hints, Type, Awaitable
from unittest.mock import Base
from pydantic import BaseModel, Field, ValidationError



# ------------------------------
# 工具函数： 格式化复杂参数/返回值（不变）
# ------------------------------
def format_value(value: Any) -> str:
    @wraps(pprint.pformat)
    def pf(*args, **kwargs) -> str:
        """Format a Python object into a pretty-printed representation."""
        output_format_str = pprint.pformat(*args, **kwargs)
        return output_format_str
    try:
        if isinstance(value, BaseModel):
            return pf(value)+'\n'+pf(value.model_dump())
        return pf(value)
        # return json.dumps(value, ensure_ascii=False, indent=2)
    except (TypeError, ValueError):
        if hasattr(value, "__dict__"):
            obj_dict = {k: v for i, (k, v) in enumerate(value.__dict__.items()) if i < 10}
            return f"[{value.__class__.__name__}] {json.dumps(obj_dict, ensure_ascii=False)}..."
        elif isinstance(value, (set, tuple)):
            return f"{type(value).__name__}({list(value)[:20]}..." if len(value) > 20 else f"{value}"
        else:
            str_val = str(value)
            return str_val[:500] + "..." if len(str_val) > 500 else str_val