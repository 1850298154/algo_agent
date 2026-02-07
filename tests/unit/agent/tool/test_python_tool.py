from src.agent.tool import python_tool

def test_execute_python_code_tool():
    code = "print('hello world')"
    tool = python_tool.ExecutePythonCodeTool(
        tool_call_purpose="code",
        python_code_snippet=code,
        timeout=10,
        )
    result = tool.run()
    print(result)

def test_execute_python_code_tool_with_exception():
    code = """
def myadd(a, b):
    return a+b/0

def main():
    print('global :', globals().keys())
    print('local :',  locals().keys())
    print("核心逻辑执行", myadd(1, 2))
print('global :', globals().keys())
print('local :',  locals().keys())
temp = 0
main()
"""
    tool = python_tool.ExecutePythonCodeTool(
        tool_call_purpose="code",
        python_code_snippet=code,
        timeout=10,
        )
    result = tool.run()
    print(result)

test_execute_python_code_tool()
test_execute_python_code_tool_with_exception()