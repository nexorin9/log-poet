# Log Poet - 将系统错误消息转化为诗歌

> 将冰冷的系统错误消息转化为富有诗意的文字，探索技术文本的诗意表达

## 项目简介

Log Poet 是一个实验性工具，将系统错误消息转化为不同风格的诗歌。它旨在探索技术文本的诗意表达，发现错误信息背后隐藏的美感和结构。

## 功能特性

- **多种诗歌风格**：支持 AABB、ABAB、自由诗等多种诗歌模板
- **LLM 驱动**：集成 OpenAI API，生成更具创意的诗歌
- **交互式 CLI**：命令行界面，支持单条消息和批量处理
- **错误管理**：收集、过滤和管理系统错误消息

## 目录结构

```
log-poet/
├── README.md           # 项目说明
├── requirements.txt    # Python 依赖
├── pyproject.toml      # 项目配置
├── .env.example        # 环境变量示例
├── setup.py            # 安装脚本
├── main.py             # CLI 入口
├── poetry_generator.py # 诗歌生成器
├── llm_poetry_generator.py  # LLM 诗歌生成器
├── error_collector.py  # 错误消息收集器
├── data/               # 数据存储目录
│   ├── errors.json     # 收集的错误消息
│   └── poems.json      # 生成的诗歌
├── templates/          # 诗歌模板目录
│   ├── aabb.txt        # AABB 押韵模板
│   ├── abab.txt        # ABAB 押韵模板
│   ├── freeverse.txt   # 自由诗模板
│   └── haiku.txt       # 俳句模板
└── output/             # 输出目录
```

## 安装

### 前置要求

- Python 3.8+
- OpenAI API Key（可选，用于 LLM 生成）

### 安装步骤

1. 克隆或下载项目

2. 安装依赖
```bash
cd log-poet
pip install -r requirements.txt
```

3. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，添加你的 OpenAI API Key
```

## 使用方法

### 基本用法

```bash
# 从命令行输入生成诗歌
log-poet --input "File not found: example.txt"

# 从文件加载错误消息
log-poet --file data/errors.json

# 指定诗歌风格
log-poet --input "Error" --style aabb

# 批量生成
log-poet --batch --input data/errors.json --output data/poems.json
```

### 命令选项

| 选项 | 说明 |
|------|------|
| `--input TEXT` | 输入错误消息 |
| `--file PATH` | 从文件加载错误消息 |
| `--style STYLE` | 诗歌风格 (aabb/abab/freeverse/haiku) |
| `--batch` | 批量处理模式 |
| `--output PATH` | 输出文件路径 |
| `--save TEXT` | 保存诗歌 |
| `--load PATH` | 加载诗歌 |
| `--list-errors` | 列出所有错误消息 |
| `--filter CATEGORY` | 按类别过滤错误 |
| `--search KEYWORD` | 搜索错误消息 |

## 诗歌模板

项目提供多种诗歌模板，支持不同的韵律和风格：

- **AABB**：两两押韵，如"天/边，花/间"
- **ABAB**：交叉押韵，如"天/间，花/边"
- **Freeverse**：自由诗，无严格韵律
- **Haiku**：俳句，三行短诗（可选）

## 数据格式

### 错误消息格式 (errors.json)

```json
{
  "errors": [
    {
      "code": "ENOENT",
      "message": "File not found",
      "category": "IO"
    }
  ]
}
```

### 诗歌输出格式 (poems.json)

```json
{
  "poems": [
    {
      "error": "File not found",
      "poem": "A poem about the error",
      "style": "aabb"
    }
  ]
}
```

## 开发

### 项目结构说明

- `poetry_generator.py`：基于模板的诗歌生成器
- `llm_poetry_generator.py`：基于 LLM 的诗歌生成器
- `error_collector.py`：收集系统错误消息
- `main.py`：CLI 入口和命令处理

### 运行开发模式

```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
pytest tests/

# 运行代码检查
flake8 .
```

## 示例

### 示例 1：单条错误消息

```bash
$ log-poet --input "File not found: example.txt" --style aabb
```

输出：
```
A file was lost, in the digital night,
Searching the void with all our might,
No trace remains, in the endless space,
Just silence echoes in this empty place.
```

### 示例 2：批量生成

```bash
$ log-poet --batch --input data/errors.json --output data/poems.json
```

### 示例 3：使用 LLM 生成

```bash
$ log-poet --input "Connection timeout" --style freeverse --model gpt-4
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 致谢

灵感来源于对技术文本诗意的探索，以及对错误信息背后隐藏美学的发现。

---

## 支持作者

如果您觉得这个项目对您有帮助，欢迎打赏支持！

![Buy Me a Coffee](buymeacoffee.png)

**Buy me a coffee (crypto)**

| 币种 | 地址 |
|------|------|
| BTC | `bc1qc0f5tv577z7yt59tw8sqaq3tey98xehy32frzd` |
| ETH / USDT | `0x3b7b6c47491e4778157f0756102f134d05070704` |
| SOL | `6Xuk373zc6x6XWcAAuqvbWW92zabJdCmN3CSwpsVM6sd` |
