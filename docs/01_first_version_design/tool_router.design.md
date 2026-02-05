https://www.doubao.com/chat/28971914761641218

# 使用 Pydantic 定义 AI Agent 工具（Tool）Schema 的完整实现方案
用 `pydantic.BaseModel` 定义 AI Agent 的 Tool Schema 是**行业标准做法**（如 LangChain、LlamaIndex 等框架均推荐）——它能同时实现「参数校验」「JSON 序列化（适配 Agent 工具调用协议）」「自动生成工具描述」，完美匹配 Agent 调用工具时的核心需求（明确输入参数、格式标准化、错误兜底）。

以下是一套完整的 Tool Schema 定义方案，包含基础工具、带复杂参数的工具、工具集管理，同时兼容 Agent 常见的工具调用流程：


## 核心思路
AI Agent 调用工具的核心是「理解工具的输入参数格式 + 按格式传参」，`BaseModel` 刚好解决这两个问题：
1. 用类字段定义工具的输入参数（类型、默认值、描述）；
2. 自带 `model_dump_json()` 生成 Agent 可识别的 JSON Schema；
3. 自动校验 Agent 传入的参数（避免类型错误、必填项缺失）；
4. 可通过字段注释/配置生成工具描述（让 Agent 知道工具用途）。


## 完整实现方案
### 1. 基础工具定义（单工具 + 简单参数）
适用于功能单一、参数简单的工具（如「天气查询」「计算」）。

```python
from pydantic import BaseModel, Field
from typing import Optional

# ---------------------- 定义 Tool Schema ----------------------
class WeatherQueryTool(BaseModel):
    """
    工具描述：查询指定城市的实时天气（让 Agent 知道该什么时候用）
    """
    # 字段 = Field(默认值, description="参数描述", ...) —— 核心配置
    city: str = Field(..., description="要查询的城市名称（必填，如：北京、上海）")
    date: Optional[str] = Field(
        default="today", 
        description="查询日期（可选，默认今天；格式：YYYY-MM-DD，如：2025-11-14）"
    )
    temperature_unit: Optional[str] = Field(
        default="celsius", 
        description="温度单位（可选，仅支持 celsius/fahrenheit，默认摄氏度）"
    )

    # ---------------------- 工具核心逻辑 ----------------------
    def run(self) -> str:
        """工具执行逻辑（Agent 调用工具时实际运行的代码）"""
        # 这里替换为真实的天气查询逻辑（如调用天气 API）
        return (
            f"【天气查询结果】\n"
            f"城市：{self.city}\n"
            f"日期：{self.date}\n"
            f"温度单位：{self.temperature_unit}\n"
            f"实时温度：18℃（示例数据）\n"
            f"天气状况：晴"
        )

    # ---------------------- 兼容 Agent 工具调用协议 ----------------------
    def get_schema(self) -> dict:
        """生成 Agent 可识别的 JSON Schema（描述参数格式）"""
        return self.model_json_schema()  # Pydantic 自带方法，直接生成标准 JSON Schema

# ---------------------- Agent 调用工具的模拟流程 ----------------------
if __name__ == "__main__":
    # 1. Agent 先获取工具的 Schema（知道需要传什么参数）
    tool = WeatherQueryTool(city="北京")
    print("工具 JSON Schema：")
    print(tool.get_schema())  # 输出参数格式描述，供 Agent 参考

    # 2. Agent 按 Schema 传入参数（Pydantic 自动校验）
    try:
        # 正确参数（符合 Schema）
        valid_tool = WeatherQueryTool(city="上海", date="2025-11-14")
        # 3. 执行工具并获取结果
        result = valid_tool.run()
        print("\n工具执行结果：")
        print(result)
    except ValueError as e:
        print(f"参数错误：{e}")

    # 4. 错误参数示例（触发 Pydantic 校验）
    try:
        invalid_tool = WeatherQueryTool(city=123)  # city 应为字符串，触发类型错误
    except ValueError as e:
        print(f"\n参数校验失败：{e}")
```


### 2. 复杂工具定义（嵌套参数 + 多类型支持）
适用于参数复杂的工具（如「订单创建」「数据筛选」），支持嵌套 `BaseModel` 作为参数。

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

# ---------------------- 嵌套参数 Schema（子模型） ----------------------
class ProductInfo(BaseModel):
    """订单中的商品信息（嵌套参数）"""
    product_id: str = Field(..., description="商品ID（必填，如：PROD1001）")
    quantity: int = Field(..., ge=1, description="购买数量（必填，至少1件）")
    price: float = Field(..., gt=0, description="商品单价（必填，大于0）")

# ---------------------- 主工具 Schema ----------------------
class CreateOrderTool(BaseModel):
    """
    工具描述：创建用户订单（支持多商品批量下单，自动计算总价）
    """
    user_id: str = Field(..., description="用户ID（必填，如：U123456）")
    products: List[ProductInfo] = Field(..., description="商品列表（必填，至少1件商品）")
    payment_method: Literal["wechat", "alipay", "card"] = Field(
        ..., description="支付方式（必填，仅支持 wechat/alipay/card）"
    )
    coupon_code: Optional[str] = Field(
        default=None, description="优惠券码（可选，如：COUPON2025）"
    )

    # 工具执行逻辑
    def run(self) -> str:
        """计算订单总价并返回订单信息"""
        total_amount = sum(p.price * p.quantity for p in self.products)
        order_id = f"ORD-{self.user_id}-{len(self.products)}-{hash(self)}"[:16]  # 生成临时订单ID
        return (
            f"【订单创建成功】\n"
            f"订单ID：{order_id}\n"
            f"用户ID：{self.user_id}\n"
            f"商品数量：{len(self.products)}件\n"
            f"支付方式：{self.payment_method}\n"
            f"订单总价：{total_amount:.2f}元\n"
            f"优惠券码：{self.coupon_code or '无'}"
        )

