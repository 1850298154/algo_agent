from unittest.mock import Base
from typing import Optional
from pydantic import BaseModel, Field
from src.utils.path_util import static_path

class MsgMemPath(BaseModel):
    agent_name_id: str
    message_len: Optional[int] = None
    def path(self) -> str:
        if self.message_len is None:
            path = static_path.Dir.MSG_DIR / f"nameid.{self.agent_name_id}..msg_all.json"
        else:
            path = static_path.Dir.MSG_DIR / f"nameid.{self.agent_name_id}..msg_head_len_{self.message_len:04d}.json"
        return path.absolute().as_posix()

class RunVarPath(BaseModel):
    success_cnt: Optional[int] = None
    def path(self) -> str:
        if self.success_cnt is None:
            path = static_path.Dir.PY_RUNTIME_VAR_DIR / f"all.pkl"
        else:
            path = static_path.Dir.PY_RUNTIME_VAR_DIR / f"success_cnt_{self.success_cnt:04d}.pkl"
        return path.absolute().as_posix()
