import asyncio
import pprint
import json
from src.agent.deep_research_api import user_query
from src.agent.system_prompt import react_system_prompt
from src.agent import tool 
from src.utils import global_logger 
# from src.runtime import subthread_python_executor
# subthread_python_executor.work_dir = None
if __name__ == "__main__":

    p_user = "给我执行一下斐波那契 f(6)，必须调用python工具执行，不能口算"
    
    user_input = p_user
    m=asyncio.run(user_query(
            react_system_prompt, 
            user_input, 
            [tool.python_tool.ExecutePythonCodeTool]
        ))
    json_str = json.dumps(m, default=lambda o: o.model_dump())
    pure_python_data = json.loads(json_str)
    global_logger.info(f"一共{len(m)}条对话：\n\n {pprint.pformat(m)}\n\n")
