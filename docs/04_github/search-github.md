你希望我将这5个GitHub搜索相关功能的输入参数和输出信息整理成一个清晰的表格，方便你快速查阅每个功能的使用规范。

### GitHub搜索功能输入输出对照表
| 功能名称          | 功能描述                                                                 | 必填输入参数 | 可选输入参数                                                                 | 输出说明                                                                 |
|-------------------|--------------------------------------------------------------------------|--------------|------------------------------------------------------------------------------|--------------------------------------------------------------------------|
| `search_code`     | 跨所有GitHub仓库快速精准搜索代码，适用于查找精确的符号、函数、类或特定代码模式 | `query`      | `order`（asc/desc）、`page`（≥1）、`perPage`（1-100）、`sort`（仅indexed）    | `outputSchema`为null，输出GitHub原生代码搜索结果（含代码片段、仓库信息等） |
| `search_issues`   | 搜索GitHub仓库中的issues，搜索语法自动限定为`is:issue`                    | `query`      | `order`（asc/desc）、`owner`、`page`（≥1）、`perPage`（1-100）、`repo`、`sort`（comments/reactions/created等） | `outputSchema`为null，输出符合条件的GitHub Issues列表                   |
| `search_pull_requests` | 搜索GitHub仓库中的PR，搜索语法自动限定为`is:pr`                          | `query`      | `order`（asc/desc）、`owner`、`page`（≥1）、`perPage`（1-100）、`repo`、`sort`（comments/reactions/created等） | `outputSchema`为null，输出符合条件的GitHub Pull Requests列表            |
| `search_repositories` | 按名称、描述、README、主题等元数据查找GitHub仓库，用于发现项目/示例        | `query`      | `minimal_output`（布尔，默认true）、`order`（asc/desc）、`page`（≥1）、`perPage`（1-100）、`sort`（stars/forks/updated等） | `outputSchema`为null，默认输出精简的仓库信息，false时输出完整GitHub仓库API对象 |
| `search_users`    | 按用户名、真实姓名等资料查找GitHub用户，用于定位开发者/贡献者             | `query`      | `order`（asc/desc）、`page`（≥1）、`perPage`（1-100）、`sort`（followers/repositories/joined） | `outputSchema`为null，输出符合条件的GitHub用户信息列表                   |

### 总结
1. **核心共性**：所有功能的**必填参数均为`query`**（指定搜索语法），且都支持分页（`page`/`perPage`）和排序（`order`/`sort`）参数。
2. **参数差异**：仅`search_repositories`有`minimal_output`参数；`search_issues`/`search_pull_requests`支持`owner`/`repo`限定仓库；各功能的`sort`枚举值随搜索类型不同有专属配置。
3. **输出统一**：所有功能的`outputSchema`均为null，输出内容为对应类型的GitHub原生搜索结果（代码/Issues/PR/仓库/用户）。
