# 
[docker compose postgresql](https://www.doubao.com/chat/32062099877723906)

以下是针对 **Windows 系统** 的 PostgreSQL Docker Compose 配置，实现数据持久化到项目的 `data` 文件夹，包含详细注释和操作步骤：

### 一、最终目录结构
```
你的项目目录/
├── docker-compose.yml  # 核心配置文件
└── data/               # 自动生成，存储PostgreSQL数据
```

### 二、Docker Compose 配置文件（docker-compose.yml）
```yaml
version: '3.8'  # Compose文件版本（兼容主流Docker版本）

services:
  postgres:
    # 指定PostgreSQL镜像（推荐固定版本，避免自动更新）
    image: postgres:16-alpine  
    # 容器名称（自定义，方便管理）
    container_name: my-postgres
    # 端口映射：宿主机5432端口 → 容器5432端口（Windows本地可通过localhost:5432访问）
    ports:
      - "5432:5432"
    # 环境变量（必配，设置数据库密码、用户名、库名）
    environment:
      POSTGRES_PASSWORD: 123456       # 数据库密码（自定义）
      POSTGRES_USER: postgres         # 数据库用户名（默认postgres）
      POSTGRES_DB: mydb               # 初始化创建的数据库名（自定义）
      PGDATA: /var/lib/postgresql/data/pgdata  # 容器内数据存储路径（固定）
    # 数据卷挂载：Windows项目data目录 → 容器内数据目录（核心持久化配置）
    volumes:
      # 注意：./data 是相对路径，指向项目根目录下的data文件夹
      # 冒号前是宿主机路径（Windows路径自动兼容），冒号后是容器内路径
      - ./data:/var/lib/postgresql/data/pgdata
    # 重启策略：容器退出时自动重启（可选，增强稳定性）
    restart: always
    # 额外配置（可选，解决Windows下权限问题）
    user: root  # 以root用户运行，避免data目录权限不足
    # 字符集配置（可选，解决中文乱码）
    command: ["postgres", "-c", "encoding=UTF8", "-c", "lc_collate=C", "-c", "lc_ctype=C"]
```

### 三、关键说明（针对Windows）
1. **路径兼容**：
   - Windows 下 Docker Compose 会自动将相对路径 `./data` 转换为绝对路径（如 `D:\你的项目目录\data`）。
   - 若手动指定绝对路径，需用 `/` 分隔（如 `D:/项目目录/data:/var/lib/postgresql/data/pgdata`），避免反斜杠 `\` 转义问题。

2. **权限问题**：
   - Windows 下默认没有 Linux 的用户权限限制，但添加 `user: root` 可避免极少数情况下的权限报错。
   - 若 `data` 目录创建后权限异常，可手动右键→属性→安全，给当前用户分配完全控制权限。

3. **端口冲突**：
   - 若本地已安装 PostgreSQL（占用5432端口），可修改宿主机端口（如 `5433:5432`），访问时用 `localhost:5433`。

### 四、操作步骤
#### 1. 准备工作
- 确保 Windows 已安装 **Docker Desktop**（开启 WSL2 后端，否则性能较差）。
- 打开 Docker Desktop，确认服务正常运行。

#### 2. 创建配置文件
- 在项目根目录新建 `docker-compose.yml` 文件，粘贴上述配置。
- 无需手动创建 `data` 文件夹（启动时会自动生成）。

#### 3. 启动容器
- 打开 Windows 终端（CMD/PowerShell/VSCode终端），进入项目根目录：
  ```bash
  cd D:\你的项目目录  # 替换为实际路径
  ```
- 启动容器（后台运行）：
  ```bash
  docker-compose up -d
  ```

#### 4. 验证持久化
- 连接数据库（用 Navicat/DBeaver 等工具）：
  - 主机：`localhost`
  - 端口：`5432`
  - 用户名：`postgres`
  - 密码：`123456`
  - 数据库：`mydb`
- 创建测试表并插入数据：
  ```sql
  CREATE TABLE test (id INT PRIMARY KEY, name VARCHAR(20));
  INSERT INTO test VALUES (1, 'test data');
  ```
- 停止并删除容器：
  ```bash
  docker-compose down
  ```
- 重新启动容器：
  ```bash
  docker-compose up -d
  ```
- 再次连接数据库，查看 `test` 表数据是否存在（存在则持久化成功）。

### 五、常用命令
| 命令 | 说明 |
|------|------|
| `docker-compose up -d` | 启动容器（后台运行） |
| `docker-compose down` | 停止并删除容器（保留data目录，数据不丢失） |
| `docker-compose logs` | 查看容器日志（排查问题） |
| `docker-compose restart` | 重启容器 |
| `docker ps` | 查看运行中的容器 |
| `docker exec -it my-postgres bash` | 进入容器终端 |

### 六、注意事项
1. **不要手动删除 `data` 文件夹**：否则数据会全部丢失。
2. **镜像版本**：推荐使用 `alpine` 版本（体积小，性能好），避免使用 `latest`（版本不固定）。
3. **密码安全**：生产环境不要硬编码密码，可通过 `.env` 文件管理（参考 Docker Compose 环境变量配置）。
4. **WSL2 后端**：Windows 下务必开启 WSL2，否则 Docker 性能极差且可能出现路径兼容问题。

如果遇到路径报错，可将 `volumes` 中的路径改为绝对路径（示例）：
```yaml
volumes:
  - D:/my-project/data:/var/lib/postgresql/data/pgdata
```