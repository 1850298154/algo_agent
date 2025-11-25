import subprocess
import sys

def uv_add_package(package_name):
    """
    使用 uv 安装指定的包。
    """
    try:
        print(f"正在使用 uv 安装包: {package_name}...")
        # 注意：uv 通常作为独立命令安装，所以我们直接调用 "uv"
        # 但为了保险起见，也可以像 pip 一样使用 sys.executable -m uv
        # subprocess.check_call([sys.executable, "-m", "uv", "add", package_name])
        
        # 更常见的用法是直接调用 uv 命令
        subprocess.check_call(["uv", "add", package_name])
        print(f"包 {package_name} 安装成功！")
    except FileNotFoundError:
        print("错误：未找到 'uv' 命令。请先安装 uv (https://docs.astral.sh/uv/getting-started/installation/)。")
    except subprocess.CalledProcessError as e:
        print(f"安装包 {package_name} 失败！错误信息: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")

# --- 使用 ---
if __name__ == "__main__":
    # 安装 requests 包
    uv_add_package("wordcloud")

    # 安装到开发依赖
    # uv_add_package("--dev", "pytest")