# ---------------------- 测试复杂工具 ----------------------
if __name__ == "__main__":
    # 构造嵌套参数
    products = [
        ProductInfo(product_id="PROD1001", quantity=2, price=399.99),
        ProductInfo(product_id="PROD1002", quantity=1, price=199.99)
    ]

    # 创建工具实例（自动校验参数）
    order_tool = CreateOrderTool(
        user_id="U123456",
        products=products,
        payment_method="wechat",
        coupon_code="COUPON10"
    )

    # 执行工具
    print(order_tool.run())
```


### 3. 工具集管理（多工具统一注册 + 动态调用）
当 Agent 有多个工具时，可通过「工具注册表」统一管理，方便 Agent 按名称选择工具。

```python
from pydantic import BaseModel
from typing import Dict, Type, Any
import inspect

# ---------------------- 第一步：定义工具基类（统一接口） ----------------------
class BaseTool(BaseModel):
    """所有工具的基类，统一接口"""
    @classmethod
    def tool_name(cls) -> str:
        """工具名称（Agent 用于选择工具）"""
        return cls.__name__.lower().replace("tool", "")  # 如 WeatherQueryTool → weatherquery

    @classmethod
    def tool_description(cls) -> str:
        """工具描述（从类注释中提取，供 Agent 理解用途）"""
        return inspect.getdoc(cls) or "无描述"

    def run(self) -> str:
        """工具执行逻辑（子类必须实现）"""
        raise NotImplementedError("子类必须实现 run 方法")

    def get_schema(self) -> dict:
        """获取参数 JSON Schema"""
        return self.model_json_schema()

# ---------------------- 第二步：定义具体工具（继承基类） ----------------------
class WeatherQueryTool(BaseTool):
    """查询指定城市的实时天气"""
    city: str = Field(..., description="要查询的城市名称（必填）")
    date: Optional[str] = Field(default="today", description="查询日期（默认今天）")

    def run(self) -> str:
        return f"【天气结果】{self.city} {self.date}：晴，18℃"

class CalculatorTool(BaseTool):
    """执行简单的数学计算（支持 +-*/）"""
    expression: str = Field(..., description="数学表达式（必填，如：1+2*3、(5-2)/4）")

    def run(self) -> str:
        try:
            result = eval(self.expression)  # 实际使用需注意安全，可替换为更安全的计算方式
            return f"【计算结果】{self.expression} = {result}"
        except Exception as e:
            return f"【计算失败】{str(e)}"

# ---------------------- 第三步：工具集注册表（Agent 统一调用） ----------------------
class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Type[BaseTool]] = {}  # 工具名称 → 工具类

    def register_tool(self, tool_cls: Type[BaseTool]):
        """注册工具"""
        tool_name = tool_cls.tool_name()
        self.tools[tool_name] = tool_cls
        print(f"注册工具：{tool_name} → {tool_cls.__name__}")

    def get_tool(self, tool_name: str) -> Type[BaseTool]:
        """根据名称获取工具类"""
        if tool_name not in self.tools:
            raise ValueError(f"未找到工具：{tool_name}（可用工具：{list(self.tools.keys())}）")
        return self.tools[tool_name]

    def list_tools(self) -> list[dict]:
        """列出所有工具的信息（供 Agent 选择）"""
        return [
            {
                "tool_name": tool.tool_name(),
                "description": tool.tool_description(),
                "parameters": tool().get_schema()  # 生成参数 Schema
            }
            for tool in self.tools.values()
        ]

# ---------------------- 测试工具集 ----------------------
if __name__ == "__main__":
    # 1. 初始化注册表并注册工具
    registry = ToolRegistry()
    registry.register_tool(WeatherQueryTool)
    registry.register_tool(CalculatorTool)

    # 2. Agent 查看所有可用工具
    print("\n可用工具列表：")
    for tool_info in registry.list_tools():
        print(f"\n工具名称：{tool_info['tool_name']}")
        print(f"描述：{tool_info['description']}")
        print(f"参数格式：{tool_info['parameters']}")

    # 3. Agent 选择工具并调用
    # 示例1：调用天气工具
    weather_tool_cls = registry.get_tool("weatherquery")
    weather_tool = weather_tool_cls(city="广州", date="2025-11-14")
    print("\n天气工具执行结果：", weather_tool.run())

    # 示例2：调用计算工具
    calculator_tool_cls = registry.get_tool("calculator")
    calculator_tool = calculator_tool_cls(expression="(10+20)*3")
    print("计算工具执行结果：", calculator_tool.run())
