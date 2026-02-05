# tool list
# GitHub 辅助工具 API 手册

---

### 1. 获取维基结构 (read_wiki_structure)
**功能描述**：获取特定 GitHub 仓库的文档主题列表，用于了解该仓库都有哪些维基页面。

| 字段 | 类型 | 必填 | 描述 |
| :--- | :--- | :--- | :--- |
| **repoName** | `string` | 是 | GitHub 仓库路径，格式为 "拥有者/仓库名" (例如: "facebook/react") |

---

### 2. 读取维基内容 (read_wiki_contents)
**功能描述**：查看 GitHub 仓库维基文档的具体内容。

| 字段 | 类型 | 必填 | 描述 |
| :--- | :--- | :--- | :--- |
| **repoName** | `string` | 是 | GitHub 仓库路径，格式为 "拥有者/仓库名" (例如: "facebook/react") |

---

### 3. AI 提问对话 (ask_question)
**功能描述**：针对一个或多个 GitHub 仓库提出任何问题，并获得基于 AI 且结合上下文背景的精准回答。

| 字段 | 类型 | 必填 | 描述 |
| :--- | :--- | :--- | :--- |
| **repoName** | `string` 或 `array` | 是 | 仓库路径或路径列表 (最多支持 10 个)，例如 "owner/repo" |
| **question** | `string` | 是 | 你想要询问关于该仓库的具体问题 |

---

### 💡 使用小贴士
* **顺序建议**：建议先用 `read_wiki_structure` 探索有哪些文档，再针对性地读取。
* **多仓库对比**：`ask_question` 支持传入数组，非常适合用来对比两个不同框架的特性差异。




# MCP Streamable HTTP 协议
这个错误是因为 MCP 的 Streamable HTTP 协议需要特定的 `Accept` 头。你需要添加正确的请求头：

## 修正后的 Python 代码

```python
import requests

BASE_URL = "https://mcp.deepwiki.com/mcp"

response = requests.post(
    BASE_URL,
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"  # 必须同时接受这两种格式
    },
    json={
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "ask_question",
            "arguments": {
                "repo": "owner/repo-name",
                "question": "How does authentication work?"
            }
        },
        "id": 1
    }
)

result = response.json()
print(result)
```

**关键修改：** 添加 `Accept: application/json, text/event-stream` 头，因为 MCP Streamable HTTP 协议要求客户端同时接受 JSON 和 SSE 格式的响应。

参考来源：[DeepWiki MCP](/work-with-devin/deepwiki-mcp) 页面。

```suggestions
(DeepWiki MCP 设置说明)[/work-with-devin/deepwiki-mcp]
(Devin MCP 私有仓库访问)[/work-with-devin/devin-mcp]
(MCP Marketplace)[/work-with-devin/mcp]
```


# MCP JSON-RPC 协议
这是一个很好的问题！MCP 使用标准的 **JSON-RPC 2.0** 协议。要获取工具列表和参数 schema，你可以调用 `tools/list` 方法：

## 获取 MCP 工具列表和参数

```python
import requests

BASE_URL = "https://mcp.deepwiki.com/mcp"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream"
}

# 1. 获取所有可用工具及其参数 schema
response = requests.post(
    BASE_URL,
    headers=HEADERS,
    json={
        "jsonrpc": "2.0",
        "method": "tools/list",  # 列出所有工具
        "params": {},
        "id": 1
    }
)

tools = response.json()
print(tools)  # 会返回每个工具的 name、description 和 inputSchema
```

**返回结果会包含：**
- `read_wiki_structure` - 参数: `repo`
- `read_wiki_contents` - 参数: `repo`, `topic`  
- `ask_question` - 参数: `repo`, `question`

每个工具的 `inputSchema` 字段会告诉你具体的参数格式（JSON Schema）。

**JSON-RPC 格式说明：**
- `jsonrpc`: 固定为 `"2.0"`
- `method`: MCP 方法名（如 `tools/list`, `tools/call`）
- `params`: 方法参数
- `id`: 请求标识符

这是 MCP 协议的标准规范，参考 [Model Context Protocol](https://modelcontextprotocol.io/introduction)。

```suggestions
(DeepWiki MCP 文档)[/work-with-devin/deepwiki-mcp]
(Devin MCP 私有仓库)[/work-with-devin/devin-mcp]
(MCP Marketplace)[/work-with-devin/mcp]
```

