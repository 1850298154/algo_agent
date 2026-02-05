# https://www.doubao.com/chat/29911225351714306
要实现 **AI Agent 多轮 DeepResearch（深度推理）**，核心流程是：**自然语言意图解析 → SQL 工具查询数据 → 转换为 Pandas DataFrame → 注入 Python 全局变量 → 多轮 Python 代码计算/分析 → 结果汇总**。以下是完整的实现方案，包括代码结构、提示词设计、工具描述和多轮推理逻辑。

## 一、核心设计思路
1. **分层架构**：将 Agent 拆分为「意图解析层」「工具调度层」「数据转换层」「多轮推理层」，解耦职责。
2. **数据流转**：SQL 结果 → DataFrame → Python 全局变量（`globals()` 注入）→ 多轮代码执行 → 中间结果缓存 → 最终结论。
3. **多轮推理驱动**：通过「历史上下文+当前推理目标」生成 Python 代码，执行后将结果回写到上下文，循环直到完成深度分析。
4. **工具抽象**：统一 SQL 工具和 Python 工具的调用接口，让 Agent 无需关注底层实现，只专注推理逻辑。

## 二、完整代码结构
### 1. 依赖安装
```bash
pip install openai pandas sqlalchemy python-dotenv  # OpenAI 作为 LLM 示例，可替换为其他模型
```

### 2. 项目目录结构
```
deep_research_agent/
├── .env                # 环境变量（数据库连接、LLM API Key）
├── agents/
│   └── deep_research_agent.py  # 核心 Agent 类（意图解析、多轮推理）
├── tools/
│   ├── sql_tool.py     # SQL 查询工具（数据库连接、结果返回）
│   └── python_tool.py  # Python 执行工具（DataFrame 注入、代码执行）
├── utils/
│   └── prompt_templates.py  # 提示词模板（系统提示、工具描述）
└── main.py             # 测试入口
```

### 3. 关键文件实现

#### （1）.env 环境变量配置
```env
# LLM 配置（以 OpenAI 为例，可替换为 Claude/通义千问等）
OPENAI_API_KEY=your-openai-key
OPENAI_MODEL=gpt-4o-mini  # 推荐用 GPT-4 系列，推理能力更强

# 数据库配置（以 MySQL 为例，支持 PostgreSQL/SQLite 等）
DB_CONN_STRING=mysql+pymysql://username:password@host:port/db_name
```

#### （2）utils/prompt_templates.py 提示词模板
核心是「系统提示词」和「工具描述词」，定义 Agent 的行为边界和工具调用规则。
```python
# 系统提示词：定义 Agent 角色、多轮推理逻辑、工具使用规则
SYSTEM_PROMPT = """
你是一个 DeepResearch 数据分析师 Agent，擅长通过 SQL 查询数据、Python 代码深度分析，完成多轮推理任务。
你的工作流程：
1. 理解用户的深度分析需求（例如："分析2024年各季度的用户留存率，找出留存最高的渠道，并计算该渠道的 ROI"）；
2. 第一步：判断是否需要查询数据 → 调用 SQL 工具获取原始数据，工具返回结果会自动转换为 Pandas DataFrame 并注入 Python 全局变量（变量名：df_xxx，如 df_user_retention）；
3. 多轮推理：基于已有的 DataFrame，逐步拆解分析目标，生成 Python 代码完成计算（例如：先计算季度留存率 → 筛选最高渠道 → 计算该渠道 ROI）；
4. 代码执行规则：
   - 只能使用 Pandas 操作 DataFrame，禁止修改数据库/文件系统，禁止恶意代码；
   - 每次生成的 Python 代码需明确使用全局变量中的 DataFrame（如 df_user_retention），执行后将结果存入新的全局变量（如 df_quarterly_retention）；
   - 若前一轮代码执行失败，需修正代码后重新执行，再继续后续推理；
5. 结果汇总：所有推理步骤完成后，整理成自然语言结论，包含关键数据和分析逻辑。

工具调用格式（严格遵守）：
- 调用 SQL 工具：{"name": "sql_tool", "parameters": {"query": "SELECT ..."}}
- 调用 Python 工具：{"name": "python_tool", "parameters": {"code": "import pandas as pd\n...\ndf_quarterly_retention = df_user_retention.groupby(...)..."}}

注意：
- 工具调用需用 JSON 格式包裹，单独一行，不可添加其他内容；
- 每次只能调用一个工具，执行完成后再进行下一轮推理；
- 无需解释工具调用逻辑，直接输出调用格式即可。
"""

# SQL 工具描述（给 LLM 看，明确工具功能和参数）
SQL_TOOL_DESCRIPTION = """
功能：查询数据库中的原始数据，返回结构化结果（自动转换为 Pandas DataFrame 并注入 Python 全局变量）。
参数：
- query: SQL 查询语句（必须合法，支持 SELECT 操作，禁止 DELETE/UPDATE/INSERT 等写操作）。
返回：查询结果对应的 DataFrame 全局变量名（如 df_user_data），以及数据的前 5 行预览。
"""

# Python 工具描述（给 LLM 看，明确工具功能和参数）
PYTHON_TOOL_DESCRIPTION = """
功能：执行 Python 代码进行数据计算/分析，基于已注入的 DataFrame 全局变量。
参数：
- code: Python 代码片段（需满足以下要求）：
  1. 必须导入必要的库（如 import pandas as pd）；
  2. 只能操作全局变量中的 DataFrame（如 df_xxx），禁止定义无关变量；
  3. 计算结果需存入新的全局变量（命名规范：df_+分析目标，如 df_quarterly_retention）；
  4. 禁止包含 print 语句，禁止修改/删除全局变量，禁止恶意代码。
返回：执行结果（成功则返回新变量名和数据预览，失败则返回错误信息）。
"""

# 多轮推理提示词（每轮推理前追加，引导 LLM 基于历史上下文继续分析）
MULTI_ROUND_PROMPT = """
当前进度：
{history_context}

下一步推理目标：{next_goal}
请生成对应的 Python 代码（调用 python_tool），或判断是否需要补充查询数据（调用 sql_tool）。
若已完成所有推理步骤，直接整理自然语言结论。
"""
```