```


## 关键配置说明（适配 Agent 需求）
### 1. `Field` 字段配置（核心）
Agent 需要明确知道参数的「是否必填」「描述」「可选值」，`Field` 是关键：
- `...`：表示必填参数（Agent 必须传入）；
- `default=xxx`：可选参数，指定默认值；
- `description="xxx"`：参数说明（让 Agent 理解该传什么）；
- `ge/gt/le/lt`：数值校验（如 `ge=1` 表示大于等于1）；
- `Literal["a", "b"]`：限制参数只能是指定值（如支付方式仅支持3种）；
- `examples=["xxx"]`：添加示例值（帮助 Agent 更准确传参）。

示例：
```python
phone: str = Field(
    ...,
    description="用户手机号（必填）",
    pattern=r"^1[3-9]\d{9}$",  # 正则校验手机号格式
    examples=["13800138000"]
)
```

### 2. 工具描述（类注释）
类注释会被 Agent 读取，用于判断「什么时候该调用这个工具」，需明确：
- 工具用途（如「查询天气」「创建订单」）；
- 适用场景（如「当用户询问某个城市的天气时使用」）。

### 3. JSON Schema 生成
`model_json_schema()` 是 Pydantic 自带方法，会生成**标准 JSON Schema**（符合 OpenAPI 规范），Agent 可通过该 Schema 自动构造参数（无需手动写 JSON）。

生成的 Schema 示例（WeatherQueryTool）：
```json
{
  "title": "WeatherQueryTool",
  "type": "object",
  "properties": {
    "city": {"type": "string", "description": "要查询的城市名称（必填）"},
    "date": {"type": "string", "description": "查询日期（默认今天）", "default": "today"}
  },
  "required": ["city"]  // 明确必填项
}
```


## 与 AI Agent 集成的核心优势
1. **参数校验兜底**：Agent 传入错误参数（如类型错误、必填项缺失）时，Pydantic 会直接报错，避免工具执行失败；
2. **格式标准化**：`model_dump_json()` 生成的 JSON 格式统一，Agent 无需关心序列化细节；
3. **自动生成文档**：通过 `get_schema()` 和类注释，Agent 可自动获取工具信息，无需额外写文档；
4. **扩展性强**：支持嵌套参数、复杂类型校验、自定义逻辑，满足各种工具需求。


## 常见扩展场景
1. **工具异步执行**：如果工具需要调用 API（耗时操作），可将 `run` 方法改为异步：
   ```python
   async def run(self) -> str:
       # 异步调用 API
       response = await aiohttp.request("GET", f"https://api.weather.com/{self.city}")
       return response.json()
   ```

2. **参数别名**：如果工具参数名与 API 字段名不一致，可用 `alias`：
   ```python
   user_name: str = Field(..., alias="username", description="用户名")
   ```
   序列化时会自动转为 `username`：`tool.model_dump_json(by_alias=True)`。

3. **忽略字段**：如果某个字段不需要被 Agent 看到，可用 `exclude`：
   ```python
   class Tool(BaseModel):
       secret_key: str = Field(..., exclude=True)  # 序列化时忽略该字段
   ```


总结：用 `pydantic.BaseModel` 定义 Agent Tool Schema，既能保证参数的规范性和安全性，又能无缝对接 Agent 的工具调用流程，是目前最成熟、最高效的实现方式。

# 工具路由器实现

要实现「根据工具名路由到对应工具+传递参数」的分类器（本质是 **工具路由器**），核心思路是：**建立「工具名→工具类」的映射关系，接收工具名和参数后，自动匹配工具、校验参数、执行逻辑**。

结合之前的 Pydantic Tool Schema，以下是一套完整的实现方案，支持「自动路由、参数校验、结果返回」，可直接集成到 AI Agent 中：


## 核心架构
工具路由器的核心流程：
1. **注册工具**：将所有工具类（继承自 `BaseTool`）注册到路由器，建立「工具名→工具类」的映射；
2. **接收请求**：AI Agent 输出「工具名+参数字典」（如 `{"tool_name": "weatherquery", "parameters": {"city": "北京"}}`）；
3. **路由匹配**：根据工具名找到对应的工具类；
4. **参数校验**：用工具类的 Pydantic Schema 校验传入的参数（自动处理类型错误、必填项缺失）；
5. **执行工具**：调用工具的 `run` 方法，返回执行结果；
6. **错误处理**：统一捕获路由失败、参数错误、工具执行异常。


## 完整实现代码
### 1. 基础准备（工具基类 + 具体工具）
先定义工具基类和2个示例工具（天气查询、计算器），复用之前的 Pydantic Schema 逻辑：

```python
from pydantic import BaseModel, Field, ValidationError
from typing import Dict, Type, Any, Optional, Literal, List
import inspect

# ---------------------- 工具基类（统一接口） ----------------------
class BaseTool(BaseModel):
    """所有工具的基类，定义统一接口"""
    @classmethod
    def tool_name(cls) -> str:
        """工具唯一标识名（用于路由匹配，如 "weatherquery"）"""
        return cls.__name__.lower().replace("tool", "")  # 自动生成工具名

    @classmethod
    def tool_description(cls) -> str:
        """工具描述（供 Agent 理解用途）"""
        return inspect.getdoc(cls) or "无工具描述"

    def run(self) -> str:
        """工具核心执行逻辑（子类必须实现）"""
        raise NotImplementedError("所有工具必须实现 run 方法")

    @classmethod
    def get_parameter_schema(cls) -> dict:
        """获取参数 JSON Schema（供 Agent 构造参数）"""
        return cls.model_json_schema()

# ---------------------- 具体工具实现 ----------------------
class WeatherQueryTool(BaseTool):
    """
    工具描述：查询指定城市的实时天气
    适用场景：当用户询问某个城市的天气、温度、天气状况时使用
    """
    city: str = Field(
        ..., 
        description="要查询的城市名称（必填，如：北京、上海、广州）",
        examples=["北京"]
    )
    date: Optional[str] = Field(
        default="today", 
        description="查询日期（可选，格式：YYYY-MM-DD，默认今天）",
        examples=["2025-11-15"]
    )
    unit: Literal["celsius", "fahrenheit"] = Field(
        default="celsius", 
        description="温度单位（可选，默认摄氏度，支持 celsius/fahrenheit）"
    )

    def run(self) -> str:
        """模拟天气查询逻辑"""
        return (
            f"✅ 天气查询结果\n"
            f"城市：{self.city}\n"
            f"日期：{self.date}\n"
            f"温度单位：{'摄氏度' if self.unit == 'celsius' else '华氏度'}\n"
            f"天气状况：晴\n"
            f"实时温度：19℃"
        )

