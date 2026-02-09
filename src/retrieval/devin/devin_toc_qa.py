from src.mcp import mcp_api, mcp_enum
import asyncio

# --- 执行所有工具调用 ---
async def devin_toc(repoName: str):
    # 1. 保存结构
    return await mcp_api.call_mcp_tool(
        cache_item=mcp_enum.devin_cache_item,
        tool_name="read_wiki_structure", 
        arguments={"repoName": repoName}
    )

async def devin_qa(repoName: str, question: str):
    # 3. 保存提问结果
    return await mcp_api.call_mcp_tool(
        cache_item=mcp_enum.devin_cache_item,
        tool_name="ask_question", 
        arguments={
            "repoName": repoName, 
            "question": question
        }
    )

async def main():
    toc_result = await devin_toc("1850298154/algo_agent")
    print("devin_toc", toc_result)

if __name__ == "__main__":
    asyncio.run(main())
