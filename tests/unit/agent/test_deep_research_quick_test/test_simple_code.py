from src.agent.deep_research_api import user_query
from src.agent.system_prompt import react_system_prompt
from src.agent import tool 
from src.runtime import subthread_python_executor
subthread_python_executor.work_dir = None

if __name__ == "__main__":

    p_user = "给我执行一下斐波那契 f(6)，必须调用python工具执行，不能口算"
    
    user_input = p_user
    user_query(
            react_system_prompt, 
            user_input, 
            [tool.python_tool.ExecutePythonCodeTool]
        )