#### （3）tools/sql_tool.py SQL 工具
负责数据库连接、执行查询、返回结果（后续会被转换为 DataFrame）。
```python
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

class SQLTool:
    def __init__(self):
        # 初始化数据库连接
        self.engine = create_engine(os.getenv("DB_CONN_STRING"))
        self.df_counter = 0  # 用于生成唯一的 DataFrame 变量名

    def run(self, query: str) -> dict:
        """
        执行 SQL 查询，返回结果（包含 DataFrame 变量名和数据预览）
        :param query: SQL 查询语句
        :return: 结果字典（status: success/error, data: 数据预览, var_name: DataFrame 变量名, message: 提示）
        """
        try:
            # 校验 SQL 语句（只允许 SELECT）
            if not query.strip().upper().startswith("SELECT"):
                return {
                    "status": "error",
                    "message": "SQL 工具仅支持 SELECT 查询，禁止写操作"
                }

            # 执行查询并转换为 DataFrame
            df = pd.read_sql(query, self.engine)
            self.df_counter += 1
            var_name = f"df_sql_{self.df_counter}"  # 生成唯一变量名（如 df_sql_1）

            # 返回结果（包含变量名和前 5 行预览）
            return {
                "status": "success",
                "var_name": var_name,
                "data": df.head().to_dict("records"),
                "message": f"SQL 查询成功，数据已存入全局变量 {var_name}（共 {len(df)} 行）"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"SQL 查询失败：{str(e)}"
            }
```

