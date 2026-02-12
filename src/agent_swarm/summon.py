from src.agent import deep_research_api
from src.agent.msg import msg_mem

async def summon_agent(
    message_mem: deep_research_api.msg_mem.MessageMemory,
    tool_class_list: list = [],
    mcp_tool_name_list: list = [],
    msg_ctr_config: deep_research_api.msg_ctr.MessageControlConfig = deep_research_api.msg_ctr.MessageControlConfig()
) -> deep_research_api.msg_mem.MessageMemory:
    """
    Agent Swarm 的核心接口：用于启动一个智能体进行对话，直到对话结束，返回最终的消息记忆对象
    参数说明：
    - message_mem: 消息记忆对象，用于存储对话历史
    - tool_class_list: 可用工具类列表
    - mcp_tool_name_list: 可用的多轮对话工具名称列表
    - msg_ctr_config: 消息控制配置
    """
    genor = deep_research_api.run_agent_generator(
        message_mem=message_mem,
        tool_class_list=tool_class_list,
        mcp_tool_name_list=mcp_tool_name_list,
        msg_ctr_config=msg_ctr_config
    )
    try:
        async for ret_message_mem in genor: 
            pass
        return ret_message_mem
    finally:
        await genor.aclose()  # 确保生成器被正确关闭，释放资源，不然后又 cancel 异常