class CalculatorTool(BaseTool):
    """
    工具描述：执行简单数学计算（支持 +-*/ 及括号优先级）
    适用场景：当用户需要计算数值、求解数学表达式时使用
    """
    expression: str = Field(
        ..., 
        description="数学表达式（必填，如：1+2*3、(5-2)/4、10^2）",
        examples=["(10+20)*3", "5^2-3"]
    )

    def run(self) -> str:
        """模拟数学计算逻辑（实际使用需注意安全，避免恶意表达式）"""
        try:
            # 替换 ^ 为 **（Python 幂运算）
            safe_expr = self.expression.replace("^", "**")
            # 用 eval 执行计算（仅示例，生产环境建议用 ast 模块安全解析）
            result = eval(safe_expr)
            return f"✅ 计算结果\n表达式：{self.expression}\n结果：{result}"
        except Exception as e:
            return f"❌ 计算失败：{str(e)}（请检查表达式格式）"

class OrderCreateTool(BaseTool):
    """
    工具描述：创建用户订单（支持多商品批量下单）
    适用场景：当用户需要购买商品、生成订单时使用
    """
    user_id: str = Field(..., description="用户ID（必填，如：U123456）")
    products: List[Dict[str, Any]] = Field(
        ..., 
        description="商品列表（必填，每个商品包含 product_id:str、quantity:int、price:float）"
    )

    def run(self) -> str:
        """模拟创建订单逻辑"""
        total_price = sum(p["price"] * p["quantity"] for p in self.products)
        order_id = f"ORD-{self.user_id}-{hash(str(self.products))}"[:12]
        return (
            f"✅ 订单创建成功\n"
            f"订单ID：{order_id}\n"
            f"用户ID：{self.user_id}\n"
            f"商品数量：{len(self.products)}件\n"
            f"订单总价：{total_price:.2f}元"
        )
```


### 2. 实现工具路由器（核心分类器）
路由器负责「工具注册、路由匹配、参数校验、执行调度」，提供简洁的调用接口：

```python
class ToolRouter:
    def __init__(self):
        # 存储工具映射：key=工具名（str），value=工具类（BaseTool 子类）
        self.tool_map: Dict[str, Type[BaseTool]] = {}

    def register_tool(self, tool_cls: Type[BaseTool]) -> None:
        """
        注册工具到路由器
        :param tool_cls: 工具类（必须继承 BaseTool）
        """
        if not issubclass(tool_cls, BaseTool):
            raise TypeError(f"工具类必须继承 BaseTool，当前类型：{type(tool_cls)}")
        
        tool_name = tool_cls.tool_name()
        if tool_name in self.tool_map:
            raise ValueError(f"工具名已存在：{tool_name}（避免重复注册）")
        
        self.tool_map[tool_name] = tool_cls
        print(f"✅ 注册工具成功：{tool_name} → {tool_cls.__name__}")

    def list_tools(self) -> List[Dict[str, Any]]:
        """
        列出所有已注册工具的信息（供 AI Agent 选择工具）
        :return: 工具列表（包含工具名、描述、参数 Schema）
        """
        return [
            {
                "tool_name": tool_cls.tool_name(),
                "description": tool_cls.tool_description(),
                "parameter_schema": tool_cls.get_parameter_schema()
            }
            for tool_cls in self.tool_map.values()
        ]

    def route(self, tool_name: str, parameters: Dict[str, Any]) -> str:
        """
        核心路由方法：根据工具名匹配工具，校验参数并执行
        :param tool_name: AI Agent 返回的工具名
        :param parameters: AI Agent 返回的参数字典
        :return: 工具执行结果（字符串）
        """
        # 1. 检查工具是否存在
        if tool_name not in self.tool_map:
            available_tools = list(self.tool_map.keys())
            return f"❌ 路由失败：未找到工具「{tool_name}」，可用工具：{available_tools}"
        
        # 2. 获取工具类并校验参数
        tool_cls = self.tool_map[tool_name]
        try:
            # 用 Pydantic 自动校验参数（不符合 Schema 会抛出 ValidationError）
            tool_instance = tool_cls(**parameters)
        except ValidationError as e:
            # 格式化参数错误信息，让 Agent 能修正
            error_details = "\n".join([f"- {err['loc'][0]}: {err['msg']}" for err in e.errors()])
            return f"❌ 参数校验失败（工具：{tool_name}）\n错误详情：\n{error_details}"
        
        # 3. 执行工具并返回结果
        try:
            result = tool_instance.run()
            return result
        except Exception as e:
            return f"❌ 工具执行失败（工具：{tool_name}）\n错误原因：{str(e)}"
