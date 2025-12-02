# docker
[docker](https://www.doubao.com/chat/32183231215320066)

### 一、PostgreSQL 16 启动与使用
PostgreSQL 16 是官方标准镜像，核心是启动容器并配置基础连接（端口、密码、数据持久化）。

#### 1. 启动命令（基础版，无数据持久化）
```bash
# 启动PostgreSQL 16容器，设置密码、暴露端口
docker run -d \
  --name postgres16 \          # 容器名称（自定义）
  -p 5432:5432 \               # 端口映射：主机5432 → 容器5432
  -e POSTGRES_PASSWORD=123456 \ # 数据库超级管理员（postgres）密码
  -e POSTGRES_USER=myuser \    # 可选：自定义默认用户（默认postgres）
  -e POSTGRES_DB=mydb \        # 可选：自定义默认数据库（默认postgres）
  postgres:16
```

#### 2. 启动命令（生产版，数据持久化）
```bash
# 创建本地目录存储PostgreSQL数据（避免容器删除数据丢失）
mkdir -p /docker/postgres16/data

# 启动容器，挂载数据卷
docker run -d \
  --name postgres16 \
  --restart always \           # 开机自启
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=123456 \
  -v /docker/postgres16/data:/var/lib/postgresql/data \ # 数据卷挂载
  postgres:16
```

#### 3. 如何使用PostgreSQL 16
##### 方式1：进入容器内操作
```bash
# 进入postgres16容器，连接数据库
docker exec -it postgres16 psql -U postgres

# 常用SQL操作示例
\l          # 查看所有数据库
\c mydb     # 切换到mydb数据库
\d          # 查看当前数据库的表
CREATE TABLE test (id INT, name VARCHAR(50)); # 创建表
INSERT INTO test VALUES (1, 'test');          # 插入数据
SELECT * FROM test;                           # 查询数据
\q          # 退出psql
```

##### 方式2：外部客户端连接（如Navicat/DBeaver/psql）
- 主机：你的服务器/本地IP（如`127.0.0.1`）
- 端口：5432
- 用户名：postgres（或自定义的myuser）
- 密码：123456（你设置的密码）
- 数据库：postgres（或自定义的mydb）

### 二、pgvector/pgvector:pg17 启动与使用
pgvector 是 PostgreSQL 的扩展，用于存储和查询向量数据（AI/机器学习场景常用），`pg17` 标签表示适配 PostgreSQL 17 的版本。
**核心前提**：pgvector 镜像本身就是带 vector 扩展的 PostgreSQL，启动方式和普通 PG 一致，只是多了「启用 vector 扩展」的步骤。

#### 1. 启动命令（带数据持久化）
```bash
# 创建本地数据目录
mkdir -p /docker/pgvector17/data

# 启动pgvector容器（适配PG17）
docker run -d \
  --name pgvector17 \
  --restart always \
  -p 5433:5432 \               # 避免和postgres16端口冲突，主机用5433
  -e POSTGRES_PASSWORD=123456 \
  -v /docker/pgvector17/data:/var/lib/postgresql/data \
  pgvector/pgvector:pg17
```

#### 2. 如何使用pgvector扩展
##### 步骤1：进入容器，连接数据库
```bash
docker exec -it pgvector17 psql -U postgres
```

##### 步骤2：启用vector扩展（核心）
```sql
-- 1. 创建测试数据库（可选）
CREATE DATABASE vector_db;
\c vector_db;

-- 2. 启用vector扩展（必须）
CREATE EXTENSION vector;

-- 3. 验证扩展是否生效
\dx; -- 查看已安装的扩展，能看到vector即成功
```

##### 步骤3：vector 核心用法示例（存储/查询向量）
```sql
-- 1. 创建带向量字段的表（vector(3)表示3维向量）
CREATE TABLE embeddings (
  id SERIAL PRIMARY KEY,
  vec vector(3),  -- 向量字段，维度自定义（如768维对应vector(768)
  content TEXT
);

-- 2. 插入向量数据
INSERT INTO embeddings (vec, content)
VALUES 
  ('[1.1, 2.2, 3.3]', '测试文本1'),
  ('[4.4, 5.5, 6.6]', '测试文本2');

-- 3. 向量相似度查询（L2距离，越小越相似）
SELECT 
  id, content, 
  vec <-> '[1.0, 2.0, 3.0]' AS distance  -- <-> 表示L2距离
FROM embeddings
ORDER BY distance ASC;
```

### 三、关键补充说明
1. **端口冲突**：如果同时启动 postgres16 和 pgvector17，需保证主机端口不同（如示例中 5432 和 5433）。
2. **pgvector 版本适配**：`pg17` 标签适配 PG17，若需适配 PG16，可改用 `pgvector/pgvector:pg16` 镜像。
3. **容器管理**：
   ```bash
   # 停止容器
   docker stop postgres16 pgvector17
   # 启动容器
   docker start postgres16 pgvector17
   # 查看容器日志（排错用）
   docker logs postgres16
   ```
4. **权限问题**：若本地数据目录挂载后报权限错误，可先执行：
   ```bash
   chmod 777 /docker/postgres16/data
   chmod 777 /docker/pgvector17/data
   ```
# [sql](https://www.doubao.com/chat/32182564710304514)
### 需求分析
需要找出**连续3天及以上登录**的用户，并输出用户ID、连续登录的起始/结束日期、连续天数。核心思路是：
1. 先对用户登录记录去重（避免同一天多次登录干扰连续天数计算）；
2. 使用窗口函数`ROW_NUMBER()`按用户分组、登录日期排序，计算「日期偏移量」；
3. 相同连续登录区间的用户，其「登录日期 - 偏移量」结果一致，以此分组统计连续天数；
4. 筛选出连续天数≥3的分组。

### 一、MySQL 实现（兼容 8.0+）
#### 1. 基础表结构（示例）
```sql
CREATE TABLE user_login (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,  -- 用户ID
    login_date DATE NOT NULL       -- 登录日期
);

-- 插入测试数据
INSERT INTO user_login (user_id, login_date) VALUES
('u001', '2025-01-01'), ('u001', '2025-01-01'),  -- 同一天重复登录
('u001', '2025-01-02'), ('u001', '2025-01-03'), ('u001', '2025-01-04'),
('u002', '2025-01-01'), ('u002', '2025-01-03'), ('u002', '2025-01-04'),
('u003', '2025-01-01'), ('u003', '2025-01-02'), ('u003', '2025-01-03');
```

#### 2. 核心SQL（窗口函数实现）
```sql
WITH 
-- 步骤1：去重，每个用户每天只保留一条登录记录
distinct_login AS (
    SELECT DISTINCT user_id, login_date 
    FROM user_login
),
-- 步骤2：按用户分组，日期排序，计算行号（偏移量）
login_rn AS (
    SELECT 
        user_id,
        login_date,
        -- 计算：登录日期 - 行号（天），连续日期的结果会相同
        DATE_SUB(login_date, INTERVAL ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) DAY) AS group_key
    FROM distinct_login
),
-- 步骤3：按用户+分组键统计连续天数
continuous_login AS (
    SELECT 
        user_id,
        MIN(login_date) AS start_date,  -- 连续登录起始日
        MAX(login_date) AS end_date,    -- 连续登录结束日
        COUNT(*) AS continuous_days     -- 连续天数
    FROM login_rn
    GROUP BY user_id, group_key
)
-- 步骤4：筛选连续天数≥3的记录
SELECT 
    user_id,
    start_date,
    end_date,
    continuous_days
FROM continuous_login
WHERE continuous_days >= 3
ORDER BY user_id, start_date;
```

#### 结果说明
| user_id | start_date | end_date   | continuous_days |
|---------|------------|------------|-----------------|
| u001    | 2025-01-01 | 2025-01-04 | 4               |
| u003    | 2025-01-01 | 2025-01-03 | 3               |

### 二、PostgreSQL 实现
PostgreSQL 语法与MySQL核心逻辑一致，仅日期函数略有差异（`DATE_SUB` → `- INTERVAL`）：

#### 1. 核心SQL
```sql
WITH 
-- 步骤1：去重
distinct_login AS (
    SELECT DISTINCT user_id, login_date 
    FROM user_login
),
-- 步骤2：计算分组键（PostgreSQL 日期运算）
login_rn AS (
    SELECT 
        user_id,
        login_date,
        login_date - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) * INTERVAL '1 day' AS group_key
    FROM distinct_login
),
-- 步骤3：统计连续天数
continuous_login AS (
    SELECT 
        user_id,
        MIN(login_date) AS start_date,
        MAX(login_date) AS end_date,
        COUNT(*) AS continuous_days
    FROM login_rn
    GROUP BY user_id, group_key
)
-- 步骤4：筛选连续≥3天的用户
SELECT 
    user_id,
    start_date,
    end_date,
    continuous_days
FROM continuous_login
WHERE continuous_days >= 3
ORDER BY user_id, start_date;
```

### 关键逻辑解释
1. **去重**：`DISTINCT user_id, login_date` 确保每个用户每天只算一次登录，避免重复登录导致连续天数误判；
2. **分组键（group_key）**：  
   - 对每个用户的登录日期排序后，用「登录日期 - 行号（天）」生成分组键；  
   - 连续的日期会得到相同的分组键（例如：2025-01-01-1=2024-12-31，2025-01-02-2=2024-12-31，2025-01-03-3=2024-12-31）；  
   - 非连续日期的分组键会不同（例如：2025-01-01-1=2024-12-31，2025-01-03-2=2025-01-01）；
3. **统计连续天数**：按「用户+分组键」分组，统计每组的记录数即为连续天数，筛选≥3的分组即可。

### 扩展场景
- 若需要「所有连续登录区间（包括<3天）」，只需去掉最后一步的`WHERE continuous_days >=3`；
- 若登录时间是datetime类型（而非date），需先转换为日期：`DATE(login_time)`（MySQL）或`login_time::date`（PostgreSQL）；
- 若需按自然日连续（跨月份也适用），上述逻辑无需修改（日期运算天然支持跨月）。


# docker
### 一、前提确认
1. 确保Windows已安装Docker Desktop并启动（桌面右下角Docker图标正常运行）；
2. 以下操作通过**Windows终端（PowerShell/CMD）** 执行，优先用PowerShell（语法更通用）；
3. 会自动拉取主流稳定版本（PostgreSQL 16、MySQL 8.0），若本地已有对应版本镜像，会直接复用。

### 二、快速启动MySQL 8.0容器
#### 1. 启动MySQL容器（带初始化配置）
```powershell
# 启动MySQL容器（端口映射3306，密码设为123456，容器名mysql-test）
docker run -d --name mysql-test -p 3306:3306 ^
-e MYSQL_ROOT_PASSWORD=123456 ^
-e MYSQL_DATABASE=test_db ^
mysql:8.0

# 验证容器是否启动成功
docker ps | findstr mysql-test
```
- 参数说明：
  - `-d`：后台运行；
  - `-p 3306:3306`：主机3306端口映射到容器3306；
  - `MYSQL_ROOT_PASSWORD`：root密码（自定义，这里用123456）；
  - `MYSQL_DATABASE`：自动创建test_db数据库。

#### 2. 进入MySQL容器并执行测试SQL
```powershell
# 进入MySQL容器的命令行
docker exec -it mysql-test mysql -uroot -p123456 test_db

# 粘贴以下SQL（先创建表+插入测试数据，再执行连续登录查询）
CREATE TABLE user_login (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    login_date DATE NOT NULL
);

INSERT INTO user_login (user_id, login_date) VALUES
('u001', '2025-01-01'), ('u001', '2025-01-01'),
('u001', '2025-01-02'), ('u001', '2025-01-03'), ('u001', '2025-01-04'),
('u002', '2025-01-01'), ('u002', '2025-01-03'), ('u002', '2025-01-04'),
('u003', '2025-01-01'), ('u003', '2025-01-02'), ('u003', '2025-01-03');

# 执行连续登录查询SQL
WITH 
distinct_login AS (
    SELECT DISTINCT user_id, login_date 
    FROM user_login
),
login_rn AS (
    SELECT 
        user_id,
        login_date,
        DATE_SUB(login_date, INTERVAL ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) DAY) AS group_key
    FROM distinct_login
),
continuous_login AS (
    SELECT 
        user_id,
        MIN(login_date) AS start_date,
        MAX(login_date) AS end_date,
        COUNT(*) AS continuous_days
    FROM login_rn
    GROUP BY user_id, group_key
)
SELECT user_id, start_date, end_date, continuous_days 
FROM continuous_login 
WHERE continuous_days >= 3 
ORDER BY user_id;
```
- 执行后会输出结果：
  ```
  +---------+------------+------------+-----------------+
  | user_id | start_date | end_date   | continuous_days |
  +---------+------------+------------+-----------------+
  | u001    | 2025-01-01 | 2025-01-04 | 4               |
  | u003    | 2025-01-01 | 2025-01-03 | 3               |
  +---------+------------+------------+-----------------+
  ```

### 三、快速启动PostgreSQL 16容器
#### 1. 启动PostgreSQL容器
```powershell
# 启动PostgreSQL容器（端口映射5432，密码123456，容器名pg-test）
docker run -d --name pg-test -p 5432:5432 ^
-e POSTGRES_PASSWORD=123456 ^
-e POSTGRES_DB=test_db ^
postgres:16

# 验证容器是否启动成功
docker ps | findstr pg-test
```
- 参数说明：
  - `POSTGRES_PASSWORD`：postgres用户密码；
  - `POSTGRES_DB`：自动创建test_db数据库。

#### 2. 进入PostgreSQL容器并执行测试SQL
```powershell
# 进入PostgreSQL命令行（切换到test_db数据库）
docker exec -it pg-test psql -U postgres -d test_db

# 粘贴以下SQL（创建表+插入数据+查询）
CREATE TABLE user_login (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    login_date DATE NOT NULL
);

INSERT INTO user_login (user_id, login_date) VALUES
('u001', '2025-01-01'), ('u001', '2025-01-01'),
('u001', '2025-01-02'), ('u001', '2025-01-03'), ('u001', '2025-01-04'),
('u002', '2025-01-01'), ('u002', '2025-01-03'), ('u002', '2025-01-04'),
('u003', '2025-01-01'), ('u003', '2025-01-02'), ('u003', '2025-01-03');

# 执行连续登录查询SQL
WITH 
distinct_login AS (
    SELECT DISTINCT user_id, login_date 
    FROM user_login
),
login_rn AS (
    SELECT 
        user_id,
        login_date,
        login_date - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY login_date) * INTERVAL '1 day' AS group_key
    FROM distinct_login
),
continuous_login AS (
    SELECT 
        user_id,
        MIN(login_date) AS start_date,
        MAX(login_date) AS end_date,
        COUNT(*) AS continuous_days
    FROM login_rn
    GROUP BY user_id, group_key
)
SELECT user_id, start_date, end_date, continuous_days 
FROM continuous_login 
WHERE continuous_days >= 3 
ORDER BY user_id;
```
- 执行后输出结果：
  ```
  user_id | start_date | end_date   | continuous_days
  --------+------------+------------+-----------------
  u001    | 2025-01-01 | 2025-01-04 |               4
  u003    | 2025-01-01 | 2025-01-03 |               3
  ```

### 四、常用运维命令（可选）
#### 1. 停止/重启容器
```powershell
# 停止MySQL容器
docker stop mysql-test
# 重启MySQL容器
docker start mysql-test

# 停止PostgreSQL容器
docker stop pg-test
# 重启PostgreSQL容器
docker start pg-test
```

#### 2. 彻底删除容器（如需重新测试）
```powershell
# 先停止再删除MySQL容器
docker stop mysql-test && docker rm mysql-test
# 先停止再删除PostgreSQL容器
docker stop pg-test && docker rm pg-test
```

### 五、注意事项
1. 若端口被占用（如本地已装MySQL/PostgreSQL），修改端口映射（例如`-p 3307:3306`、`-p 5433:5432`）；
2. Docker Desktop需开启“Hyper-V”或“WSL 2”（安装时默认配置，若报错需在Windows功能中启用）；
3. 首次启动会拉取镜像，需等待网络下载完成（国内可配置Docker镜像源加速）；
4. 容器内数据默认存储在容器内，若需持久化数据，可添加`-v`挂载卷（例如`-v mysql-data:/var/lib/mysql`）。

