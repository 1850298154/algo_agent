from src.agent import deep_research_api
from src.agent.msg import msg_mem
from src.agent_swarm import summon
from openai.types.chat.chat_completion_message_param import (
    ChatCompletionDeveloperMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionAssistantMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionFunctionMessageParam,    
    ChatCompletionMessageParam,
) 


import asyncio
import pprint
import json
from src.agent.deep_research_api import run_agent_generator
from src.agent import system_prompt
from src.agent import tool 
from src.utils.log_decorator import global_logger 
from src.agent.msg import msg_ctr 
from src.agent.msg import msg_mem 
from src.mcp import mcp_enum 


# from src.runtime import subthread_python_executor
# subthread_python_executor.work_dir = None
if __name__ == "__main__":

    p_user = "一次调用所有工具就调用所有工具，测试一下"
    p_user = "给我执行一下斐波那契 f(6)， f(7)，f(8)必须调用python工具执行，存成一个list变量，不能口算"
    
    user_prompt = p_user
    message_mem: msg_mem.MessageMemory = msg_mem.init_messages_with_system_prompt(
        agent_name_id="test_simple_code_agent",
        system_prompt=system_prompt.obedient_system_prompt,
        user_prompt=user_prompt,
        msg_ctr_config=msg_ctr.MessageControlConfig(max_rounds=3)
    )
    
    ret_message_mem = asyncio.run(
        summon.summon_agent(
            message_mem            = message_mem,
            tool_class_list     = [tool.python_tool.ExecutePythonCodeTool],
            # tool_class_list     = [],
            # mcp_tool_name_list  = mcp_enum.mcp_list_tool_name_list,
            mcp_tool_name_list  = [],
        ))
    json_str = json.dumps(ret_message_mem, default=lambda o: o.model_dump())
    pure_python_data = json.loads(json_str)
    global_logger.info(f"一共{len(ret_message_mem.messages)}条对话：\n\n {pprint.pformat(ret_message_mem)}\n\n")
    pass