```


### 3. 测试工具路由器（模拟 AI Agent 调用流程）
模拟 AI Agent 输出「工具名+参数」，路由器自动路由并执行：

```python
if __name__ == "__main__":
    # 1. 初始化路由器
    router = ToolRouter()

    # 2. 注册所有工具
    router.register_tool(WeatherQueryTool)
    router.register_tool(CalculatorTool)
    router.register_tool(OrderCreateTool)

    # 3. 查看已注册工具（供 Agent 参考）
    print("\n📋 已注册工具列表：")
    for tool_info in router.list_tools():
        print(f"\n工具名：{tool_info['tool_name']}")
        print(f"描述：{tool_info['description']}")
        print(f"参数格式：{tool_info['parameter_schema']['properties']}")

    # 4. 模拟 AI Agent 调用工具（核心测试）
    print("\n" + "="*50)
    print("🚀 模拟 AI Agent 调用工具：")

    # 测试1：调用天气工具（正确参数）
    agent_request1 = {
        "tool_name": "weatherquery",
        "parameters": {"city": "深圳", "date": "2025-11-15", "unit": "celsius"}
    }
    print("\n请求1：", agent_request1)
    result1 = router.route(**agent_request1)
    print("结果1：", result1)

    # 测试2：调用计算工具（错误参数：表达式格式错误）
    agent_request2 = {
        "tool_name": "calculator",
        "parameters": {"expression": "10+*2"}  # 语法错误
    }
    print("\n请求2：", agent_request2)
    result2 = router.route(**agent_request2)
    print("结果2：", result2)

    # 测试3：调用订单工具（正确参数）
    agent_request3 = {
        "tool_name": "ordercreate",
        "parameters": {
            "user_id": "U654321",
            "products": [
                {"product_id": "PROD1001", "quantity": 2, "price": 399.99},
                {"product_id": "PROD1002", "quantity": 1, "price": 199.99}
            ]
        }
    }
    print("\n请求3：", agent_request3)
    result3 = router.route(**agent_request3)
    print("结果3：", result3)

    # 测试4：调用不存在的工具
    agent_request4 = {
        "tool_name": "nonexistent",
        "parameters": {"key": "value"}
    }
    print("\n请求4：", agent_request4)
    result4 = router.route(**agent_request4)
    print("结果4：", result4)
```


## 关键功能说明
### 1. 自动路由匹配
- 工具名由 `BaseTool.tool_name()` 自动生成（如 `WeatherQueryTool` → `weatherquery`），也可手动重写工具名（更灵活）：
  ```python
  class WeatherQueryTool(BaseTool):
      @classmethod
      def tool_name(cls) -> str:
          return "query_weather"  # 手动指定工具名，优先级更高
  ```
- 路由器通过 `tool_name` 快速匹配工具类，时间复杂度 O(1)。

### 2. 严格参数校验
- 利用 Pydantic 的 `ValidationError` 自动捕获参数错误（类型错误、必填项缺失、格式错误等）；
- 错误信息格式化输出，AI Agent 可根据错误详情修正参数（如「city 字段为必填项」「expression 格式错误」）。

### 3. 灵活扩展
- 新增工具只需：① 继承 `BaseTool`；② 定义字段和 `run` 方法；③ 调用 `router.register_tool()` 注册；
- 支持任意复杂工具（嵌套参数、异步执行、第三方 API 调用等）。

### 4. 与 AI Agent 无缝集成
- Agent 可通过 `router.list_tools()` 获取所有工具的「名称+描述+参数 Schema」，自动判断该调用哪个工具；
- Agent 只需输出「工具名+参数字典」，无需关心工具的具体实现和参数校验。


## 扩展场景
### 1. 异步工具支持
如果工具需要异步执行（如调用 HTTP API、数据库查询），可修改基类和路由器支持异步：
```python
# 异步基类
import asyncio
class AsyncBaseTool(BaseModel):
    @classmethod
    def tool_name(cls) -> str:
        return cls.__name__.lower().replace("tool", "")
    
    async def run(self) -> str:
        raise NotImplementedError()

# 异步路由器方法
class ToolRouter:
    # ... 其他方法不变 ...
    async def async_route(self, tool_name: str, parameters: Dict[str, Any]) -> str:
        """异步路由方法"""
        if tool_name not in self.tool_map:
            return f"未找到工具：{tool_name}"
        
        tool_cls = self.tool_map[tool_name]
        try:
            tool_instance = tool_cls(**parameters)
            result = await tool_instance.run()  # 异步执行
            return result
        except Exception as e:
            return f"执行失败：{str(e)}"

# 测试异步调用
async def test_async():
    result = await router.async_route("async_weatherquery", {"city": "北京"})
    print(result)
```

### 2. 工具权限控制
可在路由器中添加权限校验，限制某些工具的调用：
```python
class ToolRouter:
    def __init__(self):
        self.tool_map = {}
        self.tool_permissions: Dict[str, List[str]] = {}  # 工具名 → 允许的角色列表

    def register_tool(self, tool_cls: Type[BaseTool], permissions: List[str] = None):
        super().register_tool(tool_cls)
        self.tool_permissions[tool_cls.tool_name()] = permissions or ["admin", "user"]

    def route(self, tool_name: str, parameters: Dict[str, Any], user_role: str = "user") -> str:
        # 权限校验
        if user_role not in self.tool_permissions.get(tool_name, []):
            return f"❌ 权限不足：角色「{user_role}」无法调用工具「{tool_name}」"
        # ... 后续逻辑不变 ...
```

### 3. 日志记录
添加日志记录工具调用过程（便于调试和监控）：
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ToolRouter")

class ToolRouter:
    def route(self, tool_name: str, parameters: Dict[str, Any]) -> str:
        logger.info(f"收到工具调用请求：tool_name={tool_name}, parameters={parameters}")
        try:
            # ... 执行逻辑 ...
            logger.info(f"工具调用成功：tool_name={tool_name}, result={result[:50]}...")
            return result
        except Exception as e:
            logger.error(f"工具调用失败：tool_name={tool_name}, error={str(e)}")
            return f"执行失败：{str(e)}"
```


## 总结
这个工具路由器（分类器）的核心价值是：
1. **解耦**：AI Agent 无需知道工具的具体实现，只需输出「工具名+参数」；
2. **标准化**：所有工具遵循统一接口，新增工具无需修改 Agent 逻辑；
3. **健壮性**：Pydantic 提供严格的参数校验，减少工具执行失败的概率；
4. **易用性**：一行代码注册工具，一行代码调用工具，集成成本极低。