#### （4）tools/python_tool.py Python 工具
负责注入 DataFrame 到全局变量、执行 Python 代码、缓存中间结果。
```python
import pandas as pd
import sys
from typing import Dict, Any

class PythonTool:
    def __init__(self):
        # 初始化全局变量存储（key: 变量名，value: DataFrame/结果）
        self.global_vars: Dict[str, Any] = {
            "pd": pd  # 预先注入 pandas 库
        }

    def inject_df(self, var_name: str, df: pd.DataFrame) -> None:
        """将 SQL 结果的 DataFrame 注入全局变量"""
        self.global_vars[var_name] = df

    def run(self, code: str) -> dict:
        """
        执行 Python 代码，基于全局变量中的 DataFrame
        :param code: Python 代码片段
        :return: 结果字典（status: success/error, new_var: 新变量名, data: 数据预览, message: 提示）
        """
        try:
            # 记录执行前的变量名，用于判断新生成的变量
            pre_vars = set(self.global_vars.keys())

            # 执行代码（使用 exec，将全局变量传入）
            exec(code, self.global_vars)

            # 找出新生成的变量（假设每次只生成一个分析结果变量）
            post_vars = set(self.global_vars.keys())
            new_vars = post_vars - pre_vars
            new_var = new_vars.pop() if new_vars else None

            if not new_var:
                return {
                    "status": "error",
                    "message": "Python 代码未生成新的全局变量，请按规范命名（如 df_quarterly_retention）"
                }

            # 获取新变量的数据（必须是 DataFrame 或数值）
            new_data = self.global_vars[new_var]
            if isinstance(new_data, pd.DataFrame):
                data_preview = new_data.head().to_dict("records")
                data_info = f"共 {len(new_data)} 行"
            else:
                data_preview = new_data
                data_info = "数值结果"

            return {
                "status": "success",
                "new_var": new_var,
                "data": data_preview,
                "message": f"Python 代码执行成功，结果存入全局变量 {new_var}（{data_info}）"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Python 代码执行失败：{str(e)}"
            }
```

