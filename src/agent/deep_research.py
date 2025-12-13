import pprint
from openai.types.chat.chat_completion import ChatCompletionMessage

from src.utils import global_logger, traceable

import llm
import action
import memory
import tool
import tool.schema
import tool.python_tool
import tool.todo_tool


def user_query(user_input):
    user_hint = "用户输入："
    global_logger.info(f"{user_hint} ： {user_input}\n\n")

    messages = memory.init_messages_with_system_prompt(user_input)
    tools_schema_list = tool.schema.get_tools_schema([
        tool.python_tool.ExecutePythonCodeTool,
        # tool.todo_tool.RecursivePlanTreeTodoTool,
        ])

    # 模型的第一轮调用
    assistant_output: ChatCompletionMessage = llm.generate_assistant_output_append(messages, tools_schema_list)
    if not llm.has_tool_call(assistant_output) and not llm.has_function_call(assistant_output):
        global_logger.info(f"无需调用工具，我可以直接回复：{assistant_output.content}")
        return

    # 如果需要调用工具，则进行模型的多轮调用，直到模型判断无需调用工具
    while llm.has_tool_call(assistant_output) or llm.has_function_call(assistant_output):
        if llm.has_function_call(assistant_output):
            tool_info = {
                "content": "",
                "role": "function",
                "tool_call_id": "",
                # 其他非必须
                "tool_call_name": assistant_output.function_call.name,
                "tool_call_arguments": assistant_output.function_call.arguments,
            }            
            action.call_tools_safely(tool_info)
            tool_output = tool_info["content"]
            global_logger.info(f"工具 function call 输出信息： {tool_output}\n")
            global_logger.info("-" * 60)
            messages.append(tool_info)
        if llm.has_tool_call(assistant_output):
            for i in range(len(assistant_output.tool_calls)):
                # 如果判断需要调用查询天气工具，则运行查询天气工具
                tool_info = {
                    "content": "",
                    "role": "tool",
                    "tool_call_id": assistant_output.tool_calls[i].id,
                    # 其他非必须
                    "tool_call_name": assistant_output.tool_calls[i].function.name,
                    "tool_call_arguments": assistant_output.tool_calls[i].function.arguments,
                }

                action.call_tools_safely(tool_info)

                tool_output = tool_info["content"]
                global_logger.info(f"工具 tool call 输出信息： {tool_output}\n")
                global_logger.info("-" * 60)
                messages.append(tool_info)
        assistant_output = llm.generate_assistant_output_append(messages, tools_schema_list)
        if assistant_output.content is None:
            assistant_output.content = ""
        global_logger.info(
            f"""第{len(messages) // 2}轮大模型输出信息： 
\n\nassistant_output.content:: \n\n {pprint.pformat(assistant_output.content)}
\n\nassistant_output.tool_calls::\n\n {pprint.pformat([toolcall.model_dump() for toolcall in assistant_output.tool_calls] if assistant_output.tool_calls else [])}\n"""
        )
    global_logger.info(f"最终答案： {assistant_output.content}")

# 测试
if __name__ == "__main__":
    data_info = """
你所在的工作路径下面，可以用python工具  ExecutePythonCodeTool  写一段包含读取json文件的代码，读取一下文件
例如：“
import json
with open('xx_schema.json', 'r', encoding='utf-8') as file:
    schema = json.load(file)
    print(json.dumps(schema, indent=2))
”，读取以下文件：
1. **{schema}** - 完整的数据结构Schema定义，schema数据需要完整输出，知道完整的数据结构。
2. **{data_file}** 是具体问题需要计算的数据。data数据文件内容，因为数量会很大，只需按照 xx schema.json 中定义的字段分析计算和画图，如果需要print输出，需要控制输出行数和数量。
""".format(
        schema=["metro-draw-schema.json", "beijing_scenic_spot_schema_with_play_hours.json"],
        data_file=["metro-draw-data-80%.json", "beijing_scenic_spot_validated_data_with_play_hours.json"]
        ) 
    # 要把数据放到工作路径下，  同时修改工作路径的代码
    
    user_query_prompt = f"""
### 需求
需求是基于给定的JSON数据文件（景点Schema、景点数据、地铁Schema、地铁数据），通过Python编程实现**多日旅游路线规划**，核心约束与目标如下：
1. **核心目标**：最大化游玩景点的级别（5A>4A>3A）和数量，最小化通勤时间；
2. **时间约束**：
   - 每日游玩总耗时（通勤+游玩）中，游玩时间每个景点≥景点建议的游玩时长；
   - 每日白天可用游玩+通勤总时间≤8小时（仅白天时段，不含过夜）；
   - 夜间可乘坐地铁或步行前往次日游玩的景点所在区域（夜间可乘坐地铁或步行通勤时间不计入每日8小时限额），目的是缩短次日白天的通勤耗时，为景点游玩腾出更多时间；
3. **通勤规则**：
   - 白天通勤优先地铁（80km/h），无地铁则步行（3.6km/h），耗时计入每日8小时限额；
   - 夜间通勤仅可乘坐地铁（80km/h），无地铁则次日白天步行，夜间地铁通勤耗时不计入每日8小时限额；
4. **数据约束**：读取指定JSON文件（Schema用于解析字段，Data为计算核心），起点经纬度固定为[116.39088849999999, 39.92767]；
5. **输出要求**：
   - 枚举不同游玩天数（最少1天）的路线方案；
   - 详细输出连贯的地铁/步行路径信息（区分白天/夜间通勤），包括路径、距离、耗时、是否计入当日8小时限额等，存储为文件（UTF-8编码）；
   - 每次计算/读取后生成带编号的可视化图（需标注白天/夜间通勤路径、景点游玩时段、每日时间消耗等），输出图片绝对路径；
   - 全程通过Python代码实现，而非直接给出答案。

### 关键约束满足
- ✅ 全程Python代码实现，无直接人工给出答案；
- ✅ 读取JSON后生成带编号的可视化图，输出绝对路径；
- ✅ 满足时间约束（每日白天≤8小时、每个景点游玩≥景点建议的游玩时长，夜间地铁通勤不计入限额）；
- ✅ 优先地铁通勤（白天/夜间均优先地铁，夜间无地铁则次日白天步行）；
- ✅ 枚举不同天数（1~10天），最大化景点级别和数量；
- ✅ 详细输出连贯的通勤路径、距离、时间等信息（区分白天/夜间通勤属性）。
"""
    
    tool_use_prompt = """
1. 必须使用python工具进行算法编码输出得到计算答案，不能直接给出答案。
2. 在每一次读取或者计算结束，将数据画图存下来起一个带编号的有意义的名字，
3. 并将当前工作路径和图片名字拼接起来输出图片的绝对路径输出出来。
4. 如果存储文件也要使用utf-8编码存储。
"""
    # all_prompt = f"{data_info}\n\n{user_query_prompt}\n\n{tool_use_prompt}"
    all_prompt = f"{user_query_prompt}\n\n{data_info}"
    user_query(all_prompt)