可直接将该路由器集成到你的 AI Agent 中，Agent 只需通过 `list_tools()` 获取工具信息，再根据用户需求输出对应的「工具名+参数」，路由器会自动完成后续的路由和执行。

# todo
纸质 / 手写 Todo 本：用 “符号 + 颜色” 区分状态，比如：
待规划：□（空白框）+ 灰色笔
等待执行：□里画 “⌚”+ 蓝色笔
正在执行：□里画 “→”+ 橙色笔
暂停中：□里画 “||”+ 黄色笔
已完成：□里画 “✓”+ 绿色笔
已取消：□里画 “×”+ 红色笔


https://www.doubao.com/chat/28991085881222146?prev_page=new_tab
### 一、先解答核心问题：原代码的「增删改查」与「AI Agent 串联逻辑」
要理解这套 Todo 中间件的工作原理，需从 **数据流转、工具调用、状态管理** 三个核心维度拆解：


#### 1. 「增删改查」的实现方式
原代码通过 `write_todos` 工具 + `PlanningState` 状态，实现 Todo 项的全量更新式「增删改查」（核心是**全量覆盖更新**，而非单条操作）：

| 操作   | 实现逻辑                                                                 |
|--------|--------------------------------------------------------------------------|
| 新增   | AI 在调用 `write_todos` 时，在 `todos` 列表中添加新的 `Todo` 字典（状态为 `pending`/`in_progress`） |
| 修改   | 全量返回更新后的 `todos` 列表（例如：将某条 `pending` 改为 `in_progress`，或修改 `content`） |
| 删除   | 全量返回不含目标 Todo 的 `todos` 列表（直接过滤掉要删除的项）             |
| 查询   | AI 可通过读取 `PlanningState` 中的 `todos` 字段，获取当前所有 Todo 项（状态、内容） |

👉 关键限制：原设计是「全量替换」而非「单条操作」，AI 必须返回完整的 `todos` 列表才能更新，无法单独操作某一条（后续树结构设计会优化这一点）。


#### 2. 与 AI Agent 的串联逻辑
这套中间件是 LangGraph/LangChain Agent 的「插件」，通过 LangChain 的中间件机制无缝嵌入 Agent 工作流，核心串联点有 4 个：

##### （1）状态层串联：`PlanningState` 扩展 Agent 状态
- 原 Agent 状态（`AgentState`）被扩展为 `PlanningState`，新增 `todos` 字段（存储 Todo 列表）。
- `OmitFromInput` 注解表示：`todos` 字段不来自用户输入，而是由 Agent 内部工具（`write_todos`）更新和维护。
- Agent 每次执行后，`todos` 状态会被持久化，后续步骤可读取/修改。

##### （2）工具层串联：`write_todos` 工具注入 Agent
- 中间件在初始化时，动态创建 `write_todos` 工具（带自定义描述），并通过 `self.tools` 暴露给 Agent。
- Agent 可像调用其他工具（如搜索、计算）一样，调用 `write_todos` 来管理任务。

##### （3）提示层串联：系统提示引导 AI 正确使用工具
- 中间件的 `wrap_model_call` 方法，会在 Agent 调用大模型前，自动在系统提示后追加 `WRITE_TODOS_SYSTEM_PROMPT`。
- 提示明确告知 AI：「什么时候用（复杂多步任务）、什么时候不用（简单任务）、怎么用（状态更新规则）」，避免 AI 滥用工具。

##### （4）执行层串联：`Command` 更新状态 + `ToolMessage` 留痕
- AI 调用 `write_todos` 时，工具返回 `Command` 对象，其中 `update` 字段指定要修改的 Agent 状态（`todos` 列表）和消息（`ToolMessage`）。
- `ToolMessage` 会被存入 Agent 的消息历史，AI 后续可通过读取消息历史，获取之前的 Todo 列表（实现「查询」逻辑）。

👉 串联流程总结：
```
用户输入（复杂任务）→ Agent 读取系统提示（知道要用电线）→ AI 调用 write_todos 生成/更新 Todo 列表 → 工具返回 Command 更新 PlanningState.todos → Agent 基于更新后的 Todo 执行下一步（如调用其他工具完成任务）→ 完成后再次调用 write_todos 标记任务为 completed
```


### 二、进阶需求：Todo 改为「计划树」结构设计
原设计是扁平列表，无法表达「父子任务」（如「项目拆解 → 模块开发 → 接口实现」）。要做成**计划树**，需从「数据结构、工具设计、状态管理、AI 引导」四个层面重构：


#### 1. 核心：树结构数据模型设计
需定义「树形 Todo 节点」，支持父子嵌套、层级关系，同时保留原有的状态跟踪：

```python
from typing import List, Optional, Union
from uuid import uuid4
from pydantic import BaseModel  # 用 Pydantic 替代 TypedDict，更易校验和嵌套

class TodoNode(BaseModel):
    """树形 Todo 节点（支持父子嵌套）"""
    id: str = Field(default_factory=lambda: str(uuid4()), description="唯一节点 ID，用于定位修改")
    content: str = Field(description="任务描述（具体、可执行）")
    status: Literal["pending", "in_progress", "completed", "blocked"] = Field(default="pending", description="任务状态")
    parent_id: Optional[str] = Field(default=None, description="父节点 ID（根节点为 None）")
    children: List["TodoNode"] = Field(default_factory=list, description="子任务列表")
    dependencies: List[str] = Field(default_factory=list, description="依赖的其他节点 ID（需先完成依赖才能开始）")

# 递归引用支持（Pydantic v2 需显式声明）
TodoNode.update_forward_refs()

# 根状态：计划树（多个根节点支持并行任务）
class PlanningTreeState(AgentState):
    """树形计划的 Agent 状态"""
    todo_tree: Annotated[Optional[List[TodoNode]], OmitFromInput] = Field(default=None, description="计划树（根节点列表）")
    current_focus_node_id: Annotated[Optional[str], OmitFromInput] = Field(default=None, description="当前正在执行的节点 ID（辅助 AI 聚焦）")
```

