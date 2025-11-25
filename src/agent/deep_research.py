from openai.types.chat.chat_completion import ChatCompletionMessage

from src.utils import global_logger, traceable

import llm
import action
import memory
import tool
import tool.schema
import tool.python_tool
import tool.todo_tool


@traceable
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
            messages.append(        {
                "content": "没有定义function_call工具调用，无法执行function_call，请使用tool_calls调用工具。",
                "role": "user",
            })
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
                global_logger.info(f"工具输出信息： {tool_output}\n")
                global_logger.info("-" * 60)
                messages.append(tool_info)
        loop_response = llm.generate_chat_completion(messages)
        assistant_output = loop_response.choices[0].message
        if assistant_output.content is None:
            assistant_output.content = ""
        messages.append(assistant_output)
        global_logger.info(f"第{len(messages) // 2}轮大模型输出信息： {assistant_output}\n")
    global_logger.info(f"最终答案： {assistant_output.content}")

# 测试
if __name__ == "__main__":
    data_info = """
你所在的工作路径下面，可以用python工具  ExecutePythonCodeTool  写一段包含读取json文件的代码，读取一下文件
例如：“
import json

with open('schema.json', 'r') as file:
    schema = json.load(file)
    print(json.dumps(schema, indent=2))
”，读取以下文件：
1. **schema.json** - 完整的数据结构Schema定义
2. **emergency_response_data_01.json** 至 **emergency_response_data_05.json** - 5个随机生成的应急救援场景数据

### 数据特点

1. **真实性**：
   - 基于真实地理范围生成坐标
   - 模拟不同类型的灾害场景
   - 包含合理的物资、载体属性

2. **多样性**：
   - 多种任务类型和优先级
   - 不同类型的运输载体
   - 随机生成的风险点和路径

3. **完整性**：
   - 包含所有核心实体和关系
   - 覆盖各种可能的状态组合
   - 包含任务反馈和救援指标

4. **可扩展性**：
   - 代码结构清晰，易于添加新的字段或实体
   - 生成策略可调整，可根据需要增加特定场景的数据

### 使用建议

1. **测试算法**：
   - 可用于测试任务指派、路径规划、ETA预测等算法
   - 包含各种边界情况（高优先级任务、复杂路径、设备故障等）

2. **系统集成**：
   - 可作为应急物资运输调度系统的测试数据
   - 支持系统功能验证和性能测试

3. **场景模拟**：
   - 可用于模拟不同类型的灾害救援场景
   - 支持应急响应演练和决策支持系统测试

这个数据生成器可以满足你对多智能体协同调度、动态在线路径规划等场景的测试需求，生成的随机数据具有较高的真实性和多样性。
    """
    user_query_prompt = f"""你的目标是基于以下数据特点和使用建议，制定一个详细的研究计划，帮助你深入了解数据结构，并分析如何利用这些数据解决应急物资运输调度中的问题。
请列出具体的任务步骤，包括但不限于以下方面：
1. 数据结构分析：如何理解和解析 schema.json 中定义的各个实体及其关系。
2. 数据生成逻辑：如何理解随机数据生成的策略和方法。
3. 场景模拟：如何利用生成的数据模拟不同的应急救援场景。
4. 算法测试：如何设计多种不同的算法实验来测试多智能体协同调度算法的性能和效果。
"""
    tool_use_prompt = """不支持function_call，必须使用tool_calls调用多个工具执行。必须使用python工具进行算法编码和测试，不能直接给出答案"""
    all_prompt = f"{data_info}\n\n{user_query_prompt}\n\n{tool_use_prompt}"
    user_query(all_prompt)
