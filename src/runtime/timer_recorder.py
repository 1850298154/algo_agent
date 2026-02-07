import time
class TimerRecorder:
    """
    上下文计时器：传入一个对象（dict 或任意对象），会尝试写入 start_time / end_time / duration 字段。
    用法:
        with TimerRecorder(exec_time_container):
            ... 执行需要计时的代码 ...
    """
    def __init__(self, exec_time_container: list[float]):
        self.exec_time_container = exec_time_container

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.end = time.perf_counter()
        self.duration = self.end - self.start
        self.exec_time_container.append(self.duration)
        # 若返回 False，异常会向上抛出；返回 True 则抑制异常（按需选择）
        return False
