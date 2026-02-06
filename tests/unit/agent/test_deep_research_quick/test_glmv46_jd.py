from src.agent.deep_research_api import user_query

if __name__ == "__main__":

    p_user = "给我执行一下斐波那契 f(6)，必须调用python工具执行，不能口算"
    
    user_input = p_user
    from src.runtime import subthread_python_executor
    subthread_python_executor.work_dir = './wsm/5glm/2jd'
    subthread_python_executor.work_dir = None
    user_query(user_input)