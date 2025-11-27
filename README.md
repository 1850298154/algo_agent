
## start

```
uv run python src/agent/deep_research.py
```

## install
```
uv python install 3.12

uv init --python 3.12

uv add langchain_experimental

uv add langchain

``` 

## PROJECT

```
# 2. 创建核心目录结构
mkdir -p src/{agent,retrieval,algorithms,utils} tests docs

# 3. 创建空文件（按目录结构生成）
touch .dockerignore Dockerfile pyproject.toml uv.lock requirements.txt
touch src/__init__.py
touch src/agent/__init__.py src/agent/deep_research.py src/agent/executor.py
touch src/retrieval/__init__.py src/retrieval/es_retrieval.py
touch src/algorithms/__init__.py src/algorithms/task_assignment.py src/algorithms/path_planning.py src/algorithms/risk_assessment.py
touch src/utils/__init__.py src/utils/io_utils.py
touch tests/__init__.py tests/test_algorithms.py
touch docs/design.md
```