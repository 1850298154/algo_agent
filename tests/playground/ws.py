import multiprocessing
import os

# 1. 定义一个新的包装函数
def _worker_wrapper(command, _globals, _locals, timeout, child_conn):
    """
    子进程的包装函数，用于在执行实际任务前更改工作目录。
    """
    cwd = "./ws/1/g4-1" 
    # 转变成绝对路径（可选），兼容win和linux
    cwd = os.path.abspath(cwd)
    print('cwd', cwd, os.getcwd())
    if cwd:
        try:
            os.chdir(cwd)
            print(f"子进程 PID: {os.getpid()} 已将工作目录更改为: {os.getcwd()}")
        except OSError as e:
            print(f"子进程 PID: {os.getpid()} 更改工作目录失败: {e}")
            # 根据需要处理错误，例如发送错误信息到主进程或直接退出
            child_conn.send(f"Error: Failed to change directory to {cwd}. {e}")
            child_conn.close()
            return
            
    # 2. 调用原来的工作函数
    _worker_with_pipe(command, _globals, _locals, timeout, child_conn)

def _worker_with_pipe(command, _globals, _locals, timeout, child_conn):
    # ... 子进程的工作逻辑 ...
    # 现在这里的工作目录已经是我们指定的目录了
    print(f"子进程 PID: {os.getpid()} 开始执行任务, 当前工作目录: {os.getcwd()}")
    # ... 例如，在这里读写文件就会基于新的工作目录 ...
    # child_conn.close()

if __name__ == "__main__":
    # ... 假设这些变量已经定义 ...
    command = "some_command"
    _globals = {}
    _locals = {}
    timeout = 10
    parent_conn, child_conn = multiprocessing.Pipe()
    

    
    # 3. 调整 Process 的参数
    p = multiprocessing.Process(
        target=_worker_wrapper,  # 目标函数改为包装函数
        args=(command, _globals, _locals, timeout, child_conn), # 将目录作为参数传入
    )
    p.start()
    child_conn.close()  # 主进程关闭子端句柄
    
    # 从管道接收可能的错误信息或结果
    result = parent_conn.recv()
    print(f"主进程收到: {result}")
    
    p.join()