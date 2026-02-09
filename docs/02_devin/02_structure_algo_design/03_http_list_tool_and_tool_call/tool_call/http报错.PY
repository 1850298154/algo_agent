官网讲解
https://docs.devin.ai/work-with-devin/devin-mcp

BASE_URL = "https://mcp.deepwiki.com/mcp" # deepwiki 只支持公开，不支持私有库，不能配置秘钥
    # "Authorization": f"Bearer {DEVIN_API_KEY}",
    print("devin_toc",devin_toc("1850298154/HULK"))
    print('-------------------')
    print("devin_toc",devin_toc("1850298154/algo_agent"))

devin_toc {'jsonrpc': '2.0', 
	'id': 1, 
	'result': {'content': [{'type': 'text', 
	'text': 'Error fetching wiki for 1850298154/HULK: Repository not found. Visit https://deepwiki.com/1850298154/HULK to index it.'}], 
	'structuredContent': {'result': 'Error fetching wiki for 1850298154/HULK: Repository not found. Visit https://deepwiki.com/1850298154/HULK to index it.'}, 
	'isError': False}}
-------------------
devin_toc {'jsonrpc': '2.0', 
	'id': 1, 
	'result': {'content': [{'type': 'text', 
	'text': 'Available pages for 1850298154/algo_agent:\n\n- 1 Overview\n- 2 Getting Started\n- 3 Agent Orchestration\n  - 3.1 Query Processing Loop\n  - 3.2 LLM Integration\n  - 3.3 Memory and Context Management\n  - 3.4 Action Coordination\n- 4 Tool System\n  - 4.1 BaseTool Interface\n  - 4.2 Python Code Execution Tool\n  - 4.3 Recursive Task Planning Tool\n- 5 Execution Runtime\n  - 5.1 Subprocess Execution\n  - 5.2 Subthread Execution\n  - 5.3 Direct Execution\n  - 5.4 ExecutionResult and Status Handling\n  - 5.5 Workspace State Management\n  - 5.6 Working Directory and Environment\n- 6 Observability and Logging\n  - 6.1 Logging System Architecture\n  - 6.2 Log Files and Analysis\n  - 6.3 Tracing and Performance Monitoring\n- 7 Use Cases and Examples\n  - 7.1 Emergency Response Planning Example\n  - 7.2 Data Processing and Visualization\n  - 7.3 Geographic Data Processing\n- 8 Development and Testing\n  - 8.1 Testing the Execution System\n  - 8.2 Creating New Tools\n  - 8.3 Database Setup for Examples\n- 9 Architecture Reference\n  - 9.1 ExecutionResult Schema Reference\n  - 9.2 Task Tree Schema Reference\n  - 9.3 Tool Schema Format\n- 10 Troubleshooting\n  - 10.1 Common Execution Errors\n  - 10.2 Tool Call Errors'}], 
	'structuredContent': {'result': 'Available pages for 1850298154/algo_agent:\n\n- 1 Overview\n- 2 Getting Started\n- 3 Agent Orchestration\n  - 3.1 Query Processing Loop\n  - 3.2 LLM Integration\n  - 3.3 Memory and Context Management\n  - 3.4 Action Coordination\n- 4 Tool System\n  - 4.1 BaseTool Interface\n  - 4.2 Python Code Execution Tool\n  - 4.3 Recursive Task Planning Tool\n- 5 Execution Runtime\n  - 5.1 Subprocess Execution\n  - 5.2 Subthread Execution\n  - 5.3 Direct Execution\n  - 5.4 ExecutionResult and Status Handling\n  - 5.5 Workspace State Management\n  - 5.6 Working Directory and Environment\n- 6 Observability and Logging\n  - 6.1 Logging System Architecture\n  - 6.2 Log Files and Analysis\n  - 6.3 Tracing and Performance Monitoring\n- 7 Use Cases and Examples\n  - 7.1 Emergency Response Planning Example\n  - 7.2 Data Processing and Visualization\n  - 7.3 Geographic Data Processing\n- 8 Development and Testing\n  - 8.1 Testing the Execution System\n  - 8.2 Creating New Tools\n  - 8.3 Database Setup for Examples\n- 9 Architecture Reference\n  - 9.1 ExecutionResult Schema Reference\n  - 9.2 Task Tree Schema Reference\n  - 9.3 Tool Schema Format\n- 10 Troubleshooting\n  - 10.1 Common Execution Errors\n  - 10.2 Tool Call Errors'}, 
	'isError': False}}     



BASE_URL = "https://mcp.deepwiki.com/mcp" # deepwiki 公开和秘钥不能同时使用
    "Authorization": f"Bearer {DEVIN_API_KEY}",
    print("devin_toc",devin_toc("1850298154/HULK"))
    print('-------------------')
    print("devin_toc",devin_toc("1850298154/algo_agent"))
