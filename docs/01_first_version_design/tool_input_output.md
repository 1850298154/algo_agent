# https://www.doubao.com/chat/29810530194234370
# input
工具调用（如 OpenAI 的 `functions`）中的 `parameters` 与 Pydantic `BaseModel` 通过 `model_json_schema()` 生成的 Schema **不完全一样，但核心结构兼容**——前者是大模型工具调用的“适配版 Schema”，后者是标准 JSON Schema，需通过简单调整才能完全对齐。

关键结论：**Pydantic 的 `model_json_schema()` 会生成标准 JSON Schema Draft 7/2020-12 格式，而大模型（如 OpenAI）的工具 `parameters` 是基于标准 JSON Schema 的“简化子集”**，大部分字段直接复用，但部分细节存在差异，需要映射适配。


### 一、核心异同点对比（以 OpenAI 工具 `parameters` 为例）
#### 1. 相同点（核心结构一致）
大模型工具 `parameters` 的核心字段（`type: object`、`properties`、`required`、`enum`、`format` 等）完全遵循标准 JSON Schema，而 Pydantic 的 `model_json_schema()` 正是生成标准 JSON Schema，因此：
- 字段类型映射一致：`str`→`string`、`int/float`→`number`、`bool`→`boolean`、`List`→`array`、嵌套 `BaseModel`→`object`；
- 约束字段一致：`required`（必填参数）、`enum`（枚举值）、`description`（字段说明）、`format`（格式约束，如 `date`/`email`）、`pattern`（正则约束）等可直接复用。

#### 示例：Pydantic 模型与工具 `parameters` 的核心对齐
```python
from pydantic import BaseModel, Field
from typing import List, Optional

# 定义 Pydantic 模型（描述工具参数）
class WeatherParams(BaseModel):
    city: str = Field(description="城市名称（国内地级市，如北京、上海）")
    date: str = Field(description="查询日期，格式 YYYY-MM-DD", format="date")
    weather_type: Optional[List[str]] = Field(
        default=["温度", "降水", "风力"],
        description="需要查询的天气类型",
        enum=["温度", "降水", "风力", "全部"]
    )

# 生成标准 JSON Schema
pydantic_schema = WeatherParams.model_json_schema()
print("Pydantic 生成的标准 JSON Schema：")
print(pydantic_schema)
```

输出的 `pydantic_schema` 核心结构：
```json
{
  "type": "object",
  "properties": {
    "city": {"type": "string", "description": "城市名称（国内地级市，如北京、上海）"},
    "date": {"type": "string", "description": "查询日期，格式 YYYY-MM-DD", "format": "date"},
    "weather_type": {
      "type": "array",
      "items": {"type": "string", "enum": ["温度", "降水", "风力", "全部"]},
      "description": "需要查询的天气类型",
      "default": ["温度", "降水", "风力"]
    }
  },
  "required": ["city", "date"],  // Pydantic 自动识别必填字段（无默认值的非 Optional 字段）
  "$schema": "http://json-schema.org/draft-07/schema#"  // 标准 JSON Schema 标识
}
```

而 OpenAI 工具的 `parameters` 结构（直接复用上述核心字段）：
```json
{
  "type": "object",
  "properties": {
    "city": {"type": "string", "description": "城市名称（国内地级市，如北京、上海）"},
    "date": {"type": "string", "description": "查询日期，格式 YYYY-MM-DD", "format": "date"},
    "weather_type": {
      "type": "array",
      "items": {"type": "string", "enum": ["温度", "降水", "风力", "全部"]},
      "description": "需要查询的天气类型",
      "default": ["温度", "降水", "风力"]
    }
  },
  "required": ["city", "date"]
}
```

可见：**核心的 `properties`、`required`、字段约束完全一致**，这是两者兼容的基础。


#### 2. 差异点（关键！需适配）
Pydantic 生成的标准 JSON Schema 包含一些大模型工具 `parameters` 不需要/不支持的字段，同时部分模型对字段有特殊要求，具体差异如下：

| 维度                | Pydantic `model_json_schema()` 生成的 Schema                | 大模型工具 `parameters`（如 OpenAI）要求                     |
|---------------------|-------------------------------------------------------------|-------------------------------------------------------------|
| 顶层标识字段        | 包含 `$schema`（如 `"$schema": "http://json-schema.org/draft-07/schema#"`）、`title`（默认模型名）、`description`（模型文档字符串） | 不需要这些字段，仅保留 `type: object`、`properties`、`required` |
| 空值约束（`nullable`） | 对于 `Optional` 类型（如 `Optional[str]`），会生成 `nullable: true` | 大部分大模型不支持 `nullable`，需删除或替换为 `type: ["string", "null"]`（部分模型兼容） |
| 默认值（`default`） | 会保留 `default` 字段（如上述 `weather_type` 的默认值）      | OpenAI 等模型支持 `default`（模型会优先使用默认值），但部分国产模型可能忽略，需提前确认 |
| 复杂类型处理        | 嵌套 `BaseModel` 会生成完整的嵌套 `object` 结构（含子 `properties`） | 支持，但需确保嵌套层级不超过 2-3 层（模型对过深嵌套解析能力有限） |
| 额外元数据          | 可能包含 `examples`、`exclusiveMinimum` 等高级约束（Pydantic 支持的） | 大部分模型仅支持基础约束（`type`/`enum`/`format`/`pattern`），高级约束可能被忽略 |

