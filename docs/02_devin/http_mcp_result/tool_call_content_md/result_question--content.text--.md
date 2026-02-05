The tool call mechanism involves the LLM agent generating tool calls, which are then dispatched and executed by the system. The process includes defining tools with Pydantic models, generating JSON schemas for LLM consumption, and a dispatcher that routes and safely executes these tool calls.   

## Tool Definition and Schema Generation

Tools are defined as Python classes inheriting from `BaseTool` . This base class, which is a Pydantic `BaseModel`, provides automatic validation, type checking, and JSON schema generation for tool parameters . Each tool defines its parameters as Pydantic fields with descriptions and type annotations. For example, `ExecutePythonCodeTool` defines `python_code_snippet` and `timeout` as fields .

The `get_tool_schema()` method, inherited from `BaseTool`, generates a JSON schema that conforms to OpenAI's function calling format . This schema includes the tool's name, description, and parameters, allowing the LLM to understand how to invoke the tool .

## Tool Invocation Pipeline

The LLM agent initiates a tool call by generating a response with a `tool_calls` attribute . The `user_query` function in `deep_research.py` then extracts the tool call information, including the `tool_call_name` and `tool_call_arguments` .

This information is passed to the `call_tools_safely()` function in `action.py` . This function acts as the central dispatcher:
1. It parses the `tool_call_arguments` from a JSON string into a dictionary .
2. It routes the call to the appropriate tool implementation based on the `function_name` .
   - If the `function_name` matches `ExecutePythonCodeTool.tool_name()`, an `ExecutePythonCodeTool` instance is created and its `run()` method is called .
   - If it matches `RecursivePlanTreeTodoTool.tool_name()`, a `RecursivePlanTreeTodoTool` instance is created and its `run()` method is called .
3. The result of the `run()` method is stored in `tool_info["content"]`  .

Error handling is integrated into `call_tools_safely()` using a `try-except` block . If an exception occurs during tool execution, the full traceback is captured and returned in `tool_info["content"]`, allowing the LLM to understand and potentially self-correct .

After the tool execution, the `tool_output` (which contains the result or error message) is logged and appended to the message history . The agent then continues the conversation with the LLM, providing the updated context including the tool's output .

## Available Tools

Currently, two main tools are implemented:
*   **`ExecutePythonCodeTool`**: This tool executes Python code snippets in a stateful environment . It maintains execution state across calls, meaning variables and functions defined in one call are available in subsequent calls .
*   **`RecursivePlanTreeTodoTool`**: This tool manages hierarchical task structures, tracking task status, maintaining version history, and analyzing changes between plan versions . It delegates its core logic to `todo_track.run()` .

## Notes

The `RecursivePlanTreeTodoTool.run()` method constructs a detailed string containing a change summary, Markdown representation of the todo list, and status statistics, but then overwrites it with an empty string before returning . This suggests that the primary purpose of this tool is to manage internal state and provide structured output for logging and internal processing, rather than directly returning a verbose string to the LLM . The actual state management occurs through the global `arg_todo_list` storage within the `todo_track` module. 

Wiki pages you might want to explore:
- [Tool System (1850298154/algo_agent)](/wiki/1850298154/algo_agent#4)
- [Recursive Task Planning Tool (1850298154/algo_agent)](/wiki/1850298154/algo_agent#4.3)

View this search on DeepWiki: https://deepwiki.com/search/how-does-tool-call-work_b88aadfa-f282-4d36-9154-413ebdd15e29