#### （5）agents/deep_research_agent.py 核心 Agent 类
负责意图解析、工具调度、多轮推理循环、上下文管理。
```python
import openai
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
from tools.sql_tool import SQLTool
from tools.python_tool import PythonTool
from utils.prompt_templates import (
    SYSTEM_PROMPT,
    SQL_TOOL_DESCRIPTION,
    PYTHON_TOOL_DESCRIPTION,
    MULTI_ROUND_PROMPT
)

load_dotenv()

# 初始化 LLM 客户端（OpenAI 示例，可替换为其他模型）
openai.api_key = os.getenv("OPENAI_API_KEY")
LLM_MODEL = os.getenv("OPENAI_MODEL")

class DeepResearchAgent:
    def __init__(self):
        self.sql_tool = SQLTool()
        self.python_tool = PythonTool()
        self.conversation_history: List[Dict[str, str]] = []  # 存储对话上下文（LLM 消息 + 工具执行结果）
        self.inference_goals: List[str] = []  # 拆解后的推理目标列表
        self.current_goal_index = 0  # 当前执行的推理目标索引

    def _parse_user_intent(self, user_query: str) -> None:
        """第一步：解析用户意图，拆解为多轮推理目标"""
        prompt = f"""
        用户需求：{user_query}
        任务：将该需求拆解为 2-5 个递进的推理目标（按执行顺序排列），每个目标对应一个具体的分析步骤。
        示例：
        用户需求：分析2024年各季度的用户留存率，找出留存最高的渠道，并计算该渠道的 ROI
        推理目标：
        1. 查询 2024 年所有用户的注册、留存、渠道、消费数据（需 SQL 查询）
        2. 按季度分组，计算各季度的用户留存率（基于 SQL 结果的 DataFrame）
        3. 筛选留存率最高的渠道（基于步骤 2 的结果）
        4. 计算该渠道的 ROI（投入/产出，基于原始数据和步骤 3 的结果）

        要求：
        - 每个目标必须具体、可执行（对应 SQL 查询或 Python 代码）
        - 前一个目标的结果为后一个目标的输入
        - 若需要原始数据，第一个目标必须是 SQL 查询
        """

        # 调用 LLM 拆解推理目标
        response = openai.ChatCompletion.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )

        # 解析 LLM 返回的推理目标（假设返回格式为 "1. xxx\n2. xxx"）
        goals_text = response.choices[0].message.content.strip()
        self.inference_goals = [
            line.split(". ", 1)[1] for line in goals_text.split("\n") if line.strip().startswith(tuple(str(i) for i in range(1, 10)))
        ]

        # 将拆解结果存入上下文
        self.conversation_history.append({
            "role": "system",
            "content": f"拆解推理目标：\n" + "\n".join([f"{i+1}. {goal}" for i, goal in enumerate(self.inference_goals)])
        })

    def _get_llm_response(self, current_prompt: str) -> str:
        """调用 LLM 生成工具调用指令或最终结论"""
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT + "\n工具描述：\n" + SQL_TOOL_DESCRIPTION + "\n" + PYTHON_TOOL_DESCRIPTION},
            *self.conversation_history,
            {"role": "user", "content": current_prompt}
        ]

        response = openai.ChatCompletion.create(
            model=LLM_MODEL,
            messages=messages,
            temperature=0.3  # 降低随机性，保证工具调用格式正确
        )

        return response.choices[0].message.content.strip()

    def _parse_tool_call(self, llm_response: str) -> Optional[Dict[str, str]]:
        """解析 LLM 响应中的工具调用指令（JSON 格式）"""
        import json
        # 提取 JSON 格式的工具调用（假设 LLM 单独一行输出 JSON）
        lines = llm_response.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith("{") and line.endswith("}"):
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    continue
        return None  # 未识别到工具调用（可能是最终结论）

    def run_multi_round_inference(self) -> str:
        """多轮推理循环：按拆解的目标逐步执行，直到完成所有步骤"""
        while self.current_goal_index < len(self.inference_goals):
            current_goal = self.inference_goals[self.current_goal_index]
            print(f"\n=== 执行推理目标 {self.current_goal_index + 1}/{len(self.inference_goals)}: {current_goal} ===")

            # 生成当前轮的提示词（包含历史上下文和当前目标）
            history_context = "\n".join([
                f"- {msg['role']}: {msg['content'][:100]}..." for msg in self.conversation_history[-3:]  # 只保留最近 3 条上下文（避免过长）
            ])
            current_prompt = MULTI_ROUND_PROMPT.format(
                history_context=history_context,
                next_goal=current_goal
            )

            # 调用 LLM 生成响应（工具调用或结论）
            llm_response = self._get_llm_response(current_prompt)
            self.conversation_history.append({"role": "assistant", "content": llm_response})

            # 解析工具调用
            tool_call = self._parse_tool_call(llm_response)
            if not tool_call:
                # 未识别到工具调用，判断是否为最终结论
                if self.current_goal_index == len(self.inference_goals) - 1:
                    print("=== 推理完成，返回最终结论 ===")
                    return llm_response
                else:
                    # 未完成所有目标但未调用工具，提示 LLM 继续
                    self.conversation_history.append({
                        "role": "system",
                        "content": "未识别到工具调用，请按要求调用 sql_tool 或 python_tool 完成当前推理目标"
                    })
                    continue

            # 执行工具调用
            tool_name = tool_call["name"]
            tool_params = tool_call["parameters"]

            if tool_name == "sql_tool":
                # 执行 SQL 工具
                sql_result = self.sql_tool.run(tool_params["query"])
                self.conversation_history.append({"role": "system", "content": f"SQL 工具执行结果：{sql_result['message']}\n数据预览：{sql_result['data']}"})

                if sql_result["status"] == "success":
                    # 将 SQL 结果的 DataFrame 注入 Python 工具的全局变量
                    df = pd.DataFrame(sql_result["data"])  # 实际场景中需用完整结果，此处简化为预览数据
                    self.python_tool.inject_df(sql_result["var_name"], df)
                    self.current_goal_index += 1  # 执行成功，进入下一个目标
                else:
                    # SQL 执行失败，让 LLM 修正查询
                    self.conversation_history.append({"role": "system", "content": f"SQL 执行失败，请修正查询语句后重新调用"})

            elif tool_name == "python_tool":
                # 执行 Python 工具
                python_result = self.python_tool.run(tool_params["code"])
                self.conversation_history.append({"role": "system", "content": f"Python 工具执行结果：{python_result['message']}\n结果预览：{python_result['data']}"})

                if python_result["status"] == "success":
                    self.current_goal_index += 1  # 执行成功，进入下一个目标
                else:
                    # Python 执行失败，让 LLM 修正代码
                    self.conversation_history.append({"role": "system", "content": f"Python 执行失败，请修正代码后重新调用"})

            else:
                # 未知工具，提示 LLM
                self.conversation_history.append({"role": "system", "content": f"未知工具 {tool_name}，请调用 sql_tool 或 python_tool"})

        # 所有目标执行完成，生成最终结论
        final_prompt = "所有推理步骤已完成，请整理成自然语言结论，包含关键数据、分析逻辑和最终结论。"
        final_response = self._get_llm_response(final_prompt)
        return final_response

    def run(self, user_query: str) -> str:
        """Agent 主入口：接收用户查询，执行完整的多轮 DeepResearch"""
        print(f"用户需求：{user_query}")
        print("\n=== 第一步：解析意图，拆解推理目标 ===")
        self._parse_user_intent(user_query)

        print("\n=== 第二步：多轮推理执行 ===")
        final_conclusion = self.run_multi_round_inference()

        print("\n=== 最终结论 ===")
        return final_conclusion
```

