
## 🚀 快速开始（uv）

### 1️⃣ 安装依赖管理工具 uv

```bash
pip install uv
```

### 2️⃣ 创建虚拟环境并安装依赖

创建并进入虚拟环境（复现的时候不需要，直接执行 uv sync ）：

```bash
uv add playwright requests python-dotenv pydantic

uv run playwright install chromium  # or : uv run python -m playwright install chromium
```


### 3️⃣ 配置环境变量

复制 `.env.example` 并填写 API Key（**不要提交到 GitHub**）：

```bash
cp .env.example .env
```

`.env` 示例：

```env
ZHIPU_API_KEY=YOUR_API_KEY_HERE
```

---

## ▶️ 运行示例

* **输入：** “去 Hacker News 首页，找到排名前三的 AI 相关新闻，并把标题和链接整理给我。”


```bash
uv run python tests\unit\agent\test_deep_research\test_glmv46_ai_new.py
```

* **输入：** “帮我查一下京东上 RTX 4090 显卡现在的最低价格是多少。”
```bash
uv run python tests\unit\agent\test_deep_research\test_glmv46_jd_hitl.py
```

终端将输出 Agent 的思考日志（Thinking）、浏览器操作过程，以及最终结构化结果。

---


## 🧠 功能概览

* 基于 ReAct + Reflection 框架的任务规划与执行智能体（ 大语言模型 GLM-4.6  ）
* 只有一个核心工具 python 执行器
  * 写 playtwright 脚本自动化浏览器操作
  * 调用视觉大模型解析截图内容 （GLM-4.6V， 用prompt提示）
  * 人机交互辅助处理登录验证码
* 多策略代码执行运行时
  * 子进程隔离执行
  * 子线程快速执行
  * 直接执行

---

## 🛡️ 安全与工程规范

* API Key 通过 `.env` 管理
* `.env` 已加入 `.gitignore`

---

## 🎁 可扩展方向（Bonus）

- [X] Human-in-the-loop 决策确认
- [] 点击前 Bounding Box 可视化调试
- [X] JSON Schema / Pydantic 结构化输出
- [] Docker 一键运行

---

## 📌 声明

本项目为面试考核用途，重点在于 **Agent 思路、工程结构与推理闭环**，而非完整产品。

---

**Author**: Yuteng Zhao


## 📄 详细文档
两个实验
- [【hacker news】 实验输出详细文档](hacker_new.md)
- [【京东电商网站上 RTX 4090 显卡】 实验输出详细文档](jd_4096.md)