devin_toc {'jsonrpc': '2.0', 
	'id': 1, 
	'result': {'content': [{'type': 'text', 
	'text': 'Authentication is not allowed on the public DeepWiki endpoint (mcp.deepwiki.com). This endpoint is for public repositories only. Please use the Devin MCP endpoint (mcp.devin.ai) for private repositories.'}], 
	'structuredContent': {'result': 'Authentication is not allowed on the public DeepWiki endpoint (mcp.deepwiki.com). This endpoint is for public repositories only. Please use the Devin MCP endpoint (mcp.devin.ai) for private repositories.'}, 
	'isError': False}}
-------------------
devin_toc {'jsonrpc': '2.0', 
	'id': 1, 
	'result': {'content': [{'type': 'text', 
	'text': 'Authentication is not allowed on the public DeepWiki endpoint (mcp.deepwiki.com). This endpoint is for public repositories only. Please use the Devin MCP endpoint (mcp.devin.ai) for private repositories.'}], 
	'structuredContent': {'result': 'Authentication is not allowed on the public DeepWiki endpoint (mcp.deepwiki.com). This endpoint is for public repositories only. Please use the Devin MCP endpoint (mcp.devin.ai) for private repositories.'}, 
	'isError': False}}




BASE_URL = "https://mcp.devin.ai/sse" # 废弃
    "Authorization": f"Bearer {DEVIN_API_KEY}",
    print("devin_toc",devin_toc("1850298154/HULK"))
    print('-------------------')
    print("devin_toc",devin_toc("1850298154/algo_agent"))
devin_toc {'raw_error': 'Failed to parse JSON', 
	'content': 'Method Not Allowed'}
-------------------
devin_toc {'raw_error': 'Failed to parse JSON', 
	'content': 'Method Not Allowed'}



BASE_URL = "https://mcp.devin.ai/mcp" # devin 私有仓库，既可以访问公开，又可以访问私有
    "Authorization": f"Bearer {DEVIN_API_KEY}",
    print("devin_toc",devin_toc("1850298154/HULK"))
    print('-------------------')
    print("devin_toc",devin_toc("1850298154/algo_agent"))    
    print("===========================")
    print("devin_toc",devin_toc("1850298154/aella-data-explorer"))
devin_toc {'jsonrpc': '2.0', 
	'id': 1, 
	'result': {'content': [{'type': 'text', 
	'text': 'Available pages for 1850298154/HULK:\n\n- 1 Overview\n  - 1.1 Quick Start\n  - 1.2 System Architecture\n  - 1.3 Core Concepts\n- 2 Planning System\n  - 2.1 Planner and SharedInfo\n  - 2.2 Planning Algorithms\n    - 2.2.1 HULK Tree Search\n    - 2.2.2 MILP Assignment Planners\n    - 2.2.3 Greedy and Sampling Planners\n    - 2.2.4 Agent-to-Coalition Assignment (MILP)\n  - 2.3 Matcher and Capability Validation\n- 3 Tasks and Coalitions\n  - 3.1 Task Types and Lifecycle\n  - 3.2 Coalition Formation and Execution\n  - 3.3 Task Graph and Dependencies\n- 4 Agents and Environment\n  - 4.1 Agent Model\n  - 4.2 Targets and Areas\n  - 4.3 Simulation Environment (MyEnv)\n- 5 Motion Planning\n  - 5.1 Multi-Agent Motion Planners\n  - 5.2 Task-Specific Motion Planning\n- 6 GUI and Visualization\n  - 6.1 Main Window and Execution Control\n  - 6.2 Simulation Visualization\n  - 6.3 Interface Components\n- 7 Configuration System\n  - 7.1 Skill Configuration\n  - 7.2 Environment Configuration and Generation\n- 8 Analysis and Post-Processing\n  - 8.1 DataProcessor and Metrics\n  - 8.2 Development Tools\n- 9 Development Roadmap'}], 
	'structuredContent': {'result': 'Available pages for 1850298154/HULK:\n\n- 1 Overview\n  - 1.1 Quick Start\n  - 1.2 System Architecture\n  - 1.3 Core Concepts\n- 2 Planning System\n  - 2.1 Planner and SharedInfo\n  - 2.2 Planning Algorithms\n    - 2.2.1 HULK Tree Search\n    - 2.2.2 MILP Assignment Planners\n    - 2.2.3 Greedy and Sampling Planners\n    - 2.2.4 Agent-to-Coalition Assignment (MILP)\n  - 2.3 Matcher and Capability Validation\n- 3 Tasks and Coalitions\n  - 3.1 Task Types and Lifecycle\n  - 3.2 Coalition Formation and Execution\n  - 3.3 Task Graph and Dependencies\n- 4 Agents and Environment\n  - 4.1 Agent Model\n  - 4.2 Targets and Areas\n  - 4.3 Simulation Environment (MyEnv)\n- 5 Motion Planning\n  - 5.1 Multi-Agent Motion Planners\n  - 5.2 Task-Specific Motion Planning\n- 6 GUI and Visualization\n  - 6.1 Main Window and Execution Control\n  - 6.2 Simulation Visualization\n  - 6.3 Interface Components\n- 7 Configuration System\n  - 7.1 Skill Configuration\n  - 7.2 Environment Configuration and Generation\n- 8 Analysis and Post-Processing\n  - 8.1 DataProcessor and Metrics\n  - 8.2 Development Tools\n- 9 Development Roadmap'}, 
	'isError': False}}
