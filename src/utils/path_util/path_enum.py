import enum

class ProjPathEnum(enum.StrEnum):
    LOG_DIR_NAME = "./logs/"
    WST_DIR_NAME = "./wst/"

class LogPathEnum(enum.StrEnum):
    ALL_LOG_NAME = "all.log"
    PRINT_LOG_NAME = "print.log"
    TRACE_LOG_NAME = "trace.log"

class WstPathEnum(enum.StrEnum):
    UPLOAD_DIR_NAME = "./upload_files/"
    SCHEMA_DIR_NAME = "./agent_schema/"
    
class AgentPathEnum(enum.StrEnum):
    MESSAGE_DIR_NAME = "./chat_messages/"
    PY_RUNTIME_VAR_DIR_NAME = "./python_runtime_variable/"
    PY_OUTPUT_DIR_NAME = WstPathEnum.UPLOAD_DIR_NAME

