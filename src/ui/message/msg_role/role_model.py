import enum

class RoleNameEnum(enum.StrEnum):
    USER = "user"                 
    ASSISTANT = "assistant"         
    ASSISTANT_CONTENT = "assistant_content"         
    REASONING_CONTENT = "reasoning_content"  
    TOOL_CALL = "tool_call"     
    TOOL = "tool"                   
    FUNCTION_CALL = "function_call"   
    FUNCTION = "function"       
    FINISH_REASON = "finish_reason"   
    UNKNOWN = "unknown"             
AVATARS = {
    RoleNameEnum.USER: "👤",               
    RoleNameEnum.ASSISTANT: "🧑‍💻", #🤖🏁        
    RoleNameEnum.ASSISTANT_CONTENT: "📜",         
    RoleNameEnum.REASONING_CONTENT: "🧠",  
    RoleNameEnum.TOOL_CALL: "🦾", #"📞",           
    RoleNameEnum.TOOL: "🛠️",               
    RoleNameEnum.FUNCTION_CALL: "🦿",#"☎️",      
    RoleNameEnum.FUNCTION: "🔧",            
    RoleNameEnum.FINISH_REASON: "✅",      
    RoleNameEnum.UNKNOWN: "❓"             
}