👉 设计亮点：
- 用 `id` + `parent_id` 定位节点，支持任意层级的增删改查（无需全量更新）。
- 新增 `blocked` 状态处理任务阻塞场景，`dependencies` 支持任务依赖（如「设计数据库」需在「开发接口」前完成）。
- 根节点是列表，支持并行任务流（如同时处理「前端开发」和「后端开发」两个根任务）。


#### 2. 工具设计：从「全量更新」改为「单条/批量操作」
原 `write_todos` 是全量替换，树结构需更精细的工具（支持节点增删改查、子节点操作），避免 AI 每次都要输出完整树：

```python
# 定义工具输入参数的 Pydantic 模型（让 AI 更易理解参数格式）
class AddNodeParams(BaseModel):
    parent_id: Optional[str] = Field(default=None, description="父节点 ID（None 表示新增根节点）")
    node: TodoNode = Field(description="要新增的节点（无需填写 id，会自动生成）")

class UpdateNodeParams(BaseModel):
    node_id: str = Field(description="要修改的节点 ID")
    content: Optional[str] = Field(default=None, description="新的任务描述（不修改则留空）")
    status: Optional[Literal["pending", "in_progress", "completed", "blocked"]] = Field(default=None, description="新的状态（不修改则留空）")
    dependencies: Optional[List[str]] = Field(default=None, description="新的依赖节点 ID 列表（不修改则留空）")

class DeleteNodeParams(BaseModel):
    node_id: str = Field(description="要删除的节点 ID（子节点会一并删除）")

class AddChildParams(BaseModel):
    parent_id: str = Field(description="父节点 ID（必须存在）")
    child_node: TodoNode = Field(description="要新增的子节点（无需填写 id 和 parent_id）")

# 树形计划工具集
@tool(description="新增单个节点（根节点或子节点），支持创建并行任务或补充子任务")
def add_todo_node(params: AddNodeParams, tool_call_id: Annotated[str, InjectedToolCallId]) -> Command:
    node = params.node
    node.id = str(uuid4())  # 自动生成唯一 ID
    node.parent_id = params.parent_id  # 绑定父节点
    
    def update_state(state: PlanningTreeState) -> PlanningTreeState:
        if not state.todo_tree:
            state.todo_tree = []
        # 新增根节点
        if params.parent_id is None:
            state.todo_tree.append(node)
        # 新增子节点（找到父节点并添加）
        else:
            parent_node = _find_node_by_id(state.todo_tree, params.parent_id)
            if parent_node:
                parent_node.children.append(node)
            else:
                raise ValueError(f"父节点 ID {params.parent_id} 不存在")
        return state
    
    return Command(
        update=update_state,
        messages=[ToolMessage(f"成功新增节点（ID: {node.id}）：{node.content}", tool_call_id=tool_call_id)]
    )

@tool(description="更新节点的描述、状态或依赖，支持单独修改某一属性（无需全量输入）")
def update_todo_node(params: UpdateNodeParams, tool_call_id: Annotated[str, InjectedToolCallId]) -> Command:
    def update_state(state: PlanningTreeState) -> PlanningTreeState:
        node = _find_node_by_id(state.todo_tree, params.node_id)
        if not node:
            raise ValueError(f"节点 ID {params.node_id} 不存在")
        # 按需更新属性（非 None 才更新）
        if params.content:
            node.content = params.content
        if params.status:
            node.status = params.status
        if params.dependencies is not None:
            node.dependencies = params.dependencies
        return state
    
    return Command(
        update=update_state,
        messages=[ToolMessage(f"成功更新节点（ID: {params.node_id}）", tool_call_id=tool_call_id)]
    )

@tool(description="删除节点（含其子节点），适用于任务不再需要的场景")
def delete_todo_node(params: DeleteNodeParams, tool_call_id: Annotated[str, InjectedToolCallId]) -> Command:
    def update_state(state: PlanningTreeState) -> PlanningTreeState:
        if not state.todo_tree:
            return state
        # 根节点删除：过滤掉目标节点
        state.todo_tree = [n for n in state.todo_tree if n.id != params.node_id]
        # 子节点删除：递归遍历所有节点，删除目标节点及其子节点
        for root in state.todo_tree:
            _delete_node_recursive(root, params.node_id)
        return state
    
    return Command(
        update=update_state,
        messages=[ToolMessage(f"成功删除节点（ID: {params.node_id}）及其子节点", tool_call_id=tool_call_id)]
    )

# 辅助函数：递归查找节点
def _find_node_by_id(nodes: List[TodoNode], target_id: str) -> Optional[TodoNode]:
    for node in nodes:
        if node.id == target_id:
            return node
        # 递归查找子节点
        child = _find_node_by_id(node.children, target_id)
        if child:
            return child
    return None

# 辅助函数：递归删除节点
def _delete_node_recursive(node: TodoNode, target_id: str) -> None:
    node.children = [
        child for child in node.children
        if child.id != target_id and not _delete_node_recursive(child, target_id)
    ]
```

👉 工具设计核心优化：
- 拆分单一工具为「增、删、改、加子节点」四个专用工具，AI 无需记忆全量树结构，只需操作目标节点 ID。
- 用 Pydantic 模型定义参数，AI 能更清晰理解输入格式（LangChain 会自动将工具参数转为自然语言描述给 AI）。
- 内置 `_find_node_by_id` 等辅助函数，支持任意层级的节点定位，无需 AI 关心树的结构细节。


