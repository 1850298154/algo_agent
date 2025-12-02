以下是一个完整的 Streamlit 实现 AI Agent 多轮对话展示的示例，包含 Tool 调用参数、Python 代码执行、Markdown 结果展示等核心功能。这个示例模拟了一个具备工具调用能力的 AI Agent，支持多轮对话上下文管理，并能清晰展示工具调用的全过程。

```python
import streamlit as st
import json
import traceback
from datetime import datetime
import uuid
from typing import List, Dict, Any

# 设置页面配置
st.set_page_config(
    page_title="AI Agent 多轮对话演示",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化会话状态
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "current_tool_result" not in st.session_state:
    st.session_state.current_tool_result = None
if "agent_context" not in st.session_state:
    st.session_state.agent_context = {}

# 定义支持的工具
SUPPORTED_TOOLS = {
    "python_executor": {
        "name": "Python 代码执行器",
        "description": "执行Python代码并返回结果",
        "parameters": {
            "code": {
                "type": "string",
                "description": "要执行的Python代码",
                "required": True
            },
            "timeout": {
                "type": "int",
                "description": "代码执行超时时间（秒）",
                "default": 10,
                "required": False
            }
        }
    },
    "data_analyzer": {
        "name": "数据分析工具",
        "description": "分析数据并生成可视化结果",
        "parameters": {
            "data": {
                "type": "string",
                "description": "JSON格式的数据源",
                "required": True
            },
            "analysis_type": {
                "type": "string",
                "description": "分析类型：summary/chart/correlation",
                "required": True
            }
        }
    }
}

# 工具执行函数
def execute_tool(tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """执行指定工具并返回结果"""
    result = {
        "success": False,
        "output": "",
        "error": "",
        "execution_time": 0
    }
    
    start_time = datetime.now()
    
    try:
        if tool_name == "python_executor":
            # 执行Python代码
            code = parameters.get("code", "")
            timeout = parameters.get("timeout", 10)
            
            # 创建执行环境
            exec_globals = {}
            exec_locals = {}
            
            # 安全执行代码（实际生产环境需添加更多安全限制）
            exec(code, exec_globals, exec_locals)
            
            # 获取执行结果
            output = "\n".join([f"{k}: {v}" for k, v in exec_locals.items() if not k.startswith('_')])
            if not output:
                output = "代码执行成功，无返回值"
                
            result["success"] = True
            result["output"] = output
            
        elif tool_name == "data_analyzer":
            # 模拟数据分析
            data = json.loads(parameters.get("data", "{}"))
            analysis_type = parameters.get("analysis_type", "")
            
            if analysis_type == "summary":
                summary = f"""
### 数据摘要分析结果
- 数据条数: {len(data) if isinstance(data, list) else 1}
- 数据类型: {type(data).__name__}
- 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

#### 数据预览
```json
{json.dumps(data, indent=2)[:500]}...
```
                """
                result["success"] = True
                result["output"] = summary
                
            else:
                result["success"] = True
                result["output"] = f"执行{analysis_type}分析完成"
                
    except Exception as e:
        result["error"] = str(e)
        result["output"] = f"执行失败: {str(e)}\n{traceback.format_exc()}"
        
    # 计算执行时间
    result["execution_time"] = (datetime.now() - start_time).total_seconds()
    
    return result

# AI Agent 核心处理函数
def agent_process_message(user_message: str) -> Dict[str, Any]:
    """处理用户消息，模拟Agent思考和工具调用"""
    
    # 模拟Agent思考过程
    thinking_steps = [
        "理解用户请求: " + user_message,
        "判断是否需要调用工具...",
    ]
    
    # 简单的意图识别，判断是否需要调用工具
    tool_call = None
    if "执行python" in user_message.lower() or "python代码" in user_message.lower():
        thinking_steps.append("识别到需要执行Python代码")
        thinking_steps.append("选择工具: Python代码执行器")
        
        # 提取代码（简单处理，实际需用LLM解析）
        code_start = user_message.find("```")
        if code_start != -1:
            code_end = user_message.find("```", code_start + 3)
            if code_end != -1:
                code = user_message[code_start + 3:code_end].strip()
                if code.startswith("python"):
                    code = code[6:].strip()
        else:
            # 默认示例代码
            code = """
# 示例Python代码
import math

# 计算圆的面积
radius = 5
area = math.pi * radius **2
print(f"半径为{radius}的圆面积: {area}")
            """.strip()
        
        tool_call = {
            "tool_name": "python_executor",
            "parameters": {
                "code": code,
                "timeout": 10
            }
        }
        thinking_steps.append(f"构造工具参数: {json.dumps(tool_call['parameters'], indent=2)}")
        
    elif "分析数据" in user_message.lower():
        thinking_steps.append("识别到需要数据分析")
        thinking_steps.append("选择工具: 数据分析工具")
        
        tool_call = {
            "tool_name": "data_analyzer",
            "parameters": {
                "data": json.dumps([
                    {"name": "产品A", "sales": 1200, "profit": 350},
                    {"name": "产品B", "sales": 800, "profit": 200},
                    {"name": "产品C", "sales": 1500, "profit": 400}
                ]),
                "analysis_type": "summary"
            }
        }
        thinking_steps.append(f"构造工具参数: {json.dumps(tool_call['parameters'], indent=2)}")
        
    else:
        thinking_steps.append("不需要调用工具，直接回答")
    
    # 执行工具调用（如果有）
    tool_result = None
    if tool_call:
        thinking_steps.append("执行工具调用...")
        tool_result = execute_tool(tool_call["tool_name"], tool_call["parameters"])
        thinking_steps.append(f"工具执行完成，耗时: {tool_result['execution_time']:.2f}秒")
        
        if tool_result["success"]:
            thinking_steps.append("工具执行成功，整理结果...")
        else:
            thinking_steps.append(f"工具执行失败: {tool_result['error']}")
    
    # 生成最终回答
    if tool_result:
        if tool_result["success"]:
            final_answer = f"""
### 📝 执行结果
{tool_result['output']}

#### 🔧 工具调用信息
- 工具名称: {SUPPORTED_TOOLS[tool_call['tool_name']]['name']}
- 执行耗时: {tool_result['execution_time']:.2f}秒
- 调用参数:
```json
{json.dumps(tool_call['parameters'], indent=2)}
```
            """
        else:
            final_answer = f"""
### ❌ 执行失败
{tool_result['error']}

#### 🔧 工具调用信息
- 工具名称: {SUPPORTED_TOOLS[tool_call['tool_name']]['name']}
- 调用参数:
```json
{json.dumps(tool_call['parameters'], indent=2)}
```

#### 📋 错误详情
```
{tool_result['output']}
```
            """
    else:
        final_answer = f"""
### 💡 AI回答
我已收到你的消息: "{user_message}"

这是一个多轮对话演示，你可以尝试：
- 输入包含Python代码的请求（例如：执行Python代码```python print('hello world')```）
- 输入数据分析请求（例如：分析销售数据）
        """
    
    return {
        "thinking": thinking_steps,
        "tool_call": tool_call,
        "tool_result": tool_result,
        "final_answer": final_answer
    }