-------------------
devin_toc {'jsonrpc': '2.0', 
	'id': 1, 
	'result': {'content': [{'type': 'text', 
	'text': 'Available pages for 1850298154/algo_agent:\n\n- 1 Overview\n- 2 Getting Started\n- 3 Agent Orchestration\n  - 3.1 Query Processing Loop\n  - 3.2 LLM Integration\n  - 3.3 Memory and Context Management\n  - 3.4 Action Coordination\n- 4 Tool System\n  - 4.1 BaseTool Interface\n  - 4.2 Python Code Execution Tool\n  - 4.3 Recursive Task Planning Tool\n- 5 Execution Runtime\n  - 5.1 Subprocess Execution\n  - 5.2 Subthread Execution\n  - 5.3 Direct Execution\n  - 5.4 ExecutionResult and Status Handling\n  - 5.5 Workspace State Management\n  - 5.6 Working Directory and Environment\n- 6 Observability and Logging\n  - 6.1 Logging System Architecture\n  - 6.2 Log Files and Analysis\n  - 6.3 Tracing and Performance Monitoring\n- 7 Use Cases and Examples\n  - 7.1 Emergency Response Planning Example\n  - 7.2 Data Processing and Visualization\n  - 7.3 Geographic Data Processing\n- 8 Development and Testing\n  - 8.1 Testing the Execution System\n  - 8.2 Creating New Tools\n  - 8.3 Database Setup for Examples\n- 9 Architecture Reference\n  - 9.1 ExecutionResult Schema Reference\n  - 9.2 Task Tree Schema Reference\n  - 9.3 Tool Schema Format\n- 10 Troubleshooting\n  - 10.1 Common Execution Errors\n  - 10.2 Tool Call Errors'}], 
	'structuredContent': {'result': 'Available pages for 1850298154/algo_agent:\n\n- 1 Overview\n- 2 Getting Started\n- 3 Agent Orchestration\n  - 3.1 Query Processing Loop\n  - 3.2 LLM Integration\n  - 3.3 Memory and Context Management\n  - 3.4 Action Coordination\n- 4 Tool System\n  - 4.1 BaseTool Interface\n  - 4.2 Python Code Execution Tool\n  - 4.3 Recursive Task Planning Tool\n- 5 Execution Runtime\n  - 5.1 Subprocess Execution\n  - 5.2 Subthread Execution\n  - 5.3 Direct Execution\n  - 5.4 ExecutionResult and Status Handling\n  - 5.5 Workspace State Management\n  - 5.6 Working Directory and Environment\n- 6 Observability and Logging\n  - 6.1 Logging System Architecture\n  - 6.2 Log Files and Analysis\n  - 6.3 Tracing and Performance Monitoring\n- 7 Use Cases and Examples\n  - 7.1 Emergency Response Planning Example\n  - 7.2 Data Processing and Visualization\n  - 7.3 Geographic Data Processing\n- 8 Development and Testing\n  - 8.1 Testing the Execution System\n  - 8.2 Creating New Tools\n  - 8.3 Database Setup for Examples\n- 9 Architecture Reference\n  - 9.1 ExecutionResult Schema Reference\n  - 9.2 Task Tree Schema Reference\n  - 9.3 Tool Schema Format\n- 10 Troubleshooting\n  - 10.1 Common Execution Errors\n  - 10.2 Tool Call Errors'}, 
	'isError': False}}
===========================
devin_toc {'jsonrpc': '2.0', 
	'id': 1, 
	'result': {'content': [{'type': 'text', 
	'text': 'Error fetching wiki for 1850298154/aella-data-explorer: Repository 1850298154/aella-data-explorer not found. Visit https://app.devin.ai/repositories to add your repo.'}], 
	'structuredContent': {'result': 'Error fetching wiki for 1850298154/aella-data-explorer: Repository 1850298154/aella-data-explorer not found. Visit https://app.devin.ai/repositories to add your repo.'}, 
	'isError': False}}


    print("devin_toc",devin_toc("volcengine/OpenViking/"))
devin_toc {'jsonrpc': '2.0', 
	'id': 1, 
	'result': {'content': [{'type': 'text', 
	'text': 'Invalid repoName format: "volcengine/OpenViking/". Expected format is "owner/repo", e.g. "facebook/react". For custom domains you must include the host, e.g., "git.mydomain.com/facebook/react".'}], 
	'structuredContent': {'result': 'Invalid repoName format: "volcengine/OpenViking/". Expected format is "owner/repo", e.g. "facebook/react". For custom domains you must include the host, e.g., "git.mydomain.com/facebook/react".'}, 
	'isError': False}}