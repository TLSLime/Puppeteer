# Puppeteer - 桌面程序自动化操控系统

一个轻量化、可配置的通用"操控臂"系统，通过屏幕级感知 + 通用控制库 + 配置驱动的策略，实现对桌面程序/2D游戏的自动化操控。

## 功能特性

- **屏幕级感知**: 使用 mss + OpenCV 实现高效的屏幕截取和模板匹配
- **配置驱动**: 通过 YAML 配置文件快速适配不同游戏/软件
- **人性化输入**: 支持随机延迟、抖动等参数，模拟真实用户操作
- **结构化日志**: JSONL 格式日志记录，支持回放和分析
- **图形界面**: 基于 Tkinter 的最小控制面板
- **模块化设计**: 各模块独立，便于扩展和替换

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

### 1. 启动图形界面

```bash
python main.py
```

### 2. 命令行模式

```bash
python main.py --mode cli --profile example_game
```

### 3. 创建配置文件

在图形界面中点击"创建配置"按钮，或手动创建 `profiles/example_game.yaml`:

```yaml
profile: example_game
description: 示例游戏配置
screen_region: [0, 0, 1920, 1080]
keymap:
  attack: 'q'
  jump: 'space'
  move_left: 'a'
  move_right: 'd'
templates:
  enemies: ["enemy1.png", "enemy2.png"]
  items: ["item1.png", "item2.png"]
  ui_elements: ["health_bar.png", "mana_bar.png"]
rois:
  enemy1.png: [100, 100, 800, 600]
  enemy2.png: [100, 100, 800, 600]
detection:
  scene: "dungeon"
  templates:
    enemies: ["enemy1.png", "enemy2.png"]
    items: ["item1.png", "item2.png"]
    ui_elements: ["health_bar.png", "mana_bar.png"]
  self_status:
    health: "health_bar.png"
    mana: "mana_bar.png"
macros:
  combo1: ["attack", "jump", "attack"]
  combo2: ["move_left", "attack", "move_right"]
humanize:
  enabled: true
  mouse_delay_range: [50, 150]
  key_delay_range: [80, 140]
  click_delay_range: [20, 80]
  movement_jitter: 2
  timing_jitter: 20
controller:
  fps_limit: 10
  action_cooldown: 0.1
  confidence_threshold: 0.8
```

## 项目结构

```
puppeteer/
├── __init__.py          # 包初始化
├── capture.py           # 截屏模块
├── vision.py            # 视觉识别模块
├── input_provider.py    # 输入控制模块
├── config.py            # 配置管理模块
├── controller.py        # 主控制器
├── logger.py            # 日志记录模块
└── ui.py                # 用户界面模块

profiles/                # 配置文件目录
├── example_game.yaml    # 示例配置
└── ...

assets/                  # 模板资源目录
├── enemy1.png          # 敌人模板
├── enemy2.png
├── item1.png           # 物品模板
└── ...

logs/                    # 日志目录
├── puppeteer-2024-01-01.jsonl
└── ...

main.py                  # 主程序入口
requirements.txt         # 依赖包列表
README.md               # 说明文档
```

## 核心模块说明

### 1. 截屏模块 (capture.py)
- 使用 mss 库实现高性能截屏
- 支持全屏或指定区域截取
- 内置帧率控制和性能优化

### 2. 视觉识别模块 (vision.py)
- 基于 OpenCV 的模板匹配
- 支持多模板、ROI 区域检测
- 输出结构化 Observation 数据

### 3. 输入控制模块 (input_provider.py)
- 封装 PyAutoGUI 实现鼠标键盘控制
- 支持人性化参数（延迟、抖动）
- 提供动作冷却和节流功能

### 4. 配置管理模块 (config.py)
- YAML 配置文件解析和管理
- 支持配置验证和默认值
- 提供配置热切换功能

### 5. 主控制器 (controller.py)
- 协调各模块的主循环
- 实现截屏→识别→决策→动作的完整流程
- 支持启动/停止/暂停/恢复控制

### 6. 日志记录模块 (logger.py)
- 结构化日志记录（JSONL 格式）
- 支持动作、观察、系统、错误日志
- 提供日志导出和回放功能

### 7. 用户界面 (ui.py)
- 基于 Tkinter 的图形界面
- 提供配置管理、运行控制、状态监控
- 支持实时日志显示和宏执行

## 使用说明

### 1. 准备模板图片
将需要识别的游戏元素截图保存到 `assets/` 目录，如：
- `enemy1.png` - 敌人模板
- `item1.png` - 物品模板
- `health_bar.png` - 血量条模板

### 2. 配置检测区域
在配置文件中设置 `rois` 字段，指定各模板的检测区域：
```yaml
rois:
  enemy1.png: [100, 100, 800, 600]  # [x, y, width, height]
```

### 3. 设置按键映射
配置 `keymap` 字段，定义游戏中的按键：
```yaml
keymap:
  attack: 'q'
  jump: 'space'
```

### 4. 启动自动化
1. 运行 `python main.py` 启动图形界面
2. 选择或创建配置文件
3. 点击"开始"按钮启动自动化
4. 观察日志输出和运行状态

## 高级功能

### 宏操作
定义复杂的按键序列：
```yaml
macros:
  combo1: ["attack", "jump", "attack"]
  combo2: ["move_left", "attack", "move_right"]
```

### 人性化参数
调整操作的真实感：
```yaml
humanize:
  enabled: true
  mouse_delay_range: [50, 150]    # 鼠标延迟范围(ms)
  key_delay_range: [80, 140]      # 按键延迟范围(ms)
  movement_jitter: 2              # 移动抖动像素
```

### 日志分析
查看 JSONL 格式的详细日志：
```bash
# 查看今天的日志
cat logs/puppeteer-$(date +%Y-%m-%d).jsonl | jq '.'
```

## 注意事项

1. **合规使用**: 请确保在合规的环境中使用，避免违反游戏服务条款
2. **性能优化**: 根据实际需求调整 `fps_limit` 和 `confidence_threshold`
3. **模板质量**: 模板图片质量直接影响识别准确率
4. **系统兼容**: 目前主要支持 Windows 系统

## 开发计划

- [ ] 支持更多输入库（PyDirectInput、pynput）
- [ ] 集成轻量级目标检测模型
- [ ] 添加行为树/状态机决策引擎
- [ ] 实现 Web Dashboard 界面
- [ ] 支持插件系统和配置市场

## 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进项目。