#### 3. 中间件重构：适配树形结构
修改 `TodoListMiddleware` 为 `PlanningTreeMiddleware`，注入树形工具和引导提示：

```python
class PlanningTreeMiddleware(AgentMiddleware):
    """支持计划树的中间件（替代原 TodoListMiddleware）"""
    state_schema = PlanningTreeState  # 绑定树形状态

    def __init__(
        self,
        system_prompt: str = None,
    ) -> None:
        super().__init__()
        # 自定义树形计划的系统提示（引导 AI 理解树结构和工具用法）
        self.system_prompt = system_prompt or """## 计划树使用指南
你可以使用以下工具管理复杂任务的层级结构：
1. 拆分任务：用 add_todo_node（父节点 ID 为空）创建根任务，用 add_child_node 给已有任务添加子任务（如「项目开发」→「前端开发」→「登录页面实现」）
2. 状态管理：任务开始时用 update_todo_node 设为 in_progress，完成后设为 completed，阻塞时设为 blocked
3. 依赖管理：如果任务 A 必须在任务 B 完成后执行，在 A 的 dependencies 中添加 B 的 ID
4. 节点定位：所有操作都通过节点 ID 进行，可通过工具返回的消息获取节点 ID
5. 简化原则：简单任务（<3 步）无需创建计划树，复杂任务才拆分层级（根节点 → 子节点 → 孙节点，最多 3 层）

## 关键规则
- 根节点代表核心目标（如「开发电商网站」），子节点代表细分步骤
- 每个 in_progress 节点必须有明确的执行动作（如「编写登录接口代码」）
- 阻塞节点需添加子任务描述解决方案（如「解决数据库连接超时」）
- 完成父节点前，需确保所有子节点已完成（或标记为无需执行）
"""
        # 注入树形工具集
        self.tools = [add_todo_node, update_todo_node, delete_todo_node, add_child_node]

    # 复用原有的 wrap_model_call（追加系统提示）
    def wrap_model_call(self, request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]) -> ModelCallResult:
        request.system_prompt = (
            request.system_prompt + "\n\n" + self.system_prompt
            if request.system_prompt
            else self.system_prompt
        )
        return handler(request)

    async def awrap_model_call(self, request: ModelRequest, handler: Callable[[ModelRequest], Awaitable[ModelResponse]]) -> ModelCallResult:
        request.system_prompt = (
            request.system_prompt + "\n\n" + self.system_prompt
            if request.system_prompt
            else self.system_prompt
        )
        return await handler(request)
```


#### 4. AI 与计划树的协作逻辑（串联流程）
重构后的串联流程更贴合「复杂任务拆解→执行→迭代」的实际场景：

```
用户输入（复杂任务：如「开发一个电商网站」）
→ Agent 读取系统提示（知道要拆分为计划树）
→ AI 调用 add_todo_node 创建根节点：{"content": "开发电商网站", "status": "in_progress"}
→ 工具返回 Command 更新 PlanningTreeState.todo_tree
→ AI 继续调用 add_child_node 给根节点加子节点：
  - 父节点 ID: 根节点 ID，子节点 1：{"content": "需求分析", "status": "in_progress"}
  - 父节点 ID: 根节点 ID，子节点 2：{"content": "技术选型", "status": "pending"}
→ 执行「需求分析」后，AI 调用 update_todo_node 将其状态改为 completed
→ 同时调用 update_todo_node 将「技术选型」改为 in_progress，并添加子节点「确定后端框架」
→ 遇到阻塞（如「数据库选型争议」），AI 调用 update_todo_node 将「技术选型」设为 blocked，同时添加子节点「协调团队确定数据库类型」
→ 所有子节点完成后，AI 标记根节点为 completed
```


### 三、关键优化点与扩展建议
#### 1. 核心优化（相比原设计）
- 数据结构：从扁平列表→树形节点，支持层级拆解和依赖管理。
- 工具设计：从全量更新→单条操作，降低 AI 认知负担和 token 消耗。
- 状态管理：新增 `current_focus_node_id`，辅助 AI 聚焦当前执行节点（避免混乱）。
- AI 引导：系统提示明确层级拆分规则（最多 3 层）、依赖设置、状态流转，减少 AI 误用。

#### 2. 扩展建议（生产环境可用）
- 增加「查询工具」：如 `query_todo_node(node_id: str)`，让 AI 可主动查询某节点的状态/子节点。
- 支持「批量操作」：如 `batch_update_nodes`，批量修改多个节点状态（适用于并行任务同步）。
- 可视化输出：在 `ToolMessage` 中用 Markdown 树形结构展示计划树（如 `- 根节点\n  - 子节点`），方便用户查看。
- 依赖校验：在 `update_todo_node` 中添加依赖校验（确保依赖节点存在且已完成），避免 AI 设置无效依赖。
- 历史回溯：在 `messages` 中记录每一次节点操作，支持 AI 回溯计划变更历史。


### 四、总结
原代码的核心是「扁平 Todo 列表 + 全量更新工具 + 系统提示引导」，串联 Agent 的方式是通过 LangChain 中间件的「状态扩展、工具注入、提示追加」机制。

改为计划树后，核心是「树形节点数据模型 + 精细化工具 + 层级化引导」，保留了原中间件的串联逻辑，但更适合复杂任务的拆解和跟踪。AI 无需关心树的底层实现，只需通过「节点 ID」调用工具，即可实现任意层级的增删改查，同时用户能清晰看到任务的层级进度。