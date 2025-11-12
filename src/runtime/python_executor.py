from langchain_experimental.utilities.python import PythonREPL

my_globals = {"a": 123, "b": [1, 2, 3]}
repl = PythonREPL(_globals=my_globals)

res=repl.run("a+=100000")  # 输出: 123
print(res)
res=repl.run("print(a)")  # 输出: [1, 2, 3]
print(res)
