# 项目运行方式指南

本文档介绍如何运行 Omni-ReAct 项目。

## 环境准备

### 1. 激活虚拟环境

**Windows CMD:**
```bash
.venv\Scripts\activate.bat
```

**Windows PowerShell:**
```powershell
.venv\Scripts\Activate.ps1
```

**Git Bash / WSL:**
```bash
source .venv/Scripts/activate
```

### 2. 安装依赖

```bash
uv sync
```

## 运行方式

### 方式一：VSCode 调试运行（推荐）

在 VSCode 中，按 `F5` 或点击"运行和调试"按钮，选择以下配置之一：

#### 1. Python: 当前文件（根目录工作区）
- **适用场景：** 调试当前打开的任意 Python 文件
- **特点：**
  - 自动设置工作目录为项目根路径
  - 自动添加 PYTHONPATH 环境变量
  - 支持子进程调试
  - 可调试第三方库代码（justMyCode: false）

#### 2. Python: 指定脚本（根目录）
- **适用场景：** 运行固定的入口脚本
- **默认入口：** `${workspaceFolder}/src/ui/start_view.py`
- **特点：**
  - 固定运行 `src/ui/start_view.py`
  - 工作目录绑定项目根路径
  - 支持子进程调试

#### 3. Streamlit
- **适用场景：** 运行 Streamlit Web 应用
- **使用方法：**
  1. 打开要运行的 Streamlit 脚本文件
  2. 选择此配置并启动调试
- **特点：**
  - 自动启动 Streamlit 服务器
  - 禁用保存自动刷新（可手动修改）
  - 实时输出日志

### 方式二：命令行运行

#### 1. 运行主程序

```bash
python src/main.py
```

#### 2. 运行 Streamlit 应用

```bash
streamlit run src/ui/start_view.py
```

或使用 Python 模块方式：

```bash
python -m streamlit run src/ui/start_view.py
```

#### 3. 运行指定脚本

```bash
python src/retrieval/arXiv/start_main.py
```

#### 4. 保存日志输出

```bash
python src/main.py | tee -a output.log
```

### 方式三：使用 uv 运行

```bash
uv run python src/main.py
```

## 项目入口文件

- **主入口：** `src/main.py`
- **UI 入口：** `src/ui/start_view.py` (Streamlit 应用)
- **其他入口：**
  - `src/retrieval/arXiv/start_main.py` - arXiv 检索

## 配置文件

- **项目配置：** `pyproject.toml`
- **环境变量：** `.env`
- **调试配置：** `.vscode/launch.json`

## 常见问题

### 模块导入错误

确保：
1. 已激活虚拟环境
2. 工作目录为项目根路径
3. PYTHONPATH 已设置（VSCode 调试会自动设置）

**手动设置 PYTHONPATH (Windows CMD):**
```bash
set PYTHONPATH=%cd%
python src/main.py
```

**手动设置 PYTHONPATH (Bash):**
```bash
export PYTHONPATH=$(pwd)
python src/main.py
```

### Streamlit 端口被占用

修改 Streamlit 配置或指定端口：

```bash
streamlit run src/ui/start_view.py --server.port 8502
```

### 退出虚拟环境

```bash
deactivate
```

## 开发建议

1. **推荐使用 VSCode 调试：** 可以设置断点、查看变量、单步执行
2. **查看日志：** 运行日志记录在 `global.log` 文件中
3. **设计文档：** 详细设计请参阅 `docs` 目录

## 相关文档

- [项目 README](README.md)
- [设计文档](docs/)
- [模块设计](docs/module.design.md)
- [计划设计](docs/plan.design.md)
- [Python 执行器设计](docs/python.design.md)
