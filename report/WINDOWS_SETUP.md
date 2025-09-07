# Puppeteer Windows 安装和使用指南

## 系统要求

- Windows 10/11
- Python 3.7 或更高版本
- 管理员权限（用于输入控制）

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 验证安装

```bash
python quick_test.py
```

### 3. 启动程序

**方式一：使用批处理文件（推荐）**
```bash
start_puppeteer.bat
```

**方式二：直接启动图形界面**
```bash
python main.py
```

**方式三：命令行模式**
```bash
python main.py --mode cli --profile simple_test
```

## 功能验证

### 已验证的功能

✅ **截屏模块** - 使用 mss 库实现高性能截屏  
✅ **视觉识别模块** - 基于 OpenCV 的模板匹配  
✅ **输入控制模块** - 支持鼠标键盘操作和人性化参数  
✅ **配置管理模块** - YAML 配置文件解析和管理  
✅ **日志记录模块** - 结构化日志记录（JSONL格式）  
✅ **图形界面** - 基于 Tkinter 的用户界面  
✅ **主控制器** - 完整的自动化流程控制  

### 测试结果

```
通过测试: 3/3
✓ 所有测试通过! Puppeteer 可以在 Windows 上正常运行
```

## 使用说明

### 1. 图形界面模式

启动图形界面后，您可以：
- 创建和管理配置文件
- 启动/停止自动化任务
- 查看实时日志和状态
- 执行宏操作

### 2. 命令行模式

```bash
# 使用简化配置（无需模板文件）
python main.py --mode cli --profile simple_test

# 使用完整配置（需要模板文件）
python main.py --mode cli --profile example_game
```

### 3. 配置文件

配置文件位于 `profiles/` 目录：
- `simple_test.yaml` - 简化测试配置，无需模板文件
- `example_game.yaml` - 完整示例配置，需要模板文件

### 4. 模板文件

模板文件应放在 `assets/` 目录中。参考 `assets/README.md` 了解如何制作模板。

## 常见问题

### Q: 程序启动失败
A: 确保已安装所有依赖：`pip install -r requirements.txt`

### Q: 输入控制不工作
A: 确保以管理员权限运行程序

### Q: 模板匹配失败
A: 检查模板文件是否存在，路径是否正确

### Q: 日志文件被锁定
A: 这是Windows系统的正常现象，不影响程序运行

## 开发模式

### 运行测试
```bash
python test_modules.py
```

### 运行演示
```bash
python run_demo.py
```

### 快速验证
```bash
python quick_test.py
```

## 项目结构

```
re-Puppeteer/
├── puppeteer/              # 核心模块
├── profiles/               # 配置文件
├── assets/                 # 模板资源
├── main.py                 # 主程序入口
├── start_puppeteer.bat     # Windows启动脚本
├── quick_test.py           # 快速验证脚本
└── requirements.txt        # 依赖列表
```

## 技术支持

如果遇到问题，请检查：
1. Python版本是否符合要求
2. 所有依赖是否正确安装
3. 是否有足够的系统权限
4. 配置文件格式是否正确

## 注意事项

- 请确保在合规的环境中使用本程序
- 避免违反游戏服务条款
- 建议在测试环境中先验证功能
- 定期备份配置文件