示例：Pydantic 生成的 Schema 含 `$schema` 和 `nullable`，需清理后才能用于工具调用：
```python
# Pydantic 生成的 Schema （含多余字段）
pydantic_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "WeatherParams",
  "type": "object",
  "properties": {
    "optional_field": {
      "type": "string",
      "description": "可选字段",
      "nullable": true  # 部分模型不支持
    }
  },
  "required": ["city", "date"]
}

# 适配为 OpenAI 工具的 parameters
tool_parameters = {
  "type": "object",
  "properties": {
    # 移除 nullable，或改为 type: ["string", "null"]（兼容方案）
    "optional_field": {"type": ["string", "null"], "description": "可选字段"}
  },
  "required": ["city", "date"]
}
```


### 二、为什么会有差异？
1. **设计目标不同**：
   - Pydantic 的 `model_json_schema()` 目标是生成**标准、完整的 JSON Schema**，用于数据校验、API 文档（如 FastAPI 自动生成接口文档）等通用场景；
   - 大模型工具 `parameters` 目标是**让模型快速理解参数格式**，无需复杂的标准字段（如 `$schema`），且模型对部分高级约束（如 `nullable`）的解析能力有限，因此做了简化。

2. **模型兼容性考量**：
   - 主流大模型（OpenAI、Anthropic 等）仅支持 JSON Schema 的“核心子集”，冗余字段会增加模型解析负担，甚至导致格式错误；
   - Pydantic 作为通用数据校验库，需兼容完整的 JSON Schema 标准，因此会包含更多元数据。


### 三、实操：如何用 Pydantic 快速生成工具 `parameters`？
由于核心结构一致，实际开发中可直接用 Pydantic 定义参数模型，再通过“清理冗余字段”适配大模型工具，步骤如下：

#### 1. 定义 Pydantic 模型（带完整约束）
```python
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional

class CalculateParams(BaseModel):
    """数学计算工具的参数模型"""
    num1: float = Field(description="第一个运算数", ge=0)  # ge=0：大于等于0（Pydantic 高级约束）
    num2: float = Field(description="第二个运算数", ge=0)
    operator: str = Field(description="运算符号", enum=["+", "-", "*", "/", "^"])
    is_detailed: Optional[bool] = Field(default=False, description="是否返回详细计算过程")

# 生成标准 JSON Schema
raw_schema = CalculateParams.model_json_schema()
```

#### 2. 清理适配（保留核心字段，删除冗余）
```python
def adapt_pydantic_to_tool_schema(raw_schema: dict) -> dict:
    """将 Pydantic 生成的 Schema 适配为大模型工具 parameters"""
    # 保留核心字段：type、properties、required
    tool_schema = {
        "type": raw_schema.get("type"),
        "properties": raw_schema.get("properties", {}),
        "required": raw_schema.get("required", [])
    }
    
    # 清理 properties 中的冗余字段（如 nullable、$schema 等）
    for field_name, field_schema in tool_schema["properties"].items():
        # 移除 nullable（部分模型不支持），改为 type: [原类型, "null"]（兼容 Optional）
        if "nullable" in field_schema:
            nullable = field_schema.pop("nullable")
            if nullable and isinstance(field_schema.get("type"), str):
                field_schema["type"] = [field_schema["type"], "null"]
        
        # 移除 Pydantic 特有或模型不支持的字段（如 examples、ge 等）
        for key in ["examples", "ge", "le", "exclusiveMinimum", "exclusiveMaximum"]:
            field_schema.pop(key, None)
    
    return tool_schema

# 生成适配后的工具 parameters
tool_parameters = adapt_pydantic_to_tool_schema(raw_schema)
print("适配后的工具 parameters：")
print(tool_parameters)
```

#### 3. 最终用于大模型工具调用
```python
import openai

openai.api_key = "你的密钥"

# 完整的工具 Schema（结合 name、description 和适配后的 parameters）
tool = {
    "name": "calculate",
    "description": "执行数学计算（加减乘除、幂运算），仅支持非负数",
    "parameters": tool_parameters  # 直接使用适配后的 Schema
}

# 调用模型
response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "计算 3 的 4 次方，返回详细过程"}],
    functions=[tool],
    function_call="auto"
)
```

适配后的 `tool_parameters` 完全符合大模型要求，且通过 Pydantic 实现了参数约束的“一次定义、多端复用”（既用于工具调用 Schema，也可用于后续解析模型返回的参数时做数据校验）。


### 四、特殊场景：模型对 Schema 的额外要求
部分模型（如 Anthropic Claude、国产模型）对工具 Schema 有轻微差异，需针对性调整：
1. **Anthropic Claude**：工具 Schema 嵌套在 `tool.input_schema` 中，支持完整 JSON Schema，但需指定 `type: object`，无需额外清理；
2. **国产模型（通义千问/文心一言）**：基本兼容 OpenAI 格式，但部分不支持 `default` 字段，需删除；
3. **llama.cpp 等开源模型**：对 `enum`、`array` 的解析能力较弱，建议参数类型尽量简单（少用嵌套 `object`）。


### 总结
- **核心兼容**：Pydantic `model_json_schema()` 生成的标准 JSON Schema 与工具 `parameters` 核心结构（`properties`、`required`、字段约束）完全一致；
- **关键差异**：Pydantic  Schema 包含 `$schema`、`nullable` 等冗余字段，大模型工具 `parameters` 需清理这些字段；
- **实操建议**：用 Pydantic 定义参数模型（兼顾工具 Schema 生成和数据校验），通过简单函数清理冗余字段，快速适配不同模型的工具调用格式。

这种方式是工业界的主流实践——既保证了参数约束的一致性，又避免了手动编写 JSON Schema 的繁琐和错误。

