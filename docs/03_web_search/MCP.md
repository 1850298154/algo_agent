---
created: 2026-02-06T02:53:00 (UTC +08:00)
tags: []
source: https://pypi.org/project/mcp/#resources
author: 
---

# MCP ·PyPI --- mcp · PyPI

> ## Excerpt
> Model Context Protocol SDK

---
## MCP Python SDK

## Table of Contents  目录

-   [MCP Python SDK](https://pypi.org/project/mcp/#mcp-python-sdk)
    -   [Overview  概述](https://pypi.org/project/mcp/#overview)
    -   [Installation  安装](https://pypi.org/project/mcp/#installation)
        -   [Adding MCP to your python project  
            将 MCP 添加到你的 Python 项目中](https://pypi.org/project/mcp/#adding-mcp-to-your-python-project)
        -   [Running the standalone MCP development tools  
            运行独立的 MCP 开发工具](https://pypi.org/project/mcp/#running-the-standalone-mcp-development-tools)
    -   [Quickstart  快速入门](https://pypi.org/project/mcp/#quickstart)
    -   [What is MCP?  什么是 MCP？](https://pypi.org/project/mcp/#what-is-mcp)
    -   [Core Concepts  核心概念](https://pypi.org/project/mcp/#core-concepts)
        -   [Server  服务器](https://pypi.org/project/mcp/#server)
        -   [Resources  资源](https://pypi.org/project/mcp/#resources)
        -   [Tools  工具](https://pypi.org/project/mcp/#tools)
            -   [Structured Output  结构化输出](https://pypi.org/project/mcp/#structured-output)
        -   [Prompts  提示](https://pypi.org/project/mcp/#prompts)
        -   [Images  图像](https://pypi.org/project/mcp/#images)
        -   [Context  背景](https://pypi.org/project/mcp/#context)
            -   [Getting Context in Functions  
                函数中的上下文获取](https://pypi.org/project/mcp/#getting-context-in-functions)
            -   [Context Properties and Methods  
                上下文属性与方法](https://pypi.org/project/mcp/#context-properties-and-methods)
        -   [Completions  完成](https://pypi.org/project/mcp/#completions)
        -   [Elicitation  启发式](https://pypi.org/project/mcp/#elicitation)
        -   [Sampling  采样](https://pypi.org/project/mcp/#sampling)
        -   [Logging and Notifications  
            日志与通知](https://pypi.org/project/mcp/#logging-and-notifications)
        -   [Authentication  认证](https://pypi.org/project/mcp/#authentication)
        -   [FastMCP Properties  FastMCP 属性](https://pypi.org/project/mcp/#fastmcp-properties)
        -   [Session Properties and Methods  
            会话属性与方法](https://pypi.org/project/mcp/#session-properties-and-methods)
        -   [Request Context Properties  
            请求上下文属性](https://pypi.org/project/mcp/#request-context-properties)
    -   [Running Your Server  
        运行你的服务器](https://pypi.org/project/mcp/#running-your-server)
        -   [Development Mode  开发模式](https://pypi.org/project/mcp/#development-mode)
        -   [Claude Desktop Integration  
            Claude 桌面集成](https://pypi.org/project/mcp/#claude-desktop-integration)
        -   [Direct Execution  直接执行](https://pypi.org/project/mcp/#direct-execution)
        -   [Streamable HTTP Transport  
            可流式 HTTP 传输](https://pypi.org/project/mcp/#streamable-http-transport)
            -   [CORS Configuration for Browser-Based Clients  
                浏览器客户端的 CORS 配置](https://pypi.org/project/mcp/#cors-configuration-for-browser-based-clients)
        -   [Mounting to an Existing ASGI Server  
            挂载到现有的 ASGI 服务器](https://pypi.org/project/mcp/#mounting-to-an-existing-asgi-server)
            -   [StreamableHTTP servers  可流式 HTTP 服务器](https://pypi.org/project/mcp/#streamablehttp-servers)
                -   [Basic mounting  基本安装](https://pypi.org/project/mcp/#basic-mounting)
                -   [Host-based routing  基于主机的路由](https://pypi.org/project/mcp/#host-based-routing)
                -   [Multiple servers with path configuration  
                    多台服务器与路径配置](https://pypi.org/project/mcp/#multiple-servers-with-path-configuration)
                -   [Path configuration at initialization  
                    初始化时的路径配置](https://pypi.org/project/mcp/#path-configuration-at-initialization)
            -   [SSE servers  SSE 服务器](https://pypi.org/project/mcp/#sse-servers)
    -   [Advanced Usage  高级用法](https://pypi.org/project/mcp/#advanced-usage)
        -   [Low-Level Server  低级服务器](https://pypi.org/project/mcp/#low-level-server)
            -   [Structured Output Support  
                结构化输出支持](https://pypi.org/project/mcp/#structured-output-support)
        -   [Pagination (Advanced)  分页（高级）](https://pypi.org/project/mcp/#pagination-advanced)
        -   [Writing MCP Clients  编写 MCP 客户端](https://pypi.org/project/mcp/#writing-mcp-clients)
        -   [Client Display Utilities  
            客户端显示工具](https://pypi.org/project/mcp/#client-display-utilities)
        -   [OAuth Authentication for Clients  
            客户端的 OAuth 认证](https://pypi.org/project/mcp/#oauth-authentication-for-clients)
        -   [Parsing Tool Results  解析工具结果](https://pypi.org/project/mcp/#parsing-tool-results)
        -   [MCP Primitives  MCP 原语](https://pypi.org/project/mcp/#mcp-primitives)
        -   [Server Capabilities  服务器功能](https://pypi.org/project/mcp/#server-capabilities)
    -   [Documentation  文档](https://pypi.org/project/mcp/#documentation)
    -   [Contributing  贡献](https://pypi.org/project/mcp/#contributing)
    -   [License  许可证](https://pypi.org/project/mcp/#license)

## Overview  概述

The Model Context Protocol allows applications to provide context for LLMs in a standardized way, separating the concerns of providing context from the actual LLM interaction. This Python SDK implements the full MCP specification, making it easy to:  
模型上下文协议允许应用程序以标准化方式为 LLM 提供上下文，将提供上下文的顾虑与实际的 LLM 交互分开。该 Python SDK 实现了完整的 MCP 规范，使得以下作变得简单：

-   Build MCP clients that can connect to any MCP server  
    构建能够连接到任何 MCP 服务器的 MCP 客户端
-   Create MCP servers that expose resources, prompts and tools  
    创建暴露资源、提示和工具的 MCP 服务器
-   Use standard transports like stdio, SSE, and Streamable HTTP  
    使用标准传输方式，比如 stdio、SSE 和可流式 HTTP
-   Handle all MCP protocol messages and lifecycle events  
    处理所有 MCP 协议消息和生命周期事件

## Installation  安装

### Adding MCP to your python project  
将 MCP 添加到你的 Python 项目中

We recommend using [uv](https://docs.astral.sh/uv/) to manage your Python projects.  
我们建议用 [UV](https://docs.astral.sh/uv/) 来管理你的 Python 项目。

If you haven't created a uv-managed project yet, create one:  
如果你还没创建过 UV 管理项目，可以创建一个：

```
uv<span> </span>init<span> </span>mcp-server-demo
<span>cd</span><span> </span>mcp-server-demo
```

Then add MCP to your project dependencies:  
然后将 MCP 添加到你的项目依赖中：

```
uv<span> </span>add<span> </span><span>"mcp[cli]"</span>
```

Alternatively, for projects using pip for dependencies:  
或者，对于使用 pip 作为依赖的项目：

```
pip<span> </span>install<span> </span><span>"mcp[cli]"</span>
```

### Running the standalone MCP development tools  
运行独立的 MCP 开发工具

To run the mcp command with uv:  
要用 uv 运行 mcp 命令：

```
uv<span> </span>run<span> </span>mcp
```

## Quickstart  快速入门

Let's create a simple MCP server that exposes a calculator tool and some data:  
让我们创建一个简单的 MCP 服务器，它暴露一个计算器工具和一些数据：

```
<span>"""</span>
<span>FastMCP quickstart example.</span>

<span>Run from the repository root:</span>
<span>    uv run examples/snippets/servers/fastmcp_quickstart.py</span>
<span>"""</span>

<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>FastMCP</span>

<span># Create an MCP server</span>
<span>mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>"Demo"</span><span>,</span> <span>json_response</span><span>=</span><span>True</span><span>)</span>


<span># Add an addition tool</span>
<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>add</span><span>(</span><span>a</span><span>:</span> <span>int</span><span>,</span> <span>b</span><span>:</span> <span>int</span><span>)</span> <span>-&gt;</span> <span>int</span><span>:</span>
<span>    </span><span>"""Add two numbers"""</span>
    <span>return</span> <span>a</span> <span>+</span> <span>b</span>


<span># Add a dynamic greeting resource</span>
<span>@mcp</span><span>.</span><span>resource</span><span>(</span><span>"greeting://</span><span>{name}</span><span>"</span><span>)</span>
<span>def</span><span> </span><span>get_greeting</span><span>(</span><span>name</span><span>:</span> <span>str</span><span>)</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Get a personalized greeting"""</span>
    <span>return</span> <span>f</span><span>"Hello, </span><span>{</span><span>name</span><span>}</span><span>!"</span>


<span># Add a prompt</span>
<span>@mcp</span><span>.</span><span>prompt</span><span>()</span>
<span>def</span><span> </span><span>greet_user</span><span>(</span><span>name</span><span>:</span> <span>str</span><span>,</span> <span>style</span><span>:</span> <span>str</span> <span>=</span> <span>"friendly"</span><span>)</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Generate a greeting prompt"""</span>
    <span>styles</span> <span>=</span> <span>{</span>
        <span>"friendly"</span><span>:</span> <span>"Please write a warm, friendly greeting"</span><span>,</span>
        <span>"formal"</span><span>:</span> <span>"Please write a formal, professional greeting"</span><span>,</span>
        <span>"casual"</span><span>:</span> <span>"Please write a casual, relaxed greeting"</span><span>,</span>
    <span>}</span>

    <span>return</span> <span>f</span><span>"</span><span>{</span><span>styles</span><span>.</span><span>get</span><span>(</span><span>style</span><span>,</span><span> </span><span>styles</span><span>[</span><span>'friendly'</span><span>])</span><span>}</span><span> for someone named </span><span>{</span><span>name</span><span>}</span><span>."</span>


<span># Run with streamable HTTP transport</span>
<span>if</span> <span>__name__</span> <span>==</span> <span>"__main__"</span><span>:</span>
    <span>mcp</span><span>.</span><span>run</span><span>(</span><span>transport</span><span>=</span><span>"streamable-http"</span><span>)</span>
```

_Full example: [examples/snippets/servers/fastmcp\_quickstart.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/fastmcp_quickstart.py)  
完整示例： [示例/片段/服务器/fastmcp\_quickstart.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/fastmcp_quickstart.py)_

You can install this server in [Claude Code](https://docs.claude.com/en/docs/claude-code/mcp) and interact with it right away. First, run the server:  
你可以用 [Claude Code](https://docs.claude.com/en/docs/claude-code/mcp) 安装这个服务器，并立即与它交互。首先，运行服务器：

```
uv<span> </span>run<span> </span>--with<span> </span>mcp<span> </span>examples/snippets/servers/fastmcp_quickstart.py
```

Then add it to Claude Code:  
然后把它加入 Claude 代码：

```
claude<span> </span>mcp<span> </span>add<span> </span>--transport<span> </span>http<span> </span>my-server<span> </span>http://localhost:8000/mcp
```

Alternatively, you can test it with the MCP Inspector. Start the server as above, then in a separate terminal:  
或者，你也可以用 MCP Inspector 测试。启动服务器如上，然后在独立终端中启动：

```
npx<span> </span>-y<span> </span>@modelcontextprotocol/inspector
```

In the inspector UI, connect to `http://localhost:8000/mcp`.  
在检查员界面中，连接到 `http://localhost:8000/mcp`。

## What is MCP?  什么是 MCP？

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) lets you build servers that expose data and functionality to LLM applications in a secure, standardized way. Think of it like a web API, but specifically designed for LLM interactions. MCP servers can:  
[模型上下文协议（MCP）](https://modelcontextprotocol.io/) 允许你构建服务器，以安全、标准化的方式向 LLM 应用暴露数据和功能。可以把它看作是一个专门为大型语言模型交互设计的 Web API。MCP 服务器可以：

-   Expose data through **Resources** (think of these sort of like GET endpoints; they are used to load information into the LLM's context)  
    通过**资源**暴露数据（可以把它们想象成 GET 端点;它们用来将信息加载到 LLM 的上下文中）
-   Provide functionality through **Tools** (sort of like POST endpoints; they are used to execute code or otherwise produce a side effect)  
    通过**工具**提供功能（有点像 POST 端点;它们用于执行代码或产生副作用）
-   Define interaction patterns through **Prompts** (reusable templates for LLM interactions)  
    通过**提示** （用于大型语言模型交互的可复用模板）定义交互模式
-   And more!  还有更多！

## Core Concepts  核心概念

### Server  服务器

The FastMCP server is your core interface to the MCP protocol. It handles connection management, protocol compliance, and message routing:  
FastMCP 服务器是你与 MCP 协议的核心接口。它负责连接管理、协议合规和消息路由：

```
<span>"""Example showing lifespan support for startup/shutdown with strong typing."""</span>

<span>from</span><span> </span><span>collections.abc</span><span> </span><span>import</span> <span>AsyncIterator</span>
<span>from</span><span> </span><span>contextlib</span><span> </span><span>import</span> <span>asynccontextmanager</span>
<span>from</span><span> </span><span>dataclasses</span><span> </span><span>import</span> <span>dataclass</span>

<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>Context</span><span>,</span> <span>FastMCP</span>
<span>from</span><span> </span><span>mcp.server.session</span><span> </span><span>import</span> <span>ServerSession</span>


<span># Mock database class for example</span>
<span>class</span><span> </span><span>Database</span><span>:</span>
<span>    </span><span>"""Mock database class for example."""</span>

    <span>@classmethod</span>
    <span>async</span> <span>def</span><span> </span><span>connect</span><span>(</span><span>cls</span><span>)</span> <span>-&gt;</span> <span>"Database"</span><span>:</span>
<span>        </span><span>"""Connect to database."""</span>
        <span>return</span> <span>cls</span><span>()</span>

    <span>async</span> <span>def</span><span> </span><span>disconnect</span><span>(</span><span>self</span><span>)</span> <span>-&gt;</span> <span>None</span><span>:</span>
<span>        </span><span>"""Disconnect from database."""</span>
        <span>pass</span>

    <span>def</span><span> </span><span>query</span><span>(</span><span>self</span><span>)</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>        </span><span>"""Execute a query."""</span>
        <span>return</span> <span>"Query result"</span>


<span>@dataclass</span>
<span>class</span><span> </span><span>AppContext</span><span>:</span>
<span>    </span><span>"""Application context with typed dependencies."""</span>

    <span>db</span><span>:</span> <span>Database</span>


<span>@asynccontextmanager</span>
<span>async</span> <span>def</span><span> </span><span>app_lifespan</span><span>(</span><span>server</span><span>:</span> <span>FastMCP</span><span>)</span> <span>-&gt;</span> <span>AsyncIterator</span><span>[</span><span>AppContext</span><span>]:</span>
<span>    </span><span>"""Manage application lifecycle with type-safe context."""</span>
    <span># Initialize on startup</span>
    <span>db</span> <span>=</span> <span>await</span> <span>Database</span><span>.</span><span>connect</span><span>()</span>
    <span>try</span><span>:</span>
        <span>yield</span> <span>AppContext</span><span>(</span><span>db</span><span>=</span><span>db</span><span>)</span>
    <span>finally</span><span>:</span>
        <span># Cleanup on shutdown</span>
        <span>await</span> <span>db</span><span>.</span><span>disconnect</span><span>()</span>


<span># Pass lifespan to server</span>
<span>mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>"My App"</span><span>,</span> <span>lifespan</span><span>=</span><span>app_lifespan</span><span>)</span>


<span># Access type-safe lifespan context in tools</span>
<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>query_db</span><span>(</span><span>ctx</span><span>:</span> <span>Context</span><span>[</span><span>ServerSession</span><span>,</span> <span>AppContext</span><span>])</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Tool that uses initialized resources."""</span>
    <span>db</span> <span>=</span> <span>ctx</span><span>.</span><span>request_context</span><span>.</span><span>lifespan_context</span><span>.</span><span>db</span>
    <span>return</span> <span>db</span><span>.</span><span>query</span><span>()</span>
```

_Full example: [examples/snippets/servers/lifespan\_example.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/lifespan_example.py)  
完整示例： [示例/片段/服务器/lifespan\_example.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/lifespan_example.py)_

### Resources  资源

Resources are how you expose data to LLMs. They're similar to GET endpoints in a REST API - they provide data but shouldn't perform significant computation or have side effects:  
资源是你向大型语言模型展示数据的方式。它们类似于 REST API 中的 GET 端点——它们提供数据，但不应该执行大量计算或带来副作用：

```
<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>FastMCP</span>

<span>mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>name</span><span>=</span><span>"Resource Example"</span><span>)</span>


<span>@mcp</span><span>.</span><span>resource</span><span>(</span><span>"file://documents/</span><span>{name}</span><span>"</span><span>)</span>
<span>def</span><span> </span><span>read_document</span><span>(</span><span>name</span><span>:</span> <span>str</span><span>)</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Read a document by name."""</span>
    <span># This would normally read from disk</span>
    <span>return</span> <span>f</span><span>"Content of </span><span>{</span><span>name</span><span>}</span><span>"</span>


<span>@mcp</span><span>.</span><span>resource</span><span>(</span><span>"config://settings"</span><span>)</span>
<span>def</span><span> </span><span>get_settings</span><span>()</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Get application settings."""</span>
    <span>return</span> <span>"""{</span>
<span>  "theme": "dark",</span>
<span>  "language": "en",</span>
<span>  "debug": false</span>
<span>}"""</span>
```

_Full example: [examples/snippets/servers/basic\_resource.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/basic_resource.py)  
完整示例： [示例/片段/服务器/basic\_resource.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/basic_resource.py)_

### Tools  工具

Tools let LLMs take actions through your server. Unlike resources, tools are expected to perform computation and have side effects:  
工具让大型语言模型通过你的服务器执行作。与资源不同，工具被期望执行计算，并产生副作用：

```
<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>FastMCP</span>

<span>mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>name</span><span>=</span><span>"Tool Example"</span><span>)</span>


<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>sum</span><span>(</span><span>a</span><span>:</span> <span>int</span><span>,</span> <span>b</span><span>:</span> <span>int</span><span>)</span> <span>-&gt;</span> <span>int</span><span>:</span>
<span>    </span><span>"""Add two numbers together."""</span>
    <span>return</span> <span>a</span> <span>+</span> <span>b</span>


<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>get_weather</span><span>(</span><span>city</span><span>:</span> <span>str</span><span>,</span> <span>unit</span><span>:</span> <span>str</span> <span>=</span> <span>"celsius"</span><span>)</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Get weather for a city."""</span>
    <span># This would normally call a weather API</span>
    <span>return</span> <span>f</span><span>"Weather in </span><span>{</span><span>city</span><span>}</span><span>: 22degrees</span><span>{</span><span>unit</span><span>[</span><span>0</span><span>]</span><span>.</span><span>upper</span><span>()</span><span>}</span><span>"</span>
```

_Full example: [examples/snippets/servers/basic\_tool.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/basic_tool.py)  
完整示例： [示例/片段/服务器/basic\_tool.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/basic_tool.py)_

Tools can optionally receive a Context object by including a parameter with the `Context` type annotation. This context is automatically injected by the FastMCP framework and provides access to MCP capabilities:  
工具可以通过在`上下文类型注释`中加入参数来选择接收上下文对象。FastMCP 框架自动注入该上下文，提供 MCP 功能访问：

```
<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>Context</span><span>,</span> <span>FastMCP</span>
<span>from</span><span> </span><span>mcp.server.session</span><span> </span><span>import</span> <span>ServerSession</span>

<span>mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>name</span><span>=</span><span>"Progress Example"</span><span>)</span>


<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>async</span> <span>def</span><span> </span><span>long_running_task</span><span>(</span><span>task_name</span><span>:</span> <span>str</span><span>,</span> <span>ctx</span><span>:</span> <span>Context</span><span>[</span><span>ServerSession</span><span>,</span> <span>None</span><span>],</span> <span>steps</span><span>:</span> <span>int</span> <span>=</span> <span>5</span><span>)</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Execute a task with progress updates."""</span>
    <span>await</span> <span>ctx</span><span>.</span><span>info</span><span>(</span><span>f</span><span>"Starting: </span><span>{</span><span>task_name</span><span>}</span><span>"</span><span>)</span>

    <span>for</span> <span>i</span> <span>in</span> <span>range</span><span>(</span><span>steps</span><span>):</span>
        <span>progress</span> <span>=</span> <span>(</span><span>i</span> <span>+</span> <span>1</span><span>)</span> <span>/</span> <span>steps</span>
        <span>await</span> <span>ctx</span><span>.</span><span>report_progress</span><span>(</span>
            <span>progress</span><span>=</span><span>progress</span><span>,</span>
            <span>total</span><span>=</span><span>1.0</span><span>,</span>
            <span>message</span><span>=</span><span>f</span><span>"Step </span><span>{</span><span>i</span><span> </span><span>+</span><span> </span><span>1</span><span>}</span><span>/</span><span>{</span><span>steps</span><span>}</span><span>"</span><span>,</span>
        <span>)</span>
        <span>await</span> <span>ctx</span><span>.</span><span>debug</span><span>(</span><span>f</span><span>"Completed step </span><span>{</span><span>i</span><span> </span><span>+</span><span> </span><span>1</span><span>}</span><span>"</span><span>)</span>

    <span>return</span> <span>f</span><span>"Task '</span><span>{</span><span>task_name</span><span>}</span><span>' completed"</span>
```

_Full example: [examples/snippets/servers/tool\_progress.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/tool_progress.py)  
完整示例： [示例/摘要/服务器/tool\_progress.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/tool_progress.py)_

#### Structured Output  结构化输出

Tools will return structured results by default, if their return type annotation is compatible. Otherwise, they will return unstructured results.  
如果工具的返回类型注释兼容，默认会返回结构化结果。否则，他们会返回无结构化的结果。

Structured output supports these return types:  
结构化输出支持以下返回类型：

-   Pydantic models (BaseModel subclasses)  
    态态模型（基础模型子类）
-   TypedDicts  TypedDict
-   Dataclasses and other classes with type hints  
    Data 类及其他带有类型提示的类
-   `dict[str, T]` (where T is any JSON-serializable type)  
    `dict[str， T]`（其中 T 是任意可序列化的 JSON 类型）
-   Primitive types (str, int, float, bool, bytes, None) - wrapped in `{"result": value}`  
    原始类型（str、int、float、bool、bytes、None）——封装在 `{“result”： value}` 中
-   Generic types (list, tuple, Union, Optional, etc.) - wrapped in `{"result": value}`  
    泛型类型（列表、元组、Union、可选等）——被 `{“result”： value}` 封装

Classes without type hints cannot be serialized for structured output. Only classes with properly annotated attributes will be converted to Pydantic models for schema generation and validation.  
没有类型提示的类无法用于结构化输出的序列化。只有带有正确注释属性的类才会被转换为 Pydantic 模型，用于模式生成和验证。

Structured results are automatically validated against the output schema generated from the annotation. This ensures the tool returns well-typed, validated data that clients can easily process.  
结构化结果会自动根据注释生成的输出模式进行验证。这确保工具返回的是类型清晰、经过验证的数据，客户可以轻松处理。

**Note:** For backward compatibility, unstructured results are also returned. Unstructured results are provided for backward compatibility with previous versions of the MCP specification, and are quirks-compatible with previous versions of FastMCP in the current version of the SDK.  
**注意：** 为了向后兼容，还返回无结构化结果。为向后兼容 MCP 规范的旧版本提供了非结构化结果，并且在当前版本 SDK 中与 FastMCP 的旧版本具有特殊兼容性。

**Note:** In cases where a tool function's return type annotation causes the tool to be classified as structured _and this is undesirable_, the classification can be suppressed by passing `structured_output=False` to the `@tool` decorator.  
**注意：** 当工具函数的返回类型注释导致工具被归类为结构化且_不受欢迎_时，可以通过传递 `structured_output=False` 来抑制分类 给 `@tool` 装饰师。

##### Advanced: Direct CallToolResult  
高级：直接 CALLTOOLRESULT

For full control over tool responses including the `_meta` field (for passing data to client applications without exposing it to the model), you can return `CallToolResult` directly:  
为了完全控制工具响应，包括 `_meta` 字段（用于将数据传递给客户端应用而不暴露给模型），你可以直接返回 `CallToolResult`：

```
<span>"""Example showing direct CallToolResult return for advanced control."""</span>

<span>from</span><span> </span><span>typing</span><span> </span><span>import</span> <span>Annotated</span>

<span>from</span><span> </span><span>pydantic</span><span> </span><span>import</span> <span>BaseModel</span>

<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>FastMCP</span>
<span>from</span><span> </span><span>mcp.types</span><span> </span><span>import</span> <span>CallToolResult</span><span>,</span> <span>TextContent</span>

<span>mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>"CallToolResult Example"</span><span>)</span>


<span>class</span><span> </span><span>ValidationModel</span><span>(</span><span>BaseModel</span><span>):</span>
<span>    </span><span>"""Model for validating structured output."""</span>

    <span>status</span><span>:</span> <span>str</span>
    <span>data</span><span>:</span> <span>dict</span><span>[</span><span>str</span><span>,</span> <span>int</span><span>]</span>


<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>advanced_tool</span><span>()</span> <span>-&gt;</span> <span>CallToolResult</span><span>:</span>
<span>    </span><span>"""Return CallToolResult directly for full control including _meta field."""</span>
    <span>return</span> <span>CallToolResult</span><span>(</span>
        <span>content</span><span>=</span><span>[</span><span>TextContent</span><span>(</span><span>type</span><span>=</span><span>"text"</span><span>,</span> <span>text</span><span>=</span><span>"Response visible to the model"</span><span>)],</span>
        <span>_meta</span><span>=</span><span>{</span><span>"hidden"</span><span>:</span> <span>"data for client applications only"</span><span>},</span>
    <span>)</span>


<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>validated_tool</span><span>()</span> <span>-&gt;</span> <span>Annotated</span><span>[</span><span>CallToolResult</span><span>,</span> <span>ValidationModel</span><span>]:</span>
<span>    </span><span>"""Return CallToolResult with structured output validation."""</span>
    <span>return</span> <span>CallToolResult</span><span>(</span>
        <span>content</span><span>=</span><span>[</span><span>TextContent</span><span>(</span><span>type</span><span>=</span><span>"text"</span><span>,</span> <span>text</span><span>=</span><span>"Validated response"</span><span>)],</span>
        <span>structuredContent</span><span>=</span><span>{</span><span>"status"</span><span>:</span> <span>"success"</span><span>,</span> <span>"data"</span><span>:</span> <span>{</span><span>"result"</span><span>:</span> <span>42</span><span>}},</span>
        <span>_meta</span><span>=</span><span>{</span><span>"internal"</span><span>:</span> <span>"metadata"</span><span>},</span>
    <span>)</span>


<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>empty_result_tool</span><span>()</span> <span>-&gt;</span> <span>CallToolResult</span><span>:</span>
<span>    </span><span>"""For empty results, return CallToolResult with empty content."""</span>
    <span>return</span> <span>CallToolResult</span><span>(</span><span>content</span><span>=</span><span>[])</span>
```

_Full example: [examples/snippets/servers/direct\_call\_tool\_result.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/direct_call_tool_result.py)  
完整示例： [示例/片段/服务器/direct\_call\_tool\_result.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/direct_call_tool_result.py)_

**Important:** `CallToolResult` must always be returned (no `Optional` or `Union`). For empty results, use `CallToolResult(content=[])`. For optional simple types, use `str | None` without `CallToolResult`.  
**重要：**`CallToolResult` 必须始终返回（不可`选择`或`联合` ）。对于空结果，请使用 `CallToolResult（content=[]）。` 对于可选的简单类型，使用 `str |没有` `CallToolResult` 的。

```
<span>"""Example showing structured output with tools."""</span>

<span>from</span><span> </span><span>typing</span><span> </span><span>import</span> <span>TypedDict</span>

<span>from</span><span> </span><span>pydantic</span><span> </span><span>import</span> <span>BaseModel</span><span>,</span> <span>Field</span>

<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>FastMCP</span>

<span>mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>"Structured Output Example"</span><span>)</span>


<span># Using Pydantic models for rich structured data</span>
<span>class</span><span> </span><span>WeatherData</span><span>(</span><span>BaseModel</span><span>):</span>
<span>    </span><span>"""Weather information structure."""</span>

    <span>temperature</span><span>:</span> <span>float</span> <span>=</span> <span>Field</span><span>(</span><span>description</span><span>=</span><span>"Temperature in Celsius"</span><span>)</span>
    <span>humidity</span><span>:</span> <span>float</span> <span>=</span> <span>Field</span><span>(</span><span>description</span><span>=</span><span>"Humidity percentage"</span><span>)</span>
    <span>condition</span><span>:</span> <span>str</span>
    <span>wind_speed</span><span>:</span> <span>float</span>


<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>get_weather</span><span>(</span><span>city</span><span>:</span> <span>str</span><span>)</span> <span>-&gt;</span> <span>WeatherData</span><span>:</span>
<span>    </span><span>"""Get weather for a city - returns structured data."""</span>
    <span># Simulated weather data</span>
    <span>return</span> <span>WeatherData</span><span>(</span>
        <span>temperature</span><span>=</span><span>22.5</span><span>,</span>
        <span>humidity</span><span>=</span><span>45.0</span><span>,</span>
        <span>condition</span><span>=</span><span>"sunny"</span><span>,</span>
        <span>wind_speed</span><span>=</span><span>5.2</span><span>,</span>
    <span>)</span>


<span># Using TypedDict for simpler structures</span>
<span>class</span><span> </span><span>LocationInfo</span><span>(</span><span>TypedDict</span><span>):</span>
    <span>latitude</span><span>:</span> <span>float</span>
    <span>longitude</span><span>:</span> <span>float</span>
    <span>name</span><span>:</span> <span>str</span>


<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>get_location</span><span>(</span><span>address</span><span>:</span> <span>str</span><span>)</span> <span>-&gt;</span> <span>LocationInfo</span><span>:</span>
<span>    </span><span>"""Get location coordinates"""</span>
    <span>return</span> <span>LocationInfo</span><span>(</span><span>latitude</span><span>=</span><span>51.5074</span><span>,</span> <span>longitude</span><span>=-</span><span>0.1278</span><span>,</span> <span>name</span><span>=</span><span>"London, UK"</span><span>)</span>


<span># Using dict[str, Any] for flexible schemas</span>
<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>get_statistics</span><span>(</span><span>data_type</span><span>:</span> <span>str</span><span>)</span> <span>-&gt;</span> <span>dict</span><span>[</span><span>str</span><span>,</span> <span>float</span><span>]:</span>
<span>    </span><span>"""Get various statistics"""</span>
    <span>return</span> <span>{</span><span>"mean"</span><span>:</span> <span>42.5</span><span>,</span> <span>"median"</span><span>:</span> <span>40.0</span><span>,</span> <span>"std_dev"</span><span>:</span> <span>5.2</span><span>}</span>


<span># Ordinary classes with type hints work for structured output</span>
<span>class</span><span> </span><span>UserProfile</span><span>:</span>
    <span>name</span><span>:</span> <span>str</span>
    <span>age</span><span>:</span> <span>int</span>
    <span>email</span><span>:</span> <span>str</span> <span>|</span> <span>None</span> <span>=</span> <span>None</span>

    <span>def</span><span> </span><span>__init__</span><span>(</span><span>self</span><span>,</span> <span>name</span><span>:</span> <span>str</span><span>,</span> <span>age</span><span>:</span> <span>int</span><span>,</span> <span>email</span><span>:</span> <span>str</span> <span>|</span> <span>None</span> <span>=</span> <span>None</span><span>):</span>
        <span>self</span><span>.</span><span>name</span> <span>=</span> <span>name</span>
        <span>self</span><span>.</span><span>age</span> <span>=</span> <span>age</span>
        <span>self</span><span>.</span><span>email</span> <span>=</span> <span>email</span>


<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>get_user</span><span>(</span><span>user_id</span><span>:</span> <span>str</span><span>)</span> <span>-&gt;</span> <span>UserProfile</span><span>:</span>
<span>    </span><span>"""Get user profile - returns structured data"""</span>
    <span>return</span> <span>UserProfile</span><span>(</span><span>name</span><span>=</span><span>"Alice"</span><span>,</span> <span>age</span><span>=</span><span>30</span><span>,</span> <span>email</span><span>=</span><span>"alice@example.com"</span><span>)</span>


<span># Classes WITHOUT type hints cannot be used for structured output</span>
<span>class</span><span> </span><span>UntypedConfig</span><span>:</span>
    <span>def</span><span> </span><span>__init__</span><span>(</span><span>self</span><span>,</span> <span>setting1</span><span>,</span> <span>setting2</span><span>):</span>  <span># type: ignore[reportMissingParameterType]</span>
        <span>self</span><span>.</span><span>setting1</span> <span>=</span> <span>setting1</span>
        <span>self</span><span>.</span><span>setting2</span> <span>=</span> <span>setting2</span>


<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>get_config</span><span>()</span> <span>-&gt;</span> <span>UntypedConfig</span><span>:</span>
<span>    </span><span>"""This returns unstructured output - no schema generated"""</span>
    <span>return</span> <span>UntypedConfig</span><span>(</span><span>"value1"</span><span>,</span> <span>"value2"</span><span>)</span>


<span># Lists and other types are wrapped automatically</span>
<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>list_cities</span><span>()</span> <span>-&gt;</span> <span>list</span><span>[</span><span>str</span><span>]:</span>
<span>    </span><span>"""Get a list of cities"""</span>
    <span>return</span> <span>[</span><span>"London"</span><span>,</span> <span>"Paris"</span><span>,</span> <span>"Tokyo"</span><span>]</span>
    <span># Returns: {"result": ["London", "Paris", "Tokyo"]}</span>


<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>get_temperature</span><span>(</span><span>city</span><span>:</span> <span>str</span><span>)</span> <span>-&gt;</span> <span>float</span><span>:</span>
<span>    </span><span>"""Get temperature as a simple float"""</span>
    <span>return</span> <span>22.5</span>
    <span># Returns: {"result": 22.5}</span>
```

_Full example: [examples/snippets/servers/structured\_output.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/structured_output.py)  
完整示例： [示例/片段/服务器/structured\_output.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/structured_output.py)_

### Prompts  提示

Prompts are reusable templates that help LLMs interact with your server effectively:  
提示词是可重复使用的模板，帮助大型语言模型有效与你的服务器交互：

```
<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>FastMCP</span>
<span>from</span><span> </span><span>mcp.server.fastmcp.prompts</span><span> </span><span>import</span> <span>base</span>

<span>mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>name</span><span>=</span><span>"Prompt Example"</span><span>)</span>


<span>@mcp</span><span>.</span><span>prompt</span><span>(</span><span>title</span><span>=</span><span>"Code Review"</span><span>)</span>
<span>def</span><span> </span><span>review_code</span><span>(</span><span>code</span><span>:</span> <span>str</span><span>)</span> <span>-&gt;</span> <span>str</span><span>:</span>
    <span>return</span> <span>f</span><span>"Please review this code:</span><span>\n\n</span><span>{</span><span>code</span><span>}</span><span>"</span>


<span>@mcp</span><span>.</span><span>prompt</span><span>(</span><span>title</span><span>=</span><span>"Debug Assistant"</span><span>)</span>
<span>def</span><span> </span><span>debug_error</span><span>(</span><span>error</span><span>:</span> <span>str</span><span>)</span> <span>-&gt;</span> <span>list</span><span>[</span><span>base</span><span>.</span><span>Message</span><span>]:</span>
    <span>return</span> <span>[</span>
        <span>base</span><span>.</span><span>UserMessage</span><span>(</span><span>"I'm seeing this error:"</span><span>),</span>
        <span>base</span><span>.</span><span>UserMessage</span><span>(</span><span>error</span><span>),</span>
        <span>base</span><span>.</span><span>AssistantMessage</span><span>(</span><span>"I'll help debug that. What have you tried so far?"</span><span>),</span>
    <span>]</span>
```

_Full example: [examples/snippets/servers/basic\_prompt.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/basic_prompt.py)  
完整示例： [示例/片段/服务器/basic\_prompt.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/basic_prompt.py)_

### Icons  图标

MCP servers can provide icons for UI display. Icons can be added to the server implementation, tools, resources, and prompts:  
MCP 服务器可以提供 UI 显示的图标。图标可以添加到服务器实现、工具、资源和提示中：

```
<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>FastMCP</span><span>,</span> <span>Icon</span>

<span># Create an icon from a file path or URL</span>
<span>icon</span> <span>=</span> <span>Icon</span><span>(</span>
    <span>src</span><span>=</span><span>"icon.png"</span><span>,</span>
    <span>mimeType</span><span>=</span><span>"image/png"</span><span>,</span>
    <span>sizes</span><span>=</span><span>"64x64"</span>
<span>)</span>

<span># Add icons to server</span>
<span>mcp</span> <span>=</span> <span>FastMCP</span><span>(</span>
    <span>"My Server"</span><span>,</span>
    <span>website_url</span><span>=</span><span>"https://example.com"</span><span>,</span>
    <span>icons</span><span>=</span><span>[</span><span>icon</span><span>]</span>
<span>)</span>

<span># Add icons to tools, resources, and prompts</span>
<span>@mcp</span><span>.</span><span>tool</span><span>(</span><span>icons</span><span>=</span><span>[</span><span>icon</span><span>])</span>
<span>def</span><span> </span><span>my_tool</span><span>():</span>
<span>    </span><span>"""Tool with an icon."""</span>
    <span>return</span> <span>"result"</span>

<span>@mcp</span><span>.</span><span>resource</span><span>(</span><span>"demo://resource"</span><span>,</span> <span>icons</span><span>=</span><span>[</span><span>icon</span><span>])</span>
<span>def</span><span> </span><span>my_resource</span><span>():</span>
<span>    </span><span>"""Resource with an icon."""</span>
    <span>return</span> <span>"content"</span>
```

_Full example: [examples/fastmcp/icons\_demo.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/fastmcp/icons_demo.py)  
完整示例： [示例/fastmcp/icons\_demo.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/fastmcp/icons_demo.py)_

### Images  图片

FastMCP provides an `Image` class that automatically handles image data:  
FastMCP 提供了一个自动处理图像数据的 `Image` 类：

```
<span>"""Example showing image handling with FastMCP."""</span>

<span>from</span><span> </span><span>PIL</span><span> </span><span>import</span> <span>Image</span> <span>as</span> <span>PILImage</span>

<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>FastMCP</span><span>,</span> <span>Image</span>

<span>mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>"Image Example"</span><span>)</span>


<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>create_thumbnail</span><span>(</span><span>image_path</span><span>:</span> <span>str</span><span>)</span> <span>-&gt;</span> <span>Image</span><span>:</span>
<span>    </span><span>"""Create a thumbnail from an image"""</span>
    <span>img</span> <span>=</span> <span>PILImage</span><span>.</span><span>open</span><span>(</span><span>image_path</span><span>)</span>
    <span>img</span><span>.</span><span>thumbnail</span><span>((</span><span>100</span><span>,</span> <span>100</span><span>))</span>
    <span>return</span> <span>Image</span><span>(</span><span>data</span><span>=</span><span>img</span><span>.</span><span>tobytes</span><span>(),</span> <span>format</span><span>=</span><span>"png"</span><span>)</span>
```

_Full example: [examples/snippets/servers/images.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/images.py)  
完整示例： [示例/片段/服务器/images.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/images.py)_

### Context  上下文

The Context object is automatically injected into tool and resource functions that request it via type hints. It provides access to MCP capabilities like logging, progress reporting, resource reading, user interaction, and request metadata.  
上下文对象会自动注入通过类型提示请求的工具和资源函数中。它提供访问 MCP 功能，如日志、进度报告、资源读取、用户交互和请求元数据。

#### Getting Context in Functions  
函数中的上下文获取

To use context in a tool or resource function, add a parameter with the `Context` type annotation:  
要在工具或资源函数中使用上下文，添加带有`上下文`类型注释的参数：

```
<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>Context</span><span>,</span> <span>FastMCP</span>

<span>mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>name</span><span>=</span><span>"Context Example"</span><span>)</span>


<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>async</span> <span>def</span><span> </span><span>my_tool</span><span>(</span><span>x</span><span>:</span> <span>int</span><span>,</span> <span>ctx</span><span>:</span> <span>Context</span><span>)</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Tool that uses context capabilities."""</span>
    <span># The context parameter can have any name as long as it's type-annotated</span>
    <span>return</span> <span>await</span> <span>process_with_context</span><span>(</span><span>x</span><span>,</span> <span>ctx</span><span>)</span>
```

#### Context Properties and Methods  
上下文属性与方法

The Context object provides the following capabilities:  
上下文对象提供以下功能：

-   `ctx.request_id` - Unique ID for the current request  
    `ctx.request_id` - 当前请求的唯一 ID
-   `ctx.client_id` - Client ID if available  
    `ctx.client_id` - 如有客户 ID
-   `ctx.fastmcp` - Access to the FastMCP server instance (see [FastMCP Properties](https://pypi.org/project/mcp/#fastmcp-properties))  
    `ctx.fastmcp` - 访问 FastMCP 服务器实例（参见 [FastMCP 属性](https://pypi.org/project/mcp/#fastmcp-properties) ）
-   `ctx.session` - Access to the underlying session for advanced communication (see [Session Properties and Methods](https://pypi.org/project/mcp/#session-properties-and-methods))  
    `ctx.session` - 访问底层会话以进行高级通信（参见[会话属性和方法](https://pypi.org/project/mcp/#session-properties-and-methods) ）
-   `ctx.request_context` - Access to request-specific data and lifespan resources (see [Request Context Properties](https://pypi.org/project/mcp/#request-context-properties))  
    `ctx.request_context` - 访问请求特定数据和生命周期资源（参见[请求上下文属性](https://pypi.org/project/mcp/#request-context-properties) ）
-   `await ctx.debug(message)` - Send debug log message  
    `await ctx.debug（message）` - 发送调试日志消息
-   `await ctx.info(message)` - Send info log message  
    `等待 ctx.info（消息）`\- 发送信息日志消息
-   `await ctx.warning(message)` - Send warning log message  
    `waititctx.warning（message）` - 发送警告日志消息
-   `await ctx.error(message)` - Send error log message  
    `await ctx.error（message）` - 发送错误日志消息
-   `await ctx.log(level, message, logger_name=None)` - Send log with custom level  
    `await ctx.log(level, message, logger_name=None)` - 发送带有自定义电平的日志
-   `await ctx.report_progress(progress, total=None, message=None)` - Report operation progress  
    `await ctx.report_progress(progress, total=None, message=None)` - 报告运营进展
-   `await ctx.read_resource(uri)` - Read a resource by URI  
    `等待 ctx.read_resource（URI）`——阅读 URI 的资源
-   `await ctx.elicit(message, schema)` - Request additional information from user with validation  
    `await ctx.elicit(message, schema)` - 向用户请求额外信息并进行验证

```
<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>Context</span><span>,</span> <span>FastMCP</span>
<span>from</span><span> </span><span>mcp.server.session</span><span> </span><span>import</span> <span>ServerSession</span>

<span>mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>name</span><span>=</span><span>"Progress Example"</span><span>)</span>


<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>async</span> <span>def</span><span> </span><span>long_running_task</span><span>(</span><span>task_name</span><span>:</span> <span>str</span><span>,</span> <span>ctx</span><span>:</span> <span>Context</span><span>[</span><span>ServerSession</span><span>,</span> <span>None</span><span>],</span> <span>steps</span><span>:</span> <span>int</span> <span>=</span> <span>5</span><span>)</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Execute a task with progress updates."""</span>
    <span>await</span> <span>ctx</span><span>.</span><span>info</span><span>(</span><span>f</span><span>"Starting: </span><span>{</span><span>task_name</span><span>}</span><span>"</span><span>)</span>

    <span>for</span> <span>i</span> <span>in</span> <span>range</span><span>(</span><span>steps</span><span>):</span>
        <span>progress</span> <span>=</span> <span>(</span><span>i</span> <span>+</span> <span>1</span><span>)</span> <span>/</span> <span>steps</span>
        <span>await</span> <span>ctx</span><span>.</span><span>report_progress</span><span>(</span>
            <span>progress</span><span>=</span><span>progress</span><span>,</span>
            <span>total</span><span>=</span><span>1.0</span><span>,</span>
            <span>message</span><span>=</span><span>f</span><span>"Step </span><span>{</span><span>i</span><span> </span><span>+</span><span> </span><span>1</span><span>}</span><span>/</span><span>{</span><span>steps</span><span>}</span><span>"</span><span>,</span>
        <span>)</span>
        <span>await</span> <span>ctx</span><span>.</span><span>debug</span><span>(</span><span>f</span><span>"Completed step </span><span>{</span><span>i</span><span> </span><span>+</span><span> </span><span>1</span><span>}</span><span>"</span><span>)</span>

    <span>return</span> <span>f</span><span>"Task '</span><span>{</span><span>task_name</span><span>}</span><span>' completed"</span>
```

_Full example: [examples/snippets/servers/tool\_progress.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/tool_progress.py)  
完整示例： [示例/摘要/服务器/tool\_progress.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/tool_progress.py)_

### Completions  完工

MCP supports providing completion suggestions for prompt arguments and resource template parameters. With the context parameter, servers can provide completions based on previously resolved values:  
MCP 支持为提示词参数和资源模板参数提供补全建议。利用上下文参数，服务器可以基于先前解析的值提供补全：

Client usage:  客户端使用情况：

```
<span>"""</span>
<span>cd to the `examples/snippets` directory and run:</span>
<span>    uv run completion-client</span>
<span>"""</span>

<span>import</span><span> </span><span>asyncio</span>
<span>import</span><span> </span><span>os</span>

<span>from</span><span> </span><span>mcp</span><span> </span><span>import</span> <span>ClientSession</span><span>,</span> <span>StdioServerParameters</span>
<span>from</span><span> </span><span>mcp.client.stdio</span><span> </span><span>import</span> <span>stdio_client</span>
<span>from</span><span> </span><span>mcp.types</span><span> </span><span>import</span> <span>PromptReference</span><span>,</span> <span>ResourceTemplateReference</span>

<span># Create server parameters for stdio connection</span>
<span>server_params</span> <span>=</span> <span>StdioServerParameters</span><span>(</span>
    <span>command</span><span>=</span><span>"uv"</span><span>,</span>  <span># Using uv to run the server</span>
    <span>args</span><span>=</span><span>[</span><span>"run"</span><span>,</span> <span>"server"</span><span>,</span> <span>"completion"</span><span>,</span> <span>"stdio"</span><span>],</span>  <span># Server with completion support</span>
    <span>env</span><span>=</span><span>{</span><span>"UV_INDEX"</span><span>:</span> <span>os</span><span>.</span><span>environ</span><span>.</span><span>get</span><span>(</span><span>"UV_INDEX"</span><span>,</span> <span>""</span><span>)},</span>
<span>)</span>


<span>async</span> <span>def</span><span> </span><span>run</span><span>():</span>
<span>    </span><span>"""Run the completion client example."""</span>
    <span>async</span> <span>with</span> <span>stdio_client</span><span>(</span><span>server_params</span><span>)</span> <span>as</span> <span>(</span><span>read</span><span>,</span> <span>write</span><span>):</span>
        <span>async</span> <span>with</span> <span>ClientSession</span><span>(</span><span>read</span><span>,</span> <span>write</span><span>)</span> <span>as</span> <span>session</span><span>:</span>
            <span># Initialize the connection</span>
            <span>await</span> <span>session</span><span>.</span><span>initialize</span><span>()</span>

            <span># List available resource templates</span>
            <span>templates</span> <span>=</span> <span>await</span> <span>session</span><span>.</span><span>list_resource_templates</span><span>()</span>
            <span>print</span><span>(</span><span>"Available resource templates:"</span><span>)</span>
            <span>for</span> <span>template</span> <span>in</span> <span>templates</span><span>.</span><span>resourceTemplates</span><span>:</span>
                <span>print</span><span>(</span><span>f</span><span>"  - </span><span>{</span><span>template</span><span>.</span><span>uriTemplate</span><span>}</span><span>"</span><span>)</span>

            <span># List available prompts</span>
            <span>prompts</span> <span>=</span> <span>await</span> <span>session</span><span>.</span><span>list_prompts</span><span>()</span>
            <span>print</span><span>(</span><span>"</span><span>\n</span><span>Available prompts:"</span><span>)</span>
            <span>for</span> <span>prompt</span> <span>in</span> <span>prompts</span><span>.</span><span>prompts</span><span>:</span>
                <span>print</span><span>(</span><span>f</span><span>"  - </span><span>{</span><span>prompt</span><span>.</span><span>name</span><span>}</span><span>"</span><span>)</span>

            <span># Complete resource template arguments</span>
            <span>if</span> <span>templates</span><span>.</span><span>resourceTemplates</span><span>:</span>
                <span>template</span> <span>=</span> <span>templates</span><span>.</span><span>resourceTemplates</span><span>[</span><span>0</span><span>]</span>
                <span>print</span><span>(</span><span>f</span><span>"</span><span>\n</span><span>Completing arguments for resource template: </span><span>{</span><span>template</span><span>.</span><span>uriTemplate</span><span>}</span><span>"</span><span>)</span>

                <span># Complete without context</span>
                <span>result</span> <span>=</span> <span>await</span> <span>session</span><span>.</span><span>complete</span><span>(</span>
                    <span>ref</span><span>=</span><span>ResourceTemplateReference</span><span>(</span><span>type</span><span>=</span><span>"ref/resource"</span><span>,</span> <span>uri</span><span>=</span><span>template</span><span>.</span><span>uriTemplate</span><span>),</span>
                    <span>argument</span><span>=</span><span>{</span><span>"name"</span><span>:</span> <span>"owner"</span><span>,</span> <span>"value"</span><span>:</span> <span>"model"</span><span>},</span>
                <span>)</span>
                <span>print</span><span>(</span><span>f</span><span>"Completions for 'owner' starting with 'model': </span><span>{</span><span>result</span><span>.</span><span>completion</span><span>.</span><span>values</span><span>}</span><span>"</span><span>)</span>

                <span># Complete with context - repo suggestions based on owner</span>
                <span>result</span> <span>=</span> <span>await</span> <span>session</span><span>.</span><span>complete</span><span>(</span>
                    <span>ref</span><span>=</span><span>ResourceTemplateReference</span><span>(</span><span>type</span><span>=</span><span>"ref/resource"</span><span>,</span> <span>uri</span><span>=</span><span>template</span><span>.</span><span>uriTemplate</span><span>),</span>
                    <span>argument</span><span>=</span><span>{</span><span>"name"</span><span>:</span> <span>"repo"</span><span>,</span> <span>"value"</span><span>:</span> <span>""</span><span>},</span>
                    <span>context_arguments</span><span>=</span><span>{</span><span>"owner"</span><span>:</span> <span>"modelcontextprotocol"</span><span>},</span>
                <span>)</span>
                <span>print</span><span>(</span><span>f</span><span>"Completions for 'repo' with owner='modelcontextprotocol': </span><span>{</span><span>result</span><span>.</span><span>completion</span><span>.</span><span>values</span><span>}</span><span>"</span><span>)</span>

            <span># Complete prompt arguments</span>
            <span>if</span> <span>prompts</span><span>.</span><span>prompts</span><span>:</span>
                <span>prompt_name</span> <span>=</span> <span>prompts</span><span>.</span><span>prompts</span><span>[</span><span>0</span><span>]</span><span>.</span><span>name</span>
                <span>print</span><span>(</span><span>f</span><span>"</span><span>\n</span><span>Completing arguments for prompt: </span><span>{</span><span>prompt_name</span><span>}</span><span>"</span><span>)</span>

                <span>result</span> <span>=</span> <span>await</span> <span>session</span><span>.</span><span>complete</span><span>(</span>
                    <span>ref</span><span>=</span><span>PromptReference</span><span>(</span><span>type</span><span>=</span><span>"ref/prompt"</span><span>,</span> <span>name</span><span>=</span><span>prompt_name</span><span>),</span>
                    <span>argument</span><span>=</span><span>{</span><span>"name"</span><span>:</span> <span>"style"</span><span>,</span> <span>"value"</span><span>:</span> <span>""</span><span>},</span>
                <span>)</span>
                <span>print</span><span>(</span><span>f</span><span>"Completions for 'style' argument: </span><span>{</span><span>result</span><span>.</span><span>completion</span><span>.</span><span>values</span><span>}</span><span>"</span><span>)</span>


<span>def</span><span> </span><span>main</span><span>():</span>
<span>    </span><span>"""Entry point for the completion client."""</span>
    <span>asyncio</span><span>.</span><span>run</span><span>(</span><span>run</span><span>())</span>


<span>if</span> <span>__name__</span> <span>==</span> <span>"__main__"</span><span>:</span>
    <span>main</span><span>()</span>
```

_Full example: [examples/snippets/clients/completion\_client.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/completion_client.py)  
完整示例： [示例/片段/客户端/completion\_client.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/completion_client.py)_

### Elicitation  引发

Request additional information from users. This example shows an Elicitation during a Tool Call:  
向用户索取额外信息。这个示例展示了工具调用期间的引发：

```
<span>"""Elicitation examples demonstrating form and URL mode elicitation.</span>

<span>Form mode elicitation collects structured, non-sensitive data through a schema.</span>
<span>URL mode elicitation directs users to external URLs for sensitive operations</span>
<span>like OAuth flows, credential collection, or payment processing.</span>
<span>"""</span>

<span>import</span><span> </span><span>uuid</span>

<span>from</span><span> </span><span>pydantic</span><span> </span><span>import</span> <span>BaseModel</span><span>,</span> <span>Field</span>

<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>Context</span><span>,</span> <span>FastMCP</span>
<span>from</span><span> </span><span>mcp.server.session</span><span> </span><span>import</span> <span>ServerSession</span>
<span>from</span><span> </span><span>mcp.shared.exceptions</span><span> </span><span>import</span> <span>UrlElicitationRequiredError</span>
<span>from</span><span> </span><span>mcp.types</span><span> </span><span>import</span> <span>ElicitRequestURLParams</span>

<span>mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>name</span><span>=</span><span>"Elicitation Example"</span><span>)</span>


<span>class</span><span> </span><span>BookingPreferences</span><span>(</span><span>BaseModel</span><span>):</span>
<span>    </span><span>"""Schema for collecting user preferences."""</span>

    <span>checkAlternative</span><span>:</span> <span>bool</span> <span>=</span> <span>Field</span><span>(</span><span>description</span><span>=</span><span>"Would you like to check another date?"</span><span>)</span>
    <span>alternativeDate</span><span>:</span> <span>str</span> <span>=</span> <span>Field</span><span>(</span>
        <span>default</span><span>=</span><span>"2024-12-26"</span><span>,</span>
        <span>description</span><span>=</span><span>"Alternative date (YYYY-MM-DD)"</span><span>,</span>
    <span>)</span>


<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>async</span> <span>def</span><span> </span><span>book_table</span><span>(</span><span>date</span><span>:</span> <span>str</span><span>,</span> <span>time</span><span>:</span> <span>str</span><span>,</span> <span>party_size</span><span>:</span> <span>int</span><span>,</span> <span>ctx</span><span>:</span> <span>Context</span><span>[</span><span>ServerSession</span><span>,</span> <span>None</span><span>])</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Book a table with date availability check.</span>

<span>    This demonstrates form mode elicitation for collecting non-sensitive user input.</span>
<span>    """</span>
    <span># Check if date is available</span>
    <span>if</span> <span>date</span> <span>==</span> <span>"2024-12-25"</span><span>:</span>
        <span># Date unavailable - ask user for alternative</span>
        <span>result</span> <span>=</span> <span>await</span> <span>ctx</span><span>.</span><span>elicit</span><span>(</span>
            <span>message</span><span>=</span><span>(</span><span>f</span><span>"No tables available for </span><span>{</span><span>party_size</span><span>}</span><span> on </span><span>{</span><span>date</span><span>}</span><span>. Would you like to try another date?"</span><span>),</span>
            <span>schema</span><span>=</span><span>BookingPreferences</span><span>,</span>
        <span>)</span>

        <span>if</span> <span>result</span><span>.</span><span>action</span> <span>==</span> <span>"accept"</span> <span>and</span> <span>result</span><span>.</span><span>data</span><span>:</span>
            <span>if</span> <span>result</span><span>.</span><span>data</span><span>.</span><span>checkAlternative</span><span>:</span>
                <span>return</span> <span>f</span><span>"[SUCCESS] Booked for </span><span>{</span><span>result</span><span>.</span><span>data</span><span>.</span><span>alternativeDate</span><span>}</span><span>"</span>
            <span>return</span> <span>"[CANCELLED] No booking made"</span>
        <span>return</span> <span>"[CANCELLED] Booking cancelled"</span>

    <span># Date available</span>
    <span>return</span> <span>f</span><span>"[SUCCESS] Booked for </span><span>{</span><span>date</span><span>}</span><span> at </span><span>{</span><span>time</span><span>}</span><span>"</span>


<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>async</span> <span>def</span><span> </span><span>secure_payment</span><span>(</span><span>amount</span><span>:</span> <span>float</span><span>,</span> <span>ctx</span><span>:</span> <span>Context</span><span>[</span><span>ServerSession</span><span>,</span> <span>None</span><span>])</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Process a secure payment requiring URL confirmation.</span>

<span>    This demonstrates URL mode elicitation using ctx.elicit_url() for</span>
<span>    operations that require out-of-band user interaction.</span>
<span>    """</span>
    <span>elicitation_id</span> <span>=</span> <span>str</span><span>(</span><span>uuid</span><span>.</span><span>uuid4</span><span>())</span>

    <span>result</span> <span>=</span> <span>await</span> <span>ctx</span><span>.</span><span>elicit_url</span><span>(</span>
        <span>message</span><span>=</span><span>f</span><span>"Please confirm payment of $</span><span>{</span><span>amount</span><span>:</span><span>.2f</span><span>}</span><span>"</span><span>,</span>
        <span>url</span><span>=</span><span>f</span><span>"https://payments.example.com/confirm?amount=</span><span>{</span><span>amount</span><span>}</span><span>&amp;id=</span><span>{</span><span>elicitation_id</span><span>}</span><span>"</span><span>,</span>
        <span>elicitation_id</span><span>=</span><span>elicitation_id</span><span>,</span>
    <span>)</span>

    <span>if</span> <span>result</span><span>.</span><span>action</span> <span>==</span> <span>"accept"</span><span>:</span>
        <span># In a real app, the payment confirmation would happen out-of-band</span>
        <span># and you'd verify the payment status from your backend</span>
        <span>return</span> <span>f</span><span>"Payment of $</span><span>{</span><span>amount</span><span>:</span><span>.2f</span><span>}</span><span> initiated - check your browser to complete"</span>
    <span>elif</span> <span>result</span><span>.</span><span>action</span> <span>==</span> <span>"decline"</span><span>:</span>
        <span>return</span> <span>"Payment declined by user"</span>
    <span>return</span> <span>"Payment cancelled"</span>


<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>async</span> <span>def</span><span> </span><span>connect_service</span><span>(</span><span>service_name</span><span>:</span> <span>str</span><span>,</span> <span>ctx</span><span>:</span> <span>Context</span><span>[</span><span>ServerSession</span><span>,</span> <span>None</span><span>])</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Connect to a third-party service requiring OAuth authorization.</span>

<span>    This demonstrates the "throw error" pattern using UrlElicitationRequiredError.</span>
<span>    Use this pattern when the tool cannot proceed without user authorization.</span>
<span>    """</span>
    <span>elicitation_id</span> <span>=</span> <span>str</span><span>(</span><span>uuid</span><span>.</span><span>uuid4</span><span>())</span>

    <span># Raise UrlElicitationRequiredError to signal that the client must complete</span>
    <span># a URL elicitation before this request can be processed.</span>
    <span># The MCP framework will convert this to a -32042 error response.</span>
    <span>raise</span> <span>UrlElicitationRequiredError</span><span>(</span>
        <span>[</span>
            <span>ElicitRequestURLParams</span><span>(</span>
                <span>mode</span><span>=</span><span>"url"</span><span>,</span>
                <span>message</span><span>=</span><span>f</span><span>"Authorization required to connect to </span><span>{</span><span>service_name</span><span>}</span><span>"</span><span>,</span>
                <span>url</span><span>=</span><span>f</span><span>"https://</span><span>{</span><span>service_name</span><span>}</span><span>.example.com/oauth/authorize?elicit=</span><span>{</span><span>elicitation_id</span><span>}</span><span>"</span><span>,</span>
                <span>elicitationId</span><span>=</span><span>elicitation_id</span><span>,</span>
            <span>)</span>
        <span>]</span>
    <span>)</span>
```

_Full example: [examples/snippets/servers/elicitation.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/elicitation.py)  
完整示例： [示例/片段/服务器/elicitation.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/elicitation.py)_

Elicitation schemas support default values for all field types. Default values are automatically included in the JSON schema sent to clients, allowing them to pre-populate forms.  
引发模式支持所有字段类型的默认值。默认值会自动包含在发送给客户端的 JSON 模式中，允许他们预先填充表单。

The `elicit()` method returns an `ElicitationResult` with:  
`elicit（）` 方法返回一个 `ElicitationResult`，结果为：

-   `action`: "accept", "decline", or "cancel"  
    `作` ：“接受”、“拒绝”或“取消”
-   `data`: The validated response (only when accepted)  
    `数据` ：验证后的响应（仅在接受时）
-   `validation_error`: Any validation error message  
    `validation_error`：任何验证错误信息

### Sampling  采样

Tools can interact with LLMs through sampling (generating text):  
工具可以通过抽样（生成文本）与大型语言模型交互：

```
<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>Context</span><span>,</span> <span>FastMCP</span>
<span>from</span><span> </span><span>mcp.server.session</span><span> </span><span>import</span> <span>ServerSession</span>
<span>from</span><span> </span><span>mcp.types</span><span> </span><span>import</span> <span>SamplingMessage</span><span>,</span> <span>TextContent</span>

<span>mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>name</span><span>=</span><span>"Sampling Example"</span><span>)</span>


<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>async</span> <span>def</span><span> </span><span>generate_poem</span><span>(</span><span>topic</span><span>:</span> <span>str</span><span>,</span> <span>ctx</span><span>:</span> <span>Context</span><span>[</span><span>ServerSession</span><span>,</span> <span>None</span><span>])</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Generate a poem using LLM sampling."""</span>
    <span>prompt</span> <span>=</span> <span>f</span><span>"Write a short poem about </span><span>{</span><span>topic</span><span>}</span><span>"</span>

    <span>result</span> <span>=</span> <span>await</span> <span>ctx</span><span>.</span><span>session</span><span>.</span><span>create_message</span><span>(</span>
        <span>messages</span><span>=</span><span>[</span>
            <span>SamplingMessage</span><span>(</span>
                <span>role</span><span>=</span><span>"user"</span><span>,</span>
                <span>content</span><span>=</span><span>TextContent</span><span>(</span><span>type</span><span>=</span><span>"text"</span><span>,</span> <span>text</span><span>=</span><span>prompt</span><span>),</span>
            <span>)</span>
        <span>],</span>
        <span>max_tokens</span><span>=</span><span>100</span><span>,</span>
    <span>)</span>

    <span># Since we're not passing tools param, result.content is single content</span>
    <span>if</span> <span>result</span><span>.</span><span>content</span><span>.</span><span>type</span> <span>==</span> <span>"text"</span><span>:</span>
        <span>return</span> <span>result</span><span>.</span><span>content</span><span>.</span><span>text</span>
    <span>return</span> <span>str</span><span>(</span><span>result</span><span>.</span><span>content</span><span>)</span>
```

_Full example: [examples/snippets/servers/sampling.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/sampling.py)  
完整示例： [示例/片段/服务器/sampling.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/sampling.py)_

### Logging and Notifications  
日志与通知

Tools can send logs and notifications through the context:  
工具可以通过以下上下文发送日志和通知：

```
<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>Context</span><span>,</span> <span>FastMCP</span>
<span>from</span><span> </span><span>mcp.server.session</span><span> </span><span>import</span> <span>ServerSession</span>

<span>mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>name</span><span>=</span><span>"Notifications Example"</span><span>)</span>


<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>async</span> <span>def</span><span> </span><span>process_data</span><span>(</span><span>data</span><span>:</span> <span>str</span><span>,</span> <span>ctx</span><span>:</span> <span>Context</span><span>[</span><span>ServerSession</span><span>,</span> <span>None</span><span>])</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Process data with logging."""</span>
    <span># Different log levels</span>
    <span>await</span> <span>ctx</span><span>.</span><span>debug</span><span>(</span><span>f</span><span>"Debug: Processing '</span><span>{</span><span>data</span><span>}</span><span>'"</span><span>)</span>
    <span>await</span> <span>ctx</span><span>.</span><span>info</span><span>(</span><span>"Info: Starting processing"</span><span>)</span>
    <span>await</span> <span>ctx</span><span>.</span><span>warning</span><span>(</span><span>"Warning: This is experimental"</span><span>)</span>
    <span>await</span> <span>ctx</span><span>.</span><span>error</span><span>(</span><span>"Error: (This is just a demo)"</span><span>)</span>

    <span># Notify about resource changes</span>
    <span>await</span> <span>ctx</span><span>.</span><span>session</span><span>.</span><span>send_resource_list_changed</span><span>()</span>

    <span>return</span> <span>f</span><span>"Processed: </span><span>{</span><span>data</span><span>}</span><span>"</span>
```

_Full example: [examples/snippets/servers/notifications.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/notifications.py)  
完整示例： [示例/片段/服务器/notifications.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/notifications.py)_

### Authentication  认证

Authentication can be used by servers that want to expose tools accessing protected resources.  
认证可以被想要暴露访问受保护资源工具的服务器使用。

`mcp.server.auth` implements OAuth 2.1 resource server functionality, where MCP servers act as Resource Servers (RS) that validate tokens issued by separate Authorization Servers (AS). This follows the [MCP authorization specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) and implements RFC 9728 (Protected Resource Metadata) for AS discovery.  
`mcp.server.auth` 实现了 OAuth 2.1 资源服务器功能，其中 MCP 服务器作为资源服务器（RS）来验证由独立授权服务器（AS）发出的令牌。这遵循 [MCP 授权规范](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) ，并实现了 RFC 9728（受保护资源元数据）用于 AS 发现。

MCP servers can use authentication by providing an implementation of the `TokenVerifier` protocol:  
MCP 服务器可以通过提供 `TokenVerifier` 协议的实现来使用认证：

```
<span>"""</span>
<span>Run from the repository root:</span>
<span>    uv run examples/snippets/servers/oauth_server.py</span>
<span>"""</span>

<span>from</span><span> </span><span>pydantic</span><span> </span><span>import</span> <span>AnyHttpUrl</span>

<span>from</span><span> </span><span>mcp.server.auth.provider</span><span> </span><span>import</span> <span>AccessToken</span><span>,</span> <span>TokenVerifier</span>
<span>from</span><span> </span><span>mcp.server.auth.settings</span><span> </span><span>import</span> <span>AuthSettings</span>
<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>FastMCP</span>


<span>class</span><span> </span><span>SimpleTokenVerifier</span><span>(</span><span>TokenVerifier</span><span>):</span>
<span>    </span><span>"""Simple token verifier for demonstration."""</span>

    <span>async</span> <span>def</span><span> </span><span>verify_token</span><span>(</span><span>self</span><span>,</span> <span>token</span><span>:</span> <span>str</span><span>)</span> <span>-&gt;</span> <span>AccessToken</span> <span>|</span> <span>None</span><span>:</span>
        <span>pass</span>  <span># This is where you would implement actual token validation</span>


<span># Create FastMCP instance as a Resource Server</span>
<span>mcp</span> <span>=</span> <span>FastMCP</span><span>(</span>
    <span>"Weather Service"</span><span>,</span>
    <span>json_response</span><span>=</span><span>True</span><span>,</span>
    <span># Token verifier for authentication</span>
    <span>token_verifier</span><span>=</span><span>SimpleTokenVerifier</span><span>(),</span>
    <span># Auth settings for RFC 9728 Protected Resource Metadata</span>
    <span>auth</span><span>=</span><span>AuthSettings</span><span>(</span>
        <span>issuer_url</span><span>=</span><span>AnyHttpUrl</span><span>(</span><span>"https://auth.example.com"</span><span>),</span>  <span># Authorization Server URL</span>
        <span>resource_server_url</span><span>=</span><span>AnyHttpUrl</span><span>(</span><span>"http://localhost:3001"</span><span>),</span>  <span># This server's URL</span>
        <span>required_scopes</span><span>=</span><span>[</span><span>"user"</span><span>],</span>
    <span>),</span>
<span>)</span>


<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>async</span> <span>def</span><span> </span><span>get_weather</span><span>(</span><span>city</span><span>:</span> <span>str</span> <span>=</span> <span>"London"</span><span>)</span> <span>-&gt;</span> <span>dict</span><span>[</span><span>str</span><span>,</span> <span>str</span><span>]:</span>
<span>    </span><span>"""Get weather data for a city"""</span>
    <span>return</span> <span>{</span>
        <span>"city"</span><span>:</span> <span>city</span><span>,</span>
        <span>"temperature"</span><span>:</span> <span>"22"</span><span>,</span>
        <span>"condition"</span><span>:</span> <span>"Partly cloudy"</span><span>,</span>
        <span>"humidity"</span><span>:</span> <span>"65%"</span><span>,</span>
    <span>}</span>


<span>if</span> <span>__name__</span> <span>==</span> <span>"__main__"</span><span>:</span>
    <span>mcp</span><span>.</span><span>run</span><span>(</span><span>transport</span><span>=</span><span>"streamable-http"</span><span>)</span>
```

_Full example: [examples/snippets/servers/oauth\_server.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/oauth_server.py)  
完整示例： [示例/片段/服务器/oauth\_server.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/oauth_server.py)_

For a complete example with separate Authorization Server and Resource Server implementations, see [`examples/servers/simple-auth/`](https://pypi.org/project/mcp/examples/servers/simple-auth/).  
关于完整示例，包含独立的授权服务器和资源服务器实现，请参见 [`examples/servers/simple-auth/`](https://pypi.org/project/mcp/examples/servers/simple-auth/)。

**Architecture:  建筑：**

-   **Authorization Server (AS)**: Handles OAuth flows, user authentication, and token issuance  
    **授权服务器（AS）：** 处理 OAuth 流、用户认证和令牌发放
-   **Resource Server (RS)**: Your MCP server that validates tokens and serves protected resources  
    **资源服务器（RS）：** 您的 MCP 服务器，用于验证令牌并服务受保护资源
-   **Client**: Discovers AS through RFC 9728, obtains tokens, and uses them with the MCP server  
    **客户端** ：通过 RFC 9728 发现 AS，获取令牌，并与 MCP 服务器一起使用

See [TokenVerifier](https://pypi.org/project/mcp/src/mcp/server/auth/provider.py) for more details on implementing token validation.  
有关实现代币验证的更多细节，请参见 [TokenVerifier](https://pypi.org/project/mcp/src/mcp/server/auth/provider.py)。

### FastMCP Properties  FastMCP 属性

The FastMCP server instance accessible via `ctx.fastmcp` provides access to server configuration and metadata:  
通过 `ctx.fastmcp` 访问的 FastMCP 服务器实例提供服务器配置和元数据访问：

-   `ctx.fastmcp.name` - The server's name as defined during initialization  
    `ctx.fastmcp.name` - 初始化时定义的服务器名称
-   `ctx.fastmcp.instructions` - Server instructions/description provided to clients  
    `ctx.fastmcp.instructions` - 服务器指令/描述提供给客户端
-   `ctx.fastmcp.website_url` - Optional website URL for the server  
    `ctx.fastmcp.website_url` - 服务器可选网站网址
-   `ctx.fastmcp.icons` - Optional list of icons for UI display  
    `ctx.fastmcp.icons` - 可选的 UI 显示图标列表
-   `ctx.fastmcp.settings` - Complete server configuration object containing:  
    `ctx.fastmcp.settings` - 完整的服务器配置对象，包含：
    -   `debug` - Debug mode flag  
        `调试` \- 调试模式标志
    -   `log_level` - Current logging level  
        `log_level` - 当前伐木水平
    -   `host` and `port` - Server network configuration  
        `主机`和`端口` \- 服务器网络配置
    -   `mount_path`, `sse_path`, `streamable_http_path` - Transport paths  
        `mount_path`、`sse_path`、`streamable_http_path`——运输路径
    -   `stateless_http` - Whether the server operates in stateless mode  
        `stateless_http` - 服务器是否处于无状态模式
    -   And other configuration options  
        以及其他配置选项

```
<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>server_info</span><span>(</span><span>ctx</span><span>:</span> <span>Context</span><span>)</span> <span>-&gt;</span> <span>dict</span><span>:</span>
<span>    </span><span>"""Get information about the current server."""</span>
    <span>return</span> <span>{</span>
        <span>"name"</span><span>:</span> <span>ctx</span><span>.</span><span>fastmcp</span><span>.</span><span>name</span><span>,</span>
        <span>"instructions"</span><span>:</span> <span>ctx</span><span>.</span><span>fastmcp</span><span>.</span><span>instructions</span><span>,</span>
        <span>"debug_mode"</span><span>:</span> <span>ctx</span><span>.</span><span>fastmcp</span><span>.</span><span>settings</span><span>.</span><span>debug</span><span>,</span>
        <span>"log_level"</span><span>:</span> <span>ctx</span><span>.</span><span>fastmcp</span><span>.</span><span>settings</span><span>.</span><span>log_level</span><span>,</span>
        <span>"host"</span><span>:</span> <span>ctx</span><span>.</span><span>fastmcp</span><span>.</span><span>settings</span><span>.</span><span>host</span><span>,</span>
        <span>"port"</span><span>:</span> <span>ctx</span><span>.</span><span>fastmcp</span><span>.</span><span>settings</span><span>.</span><span>port</span><span>,</span>
    <span>}</span>
```

### Session Properties and Methods  
会话属性与方法

The session object accessible via `ctx.session` provides advanced control over client communication:  
通过 `ctx.session` 访问的会话对象提供了对客户端通信的高级控制：

-   `ctx.session.client_params` - Client initialization parameters and declared capabilities  
    `ctx.session.client_params` - 客户端初始化参数和声明能力
-   `await ctx.session.send_log_message(level, data, logger)` - Send log messages with full control  
    `await ctx.session.send_log_message(level, data, logger)` - 发送完全控制的日志消息
-   `await ctx.session.create_message(messages, max_tokens)` - Request LLM sampling/completion  
    `await ctx.session.create_message(messages, max_tokens)` - 请求 LLM 采样/补全
-   `await ctx.session.send_progress_notification(token, progress, total, message)` - Direct progress updates  
    `await ctx.session.send_progress_notification(token, progress, total, message)` - 直接进展更新
-   `await ctx.session.send_resource_updated(uri)` - Notify clients that a specific resource changed  
    `await ctx.session.send_resource_updated(uri)` - 通知客户端特定资源发生变化
-   `await ctx.session.send_resource_list_changed()` - Notify clients that the resource list changed  
    `await ctx.session.send_resource_list_changed()` - 通知客户端资源列表发生变化
-   `await ctx.session.send_tool_list_changed()` - Notify clients that the tool list changed  
    `await ctx.session.send_tool_list_changed()` - 通知客户工具列表发生变化
-   `await ctx.session.send_prompt_list_changed()` - Notify clients that the prompt list changed  
    `await ctx.session.send_prompt_list_changed()` - 通知客户端提示列表发生变化

```
<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>async</span> <span>def</span><span> </span><span>notify_data_update</span><span>(</span><span>resource_uri</span><span>:</span> <span>str</span><span>,</span> <span>ctx</span><span>:</span> <span>Context</span><span>)</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Update data and notify clients of the change."""</span>
    <span># Perform data update logic here</span>
    
    <span># Notify clients that this specific resource changed</span>
    <span>await</span> <span>ctx</span><span>.</span><span>session</span><span>.</span><span>send_resource_updated</span><span>(</span><span>AnyUrl</span><span>(</span><span>resource_uri</span><span>))</span>
    
    <span># If this affects the overall resource list, notify about that too</span>
    <span>await</span> <span>ctx</span><span>.</span><span>session</span><span>.</span><span>send_resource_list_changed</span><span>()</span>
    
    <span>return</span> <span>f</span><span>"Updated </span><span>{</span><span>resource_uri</span><span>}</span><span> and notified clients"</span>
```

### Request Context Properties  
请求上下文属性

The request context accessible via `ctx.request_context` contains request-specific information and resources:  
通过 `ctx.request_context` 访问的请求上下文包含了针对请求的信息和资源：

-   `ctx.request_context.lifespan_context` - Access to resources initialized during server startup  
    `ctx.request_context.lifespan_context` - 访问服务器启动时初始化的资源
    -   Database connections, configuration objects, shared services  
        数据库连接、配置对象、共享服务
    -   Type-safe access to resources defined in your server's lifespan function  
        对服务器生命周期函数定义的资源的类型安全访问
-   `ctx.request_context.meta` - Request metadata from the client including:  
    `ctx.request_context.meta` - 向客户端请求包括：
    -   `progressToken` - Token for progress notifications  
        `progressToken` - 用于进度通知的 Token
    -   Other client-provided metadata  
        其他客户端提供的元数据
-   `ctx.request_context.request` - The original MCP request object for advanced processing  
    `ctx.request_context.request` - 最初用于高级处理的 MCP 请求对象
-   `ctx.request_context.request_id` - Unique identifier for this request  
    `ctx.request_context.request_id` - 该请求的唯一标识符

```
<span># Example with typed lifespan context</span>
<span>@dataclass</span>
<span>class</span><span> </span><span>AppContext</span><span>:</span>
    <span>db</span><span>:</span> <span>Database</span>
    <span>config</span><span>:</span> <span>AppConfig</span>

<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>query_with_config</span><span>(</span><span>query</span><span>:</span> <span>str</span><span>,</span> <span>ctx</span><span>:</span> <span>Context</span><span>)</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Execute a query using shared database and configuration."""</span>
    <span># Access typed lifespan context</span>
    <span>app_ctx</span><span>:</span> <span>AppContext</span> <span>=</span> <span>ctx</span><span>.</span><span>request_context</span><span>.</span><span>lifespan_context</span>
    
    <span># Use shared resources</span>
    <span>connection</span> <span>=</span> <span>app_ctx</span><span>.</span><span>db</span>
    <span>settings</span> <span>=</span> <span>app_ctx</span><span>.</span><span>config</span>
    
    <span># Execute query with configuration</span>
    <span>result</span> <span>=</span> <span>connection</span><span>.</span><span>execute</span><span>(</span><span>query</span><span>,</span> <span>timeout</span><span>=</span><span>settings</span><span>.</span><span>query_timeout</span><span>)</span>
    <span>return</span> <span>str</span><span>(</span><span>result</span><span>)</span>
```

_Full lifespan example: [examples/snippets/servers/lifespan\_example.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/lifespan_example.py)  
完整生命周期示例： [示例/片段/服务器/lifespan\_example.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/lifespan_example.py)_

## Running Your Server  运行你的服务器

### Development Mode  开发模式

The fastest way to test and debug your server is with the MCP Inspector:  
最快的测试和调试服务器方式是使用 MCP 检查器：

```
uv<span> </span>run<span> </span>mcp<span> </span>dev<span> </span>server.py

<span># Add dependencies</span>
uv<span> </span>run<span> </span>mcp<span> </span>dev<span> </span>server.py<span> </span>--with<span> </span>pandas<span> </span>--with<span> </span>numpy

<span># Mount local code</span>
uv<span> </span>run<span> </span>mcp<span> </span>dev<span> </span>server.py<span> </span>--with-editable<span> </span>.
```

### Claude Desktop Integration  
Claude 桌面集成

Once your server is ready, install it in Claude Desktop:  
服务器准备好后，安装在 Claude Desktop 中：

```
uv<span> </span>run<span> </span>mcp<span> </span>install<span> </span>server.py

<span># Custom name</span>
uv<span> </span>run<span> </span>mcp<span> </span>install<span> </span>server.py<span> </span>--name<span> </span><span>"My Analytics Server"</span>

<span># Environment variables</span>
uv<span> </span>run<span> </span>mcp<span> </span>install<span> </span>server.py<span> </span>-v<span> </span><span>API_KEY</span><span>=</span>abc123<span> </span>-v<span> </span><span>DB_URL</span><span>=</span>postgres://...
uv<span> </span>run<span> </span>mcp<span> </span>install<span> </span>server.py<span> </span>-f<span> </span>.env
```

### Direct Execution  直接执行

For advanced scenarios like custom deployments:  
对于高级场景，比如自定义部署：

```
<span>"""Example showing direct execution of an MCP server.</span>

<span>This is the simplest way to run an MCP server directly.</span>
<span>cd to the `examples/snippets` directory and run:</span>
<span>    uv run direct-execution-server</span>
<span>    or</span>
<span>    python servers/direct_execution.py</span>
<span>"""</span>

<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>FastMCP</span>

<span>mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>"My App"</span><span>)</span>


<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>hello</span><span>(</span><span>name</span><span>:</span> <span>str</span> <span>=</span> <span>"World"</span><span>)</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Say hello to someone."""</span>
    <span>return</span> <span>f</span><span>"Hello, </span><span>{</span><span>name</span><span>}</span><span>!"</span>


<span>def</span><span> </span><span>main</span><span>():</span>
<span>    </span><span>"""Entry point for the direct execution server."""</span>
    <span>mcp</span><span>.</span><span>run</span><span>()</span>


<span>if</span> <span>__name__</span> <span>==</span> <span>"__main__"</span><span>:</span>
    <span>main</span><span>()</span>
```

_Full example: [examples/snippets/servers/direct\_execution.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/direct_execution.py)  
完整示例： [示例/片段/服务器/direct\_execution.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/direct_execution.py)_

Run it with:  运行方式如下：

```
python<span> </span>servers/direct_execution.py
<span># or</span>
uv<span> </span>run<span> </span>mcp<span> </span>run<span> </span>servers/direct_execution.py
```

Note that `uv run mcp run` or `uv run mcp dev` only supports server using FastMCP and not the low-level server variant.  
注意，`uv run mcp run` 或 `uv run mcp 开发`只支持使用 FastMCP 的服务器，不支持 Lower Server 版本。

### Streamable HTTP Transport  
可流式 HTTP 传输

> **Note**: Streamable HTTP transport is the recommended transport for production deployments. Use `stateless_http=True` and `json_response=True` for optimal scalability.  
> **注意** ：可流式 HTTP 传输是生产部署的推荐传输方式。使用 `stateless_http=True` 和 `json_response=True` 以实现最佳的可扩展性。

```
<span>"""</span>
<span>Run from the repository root:</span>
<span>    uv run examples/snippets/servers/streamable_config.py</span>
<span>"""</span>

<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>FastMCP</span>

<span># Stateless server with JSON responses (recommended)</span>
<span>mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>"StatelessServer"</span><span>,</span> <span>stateless_http</span><span>=</span><span>True</span><span>,</span> <span>json_response</span><span>=</span><span>True</span><span>)</span>

<span># Other configuration options:</span>
<span># Stateless server with SSE streaming responses</span>
<span># mcp = FastMCP("StatelessServer", stateless_http=True)</span>

<span># Stateful server with session persistence</span>
<span># mcp = FastMCP("StatefulServer")</span>


<span># Add a simple tool to demonstrate the server</span>
<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>greet</span><span>(</span><span>name</span><span>:</span> <span>str</span> <span>=</span> <span>"World"</span><span>)</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Greet someone by name."""</span>
    <span>return</span> <span>f</span><span>"Hello, </span><span>{</span><span>name</span><span>}</span><span>!"</span>


<span># Run server with streamable_http transport</span>
<span>if</span> <span>__name__</span> <span>==</span> <span>"__main__"</span><span>:</span>
    <span>mcp</span><span>.</span><span>run</span><span>(</span><span>transport</span><span>=</span><span>"streamable-http"</span><span>)</span>
```

_Full example: [examples/snippets/servers/streamable\_config.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/streamable_config.py)  
完整示例： [示例/片段/服务器/streamable\_config.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/streamable_config.py)_

You can mount multiple FastMCP servers in a Starlette application:  
你可以在 Starlette 应用中挂载多个 FastMCP 服务器：

```
<span>"""</span>
<span>Run from the repository root:</span>
<span>    uvicorn examples.snippets.servers.streamable_starlette_mount:app --reload</span>
<span>"""</span>

<span>import</span><span> </span><span>contextlib</span>

<span>from</span><span> </span><span>starlette.applications</span><span> </span><span>import</span> <span>Starlette</span>
<span>from</span><span> </span><span>starlette.routing</span><span> </span><span>import</span> <span>Mount</span>

<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>FastMCP</span>

<span># Create the Echo server</span>
<span>echo_mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>name</span><span>=</span><span>"EchoServer"</span><span>,</span> <span>stateless_http</span><span>=</span><span>True</span><span>,</span> <span>json_response</span><span>=</span><span>True</span><span>)</span>


<span>@echo_mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>echo</span><span>(</span><span>message</span><span>:</span> <span>str</span><span>)</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""A simple echo tool"""</span>
    <span>return</span> <span>f</span><span>"Echo: </span><span>{</span><span>message</span><span>}</span><span>"</span>


<span># Create the Math server</span>
<span>math_mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>name</span><span>=</span><span>"MathServer"</span><span>,</span> <span>stateless_http</span><span>=</span><span>True</span><span>,</span> <span>json_response</span><span>=</span><span>True</span><span>)</span>


<span>@math_mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>add_two</span><span>(</span><span>n</span><span>:</span> <span>int</span><span>)</span> <span>-&gt;</span> <span>int</span><span>:</span>
<span>    </span><span>"""Tool to add two to the input"""</span>
    <span>return</span> <span>n</span> <span>+</span> <span>2</span>


<span># Create a combined lifespan to manage both session managers</span>
<span>@contextlib</span><span>.</span><span>asynccontextmanager</span>
<span>async</span> <span>def</span><span> </span><span>lifespan</span><span>(</span><span>app</span><span>:</span> <span>Starlette</span><span>):</span>
    <span>async</span> <span>with</span> <span>contextlib</span><span>.</span><span>AsyncExitStack</span><span>()</span> <span>as</span> <span>stack</span><span>:</span>
        <span>await</span> <span>stack</span><span>.</span><span>enter_async_context</span><span>(</span><span>echo_mcp</span><span>.</span><span>session_manager</span><span>.</span><span>run</span><span>())</span>
        <span>await</span> <span>stack</span><span>.</span><span>enter_async_context</span><span>(</span><span>math_mcp</span><span>.</span><span>session_manager</span><span>.</span><span>run</span><span>())</span>
        <span>yield</span>


<span># Create the Starlette app and mount the MCP servers</span>
<span>app</span> <span>=</span> <span>Starlette</span><span>(</span>
    <span>routes</span><span>=</span><span>[</span>
        <span>Mount</span><span>(</span><span>"/echo"</span><span>,</span> <span>echo_mcp</span><span>.</span><span>streamable_http_app</span><span>()),</span>
        <span>Mount</span><span>(</span><span>"/math"</span><span>,</span> <span>math_mcp</span><span>.</span><span>streamable_http_app</span><span>()),</span>
    <span>],</span>
    <span>lifespan</span><span>=</span><span>lifespan</span><span>,</span>
<span>)</span>

<span># Note: Clients connect to http://localhost:8000/echo/mcp and http://localhost:8000/math/mcp</span>
<span># To mount at the root of each path (e.g., /echo instead of /echo/mcp):</span>
<span># echo_mcp.settings.streamable_http_path = "/"</span>
<span># math_mcp.settings.streamable_http_path = "/"</span>
```

_Full example: [examples/snippets/servers/streamable\_starlette\_mount.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/streamable_starlette_mount.py)  
完整示例： [示例/片段/服务器/streamable\_starlette\_mount.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/streamable_starlette_mount.py)_

For low level server with Streamable HTTP implementations, see:  
关于带有可流式 HTTP 实现的低级服务器，请参见：

-   Stateful server: [`examples/servers/simple-streamablehttp/`](https://pypi.org/project/mcp/examples/servers/simple-streamablehttp/)  
    有状态服务器： [`examples/servers/simple-streamablehttp/`](https://pypi.org/project/mcp/examples/servers/simple-streamablehttp/)
-   Stateless server: [`examples/servers/simple-streamablehttp-stateless/`](https://pypi.org/project/mcp/examples/servers/simple-streamablehttp-stateless/)  
    无状态服务器： [`examples/servers/simple-streamablehttp-stateless/`](https://pypi.org/project/mcp/examples/servers/simple-streamablehttp-stateless/)

The streamable HTTP transport supports:  
可流式 HTTP 传输支持：

-   Stateful and stateless operation modes  
    有状态和无状态作模式
-   Resumability with event stores  
    活动商店的续集性
-   JSON or SSE response formats  
    JSON 或 SSE 响应格式
-   Better scalability for multi-node deployments  
    多节点部署的可扩展性提升

#### CORS Configuration for Browser-Based Clients  
浏览器客户端的 CORS 配置

If you'd like your server to be accessible by browser-based MCP clients, you'll need to configure CORS headers. The `Mcp-Session-Id` header must be exposed for browser clients to access it:  
如果你想让基于浏览器的 MCP 客户端访问服务器，你需要配置 CORS 头部。浏览器客户端必须公开 `Mcp-Session-Id` 头部：

```
<span>from</span><span> </span><span>starlette.applications</span><span> </span><span>import</span> <span>Starlette</span>
<span>from</span><span> </span><span>starlette.middleware.cors</span><span> </span><span>import</span> <span>CORSMiddleware</span>

<span># Create your Starlette app first</span>
<span>starlette_app</span> <span>=</span> <span>Starlette</span><span>(</span><span>routes</span><span>=</span><span>[</span><span>...</span><span>])</span>

<span># Then wrap it with CORS middleware</span>
<span>starlette_app</span> <span>=</span> <span>CORSMiddleware</span><span>(</span>
    <span>starlette_app</span><span>,</span>
    <span>allow_origins</span><span>=</span><span>[</span><span>"*"</span><span>],</span>  <span># Configure appropriately for production</span>
    <span>allow_methods</span><span>=</span><span>[</span><span>"GET"</span><span>,</span> <span>"POST"</span><span>,</span> <span>"DELETE"</span><span>],</span>  <span># MCP streamable HTTP methods</span>
    <span>expose_headers</span><span>=</span><span>[</span><span>"Mcp-Session-Id"</span><span>],</span>
<span>)</span>
```

This configuration is necessary because:  
这种配置是必要的，因为：

-   The MCP streamable HTTP transport uses the `Mcp-Session-Id` header for session management  
    MCP 可流式 HTTP 传输使用 `Mcp-Session-ID` 头进行会话管理
-   Browsers restrict access to response headers unless explicitly exposed via CORS  
    浏览器除非通过 CORS 明确暴露，否则限制对响应头的访问
-   Without this configuration, browser-based clients won't be able to read the session ID from initialization responses  
    如果没有这种配置，基于浏览器的客户端将无法读取初始化响应中的会话 ID

### Mounting to an Existing ASGI Server  
挂载到现有的 ASGI 服务器

By default, SSE servers are mounted at `/sse` and Streamable HTTP servers are mounted at `/mcp`. You can customize these paths using the methods described below.  
默认情况下，SSE 服务器挂载于 `/sse`，流式 HTTP 服务器挂载于 `/mcp`。您可以使用以下方法自定义这些路径。

For more information on mounting applications in Starlette, see the [Starlette documentation](https://www.starlette.io/routing/#submounting-routes).  
有关 Starlette 中安装应用的更多信息，请参见 [Starlette 文档](https://www.starlette.io/routing/#submounting-routes) 。

#### StreamableHTTP servers  可流式 HTTP 服务器

You can mount the StreamableHTTP server to an existing ASGI server using the `streamable_http_app` method. This allows you to integrate the StreamableHTTP server with other ASGI applications.  
你可以用 `streamable_http_app` 方法将 StreamableHTTP 服务器挂载到现有的 ASGI 服务器上。这允许你将 StreamableHTTP 服务器与其他 ASGI 应用集成。

##### Basic mounting  基本安装

```
<span>"""</span>
<span>Basic example showing how to mount StreamableHTTP server in Starlette.</span>

<span>Run from the repository root:</span>
<span>    uvicorn examples.snippets.servers.streamable_http_basic_mounting:app --reload</span>
<span>"""</span>

<span>import</span><span> </span><span>contextlib</span>

<span>from</span><span> </span><span>starlette.applications</span><span> </span><span>import</span> <span>Starlette</span>
<span>from</span><span> </span><span>starlette.routing</span><span> </span><span>import</span> <span>Mount</span>

<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>FastMCP</span>

<span># Create MCP server</span>
<span>mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>"My App"</span><span>,</span> <span>json_response</span><span>=</span><span>True</span><span>)</span>


<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>hello</span><span>()</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""A simple hello tool"""</span>
    <span>return</span> <span>"Hello from MCP!"</span>


<span># Create a lifespan context manager to run the session manager</span>
<span>@contextlib</span><span>.</span><span>asynccontextmanager</span>
<span>async</span> <span>def</span><span> </span><span>lifespan</span><span>(</span><span>app</span><span>:</span> <span>Starlette</span><span>):</span>
    <span>async</span> <span>with</span> <span>mcp</span><span>.</span><span>session_manager</span><span>.</span><span>run</span><span>():</span>
        <span>yield</span>


<span># Mount the StreamableHTTP server to the existing ASGI server</span>
<span>app</span> <span>=</span> <span>Starlette</span><span>(</span>
    <span>routes</span><span>=</span><span>[</span>
        <span>Mount</span><span>(</span><span>"/"</span><span>,</span> <span>app</span><span>=</span><span>mcp</span><span>.</span><span>streamable_http_app</span><span>()),</span>
    <span>],</span>
    <span>lifespan</span><span>=</span><span>lifespan</span><span>,</span>
<span>)</span>
```

_Full example: [examples/snippets/servers/streamable\_http\_basic\_mounting.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/streamable_http_basic_mounting.py)  
完整示例： [示例/片段/服务器/streamable\_http\_basic\_mounting.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/streamable_http_basic_mounting.py)_

##### Host-based routing  基于主机的路由

```
<span>"""</span>
<span>Example showing how to mount StreamableHTTP server using Host-based routing.</span>

<span>Run from the repository root:</span>
<span>    uvicorn examples.snippets.servers.streamable_http_host_mounting:app --reload</span>
<span>"""</span>

<span>import</span><span> </span><span>contextlib</span>

<span>from</span><span> </span><span>starlette.applications</span><span> </span><span>import</span> <span>Starlette</span>
<span>from</span><span> </span><span>starlette.routing</span><span> </span><span>import</span> <span>Host</span>

<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>FastMCP</span>

<span># Create MCP server</span>
<span>mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>"MCP Host App"</span><span>,</span> <span>json_response</span><span>=</span><span>True</span><span>)</span>


<span>@mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>domain_info</span><span>()</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Get domain-specific information"""</span>
    <span>return</span> <span>"This is served from mcp.acme.corp"</span>


<span># Create a lifespan context manager to run the session manager</span>
<span>@contextlib</span><span>.</span><span>asynccontextmanager</span>
<span>async</span> <span>def</span><span> </span><span>lifespan</span><span>(</span><span>app</span><span>:</span> <span>Starlette</span><span>):</span>
    <span>async</span> <span>with</span> <span>mcp</span><span>.</span><span>session_manager</span><span>.</span><span>run</span><span>():</span>
        <span>yield</span>


<span># Mount using Host-based routing</span>
<span>app</span> <span>=</span> <span>Starlette</span><span>(</span>
    <span>routes</span><span>=</span><span>[</span>
        <span>Host</span><span>(</span><span>"mcp.acme.corp"</span><span>,</span> <span>app</span><span>=</span><span>mcp</span><span>.</span><span>streamable_http_app</span><span>()),</span>
    <span>],</span>
    <span>lifespan</span><span>=</span><span>lifespan</span><span>,</span>
<span>)</span>
```

_Full example: [examples/snippets/servers/streamable\_http\_host\_mounting.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/streamable_http_host_mounting.py)  
完整示例： [示例/摘要/服务器/数据 streamable\_http\_host\_mounting.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/streamable_http_host_mounting.py)_

##### Multiple servers with path configuration  
多台服务器与路径配置

```
<span>"""</span>
<span>Example showing how to mount multiple StreamableHTTP servers with path configuration.</span>

<span>Run from the repository root:</span>
<span>    uvicorn examples.snippets.servers.streamable_http_multiple_servers:app --reload</span>
<span>"""</span>

<span>import</span><span> </span><span>contextlib</span>

<span>from</span><span> </span><span>starlette.applications</span><span> </span><span>import</span> <span>Starlette</span>
<span>from</span><span> </span><span>starlette.routing</span><span> </span><span>import</span> <span>Mount</span>

<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>FastMCP</span>

<span># Create multiple MCP servers</span>
<span>api_mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>"API Server"</span><span>,</span> <span>json_response</span><span>=</span><span>True</span><span>)</span>
<span>chat_mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>"Chat Server"</span><span>,</span> <span>json_response</span><span>=</span><span>True</span><span>)</span>


<span>@api_mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>api_status</span><span>()</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Get API status"""</span>
    <span>return</span> <span>"API is running"</span>


<span>@chat_mcp</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>send_message</span><span>(</span><span>message</span><span>:</span> <span>str</span><span>)</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Send a chat message"""</span>
    <span>return</span> <span>f</span><span>"Message sent: </span><span>{</span><span>message</span><span>}</span><span>"</span>


<span># Configure servers to mount at the root of each path</span>
<span># This means endpoints will be at /api and /chat instead of /api/mcp and /chat/mcp</span>
<span>api_mcp</span><span>.</span><span>settings</span><span>.</span><span>streamable_http_path</span> <span>=</span> <span>"/"</span>
<span>chat_mcp</span><span>.</span><span>settings</span><span>.</span><span>streamable_http_path</span> <span>=</span> <span>"/"</span>


<span># Create a combined lifespan to manage both session managers</span>
<span>@contextlib</span><span>.</span><span>asynccontextmanager</span>
<span>async</span> <span>def</span><span> </span><span>lifespan</span><span>(</span><span>app</span><span>:</span> <span>Starlette</span><span>):</span>
    <span>async</span> <span>with</span> <span>contextlib</span><span>.</span><span>AsyncExitStack</span><span>()</span> <span>as</span> <span>stack</span><span>:</span>
        <span>await</span> <span>stack</span><span>.</span><span>enter_async_context</span><span>(</span><span>api_mcp</span><span>.</span><span>session_manager</span><span>.</span><span>run</span><span>())</span>
        <span>await</span> <span>stack</span><span>.</span><span>enter_async_context</span><span>(</span><span>chat_mcp</span><span>.</span><span>session_manager</span><span>.</span><span>run</span><span>())</span>
        <span>yield</span>


<span># Mount the servers</span>
<span>app</span> <span>=</span> <span>Starlette</span><span>(</span>
    <span>routes</span><span>=</span><span>[</span>
        <span>Mount</span><span>(</span><span>"/api"</span><span>,</span> <span>app</span><span>=</span><span>api_mcp</span><span>.</span><span>streamable_http_app</span><span>()),</span>
        <span>Mount</span><span>(</span><span>"/chat"</span><span>,</span> <span>app</span><span>=</span><span>chat_mcp</span><span>.</span><span>streamable_http_app</span><span>()),</span>
    <span>],</span>
    <span>lifespan</span><span>=</span><span>lifespan</span><span>,</span>
<span>)</span>
```

_Full example: [examples/snippets/servers/streamable\_http\_multiple\_servers.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/streamable_http_multiple_servers.py)  
完整示例： [示例/片段/服务器/streamable\_http\_multiple\_servers.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/streamable_http_multiple_servers.py)_

##### Path configuration at initialization  
初始化时的路径配置

```
<span>"""</span>
<span>Example showing path configuration during FastMCP initialization.</span>

<span>Run from the repository root:</span>
<span>    uvicorn examples.snippets.servers.streamable_http_path_config:app --reload</span>
<span>"""</span>

<span>from</span><span> </span><span>starlette.applications</span><span> </span><span>import</span> <span>Starlette</span>
<span>from</span><span> </span><span>starlette.routing</span><span> </span><span>import</span> <span>Mount</span>

<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>FastMCP</span>

<span># Configure streamable_http_path during initialization</span>
<span># This server will mount at the root of wherever it's mounted</span>
<span>mcp_at_root</span> <span>=</span> <span>FastMCP</span><span>(</span>
    <span>"My Server"</span><span>,</span>
    <span>json_response</span><span>=</span><span>True</span><span>,</span>
    <span>streamable_http_path</span><span>=</span><span>"/"</span><span>,</span>
<span>)</span>


<span>@mcp_at_root</span><span>.</span><span>tool</span><span>()</span>
<span>def</span><span> </span><span>process_data</span><span>(</span><span>data</span><span>:</span> <span>str</span><span>)</span> <span>-&gt;</span> <span>str</span><span>:</span>
<span>    </span><span>"""Process some data"""</span>
    <span>return</span> <span>f</span><span>"Processed: </span><span>{</span><span>data</span><span>}</span><span>"</span>


<span># Mount at /process - endpoints will be at /process instead of /process/mcp</span>
<span>app</span> <span>=</span> <span>Starlette</span><span>(</span>
    <span>routes</span><span>=</span><span>[</span>
        <span>Mount</span><span>(</span><span>"/process"</span><span>,</span> <span>app</span><span>=</span><span>mcp_at_root</span><span>.</span><span>streamable_http_app</span><span>()),</span>
    <span>]</span>
<span>)</span>
```

_Full example: [examples/snippets/servers/streamable\_http\_path\_config.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/streamable_http_path_config.py)  
完整示例： [示例/片段/服务器/streamable\_http\_path\_config.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/streamable_http_path_config.py)_

#### SSE servers  SSE 服务器

> **Note**: SSE transport is being superseded by [Streamable HTTP transport](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http).  
> **注意** ：SSE 传输正在被[可流式 HTTP 传输](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http)所取代。

You can mount the SSE server to an existing ASGI server using the `sse_app` method. This allows you to integrate the SSE server with other ASGI applications.  
你可以用 `sse_app` 方法将 SSE 服务器挂载到现有的 ASGI 服务器上。这允许你将 SSE 服务器与其他 ASGI 应用集成。

```
<span>from</span><span> </span><span>starlette.applications</span><span> </span><span>import</span> <span>Starlette</span>
<span>from</span><span> </span><span>starlette.routing</span><span> </span><span>import</span> <span>Mount</span><span>,</span> <span>Host</span>
<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>FastMCP</span>


<span>mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>"My App"</span><span>)</span>

<span># Mount the SSE server to the existing ASGI server</span>
<span>app</span> <span>=</span> <span>Starlette</span><span>(</span>
    <span>routes</span><span>=</span><span>[</span>
        <span>Mount</span><span>(</span><span>'/'</span><span>,</span> <span>app</span><span>=</span><span>mcp</span><span>.</span><span>sse_app</span><span>()),</span>
    <span>]</span>
<span>)</span>

<span># or dynamically mount as host</span>
<span>app</span><span>.</span><span>router</span><span>.</span><span>routes</span><span>.</span><span>append</span><span>(</span><span>Host</span><span>(</span><span>'mcp.acme.corp'</span><span>,</span> <span>app</span><span>=</span><span>mcp</span><span>.</span><span>sse_app</span><span>()))</span>
```

When mounting multiple MCP servers under different paths, you can configure the mount path in several ways:  
当将多个 MCP 服务器挂载在不同路径下时，你可以以多种方式配置挂载路径：

```
<span>from</span><span> </span><span>starlette.applications</span><span> </span><span>import</span> <span>Starlette</span>
<span>from</span><span> </span><span>starlette.routing</span><span> </span><span>import</span> <span>Mount</span>
<span>from</span><span> </span><span>mcp.server.fastmcp</span><span> </span><span>import</span> <span>FastMCP</span>

<span># Create multiple MCP servers</span>
<span>github_mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>"GitHub API"</span><span>)</span>
<span>browser_mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>"Browser"</span><span>)</span>
<span>curl_mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>"Curl"</span><span>)</span>
<span>search_mcp</span> <span>=</span> <span>FastMCP</span><span>(</span><span>"Search"</span><span>)</span>

<span># Method 1: Configure mount paths via settings (recommended for persistent configuration)</span>
<span>github_mcp</span><span>.</span><span>settings</span><span>.</span><span>mount_path</span> <span>=</span> <span>"/github"</span>
<span>browser_mcp</span><span>.</span><span>settings</span><span>.</span><span>mount_path</span> <span>=</span> <span>"/browser"</span>

<span># Method 2: Pass mount path directly to sse_app (preferred for ad-hoc mounting)</span>
<span># This approach doesn't modify the server's settings permanently</span>

<span># Create Starlette app with multiple mounted servers</span>
<span>app</span> <span>=</span> <span>Starlette</span><span>(</span>
    <span>routes</span><span>=</span><span>[</span>
        <span># Using settings-based configuration</span>
        <span>Mount</span><span>(</span><span>"/github"</span><span>,</span> <span>app</span><span>=</span><span>github_mcp</span><span>.</span><span>sse_app</span><span>()),</span>
        <span>Mount</span><span>(</span><span>"/browser"</span><span>,</span> <span>app</span><span>=</span><span>browser_mcp</span><span>.</span><span>sse_app</span><span>()),</span>
        <span># Using direct mount path parameter</span>
        <span>Mount</span><span>(</span><span>"/curl"</span><span>,</span> <span>app</span><span>=</span><span>curl_mcp</span><span>.</span><span>sse_app</span><span>(</span><span>"/curl"</span><span>)),</span>
        <span>Mount</span><span>(</span><span>"/search"</span><span>,</span> <span>app</span><span>=</span><span>search_mcp</span><span>.</span><span>sse_app</span><span>(</span><span>"/search"</span><span>)),</span>
    <span>]</span>
<span>)</span>

<span># Method 3: For direct execution, you can also pass the mount path to run()</span>
<span>if</span> <span>__name__</span> <span>==</span> <span>"__main__"</span><span>:</span>
    <span>search_mcp</span><span>.</span><span>run</span><span>(</span><span>transport</span><span>=</span><span>"sse"</span><span>,</span> <span>mount_path</span><span>=</span><span>"/search"</span><span>)</span>
```

For more information on mounting applications in Starlette, see the [Starlette documentation](https://www.starlette.io/routing/#submounting-routes).  
有关 Starlette 中安装应用的更多信息，请参见 [Starlette 文档](https://www.starlette.io/routing/#submounting-routes) 。

## Advanced Usage  高级用法

### Low-Level Server  低级服务器

For more control, you can use the low-level server implementation directly. This gives you full access to the protocol and allows you to customize every aspect of your server, including lifecycle management through the lifespan API:  
为了更好地控制，你可以直接使用低层服务器实现。这让你能够完全访问协议，并允许你通过生命周期 API 定制服务器的各个方面，包括生命周期管理：

```
<span>"""</span>
<span>Run from the repository root:</span>
<span>    uv run examples/snippets/servers/lowlevel/lifespan.py</span>
<span>"""</span>

<span>from</span><span> </span><span>collections.abc</span><span> </span><span>import</span> <span>AsyncIterator</span>
<span>from</span><span> </span><span>contextlib</span><span> </span><span>import</span> <span>asynccontextmanager</span>
<span>from</span><span> </span><span>typing</span><span> </span><span>import</span> <span>Any</span>

<span>import</span><span> </span><span>mcp.server.stdio</span>
<span>import</span><span> </span><span>mcp.types</span><span> </span><span>as</span><span> </span><span>types</span>
<span>from</span><span> </span><span>mcp.server.lowlevel</span><span> </span><span>import</span> <span>NotificationOptions</span><span>,</span> <span>Server</span>
<span>from</span><span> </span><span>mcp.server.models</span><span> </span><span>import</span> <span>InitializationOptions</span>


<span># Mock database class for example</span>
<span>class</span><span> </span><span>Database</span><span>:</span>
<span>    </span><span>"""Mock database class for example."""</span>

    <span>@classmethod</span>
    <span>async</span> <span>def</span><span> </span><span>connect</span><span>(</span><span>cls</span><span>)</span> <span>-&gt;</span> <span>"Database"</span><span>:</span>
<span>        </span><span>"""Connect to database."""</span>
        <span>print</span><span>(</span><span>"Database connected"</span><span>)</span>
        <span>return</span> <span>cls</span><span>()</span>

    <span>async</span> <span>def</span><span> </span><span>disconnect</span><span>(</span><span>self</span><span>)</span> <span>-&gt;</span> <span>None</span><span>:</span>
<span>        </span><span>"""Disconnect from database."""</span>
        <span>print</span><span>(</span><span>"Database disconnected"</span><span>)</span>

    <span>async</span> <span>def</span><span> </span><span>query</span><span>(</span><span>self</span><span>,</span> <span>query_str</span><span>:</span> <span>str</span><span>)</span> <span>-&gt;</span> <span>list</span><span>[</span><span>dict</span><span>[</span><span>str</span><span>,</span> <span>str</span><span>]]:</span>
<span>        </span><span>"""Execute a query."""</span>
        <span># Simulate database query</span>
        <span>return</span> <span>[{</span><span>"id"</span><span>:</span> <span>"1"</span><span>,</span> <span>"name"</span><span>:</span> <span>"Example"</span><span>,</span> <span>"query"</span><span>:</span> <span>query_str</span><span>}]</span>


<span>@asynccontextmanager</span>
<span>async</span> <span>def</span><span> </span><span>server_lifespan</span><span>(</span><span>_server</span><span>:</span> <span>Server</span><span>)</span> <span>-&gt;</span> <span>AsyncIterator</span><span>[</span><span>dict</span><span>[</span><span>str</span><span>,</span> <span>Any</span><span>]]:</span>
<span>    </span><span>"""Manage server startup and shutdown lifecycle."""</span>
    <span># Initialize resources on startup</span>
    <span>db</span> <span>=</span> <span>await</span> <span>Database</span><span>.</span><span>connect</span><span>()</span>
    <span>try</span><span>:</span>
        <span>yield</span> <span>{</span><span>"db"</span><span>:</span> <span>db</span><span>}</span>
    <span>finally</span><span>:</span>
        <span># Clean up on shutdown</span>
        <span>await</span> <span>db</span><span>.</span><span>disconnect</span><span>()</span>


<span># Pass lifespan to server</span>
<span>server</span> <span>=</span> <span>Server</span><span>(</span><span>"example-server"</span><span>,</span> <span>lifespan</span><span>=</span><span>server_lifespan</span><span>)</span>


<span>@server</span><span>.</span><span>list_tools</span><span>()</span>
<span>async</span> <span>def</span><span> </span><span>handle_list_tools</span><span>()</span> <span>-&gt;</span> <span>list</span><span>[</span><span>types</span><span>.</span><span>Tool</span><span>]:</span>
<span>    </span><span>"""List available tools."""</span>
    <span>return</span> <span>[</span>
        <span>types</span><span>.</span><span>Tool</span><span>(</span>
            <span>name</span><span>=</span><span>"query_db"</span><span>,</span>
            <span>description</span><span>=</span><span>"Query the database"</span><span>,</span>
            <span>inputSchema</span><span>=</span><span>{</span>
                <span>"type"</span><span>:</span> <span>"object"</span><span>,</span>
                <span>"properties"</span><span>:</span> <span>{</span><span>"query"</span><span>:</span> <span>{</span><span>"type"</span><span>:</span> <span>"string"</span><span>,</span> <span>"description"</span><span>:</span> <span>"SQL query to execute"</span><span>}},</span>
                <span>"required"</span><span>:</span> <span>[</span><span>"query"</span><span>],</span>
            <span>},</span>
        <span>)</span>
    <span>]</span>


<span>@server</span><span>.</span><span>call_tool</span><span>()</span>
<span>async</span> <span>def</span><span> </span><span>query_db</span><span>(</span><span>name</span><span>:</span> <span>str</span><span>,</span> <span>arguments</span><span>:</span> <span>dict</span><span>[</span><span>str</span><span>,</span> <span>Any</span><span>])</span> <span>-&gt;</span> <span>list</span><span>[</span><span>types</span><span>.</span><span>TextContent</span><span>]:</span>
<span>    </span><span>"""Handle database query tool call."""</span>
    <span>if</span> <span>name</span> <span>!=</span> <span>"query_db"</span><span>:</span>
        <span>raise</span> <span>ValueError</span><span>(</span><span>f</span><span>"Unknown tool: </span><span>{</span><span>name</span><span>}</span><span>"</span><span>)</span>

    <span># Access lifespan context</span>
    <span>ctx</span> <span>=</span> <span>server</span><span>.</span><span>request_context</span>
    <span>db</span> <span>=</span> <span>ctx</span><span>.</span><span>lifespan_context</span><span>[</span><span>"db"</span><span>]</span>

    <span># Execute query</span>
    <span>results</span> <span>=</span> <span>await</span> <span>db</span><span>.</span><span>query</span><span>(</span><span>arguments</span><span>[</span><span>"query"</span><span>])</span>

    <span>return</span> <span>[</span><span>types</span><span>.</span><span>TextContent</span><span>(</span><span>type</span><span>=</span><span>"text"</span><span>,</span> <span>text</span><span>=</span><span>f</span><span>"Query results: </span><span>{</span><span>results</span><span>}</span><span>"</span><span>)]</span>


<span>async</span> <span>def</span><span> </span><span>run</span><span>():</span>
<span>    </span><span>"""Run the server with lifespan management."""</span>
    <span>async</span> <span>with</span> <span>mcp</span><span>.</span><span>server</span><span>.</span><span>stdio</span><span>.</span><span>stdio_server</span><span>()</span> <span>as</span> <span>(</span><span>read_stream</span><span>,</span> <span>write_stream</span><span>):</span>
        <span>await</span> <span>server</span><span>.</span><span>run</span><span>(</span>
            <span>read_stream</span><span>,</span>
            <span>write_stream</span><span>,</span>
            <span>InitializationOptions</span><span>(</span>
                <span>server_name</span><span>=</span><span>"example-server"</span><span>,</span>
                <span>server_version</span><span>=</span><span>"0.1.0"</span><span>,</span>
                <span>capabilities</span><span>=</span><span>server</span><span>.</span><span>get_capabilities</span><span>(</span>
                    <span>notification_options</span><span>=</span><span>NotificationOptions</span><span>(),</span>
                    <span>experimental_capabilities</span><span>=</span><span>{},</span>
                <span>),</span>
            <span>),</span>
        <span>)</span>


<span>if</span> <span>__name__</span> <span>==</span> <span>"__main__"</span><span>:</span>
    <span>import</span><span> </span><span>asyncio</span>

    <span>asyncio</span><span>.</span><span>run</span><span>(</span><span>run</span><span>())</span>
```

_Full example: [examples/snippets/servers/lowlevel/lifespan.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/lowlevel/lifespan.py)  
完整示例： [示例/片段/服务器/低级/大 lifespan.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/lowlevel/lifespan.py)_

The lifespan API provides:  
生命周期 API 提供：

-   A way to initialize resources when the server starts and clean them up when it stops  
    一种在服务器启动时初始化资源，停止时清理资源的方法
-   Access to initialized resources through the request context in handlers  
    通过处理器中的请求上下文访问初始化资源
-   Type-safe context passing between lifespan and request handlers  
    类型安全上下文在生命周期和请求处理程序之间传递

```
<span>"""</span>
<span>Run from the repository root:</span>
<span>uv run examples/snippets/servers/lowlevel/basic.py</span>
<span>"""</span>

<span>import</span><span> </span><span>asyncio</span>

<span>import</span><span> </span><span>mcp.server.stdio</span>
<span>import</span><span> </span><span>mcp.types</span><span> </span><span>as</span><span> </span><span>types</span>
<span>from</span><span> </span><span>mcp.server.lowlevel</span><span> </span><span>import</span> <span>NotificationOptions</span><span>,</span> <span>Server</span>
<span>from</span><span> </span><span>mcp.server.models</span><span> </span><span>import</span> <span>InitializationOptions</span>

<span># Create a server instance</span>
<span>server</span> <span>=</span> <span>Server</span><span>(</span><span>"example-server"</span><span>)</span>


<span>@server</span><span>.</span><span>list_prompts</span><span>()</span>
<span>async</span> <span>def</span><span> </span><span>handle_list_prompts</span><span>()</span> <span>-&gt;</span> <span>list</span><span>[</span><span>types</span><span>.</span><span>Prompt</span><span>]:</span>
<span>    </span><span>"""List available prompts."""</span>
    <span>return</span> <span>[</span>
        <span>types</span><span>.</span><span>Prompt</span><span>(</span>
            <span>name</span><span>=</span><span>"example-prompt"</span><span>,</span>
            <span>description</span><span>=</span><span>"An example prompt template"</span><span>,</span>
            <span>arguments</span><span>=</span><span>[</span><span>types</span><span>.</span><span>PromptArgument</span><span>(</span><span>name</span><span>=</span><span>"arg1"</span><span>,</span> <span>description</span><span>=</span><span>"Example argument"</span><span>,</span> <span>required</span><span>=</span><span>True</span><span>)],</span>
        <span>)</span>
    <span>]</span>


<span>@server</span><span>.</span><span>get_prompt</span><span>()</span>
<span>async</span> <span>def</span><span> </span><span>handle_get_prompt</span><span>(</span><span>name</span><span>:</span> <span>str</span><span>,</span> <span>arguments</span><span>:</span> <span>dict</span><span>[</span><span>str</span><span>,</span> <span>str</span><span>]</span> <span>|</span> <span>None</span><span>)</span> <span>-&gt;</span> <span>types</span><span>.</span><span>GetPromptResult</span><span>:</span>
<span>    </span><span>"""Get a specific prompt by name."""</span>
    <span>if</span> <span>name</span> <span>!=</span> <span>"example-prompt"</span><span>:</span>
        <span>raise</span> <span>ValueError</span><span>(</span><span>f</span><span>"Unknown prompt: </span><span>{</span><span>name</span><span>}</span><span>"</span><span>)</span>

    <span>arg1_value</span> <span>=</span> <span>(</span><span>arguments</span> <span>or</span> <span>{})</span><span>.</span><span>get</span><span>(</span><span>"arg1"</span><span>,</span> <span>"default"</span><span>)</span>

    <span>return</span> <span>types</span><span>.</span><span>GetPromptResult</span><span>(</span>
        <span>description</span><span>=</span><span>"Example prompt"</span><span>,</span>
        <span>messages</span><span>=</span><span>[</span>
            <span>types</span><span>.</span><span>PromptMessage</span><span>(</span>
                <span>role</span><span>=</span><span>"user"</span><span>,</span>
                <span>content</span><span>=</span><span>types</span><span>.</span><span>TextContent</span><span>(</span><span>type</span><span>=</span><span>"text"</span><span>,</span> <span>text</span><span>=</span><span>f</span><span>"Example prompt text with argument: </span><span>{</span><span>arg1_value</span><span>}</span><span>"</span><span>),</span>
            <span>)</span>
        <span>],</span>
    <span>)</span>


<span>async</span> <span>def</span><span> </span><span>run</span><span>():</span>
<span>    </span><span>"""Run the basic low-level server."""</span>
    <span>async</span> <span>with</span> <span>mcp</span><span>.</span><span>server</span><span>.</span><span>stdio</span><span>.</span><span>stdio_server</span><span>()</span> <span>as</span> <span>(</span><span>read_stream</span><span>,</span> <span>write_stream</span><span>):</span>
        <span>await</span> <span>server</span><span>.</span><span>run</span><span>(</span>
            <span>read_stream</span><span>,</span>
            <span>write_stream</span><span>,</span>
            <span>InitializationOptions</span><span>(</span>
                <span>server_name</span><span>=</span><span>"example"</span><span>,</span>
                <span>server_version</span><span>=</span><span>"0.1.0"</span><span>,</span>
                <span>capabilities</span><span>=</span><span>server</span><span>.</span><span>get_capabilities</span><span>(</span>
                    <span>notification_options</span><span>=</span><span>NotificationOptions</span><span>(),</span>
                    <span>experimental_capabilities</span><span>=</span><span>{},</span>
                <span>),</span>
            <span>),</span>
        <span>)</span>


<span>if</span> <span>__name__</span> <span>==</span> <span>"__main__"</span><span>:</span>
    <span>asyncio</span><span>.</span><span>run</span><span>(</span><span>run</span><span>())</span>
```

_Full example: [examples/snippets/servers/lowlevel/basic.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/lowlevel/basic.py)  
完整示例： [示例/片段/服务器/低级/basic.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/lowlevel/basic.py)_

Caution: The `uv run mcp run` and `uv run mcp dev` tool doesn't support low-level server.  
注意：`uv 运行 MCP 运行`和 `uv 运行 MCP 开发`工具不支持低级别服务器。

#### Structured Output Support  
结构化输出支持

The low-level server supports structured output for tools, allowing you to return both human-readable content and machine-readable structured data. Tools can define an `outputSchema` to validate their structured output:  
底层服务器支持工具的结构化输出，允许你返回人类可读内容和机器可读的结构化数据。工具可以定义输出`模式`来验证其结构化输出：

```
<span>"""</span>
<span>Run from the repository root:</span>
<span>    uv run examples/snippets/servers/lowlevel/structured_output.py</span>
<span>"""</span>

<span>import</span><span> </span><span>asyncio</span>
<span>from</span><span> </span><span>typing</span><span> </span><span>import</span> <span>Any</span>

<span>import</span><span> </span><span>mcp.server.stdio</span>
<span>import</span><span> </span><span>mcp.types</span><span> </span><span>as</span><span> </span><span>types</span>
<span>from</span><span> </span><span>mcp.server.lowlevel</span><span> </span><span>import</span> <span>NotificationOptions</span><span>,</span> <span>Server</span>
<span>from</span><span> </span><span>mcp.server.models</span><span> </span><span>import</span> <span>InitializationOptions</span>

<span>server</span> <span>=</span> <span>Server</span><span>(</span><span>"example-server"</span><span>)</span>


<span>@server</span><span>.</span><span>list_tools</span><span>()</span>
<span>async</span> <span>def</span><span> </span><span>list_tools</span><span>()</span> <span>-&gt;</span> <span>list</span><span>[</span><span>types</span><span>.</span><span>Tool</span><span>]:</span>
<span>    </span><span>"""List available tools with structured output schemas."""</span>
    <span>return</span> <span>[</span>
        <span>types</span><span>.</span><span>Tool</span><span>(</span>
            <span>name</span><span>=</span><span>"get_weather"</span><span>,</span>
            <span>description</span><span>=</span><span>"Get current weather for a city"</span><span>,</span>
            <span>inputSchema</span><span>=</span><span>{</span>
                <span>"type"</span><span>:</span> <span>"object"</span><span>,</span>
                <span>"properties"</span><span>:</span> <span>{</span><span>"city"</span><span>:</span> <span>{</span><span>"type"</span><span>:</span> <span>"string"</span><span>,</span> <span>"description"</span><span>:</span> <span>"City name"</span><span>}},</span>
                <span>"required"</span><span>:</span> <span>[</span><span>"city"</span><span>],</span>
            <span>},</span>
            <span>outputSchema</span><span>=</span><span>{</span>
                <span>"type"</span><span>:</span> <span>"object"</span><span>,</span>
                <span>"properties"</span><span>:</span> <span>{</span>
                    <span>"temperature"</span><span>:</span> <span>{</span><span>"type"</span><span>:</span> <span>"number"</span><span>,</span> <span>"description"</span><span>:</span> <span>"Temperature in Celsius"</span><span>},</span>
                    <span>"condition"</span><span>:</span> <span>{</span><span>"type"</span><span>:</span> <span>"string"</span><span>,</span> <span>"description"</span><span>:</span> <span>"Weather condition"</span><span>},</span>
                    <span>"humidity"</span><span>:</span> <span>{</span><span>"type"</span><span>:</span> <span>"number"</span><span>,</span> <span>"description"</span><span>:</span> <span>"Humidity percentage"</span><span>},</span>
                    <span>"city"</span><span>:</span> <span>{</span><span>"type"</span><span>:</span> <span>"string"</span><span>,</span> <span>"description"</span><span>:</span> <span>"City name"</span><span>},</span>
                <span>},</span>
                <span>"required"</span><span>:</span> <span>[</span><span>"temperature"</span><span>,</span> <span>"condition"</span><span>,</span> <span>"humidity"</span><span>,</span> <span>"city"</span><span>],</span>
            <span>},</span>
        <span>)</span>
    <span>]</span>


<span>@server</span><span>.</span><span>call_tool</span><span>()</span>
<span>async</span> <span>def</span><span> </span><span>call_tool</span><span>(</span><span>name</span><span>:</span> <span>str</span><span>,</span> <span>arguments</span><span>:</span> <span>dict</span><span>[</span><span>str</span><span>,</span> <span>Any</span><span>])</span> <span>-&gt;</span> <span>dict</span><span>[</span><span>str</span><span>,</span> <span>Any</span><span>]:</span>
<span>    </span><span>"""Handle tool calls with structured output."""</span>
    <span>if</span> <span>name</span> <span>==</span> <span>"get_weather"</span><span>:</span>
        <span>city</span> <span>=</span> <span>arguments</span><span>[</span><span>"city"</span><span>]</span>

        <span># Simulated weather data - in production, call a weather API</span>
        <span>weather_data</span> <span>=</span> <span>{</span>
            <span>"temperature"</span><span>:</span> <span>22.5</span><span>,</span>
            <span>"condition"</span><span>:</span> <span>"partly cloudy"</span><span>,</span>
            <span>"humidity"</span><span>:</span> <span>65</span><span>,</span>
            <span>"city"</span><span>:</span> <span>city</span><span>,</span>  <span># Include the requested city</span>
        <span>}</span>

        <span># low-level server will validate structured output against the tool's</span>
        <span># output schema, and additionally serialize it into a TextContent block</span>
        <span># for backwards compatibility with pre-2025-06-18 clients.</span>
        <span>return</span> <span>weather_data</span>
    <span>else</span><span>:</span>
        <span>raise</span> <span>ValueError</span><span>(</span><span>f</span><span>"Unknown tool: </span><span>{</span><span>name</span><span>}</span><span>"</span><span>)</span>


<span>async</span> <span>def</span><span> </span><span>run</span><span>():</span>
<span>    </span><span>"""Run the structured output server."""</span>
    <span>async</span> <span>with</span> <span>mcp</span><span>.</span><span>server</span><span>.</span><span>stdio</span><span>.</span><span>stdio_server</span><span>()</span> <span>as</span> <span>(</span><span>read_stream</span><span>,</span> <span>write_stream</span><span>):</span>
        <span>await</span> <span>server</span><span>.</span><span>run</span><span>(</span>
            <span>read_stream</span><span>,</span>
            <span>write_stream</span><span>,</span>
            <span>InitializationOptions</span><span>(</span>
                <span>server_name</span><span>=</span><span>"structured-output-example"</span><span>,</span>
                <span>server_version</span><span>=</span><span>"0.1.0"</span><span>,</span>
                <span>capabilities</span><span>=</span><span>server</span><span>.</span><span>get_capabilities</span><span>(</span>
                    <span>notification_options</span><span>=</span><span>NotificationOptions</span><span>(),</span>
                    <span>experimental_capabilities</span><span>=</span><span>{},</span>
                <span>),</span>
            <span>),</span>
        <span>)</span>


<span>if</span> <span>__name__</span> <span>==</span> <span>"__main__"</span><span>:</span>
    <span>asyncio</span><span>.</span><span>run</span><span>(</span><span>run</span><span>())</span>
```

_Full example: [examples/snippets/servers/lowlevel/structured\_output.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/lowlevel/structured_output.py)  
完整示例： [示例/片段/服务器/低级/structured\_output.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/lowlevel/structured_output.py)_

Tools can return data in four ways:  
工具可以通过四种方式返回数据：

1.  **Content only**: Return a list of content blocks (default behavior before spec revision 2025-06-18)  
    **仅限内容** ：返回内容块列表（规范修订前默认行为，2025-06-18）
2.  **Structured data only**: Return a dictionary that will be serialized to JSON (Introduced in spec revision 2025-06-18)  
    **仅限结构化数据** ：返回一个将序列化为 JSON 的词典（规范修订版 2025-06-18 引入）
3.  **Both**: Return a tuple of (content, structured\_data) preferred option to use for backwards compatibility  
    **两者：** 返回一个（内容、structured\_data）首选选项的元组，用于向后兼容
4.  **Direct CallToolResult**: Return `CallToolResult` directly for full control (including `_meta` field)  
    **直接 CallToolResult**：直接返回 `CallToolResult` 以获得完全控制（包括 `_meta` 字段）

When an `outputSchema` is defined, the server automatically validates the structured output against the schema. This ensures type safety and helps catch errors early.  
当定义输出`模式`时，服务器会自动验证结构化输出与该模式的关系。这确保了类型安全，并有助于及早发现错误。

##### Returning CallToolResult Directly  
直接返回 CALLTOOLRESULT

For full control over the response including the `_meta` field (for passing data to client applications without exposing it to the model), return `CallToolResult` directly:  
为了完全控制响应，包括 `_meta` 字段（将数据传递给客户端应用而不暴露给模型），请直接返回 `CallToolResult`：

```
<span>"""</span>
<span>Run from the repository root:</span>
<span>    uv run examples/snippets/servers/lowlevel/direct_call_tool_result.py</span>
<span>"""</span>

<span>import</span><span> </span><span>asyncio</span>
<span>from</span><span> </span><span>typing</span><span> </span><span>import</span> <span>Any</span>

<span>import</span><span> </span><span>mcp.server.stdio</span>
<span>import</span><span> </span><span>mcp.types</span><span> </span><span>as</span><span> </span><span>types</span>
<span>from</span><span> </span><span>mcp.server.lowlevel</span><span> </span><span>import</span> <span>NotificationOptions</span><span>,</span> <span>Server</span>
<span>from</span><span> </span><span>mcp.server.models</span><span> </span><span>import</span> <span>InitializationOptions</span>

<span>server</span> <span>=</span> <span>Server</span><span>(</span><span>"example-server"</span><span>)</span>


<span>@server</span><span>.</span><span>list_tools</span><span>()</span>
<span>async</span> <span>def</span><span> </span><span>list_tools</span><span>()</span> <span>-&gt;</span> <span>list</span><span>[</span><span>types</span><span>.</span><span>Tool</span><span>]:</span>
<span>    </span><span>"""List available tools."""</span>
    <span>return</span> <span>[</span>
        <span>types</span><span>.</span><span>Tool</span><span>(</span>
            <span>name</span><span>=</span><span>"advanced_tool"</span><span>,</span>
            <span>description</span><span>=</span><span>"Tool with full control including _meta field"</span><span>,</span>
            <span>inputSchema</span><span>=</span><span>{</span>
                <span>"type"</span><span>:</span> <span>"object"</span><span>,</span>
                <span>"properties"</span><span>:</span> <span>{</span><span>"message"</span><span>:</span> <span>{</span><span>"type"</span><span>:</span> <span>"string"</span><span>}},</span>
                <span>"required"</span><span>:</span> <span>[</span><span>"message"</span><span>],</span>
            <span>},</span>
        <span>)</span>
    <span>]</span>


<span>@server</span><span>.</span><span>call_tool</span><span>()</span>
<span>async</span> <span>def</span><span> </span><span>handle_call_tool</span><span>(</span><span>name</span><span>:</span> <span>str</span><span>,</span> <span>arguments</span><span>:</span> <span>dict</span><span>[</span><span>str</span><span>,</span> <span>Any</span><span>])</span> <span>-&gt;</span> <span>types</span><span>.</span><span>CallToolResult</span><span>:</span>
<span>    </span><span>"""Handle tool calls by returning CallToolResult directly."""</span>
    <span>if</span> <span>name</span> <span>==</span> <span>"advanced_tool"</span><span>:</span>
        <span>message</span> <span>=</span> <span>str</span><span>(</span><span>arguments</span><span>.</span><span>get</span><span>(</span><span>"message"</span><span>,</span> <span>""</span><span>))</span>
        <span>return</span> <span>types</span><span>.</span><span>CallToolResult</span><span>(</span>
            <span>content</span><span>=</span><span>[</span><span>types</span><span>.</span><span>TextContent</span><span>(</span><span>type</span><span>=</span><span>"text"</span><span>,</span> <span>text</span><span>=</span><span>f</span><span>"Processed: </span><span>{</span><span>message</span><span>}</span><span>"</span><span>)],</span>
            <span>structuredContent</span><span>=</span><span>{</span><span>"result"</span><span>:</span> <span>"success"</span><span>,</span> <span>"message"</span><span>:</span> <span>message</span><span>},</span>
            <span>_meta</span><span>=</span><span>{</span><span>"hidden"</span><span>:</span> <span>"data for client applications only"</span><span>},</span>
        <span>)</span>

    <span>raise</span> <span>ValueError</span><span>(</span><span>f</span><span>"Unknown tool: </span><span>{</span><span>name</span><span>}</span><span>"</span><span>)</span>


<span>async</span> <span>def</span><span> </span><span>run</span><span>():</span>
<span>    </span><span>"""Run the server."""</span>
    <span>async</span> <span>with</span> <span>mcp</span><span>.</span><span>server</span><span>.</span><span>stdio</span><span>.</span><span>stdio_server</span><span>()</span> <span>as</span> <span>(</span><span>read_stream</span><span>,</span> <span>write_stream</span><span>):</span>
        <span>await</span> <span>server</span><span>.</span><span>run</span><span>(</span>
            <span>read_stream</span><span>,</span>
            <span>write_stream</span><span>,</span>
            <span>InitializationOptions</span><span>(</span>
                <span>server_name</span><span>=</span><span>"example"</span><span>,</span>
                <span>server_version</span><span>=</span><span>"0.1.0"</span><span>,</span>
                <span>capabilities</span><span>=</span><span>server</span><span>.</span><span>get_capabilities</span><span>(</span>
                    <span>notification_options</span><span>=</span><span>NotificationOptions</span><span>(),</span>
                    <span>experimental_capabilities</span><span>=</span><span>{},</span>
                <span>),</span>
            <span>),</span>
        <span>)</span>


<span>if</span> <span>__name__</span> <span>==</span> <span>"__main__"</span><span>:</span>
    <span>asyncio</span><span>.</span><span>run</span><span>(</span><span>run</span><span>())</span>
```

_Full example: [examples/snippets/servers/lowlevel/direct\_call\_tool\_result.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/lowlevel/direct_call_tool_result.py)  
完整示例： [示例/片段/服务器/低级/direct\_call\_tool\_result.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/lowlevel/direct_call_tool_result.py)_

**Note:** When returning `CallToolResult`, you bypass the automatic content/structured conversion. You must construct the complete response yourself.  
**注：** 返回 `CallToolResult` 时，你会绕过自动内容/结构化转换。你必须自己构建完整的回答。

### Pagination (Advanced)  分页（高级）

For servers that need to handle large datasets, the low-level server provides paginated versions of list operations. This is an optional optimization - most servers won't need pagination unless they're dealing with hundreds or thousands of items.  
对于需要处理大型数据集的服务器，低级服务器提供分页版本的列表作。这是一个可选优化——大多数服务器除非处理数百甚至数千件物品，否则不需要分页。

#### Server-side Implementation  
服务器端实现

```
<span>"""</span>
<span>Example of implementing pagination with MCP server decorators.</span>
<span>"""</span>

<span>from</span><span> </span><span>pydantic</span><span> </span><span>import</span> <span>AnyUrl</span>

<span>import</span><span> </span><span>mcp.types</span><span> </span><span>as</span><span> </span><span>types</span>
<span>from</span><span> </span><span>mcp.server.lowlevel</span><span> </span><span>import</span> <span>Server</span>

<span># Initialize the server</span>
<span>server</span> <span>=</span> <span>Server</span><span>(</span><span>"paginated-server"</span><span>)</span>

<span># Sample data to paginate</span>
<span>ITEMS</span> <span>=</span> <span>[</span><span>f</span><span>"Item </span><span>{</span><span>i</span><span>}</span><span>"</span> <span>for</span> <span>i</span> <span>in</span> <span>range</span><span>(</span><span>1</span><span>,</span> <span>101</span><span>)]</span>  <span># 100 items</span>


<span>@server</span><span>.</span><span>list_resources</span><span>()</span>
<span>async</span> <span>def</span><span> </span><span>list_resources_paginated</span><span>(</span><span>request</span><span>:</span> <span>types</span><span>.</span><span>ListResourcesRequest</span><span>)</span> <span>-&gt;</span> <span>types</span><span>.</span><span>ListResourcesResult</span><span>:</span>
<span>    </span><span>"""List resources with pagination support."""</span>
    <span>page_size</span> <span>=</span> <span>10</span>

    <span># Extract cursor from request params</span>
    <span>cursor</span> <span>=</span> <span>request</span><span>.</span><span>params</span><span>.</span><span>cursor</span> <span>if</span> <span>request</span><span>.</span><span>params</span> <span>is</span> <span>not</span> <span>None</span> <span>else</span> <span>None</span>

    <span># Parse cursor to get offset</span>
    <span>start</span> <span>=</span> <span>0</span> <span>if</span> <span>cursor</span> <span>is</span> <span>None</span> <span>else</span> <span>int</span><span>(</span><span>cursor</span><span>)</span>
    <span>end</span> <span>=</span> <span>start</span> <span>+</span> <span>page_size</span>

    <span># Get page of resources</span>
    <span>page_items</span> <span>=</span> <span>[</span>
        <span>types</span><span>.</span><span>Resource</span><span>(</span><span>uri</span><span>=</span><span>AnyUrl</span><span>(</span><span>f</span><span>"resource://items/</span><span>{</span><span>item</span><span>}</span><span>"</span><span>),</span> <span>name</span><span>=</span><span>item</span><span>,</span> <span>description</span><span>=</span><span>f</span><span>"Description for </span><span>{</span><span>item</span><span>}</span><span>"</span><span>)</span>
        <span>for</span> <span>item</span> <span>in</span> <span>ITEMS</span><span>[</span><span>start</span><span>:</span><span>end</span><span>]</span>
    <span>]</span>

    <span># Determine next cursor</span>
    <span>next_cursor</span> <span>=</span> <span>str</span><span>(</span><span>end</span><span>)</span> <span>if</span> <span>end</span> <span>&lt;</span> <span>len</span><span>(</span><span>ITEMS</span><span>)</span> <span>else</span> <span>None</span>

    <span>return</span> <span>types</span><span>.</span><span>ListResourcesResult</span><span>(</span><span>resources</span><span>=</span><span>page_items</span><span>,</span> <span>nextCursor</span><span>=</span><span>next_cursor</span><span>)</span>
```

_Full example: [examples/snippets/servers/pagination\_example.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/pagination_example.py)  
完整示例： [示例/摘要/服务器/pagination\_example.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/servers/pagination_example.py)_

#### Client-side Consumption  客户端消费

```
<span>"""</span>
<span>Example of consuming paginated MCP endpoints from a client.</span>
<span>"""</span>

<span>import</span><span> </span><span>asyncio</span>

<span>from</span><span> </span><span>mcp.client.session</span><span> </span><span>import</span> <span>ClientSession</span>
<span>from</span><span> </span><span>mcp.client.stdio</span><span> </span><span>import</span> <span>StdioServerParameters</span><span>,</span> <span>stdio_client</span>
<span>from</span><span> </span><span>mcp.types</span><span> </span><span>import</span> <span>PaginatedRequestParams</span><span>,</span> <span>Resource</span>


<span>async</span> <span>def</span><span> </span><span>list_all_resources</span><span>()</span> <span>-&gt;</span> <span>None</span><span>:</span>
<span>    </span><span>"""Fetch all resources using pagination."""</span>
    <span>async</span> <span>with</span> <span>stdio_client</span><span>(</span><span>StdioServerParameters</span><span>(</span><span>command</span><span>=</span><span>"uv"</span><span>,</span> <span>args</span><span>=</span><span>[</span><span>"run"</span><span>,</span> <span>"mcp-simple-pagination"</span><span>]))</span> <span>as</span> <span>(</span>
        <span>read</span><span>,</span>
        <span>write</span><span>,</span>
    <span>):</span>
        <span>async</span> <span>with</span> <span>ClientSession</span><span>(</span><span>read</span><span>,</span> <span>write</span><span>)</span> <span>as</span> <span>session</span><span>:</span>
            <span>await</span> <span>session</span><span>.</span><span>initialize</span><span>()</span>

            <span>all_resources</span><span>:</span> <span>list</span><span>[</span><span>Resource</span><span>]</span> <span>=</span> <span>[]</span>
            <span>cursor</span> <span>=</span> <span>None</span>

            <span>while</span> <span>True</span><span>:</span>
                <span># Fetch a page of resources</span>
                <span>result</span> <span>=</span> <span>await</span> <span>session</span><span>.</span><span>list_resources</span><span>(</span><span>params</span><span>=</span><span>PaginatedRequestParams</span><span>(</span><span>cursor</span><span>=</span><span>cursor</span><span>))</span>
                <span>all_resources</span><span>.</span><span>extend</span><span>(</span><span>result</span><span>.</span><span>resources</span><span>)</span>

                <span>print</span><span>(</span><span>f</span><span>"Fetched </span><span>{</span><span>len</span><span>(</span><span>result</span><span>.</span><span>resources</span><span>)</span><span>}</span><span> resources"</span><span>)</span>

                <span># Check if there are more pages</span>
                <span>if</span> <span>result</span><span>.</span><span>nextCursor</span><span>:</span>
                    <span>cursor</span> <span>=</span> <span>result</span><span>.</span><span>nextCursor</span>
                <span>else</span><span>:</span>
                    <span>break</span>

            <span>print</span><span>(</span><span>f</span><span>"Total resources: </span><span>{</span><span>len</span><span>(</span><span>all_resources</span><span>)</span><span>}</span><span>"</span><span>)</span>


<span>if</span> <span>__name__</span> <span>==</span> <span>"__main__"</span><span>:</span>
    <span>asyncio</span><span>.</span><span>run</span><span>(</span><span>list_all_resources</span><span>())</span>
```

_Full example: [examples/snippets/clients/pagination\_client.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/pagination_client.py)  
完整示例： [示例/摘录/客户端/pagination\_client.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/pagination_client.py)_

#### Key Points  要点

-   **Cursors are opaque strings** - the server defines the format (numeric offsets, timestamps, etc.)  
    **光标是不透明的字符串** ——服务器定义格式（数字偏移量、时间戳等）。
-   **Return `nextCursor=None`** when there are no more pages  
    **返回 `nextCursor=无`** ，当页面数不存在时
-   **Backward compatible** - clients that don't support pagination will still work (they'll just get the first page)  
    **向下兼容** ——不支持分页的客户端仍然能工作（他们只会获得首页）
-   **Flexible page sizes** - Each endpoint can define its own page size based on data characteristics  
    **灵活的页面大小** ——每个端点可以根据数据特性定义自己的页面大小

See the [simple-pagination example](https://pypi.org/project/mcp/examples/servers/simple-pagination) for a complete implementation.  
完整实现请参见[简单分页示例](https://pypi.org/project/mcp/examples/servers/simple-pagination) 。

### Writing MCP Clients  编写 MCP 客户端

The SDK provides a high-level client interface for connecting to MCP servers using various [transports](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports):  
SDK 提供了一个高级客户端接口，用于通过各种[传输](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports)方式连接到 MCP 服务器：

```
<span>"""</span>
<span>cd to the `examples/snippets/clients` directory and run:</span>
<span>    uv run client</span>
<span>"""</span>

<span>import</span><span> </span><span>asyncio</span>
<span>import</span><span> </span><span>os</span>

<span>from</span><span> </span><span>pydantic</span><span> </span><span>import</span> <span>AnyUrl</span>

<span>from</span><span> </span><span>mcp</span><span> </span><span>import</span> <span>ClientSession</span><span>,</span> <span>StdioServerParameters</span><span>,</span> <span>types</span>
<span>from</span><span> </span><span>mcp.client.stdio</span><span> </span><span>import</span> <span>stdio_client</span>
<span>from</span><span> </span><span>mcp.shared.context</span><span> </span><span>import</span> <span>RequestContext</span>

<span># Create server parameters for stdio connection</span>
<span>server_params</span> <span>=</span> <span>StdioServerParameters</span><span>(</span>
    <span>command</span><span>=</span><span>"uv"</span><span>,</span>  <span># Using uv to run the server</span>
    <span>args</span><span>=</span><span>[</span><span>"run"</span><span>,</span> <span>"server"</span><span>,</span> <span>"fastmcp_quickstart"</span><span>,</span> <span>"stdio"</span><span>],</span>  <span># We're already in snippets dir</span>
    <span>env</span><span>=</span><span>{</span><span>"UV_INDEX"</span><span>:</span> <span>os</span><span>.</span><span>environ</span><span>.</span><span>get</span><span>(</span><span>"UV_INDEX"</span><span>,</span> <span>""</span><span>)},</span>
<span>)</span>


<span># Optional: create a sampling callback</span>
<span>async</span> <span>def</span><span> </span><span>handle_sampling_message</span><span>(</span>
    <span>context</span><span>:</span> <span>RequestContext</span><span>[</span><span>ClientSession</span><span>,</span> <span>None</span><span>],</span> <span>params</span><span>:</span> <span>types</span><span>.</span><span>CreateMessageRequestParams</span>
<span>)</span> <span>-&gt;</span> <span>types</span><span>.</span><span>CreateMessageResult</span><span>:</span>
    <span>print</span><span>(</span><span>f</span><span>"Sampling request: </span><span>{</span><span>params</span><span>.</span><span>messages</span><span>}</span><span>"</span><span>)</span>
    <span>return</span> <span>types</span><span>.</span><span>CreateMessageResult</span><span>(</span>
        <span>role</span><span>=</span><span>"assistant"</span><span>,</span>
        <span>content</span><span>=</span><span>types</span><span>.</span><span>TextContent</span><span>(</span>
            <span>type</span><span>=</span><span>"text"</span><span>,</span>
            <span>text</span><span>=</span><span>"Hello, world! from model"</span><span>,</span>
        <span>),</span>
        <span>model</span><span>=</span><span>"gpt-3.5-turbo"</span><span>,</span>
        <span>stopReason</span><span>=</span><span>"endTurn"</span><span>,</span>
    <span>)</span>


<span>async</span> <span>def</span><span> </span><span>run</span><span>():</span>
    <span>async</span> <span>with</span> <span>stdio_client</span><span>(</span><span>server_params</span><span>)</span> <span>as</span> <span>(</span><span>read</span><span>,</span> <span>write</span><span>):</span>
        <span>async</span> <span>with</span> <span>ClientSession</span><span>(</span><span>read</span><span>,</span> <span>write</span><span>,</span> <span>sampling_callback</span><span>=</span><span>handle_sampling_message</span><span>)</span> <span>as</span> <span>session</span><span>:</span>
            <span># Initialize the connection</span>
            <span>await</span> <span>session</span><span>.</span><span>initialize</span><span>()</span>

            <span># List available prompts</span>
            <span>prompts</span> <span>=</span> <span>await</span> <span>session</span><span>.</span><span>list_prompts</span><span>()</span>
            <span>print</span><span>(</span><span>f</span><span>"Available prompts: </span><span>{</span><span>[</span><span>p</span><span>.</span><span>name</span><span> </span><span>for</span><span> </span><span>p</span><span> </span><span>in</span><span> </span><span>prompts</span><span>.</span><span>prompts</span><span>]</span><span>}</span><span>"</span><span>)</span>

            <span># Get a prompt (greet_user prompt from fastmcp_quickstart)</span>
            <span>if</span> <span>prompts</span><span>.</span><span>prompts</span><span>:</span>
                <span>prompt</span> <span>=</span> <span>await</span> <span>session</span><span>.</span><span>get_prompt</span><span>(</span><span>"greet_user"</span><span>,</span> <span>arguments</span><span>=</span><span>{</span><span>"name"</span><span>:</span> <span>"Alice"</span><span>,</span> <span>"style"</span><span>:</span> <span>"friendly"</span><span>})</span>
                <span>print</span><span>(</span><span>f</span><span>"Prompt result: </span><span>{</span><span>prompt</span><span>.</span><span>messages</span><span>[</span><span>0</span><span>]</span><span>.</span><span>content</span><span>}</span><span>"</span><span>)</span>

            <span># List available resources</span>
            <span>resources</span> <span>=</span> <span>await</span> <span>session</span><span>.</span><span>list_resources</span><span>()</span>
            <span>print</span><span>(</span><span>f</span><span>"Available resources: </span><span>{</span><span>[</span><span>r</span><span>.</span><span>uri</span><span> </span><span>for</span><span> </span><span>r</span><span> </span><span>in</span><span> </span><span>resources</span><span>.</span><span>resources</span><span>]</span><span>}</span><span>"</span><span>)</span>

            <span># List available tools</span>
            <span>tools</span> <span>=</span> <span>await</span> <span>session</span><span>.</span><span>list_tools</span><span>()</span>
            <span>print</span><span>(</span><span>f</span><span>"Available tools: </span><span>{</span><span>[</span><span>t</span><span>.</span><span>name</span><span> </span><span>for</span><span> </span><span>t</span><span> </span><span>in</span><span> </span><span>tools</span><span>.</span><span>tools</span><span>]</span><span>}</span><span>"</span><span>)</span>

            <span># Read a resource (greeting resource from fastmcp_quickstart)</span>
            <span>resource_content</span> <span>=</span> <span>await</span> <span>session</span><span>.</span><span>read_resource</span><span>(</span><span>AnyUrl</span><span>(</span><span>"greeting://World"</span><span>))</span>
            <span>content_block</span> <span>=</span> <span>resource_content</span><span>.</span><span>contents</span><span>[</span><span>0</span><span>]</span>
            <span>if</span> <span>isinstance</span><span>(</span><span>content_block</span><span>,</span> <span>types</span><span>.</span><span>TextContent</span><span>):</span>
                <span>print</span><span>(</span><span>f</span><span>"Resource content: </span><span>{</span><span>content_block</span><span>.</span><span>text</span><span>}</span><span>"</span><span>)</span>

            <span># Call a tool (add tool from fastmcp_quickstart)</span>
            <span>result</span> <span>=</span> <span>await</span> <span>session</span><span>.</span><span>call_tool</span><span>(</span><span>"add"</span><span>,</span> <span>arguments</span><span>=</span><span>{</span><span>"a"</span><span>:</span> <span>5</span><span>,</span> <span>"b"</span><span>:</span> <span>3</span><span>})</span>
            <span>result_unstructured</span> <span>=</span> <span>result</span><span>.</span><span>content</span><span>[</span><span>0</span><span>]</span>
            <span>if</span> <span>isinstance</span><span>(</span><span>result_unstructured</span><span>,</span> <span>types</span><span>.</span><span>TextContent</span><span>):</span>
                <span>print</span><span>(</span><span>f</span><span>"Tool result: </span><span>{</span><span>result_unstructured</span><span>.</span><span>text</span><span>}</span><span>"</span><span>)</span>
            <span>result_structured</span> <span>=</span> <span>result</span><span>.</span><span>structuredContent</span>
            <span>print</span><span>(</span><span>f</span><span>"Structured tool result: </span><span>{</span><span>result_structured</span><span>}</span><span>"</span><span>)</span>


<span>def</span><span> </span><span>main</span><span>():</span>
<span>    </span><span>"""Entry point for the client script."""</span>
    <span>asyncio</span><span>.</span><span>run</span><span>(</span><span>run</span><span>())</span>


<span>if</span> <span>__name__</span> <span>==</span> <span>"__main__"</span><span>:</span>
    <span>main</span><span>()</span>
```

_Full example: [examples/snippets/clients/stdio\_client.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/stdio_client.py)  
完整示例： [示例/片段/客户端/stdio\_client.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/stdio_client.py)_

Clients can also connect using [Streamable HTTP transport](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http):  
客户端还可以使用[可流式 HTTP 传输](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports#streamable-http)连接：

```
<span>"""</span>
<span>Run from the repository root:</span>
<span>    uv run examples/snippets/clients/streamable_basic.py</span>
<span>"""</span>

<span>import</span><span> </span><span>asyncio</span>

<span>from</span><span> </span><span>mcp</span><span> </span><span>import</span> <span>ClientSession</span>
<span>from</span><span> </span><span>mcp.client.streamable_http</span><span> </span><span>import</span> <span>streamable_http_client</span>


<span>async</span> <span>def</span><span> </span><span>main</span><span>():</span>
    <span># Connect to a streamable HTTP server</span>
    <span>async</span> <span>with</span> <span>streamable_http_client</span><span>(</span><span>"http://localhost:8000/mcp"</span><span>)</span> <span>as</span> <span>(</span>
        <span>read_stream</span><span>,</span>
        <span>write_stream</span><span>,</span>
        <span>_</span><span>,</span>
    <span>):</span>
        <span># Create a session using the client streams</span>
        <span>async</span> <span>with</span> <span>ClientSession</span><span>(</span><span>read_stream</span><span>,</span> <span>write_stream</span><span>)</span> <span>as</span> <span>session</span><span>:</span>
            <span># Initialize the connection</span>
            <span>await</span> <span>session</span><span>.</span><span>initialize</span><span>()</span>
            <span># List available tools</span>
            <span>tools</span> <span>=</span> <span>await</span> <span>session</span><span>.</span><span>list_tools</span><span>()</span>
            <span>print</span><span>(</span><span>f</span><span>"Available tools: </span><span>{</span><span>[</span><span>tool</span><span>.</span><span>name</span><span> </span><span>for</span><span> </span><span>tool</span><span> </span><span>in</span><span> </span><span>tools</span><span>.</span><span>tools</span><span>]</span><span>}</span><span>"</span><span>)</span>


<span>if</span> <span>__name__</span> <span>==</span> <span>"__main__"</span><span>:</span>
    <span>asyncio</span><span>.</span><span>run</span><span>(</span><span>main</span><span>())</span>
```

_Full example: [examples/snippets/clients/streamable\_basic.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/streamable_basic.py)  
完整示例： [示例/片段/客户端/streamable\_basic.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/streamable_basic.py)_

### Client Display Utilities  
客户端显示工具

When building MCP clients, the SDK provides utilities to help display human-readable names for tools, resources, and prompts:  
在构建 MCP 客户端时，SDK 提供了工具，帮助显示工具、资源和提示的人类可读名称：

```
<span>"""</span>
<span>cd to the `examples/snippets` directory and run:</span>
<span>    uv run display-utilities-client</span>
<span>"""</span>

<span>import</span><span> </span><span>asyncio</span>
<span>import</span><span> </span><span>os</span>

<span>from</span><span> </span><span>mcp</span><span> </span><span>import</span> <span>ClientSession</span><span>,</span> <span>StdioServerParameters</span>
<span>from</span><span> </span><span>mcp.client.stdio</span><span> </span><span>import</span> <span>stdio_client</span>
<span>from</span><span> </span><span>mcp.shared.metadata_utils</span><span> </span><span>import</span> <span>get_display_name</span>

<span># Create server parameters for stdio connection</span>
<span>server_params</span> <span>=</span> <span>StdioServerParameters</span><span>(</span>
    <span>command</span><span>=</span><span>"uv"</span><span>,</span>  <span># Using uv to run the server</span>
    <span>args</span><span>=</span><span>[</span><span>"run"</span><span>,</span> <span>"server"</span><span>,</span> <span>"fastmcp_quickstart"</span><span>,</span> <span>"stdio"</span><span>],</span>
    <span>env</span><span>=</span><span>{</span><span>"UV_INDEX"</span><span>:</span> <span>os</span><span>.</span><span>environ</span><span>.</span><span>get</span><span>(</span><span>"UV_INDEX"</span><span>,</span> <span>""</span><span>)},</span>
<span>)</span>


<span>async</span> <span>def</span><span> </span><span>display_tools</span><span>(</span><span>session</span><span>:</span> <span>ClientSession</span><span>):</span>
<span>    </span><span>"""Display available tools with human-readable names"""</span>
    <span>tools_response</span> <span>=</span> <span>await</span> <span>session</span><span>.</span><span>list_tools</span><span>()</span>

    <span>for</span> <span>tool</span> <span>in</span> <span>tools_response</span><span>.</span><span>tools</span><span>:</span>
        <span># get_display_name() returns the title if available, otherwise the name</span>
        <span>display_name</span> <span>=</span> <span>get_display_name</span><span>(</span><span>tool</span><span>)</span>
        <span>print</span><span>(</span><span>f</span><span>"Tool: </span><span>{</span><span>display_name</span><span>}</span><span>"</span><span>)</span>
        <span>if</span> <span>tool</span><span>.</span><span>description</span><span>:</span>
            <span>print</span><span>(</span><span>f</span><span>"   </span><span>{</span><span>tool</span><span>.</span><span>description</span><span>}</span><span>"</span><span>)</span>


<span>async</span> <span>def</span><span> </span><span>display_resources</span><span>(</span><span>session</span><span>:</span> <span>ClientSession</span><span>):</span>
<span>    </span><span>"""Display available resources with human-readable names"""</span>
    <span>resources_response</span> <span>=</span> <span>await</span> <span>session</span><span>.</span><span>list_resources</span><span>()</span>

    <span>for</span> <span>resource</span> <span>in</span> <span>resources_response</span><span>.</span><span>resources</span><span>:</span>
        <span>display_name</span> <span>=</span> <span>get_display_name</span><span>(</span><span>resource</span><span>)</span>
        <span>print</span><span>(</span><span>f</span><span>"Resource: </span><span>{</span><span>display_name</span><span>}</span><span> (</span><span>{</span><span>resource</span><span>.</span><span>uri</span><span>}</span><span>)"</span><span>)</span>

    <span>templates_response</span> <span>=</span> <span>await</span> <span>session</span><span>.</span><span>list_resource_templates</span><span>()</span>
    <span>for</span> <span>template</span> <span>in</span> <span>templates_response</span><span>.</span><span>resourceTemplates</span><span>:</span>
        <span>display_name</span> <span>=</span> <span>get_display_name</span><span>(</span><span>template</span><span>)</span>
        <span>print</span><span>(</span><span>f</span><span>"Resource Template: </span><span>{</span><span>display_name</span><span>}</span><span>"</span><span>)</span>


<span>async</span> <span>def</span><span> </span><span>run</span><span>():</span>
<span>    </span><span>"""Run the display utilities example."""</span>
    <span>async</span> <span>with</span> <span>stdio_client</span><span>(</span><span>server_params</span><span>)</span> <span>as</span> <span>(</span><span>read</span><span>,</span> <span>write</span><span>):</span>
        <span>async</span> <span>with</span> <span>ClientSession</span><span>(</span><span>read</span><span>,</span> <span>write</span><span>)</span> <span>as</span> <span>session</span><span>:</span>
            <span># Initialize the connection</span>
            <span>await</span> <span>session</span><span>.</span><span>initialize</span><span>()</span>

            <span>print</span><span>(</span><span>"=== Available Tools ==="</span><span>)</span>
            <span>await</span> <span>display_tools</span><span>(</span><span>session</span><span>)</span>

            <span>print</span><span>(</span><span>"</span><span>\n</span><span>=== Available Resources ==="</span><span>)</span>
            <span>await</span> <span>display_resources</span><span>(</span><span>session</span><span>)</span>


<span>def</span><span> </span><span>main</span><span>():</span>
<span>    </span><span>"""Entry point for the display utilities client."""</span>
    <span>asyncio</span><span>.</span><span>run</span><span>(</span><span>run</span><span>())</span>


<span>if</span> <span>__name__</span> <span>==</span> <span>"__main__"</span><span>:</span>
    <span>main</span><span>()</span>
```

_Full example: [examples/snippets/clients/display\_utilities.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/display_utilities.py)  
完整示例： [示例/片段/客户端/display\_utilities.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/display_utilities.py)_

The `get_display_name()` function implements the proper precedence rules for displaying names:  
`get_display_name（）` 函数实现了显示名称的正确优先规则：

-   For tools: `title` > `annotations.title` > `name`  
    工具方面：`title` > `注释。title` > `名称`
-   For other objects: `title` > `name`  
    其他对象： `标题` \> `名称`

This ensures your client UI shows the most user-friendly names that servers provide.  
这确保你的客户端界面显示服务器提供的最用户友好的名字。

### OAuth Authentication for Clients  
客户端的 OAuth 认证

The SDK includes [authorization support](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization) for connecting to protected MCP servers:  
SDK 包含连接受保护 MCP 服务器的[授权支持](https://modelcontextprotocol.io/specification/2025-03-26/basic/authorization) ：

```
<span>"""</span>
<span>Before running, specify running MCP RS server URL.</span>
<span>To spin up RS server locally, see</span>
<span>    examples/servers/simple-auth/README.md</span>

<span>cd to the `examples/snippets` directory and run:</span>
<span>    uv run oauth-client</span>
<span>"""</span>

<span>import</span><span> </span><span>asyncio</span>
<span>from</span><span> </span><span>urllib.parse</span><span> </span><span>import</span> <span>parse_qs</span><span>,</span> <span>urlparse</span>

<span>import</span><span> </span><span>httpx</span>
<span>from</span><span> </span><span>pydantic</span><span> </span><span>import</span> <span>AnyUrl</span>

<span>from</span><span> </span><span>mcp</span><span> </span><span>import</span> <span>ClientSession</span>
<span>from</span><span> </span><span>mcp.client.auth</span><span> </span><span>import</span> <span>OAuthClientProvider</span><span>,</span> <span>TokenStorage</span>
<span>from</span><span> </span><span>mcp.client.streamable_http</span><span> </span><span>import</span> <span>streamable_http_client</span>
<span>from</span><span> </span><span>mcp.shared.auth</span><span> </span><span>import</span> <span>OAuthClientInformationFull</span><span>,</span> <span>OAuthClientMetadata</span><span>,</span> <span>OAuthToken</span>


<span>class</span><span> </span><span>InMemoryTokenStorage</span><span>(</span><span>TokenStorage</span><span>):</span>
<span>    </span><span>"""Demo In-memory token storage implementation."""</span>

    <span>def</span><span> </span><span>__init__</span><span>(</span><span>self</span><span>):</span>
        <span>self</span><span>.</span><span>tokens</span><span>:</span> <span>OAuthToken</span> <span>|</span> <span>None</span> <span>=</span> <span>None</span>
        <span>self</span><span>.</span><span>client_info</span><span>:</span> <span>OAuthClientInformationFull</span> <span>|</span> <span>None</span> <span>=</span> <span>None</span>

    <span>async</span> <span>def</span><span> </span><span>get_tokens</span><span>(</span><span>self</span><span>)</span> <span>-&gt;</span> <span>OAuthToken</span> <span>|</span> <span>None</span><span>:</span>
<span>        </span><span>"""Get stored tokens."""</span>
        <span>return</span> <span>self</span><span>.</span><span>tokens</span>

    <span>async</span> <span>def</span><span> </span><span>set_tokens</span><span>(</span><span>self</span><span>,</span> <span>tokens</span><span>:</span> <span>OAuthToken</span><span>)</span> <span>-&gt;</span> <span>None</span><span>:</span>
<span>        </span><span>"""Store tokens."""</span>
        <span>self</span><span>.</span><span>tokens</span> <span>=</span> <span>tokens</span>

    <span>async</span> <span>def</span><span> </span><span>get_client_info</span><span>(</span><span>self</span><span>)</span> <span>-&gt;</span> <span>OAuthClientInformationFull</span> <span>|</span> <span>None</span><span>:</span>
<span>        </span><span>"""Get stored client information."""</span>
        <span>return</span> <span>self</span><span>.</span><span>client_info</span>

    <span>async</span> <span>def</span><span> </span><span>set_client_info</span><span>(</span><span>self</span><span>,</span> <span>client_info</span><span>:</span> <span>OAuthClientInformationFull</span><span>)</span> <span>-&gt;</span> <span>None</span><span>:</span>
<span>        </span><span>"""Store client information."""</span>
        <span>self</span><span>.</span><span>client_info</span> <span>=</span> <span>client_info</span>


<span>async</span> <span>def</span><span> </span><span>handle_redirect</span><span>(</span><span>auth_url</span><span>:</span> <span>str</span><span>)</span> <span>-&gt;</span> <span>None</span><span>:</span>
    <span>print</span><span>(</span><span>f</span><span>"Visit: </span><span>{</span><span>auth_url</span><span>}</span><span>"</span><span>)</span>


<span>async</span> <span>def</span><span> </span><span>handle_callback</span><span>()</span> <span>-&gt;</span> <span>tuple</span><span>[</span><span>str</span><span>,</span> <span>str</span> <span>|</span> <span>None</span><span>]:</span>
    <span>callback_url</span> <span>=</span> <span>input</span><span>(</span><span>"Paste callback URL: "</span><span>)</span>
    <span>params</span> <span>=</span> <span>parse_qs</span><span>(</span><span>urlparse</span><span>(</span><span>callback_url</span><span>)</span><span>.</span><span>query</span><span>)</span>
    <span>return</span> <span>params</span><span>[</span><span>"code"</span><span>][</span><span>0</span><span>],</span> <span>params</span><span>.</span><span>get</span><span>(</span><span>"state"</span><span>,</span> <span>[</span><span>None</span><span>])[</span><span>0</span><span>]</span>


<span>async</span> <span>def</span><span> </span><span>main</span><span>():</span>
<span>    </span><span>"""Run the OAuth client example."""</span>
    <span>oauth_auth</span> <span>=</span> <span>OAuthClientProvider</span><span>(</span>
        <span>server_url</span><span>=</span><span>"http://localhost:8001"</span><span>,</span>
        <span>client_metadata</span><span>=</span><span>OAuthClientMetadata</span><span>(</span>
            <span>client_name</span><span>=</span><span>"Example MCP Client"</span><span>,</span>
            <span>redirect_uris</span><span>=</span><span>[</span><span>AnyUrl</span><span>(</span><span>"http://localhost:3000/callback"</span><span>)],</span>
            <span>grant_types</span><span>=</span><span>[</span><span>"authorization_code"</span><span>,</span> <span>"refresh_token"</span><span>],</span>
            <span>response_types</span><span>=</span><span>[</span><span>"code"</span><span>],</span>
            <span>scope</span><span>=</span><span>"user"</span><span>,</span>
        <span>),</span>
        <span>storage</span><span>=</span><span>InMemoryTokenStorage</span><span>(),</span>
        <span>redirect_handler</span><span>=</span><span>handle_redirect</span><span>,</span>
        <span>callback_handler</span><span>=</span><span>handle_callback</span><span>,</span>
    <span>)</span>

    <span>async</span> <span>with</span> <span>httpx</span><span>.</span><span>AsyncClient</span><span>(</span><span>auth</span><span>=</span><span>oauth_auth</span><span>,</span> <span>follow_redirects</span><span>=</span><span>True</span><span>)</span> <span>as</span> <span>custom_client</span><span>:</span>
        <span>async</span> <span>with</span> <span>streamable_http_client</span><span>(</span><span>"http://localhost:8001/mcp"</span><span>,</span> <span>http_client</span><span>=</span><span>custom_client</span><span>)</span> <span>as</span> <span>(</span><span>read</span><span>,</span> <span>write</span><span>,</span> <span>_</span><span>):</span>
            <span>async</span> <span>with</span> <span>ClientSession</span><span>(</span><span>read</span><span>,</span> <span>write</span><span>)</span> <span>as</span> <span>session</span><span>:</span>
                <span>await</span> <span>session</span><span>.</span><span>initialize</span><span>()</span>

                <span>tools</span> <span>=</span> <span>await</span> <span>session</span><span>.</span><span>list_tools</span><span>()</span>
                <span>print</span><span>(</span><span>f</span><span>"Available tools: </span><span>{</span><span>[</span><span>tool</span><span>.</span><span>name</span><span> </span><span>for</span><span> </span><span>tool</span><span> </span><span>in</span><span> </span><span>tools</span><span>.</span><span>tools</span><span>]</span><span>}</span><span>"</span><span>)</span>

                <span>resources</span> <span>=</span> <span>await</span> <span>session</span><span>.</span><span>list_resources</span><span>()</span>
                <span>print</span><span>(</span><span>f</span><span>"Available resources: </span><span>{</span><span>[</span><span>r</span><span>.</span><span>uri</span><span> </span><span>for</span><span> </span><span>r</span><span> </span><span>in</span><span> </span><span>resources</span><span>.</span><span>resources</span><span>]</span><span>}</span><span>"</span><span>)</span>


<span>def</span><span> </span><span>run</span><span>():</span>
    <span>asyncio</span><span>.</span><span>run</span><span>(</span><span>main</span><span>())</span>


<span>if</span> <span>__name__</span> <span>==</span> <span>"__main__"</span><span>:</span>
    <span>run</span><span>()</span>
```

_Full example: [examples/snippets/clients/oauth\_client.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/oauth_client.py)  
完整示例： [示例/片段/客户端/oauth\_client.py](https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/snippets/clients/oauth_client.py)_

For a complete working example, see [`examples/clients/simple-auth-client/`](https://pypi.org/project/mcp/examples/clients/simple-auth-client/).  
完整的工作示例请参见 [`examples/clients/simple-auth-client/`](https://pypi.org/project/mcp/examples/clients/simple-auth-client/) 。

### Parsing Tool Results  解析工具结果

When calling tools through MCP, the `CallToolResult` object contains the tool's response in a structured format. Understanding how to parse this result is essential for properly handling tool outputs.  
通过 MCP 调用工具时，`CallToolResult` 对象包含工具的响应，以结构化格式呈现。理解如何解析这些结果对于正确处理工具输出至关重要。

```
<span>"""examples/snippets/clients/parsing_tool_results.py"""</span>

<span>import</span><span> </span><span>asyncio</span>

<span>from</span><span> </span><span>mcp</span><span> </span><span>import</span> <span>ClientSession</span><span>,</span> <span>StdioServerParameters</span><span>,</span> <span>types</span>
<span>from</span><span> </span><span>mcp.client.stdio</span><span> </span><span>import</span> <span>stdio_client</span>


<span>async</span> <span>def</span><span> </span><span>parse_tool_results</span><span>():</span>
<span>    </span><span>"""Demonstrates how to parse different types of content in CallToolResult."""</span>
    <span>server_params</span> <span>=</span> <span>StdioServerParameters</span><span>(</span>
        <span>command</span><span>=</span><span>"python"</span><span>,</span> <span>args</span><span>=</span><span>[</span><span>"path/to/mcp_server.py"</span><span>]</span>
    <span>)</span>

    <span>async</span> <span>with</span> <span>stdio_client</span><span>(</span><span>server_params</span><span>)</span> <span>as</span> <span>(</span><span>read</span><span>,</span> <span>write</span><span>):</span>
        <span>async</span> <span>with</span> <span>ClientSession</span><span>(</span><span>read</span><span>,</span> <span>write</span><span>)</span> <span>as</span> <span>session</span><span>:</span>
            <span>await</span> <span>session</span><span>.</span><span>initialize</span><span>()</span>

            <span># Example 1: Parsing text content</span>
            <span>result</span> <span>=</span> <span>await</span> <span>session</span><span>.</span><span>call_tool</span><span>(</span><span>"get_data"</span><span>,</span> <span>{</span><span>"format"</span><span>:</span> <span>"text"</span><span>})</span>
            <span>for</span> <span>content</span> <span>in</span> <span>result</span><span>.</span><span>content</span><span>:</span>
                <span>if</span> <span>isinstance</span><span>(</span><span>content</span><span>,</span> <span>types</span><span>.</span><span>TextContent</span><span>):</span>
                    <span>print</span><span>(</span><span>f</span><span>"Text: </span><span>{</span><span>content</span><span>.</span><span>text</span><span>}</span><span>"</span><span>)</span>

            <span># Example 2: Parsing structured content from JSON tools</span>
            <span>result</span> <span>=</span> <span>await</span> <span>session</span><span>.</span><span>call_tool</span><span>(</span><span>"get_user"</span><span>,</span> <span>{</span><span>"id"</span><span>:</span> <span>"123"</span><span>})</span>
            <span>if</span> <span>hasattr</span><span>(</span><span>result</span><span>,</span> <span>"structuredContent"</span><span>)</span> <span>and</span> <span>result</span><span>.</span><span>structuredContent</span><span>:</span>
                <span># Access structured data directly</span>
                <span>user_data</span> <span>=</span> <span>result</span><span>.</span><span>structuredContent</span>
                <span>print</span><span>(</span><span>f</span><span>"User: </span><span>{</span><span>user_data</span><span>.</span><span>get</span><span>(</span><span>'name'</span><span>)</span><span>}</span><span>, Age: </span><span>{</span><span>user_data</span><span>.</span><span>get</span><span>(</span><span>'age'</span><span>)</span><span>}</span><span>"</span><span>)</span>

            <span># Example 3: Parsing embedded resources</span>
            <span>result</span> <span>=</span> <span>await</span> <span>session</span><span>.</span><span>call_tool</span><span>(</span><span>"read_config"</span><span>,</span> <span>{})</span>
            <span>for</span> <span>content</span> <span>in</span> <span>result</span><span>.</span><span>content</span><span>:</span>
                <span>if</span> <span>isinstance</span><span>(</span><span>content</span><span>,</span> <span>types</span><span>.</span><span>EmbeddedResource</span><span>):</span>
                    <span>resource</span> <span>=</span> <span>content</span><span>.</span><span>resource</span>
                    <span>if</span> <span>isinstance</span><span>(</span><span>resource</span><span>,</span> <span>types</span><span>.</span><span>TextResourceContents</span><span>):</span>
                        <span>print</span><span>(</span><span>f</span><span>"Config from </span><span>{</span><span>resource</span><span>.</span><span>uri</span><span>}</span><span>: </span><span>{</span><span>resource</span><span>.</span><span>text</span><span>}</span><span>"</span><span>)</span>
                    <span>elif</span> <span>isinstance</span><span>(</span><span>resource</span><span>,</span> <span>types</span><span>.</span><span>BlobResourceContents</span><span>):</span>
                        <span>print</span><span>(</span><span>f</span><span>"Binary data from </span><span>{</span><span>resource</span><span>.</span><span>uri</span><span>}</span><span>"</span><span>)</span>

            <span># Example 4: Parsing image content</span>
            <span>result</span> <span>=</span> <span>await</span> <span>session</span><span>.</span><span>call_tool</span><span>(</span><span>"generate_chart"</span><span>,</span> <span>{</span><span>"data"</span><span>:</span> <span>[</span><span>1</span><span>,</span> <span>2</span><span>,</span> <span>3</span><span>]})</span>
            <span>for</span> <span>content</span> <span>in</span> <span>result</span><span>.</span><span>content</span><span>:</span>
                <span>if</span> <span>isinstance</span><span>(</span><span>content</span><span>,</span> <span>types</span><span>.</span><span>ImageContent</span><span>):</span>
                    <span>print</span><span>(</span><span>f</span><span>"Image (</span><span>{</span><span>content</span><span>.</span><span>mimeType</span><span>}</span><span>): </span><span>{</span><span>len</span><span>(</span><span>content</span><span>.</span><span>data</span><span>)</span><span>}</span><span> bytes"</span><span>)</span>

            <span># Example 5: Handling errors</span>
            <span>result</span> <span>=</span> <span>await</span> <span>session</span><span>.</span><span>call_tool</span><span>(</span><span>"failing_tool"</span><span>,</span> <span>{})</span>
            <span>if</span> <span>result</span><span>.</span><span>isError</span><span>:</span>
                <span>print</span><span>(</span><span>"Tool execution failed!"</span><span>)</span>
                <span>for</span> <span>content</span> <span>in</span> <span>result</span><span>.</span><span>content</span><span>:</span>
                    <span>if</span> <span>isinstance</span><span>(</span><span>content</span><span>,</span> <span>types</span><span>.</span><span>TextContent</span><span>):</span>
                        <span>print</span><span>(</span><span>f</span><span>"Error: </span><span>{</span><span>content</span><span>.</span><span>text</span><span>}</span><span>"</span><span>)</span>


<span>async</span> <span>def</span><span> </span><span>main</span><span>():</span>
    <span>await</span> <span>parse_tool_results</span><span>()</span>


<span>if</span> <span>__name__</span> <span>==</span> <span>"__main__"</span><span>:</span>
    <span>asyncio</span><span>.</span><span>run</span><span>(</span><span>main</span><span>())</span>
```

### MCP Primitives  MCP 原语

The MCP protocol defines three core primitives that servers can implement:  
MCP 协议定义了服务器可以实现的三个核心原语：

| Primitive  原始 | Control  控制 | Description  描述 | Example Use  示例应用 |
| --- | --- | --- | --- |
| Prompts  提示 | User-controlled  用户控制 | Interactive templates invoked by user choice  
用户选择调用的交互式模板 | Slash commands, menu options  
斜击命令，菜单选项 |
| Resources  资源 | Application-controlled  应用控制 | Contextual data managed by the client application  
由客户端应用程序管理的上下文数据 | File contents, API responses  
文件内容，API 响应 |
| Tools  工具 | Model-controlled  模型控制 | Functions exposed to the LLM to take actions  
暴露给大型语言模型以执行作的功能 | API calls, data updates  
API 调用，数据更新 |

### Server Capabilities  服务器功能

MCP servers declare capabilities during initialization:  
MCP 服务器在初始化时声明能力：

| Capability  能力 | Feature Flag  特色旗帜 | Description  描述 |
| --- | --- | --- |
| `prompts` | `listChanged` | Prompt template management  
提示模板管理 |
| `resources` | `subscribe`  
`listChanged` | Resource exposure and updates  
资源曝光与更新 |
| `tools` | `listChanged` | Tool discovery and execution  
工具发现与执行 |
| `logging` | \- | Server logging configuration  
服务器日志配置 |
| `completions` | \- | Argument completion suggestions  
论证补全建议 |

## Documentation  文献资料

-   [API Reference  API 参考](https://modelcontextprotocol.github.io/python-sdk/api/)
-   [Experimental Features (Tasks)  
    实验特征（任务）](https://modelcontextprotocol.github.io/python-sdk/experimental/tasks/)
-   [Model Context Protocol documentation  
    模型上下文协议文档](https://modelcontextprotocol.io/)
-   [Model Context Protocol specification  
    模型上下文协议规范](https://modelcontextprotocol.io/specification/latest)
-   [Officially supported servers  
    官方支持的服务器](https://github.com/modelcontextprotocol/servers)

## Contributing  贡献

We are passionate about supporting contributors of all levels of experience and would love to see you get involved in the project. See the [contributing guide](https://pypi.org/project/mcp/CONTRIBUTING.md) to get started.  
我们热衷于支持各级经验的贡献者，并希望您能参与到这个项目中。请参阅[贡献指南](https://pypi.org/project/mcp/CONTRIBUTING.md)以开始。

## License  许可证

This project is licensed under the MIT License - see the LICENSE file for details.  
本项目采用 MIT 许可证授权——详情请参见 LICENSE 文件。
