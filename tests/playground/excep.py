
print("=== 1. raise 捕获并重新抛出异常，保留原始堆栈 ===")
import traceback

def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        # 捕获异常后，先做一些处理，比如记录日志
        print(f"[ERROR] 发生除零错误: {e}")
        # 再次抛出当前异常（保留原始堆栈）
        raise  

try:
    divide(10, 0)
except ZeroDivisionError as e:
    print("\n上层捕获到异常:")
    traceback.print_exc()  # 打印完整堆栈






print("\n=== 2. from 捕获并重新抛出异常，保留原始堆栈 ===")
class BusinessException(Exception):
    """自定义业务异常"""
    pass

def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        # 捕获底层异常，包装成业务异常抛出，并保留原始原因
        raise BusinessException("计算失败：除数不能为零") from e

try:
    divide(10, 0)
except BusinessException as e:
    print("上层捕获到业务异常:")
    import traceback
    traceback.print_exc()
    
    
    

print("\n=== 3. 直接抛出新异常，丢失原始堆栈 ===")
import traceback

def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        # 直接抛出新异常，丢失原始堆栈
        raise ValueError("除数不能为零")

try:
    divide(10, 0)
except ValueError as e:
    traceback.print_exc()


print("\n=== 4. pass 捕获异常，不抛出新异常 ===")
import traceback

def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        # 直接抛出新异常，丢失原始堆栈
        pass

try:
    divide(10, 0)
    print("没有异常抛出")
except ValueError as e:
    e.with_traceback(traceback.extract_stack())


print("\n=== 5. 直接抛出新异常，丢失原始堆栈 ===")
import traceback

def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError as e:
        # 直接抛出新异常，丢失原始堆栈
        raise e

try:
    divide(10, 0)
except ZeroDivisionError as e:
    traceback.print_exc()
except Exception as e:
    traceback.print_exc()

print(" 结束 ")