#### （6）main.py 测试入口
```python
from agents.deep_research_agent import DeepResearchAgent

if __name__ == "__main__":
    # 示例用户需求（深度分析任务）
    user_query = """
    分析2024年各季度的用户留存率：
    1. 按注册季度分组，计算每个季度新用户的 7 日留存率和 30 日留存率；
    2. 找出留存率最高的 2 个用户渠道；
    3. 计算这 2 个渠道的平均客单价（ARPU）和付费转化率；
    4. 给出这 2 个渠道的优化建议。
    """

    # 初始化并运行 Agent
    agent = DeepResearchAgent()
    result = agent.run(user_query)
    print(result)
```

## 三、关键设计说明
### 1. 多轮推理的核心逻辑
- **意图拆解**：将复杂需求拆分为「递进式目标」，前一个目标的输出是后一个的输入（如 SQL 查询 → 季度留存计算 → 渠道筛选 → ARPU 计算）。
- **上下文管理**：保存每轮的工具执行结果（如 SQL 变量名、Python 计算结果），让 LLM 知道当前可用的数据。
- **错误重试**：若 SQL 查询失败（语法错误）或 Python 代码执行失败（逻辑错误），Agent 会让 LLM 修正后重新执行，保证推理连续性。

### 2. 数据注入与全局变量管理
- SQL 工具查询结果自动转换为 DataFrame，并以 `df_sql_1`「`df_sql_2` 等命名注入 Python 工具的 `global_vars`。
- Python 代码执行时，可直接使用这些全局变量，计算结果存入新的全局变量（如 `df_quarterly_retention`），供后续轮次使用。
- 避免全局变量污染：Python 工具的 `global_vars` 是独立的，仅在当前 Agent 实例中有效。

### 3. 提示词设计技巧
- **系统提示词**：明确 Agent 的角色、工作流程、工具调用格式（严格 JSON 格式），避免 LLM 生成无关内容。
- **工具描述词**：详细说明工具的功能、参数要求、返回格式，让 LLM 知道如何正确调用。
- **多轮推理提示词**：每次只聚焦一个推理目标，提供最近的上下文，避免 LLM 遗忘之前的步骤。

## 四、扩展与优化方向
1. **支持更多 LLM**：将 OpenAI 客户端替换为 LangChain 的 `ChatOpenAI`「`ChatAnthropic` 等，实现多模型兼容。
2. **复杂推理目标拆解优化**：通过 Few-Shot 示例（在提示词中加入更多拆解案例），让 LLM 拆解更精准。
3. **数据缓存与复用**：将 SQL 查询结果缓存到本地（如 Parquet 文件），避免重复查询数据库。
4. **代码安全校验**：在 Python 工具中加入代码审计（如禁止 `os`「`subprocess` 等危险库），防止恶意代码执行。
5. **可视化集成**：在 Python 工具中支持 Matplotlib/Seaborn 绘图，将分析结果可视化后返回给用户。

## 五、示例运行流程
1. 用户输入需求：分析2024年各季度用户留存率、top2渠道的 ARPU 和付费转化率。
2. Agent 拆解推理目标：
   - 目标1：查询2024年用户注册时间、留存状态、渠道、消费金额（SQL 工具）。
   - 目标2：按注册季度分组，计算7日/30日留存率（Python 工具）。
   - 目标3：筛选留存率最高的2个渠道（Python 工具）。
   - 目标4：计算这2个渠道的 ARPU 和付费转化率（Python 工具）。
   - 目标5：生成优化建议（自然语言结论）。
3. 执行目标1：调用 SQL 工具，返回 `df_sql_1`，注入 Python 全局变量。
4. 执行目标2：LLM 生成 Python 代码，计算季度留存率，存入 `df_quarterly_retention`。
5. 执行目标3：LLM 生成代码，筛选 top2 渠道，存入 `df_top2_channels`。
6. 执行目标4：LLM 生成代码，计算 ARPU 和付费转化率，存入 `df_channel_metrics`。
7. 执行目标5：LLM 整理所有结果，生成自然语言结论和优化建议。

通过以上流程，Agent 实现了从「自然语言需求」到「深度数据分析」的全自动化多轮推理。