# 页面样式美化
st.markdown("""
<style>
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
    }
    .user-message {
        background-color: #2b313e;
    }
    .agent-message {
        background-color: #4b5563;
    }
    .thinking-container {
        background-color: #1f2937;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .tool-call-card {
        border: 1px solid #6b7280;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 侧边栏
with st.sidebar:
    st.title("🤖 AI Agent 控制面板")
    
    # 工具列表展示
    st.subheader("支持的工具")
    for tool_id, tool_info in SUPPORTED_TOOLS.items():
        with st.expander(f"{tool_info['name']}"):
            st.write(f"描述: {tool_info['description']}")
            st.subheader("参数")
            for param_name, param_info in tool_info['parameters'].items():
                st.write(f"- **{param_name}**: {param_info['description']} (类型: {param_info['type']}, 必填: {param_info.get('required', False)})")
                if 'default' in param_info:
                    st.write(f"  默认值: {param_info['default']}")
    
    # 清除对话历史
    if st.button("🗑️ 清除对话历史"):
        st.session_state.conversation_history = []
        st.session_state.current_tool_result = None
        st.rerun()
    
    # 关于信息
    st.divider()
    st.markdown("### ℹ️ 关于")
    st.markdown("""
    这是一个AI Agent多轮对话演示，展示：
    - 多轮对话上下文管理
    - 工具调用参数展示
    - Python代码执行
    - Markdown格式结果展示
    - Agent思考过程可视化
    """)

# 主页面
st.title("AI Agent 多轮对话演示")
st.subheader("支持工具调用的智能助手")

# 显示对话历史
st.markdown("### 📜 对话历史")
for message in st.session_state.conversation_history:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(f"**你**: {message['content']}")
    else:
        with st.chat_message("assistant"):
            # 显示Agent思考过程
            with st.expander("🧠 Agent思考过程", expanded=False):
                thinking_steps = message.get("thinking", [])
                for i, step in enumerate(thinking_steps):
                    st.markdown(f"{i+1}. {step}")
            
            # 显示工具调用信息（如果有）
            tool_call = message.get("tool_call")
            if tool_call:
                with st.expander("🔧 工具调用详情", expanded=False):
                    st.markdown(f"**工具名称**: {SUPPORTED_TOOLS[tool_call['tool_name']]['name']}")
                    st.markdown("**调用参数**:")
                    st.code(json.dumps(tool_call['parameters'], indent=2), language="json")
                    
                    # 如果是Python执行器，单独展示代码
                    if tool_call["tool_name"] == "python_executor":
                        st.markdown("**执行的Python代码**:")
                        st.code(tool_call['parameters']['code'], language="python")
            
            # 显示最终回答
            st.markdown(message['final_answer'])

# 用户输入框
user_input = st.chat_input("请输入你的消息...")

if user_input:
    # 添加用户消息到历史
    st.session_state.conversation_history.append({
        "id": str(uuid.uuid4()),
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # Agent处理消息
    with st.spinner("Agent正在思考中..."):
        agent_response = agent_process_message(user_input)
    
    # 添加Agent响应到历史
    st.session_state.conversation_history.append({
        "id": str(uuid.uuid4()),
        "role": "assistant",
        "content": agent_response["final_answer"],
        "thinking": agent_response["thinking"],
        "tool_call": agent_response["tool_call"],
        "tool_result": agent_response["tool_result"],
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    # 重新运行页面以更新显示
    st.rerun()

# 空状态提示
if not st.session_state.conversation_history:
    st.markdown("""
    ### 📌 开始对话
    尝试输入以下指令体验功能：
    
    #### 1. Python代码执行
    ```
    执行Python代码
    ```python
    # 计算斐波那契数列
    def fib(n):
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a
    
    # 计算前10个斐波那契数
    result = [fib(i) for i in range(10)]
    print("斐波那契数列前10项:", result)
    ```
    ```
    
    #### 2. 数据分析
    ```
    分析销售数据
    ```
    
    #### 3. 普通对话
    ```
    你好，介绍一下你自己
    ```
    """)
```

### 功能特点说明

1. **多轮对话管理**
   - 使用 Streamlit Session State 保存对话历史
   - 支持用户和Agent消息的区分展示
   - 保留完整的上下文信息

2. **Tool调用完整展示**
   - 可视化Agent思考过程
   - 展示工具选择和参数构造
   - 单独展示Python代码（语法高亮）
   - 显示工具执行结果和耗时

3. **Markdown结果展示**
   - 支持格式化的结果输出
   - 代码块语法高亮
   - 结构化的错误信息展示
   - 美观的UI布局

4. **交互体验优化**
   - 加载状态提示
   - 可展开/折叠的详情面板
   - 侧边栏工具说明
   - 清空对话历史功能
   - 空状态引导提示

5. **模拟Agent逻辑**
   - 简单的意图识别
   - 工具调用参数构造
   - Python代码执行环境
   - 数据分析模拟

### 使用方法

1. 安装依赖：
```bash
pip install streamlit
```

2. 保存代码为 `agent_chat.py`

3. 运行应用：
```bash
streamlit run agent_chat.py
```

4. 体验功能：
   - 输入包含Python代码的请求，体验代码执行功能
   - 输入数据分析请求，查看结构化分析结果
   - 普通对话展示基础响应能力

### 扩展建议

1. **集成真实LLM**：替换模拟的Agent逻辑，接入OpenAI/Anthropic等LLM API
2. **安全的代码执行**：使用沙箱环境（如execjs、docker）执行Python代码
3. **更多工具支持**：添加API调用、数据库查询、文件处理等工具
4. **上下文管理优化**：实现对话摘要、长上下文处理
5. **结果可视化**：集成matplotlib/plotly展示数据分析图表
6. **历史记录持久化**：保存对话历史到文件/数据库
7. **多模态支持**：添加图片、文件上传功能

这个示例提供了完整的多轮对话展示框架，你可以根据实际需求扩展工具类型、优化Agent逻辑、增强UI展示效果。