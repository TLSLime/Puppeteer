# Puppeteer 窗口管理功能指南

## 概述

Puppeteer现在集成了强大的窗口管理功能，能够自动激活目标窗口并将鼠标定位到窗口内，确保自动化程序在正确的窗口环境中执行。

## 功能特性

### 1. 目标窗口查找
- **按标题查找**: 支持精确匹配和模糊匹配
- **按类名查找**: 根据窗口类名查找
- **按进程名查找**: 根据进程名查找窗口
- **智能过滤**: 只查找可见窗口

### 2. 窗口激活
- **自动激活**: 自动将目标窗口置于前台
- **状态恢复**: 自动恢复最小化的窗口
- **激活延迟**: 可配置的激活延迟时间

### 3. 鼠标定位
- **多种位置**: 支持中心、四角等位置
- **精确定位**: 自动计算窗口内坐标
- **平滑移动**: 自然的鼠标移动

### 4. 配置管理
- **灵活配置**: 支持多种查找方式
- **参数调整**: 可配置各种参数
- **开关控制**: 可启用/禁用窗口管理

## 使用方法

### 1. 配置文件设置

#### 基本配置
```yaml
# 窗口管理配置
window:
  enabled: true                    # 启用窗口管理
  title: "记事本"                  # 目标窗口标题
  exact_match: false              # 是否精确匹配标题
  mouse_position: "center"        # 鼠标位置
  auto_activate: true             # 自动激活窗口
  activation_delay: 0.5           # 激活延迟（秒）
```

#### 高级配置
```yaml
window:
  enabled: true
  # 查找方式（三选一）
  title: "游戏窗口"               # 按标题查找
  class_name: "GameWindow"        # 按类名查找
  process_name: "game.exe"        # 按进程名查找
  
  # 匹配选项
  exact_match: false              # 标题精确匹配
  
  # 鼠标位置选项
  mouse_position: "center"        # center, top_left, top_right, bottom_left, bottom_right
  
  # 激活选项
  auto_activate: true             # 自动激活
  activation_delay: 1.0           # 激活延迟
```

### 2. 鼠标位置选项

- **center**: 窗口中心
- **top_left**: 左上角
- **top_right**: 右上角
- **bottom_left**: 左下角
- **bottom_right**: 右下角

### 3. 查找方式

#### 按标题查找
```yaml
window:
  title: "记事本"                 # 窗口标题
  exact_match: false              # 模糊匹配
```

#### 按类名查找
```yaml
window:
  class_name: "Notepad"           # 窗口类名
```

#### 按进程名查找
```yaml
window:
  process_name: "notepad.exe"     # 进程名
```

## 实际使用示例

### 1. 记事本自动化
```yaml
# profiles/notepad_automation.yaml
window:
  enabled: true
  title: "记事本"
  exact_match: false
  mouse_position: "center"
  auto_activate: true
  activation_delay: 0.5
```

### 2. 游戏自动化
```yaml
# profiles/game_automation.yaml
window:
  enabled: true
  title: "游戏窗口"
  exact_match: false
  mouse_position: "center"
  auto_activate: true
  activation_delay: 1.0
```

### 3. 浏览器自动化
```yaml
# profiles/browser_automation.yaml
window:
  enabled: true
  title: "Chrome"
  exact_match: false
  mouse_position: "top_left"
  auto_activate: true
  activation_delay: 0.3
```

## 程序集成

### 1. 自动集成
窗口管理功能已自动集成到控制器中，启动时会自动执行：

```python
# 控制器启动时自动执行
controller.start("profile_name")
# 1. 加载配置
# 2. 启动安全监控
# 3. 激活目标窗口  ← 自动执行
# 4. 加载模板
# 5. 开始自动化
```

### 2. 手动控制
```python
from puppeteer.window_manager import WindowManager

# 创建窗口管理器
manager = WindowManager()

# 查找窗口
hwnd = manager.find_window_by_title("记事本")

# 激活窗口
manager.activate_window(hwnd)

# 移动鼠标
manager.move_mouse_to_window(hwnd, "center")
```

## 测试和验证

### 1. 基本测试
```bash
# 测试窗口管理功能
python test_window_management.py
```

### 2. 集成测试
```bash
# 测试完整流程
python main.py --mode cli --profile simple_test --safety-level disabled
```

### 3. 批处理测试
```bash
# 使用批处理文件
.\puppeteer.bat
# 选择选项 10: Test Window Management
```

## 故障排除

### 1. 常见问题

**问题**: 找不到目标窗口
**解决**: 
- 检查窗口标题是否正确
- 尝试使用模糊匹配
- 确认窗口是可见的

**问题**: 窗口激活失败
**解决**:
- 检查窗口是否被其他程序锁定
- 尝试增加激活延迟
- 确认有足够的系统权限

**问题**: 鼠标定位不准确
**解决**:
- 检查窗口位置和大小
- 尝试不同的鼠标位置选项
- 确认窗口没有被遮挡

### 2. 调试方法
```python
# 列出所有窗口
manager = WindowManager()
windows = manager.list_windows()
for window in windows:
    print(f"标题: {window['title']}, 类名: {window['class_name']}")

# 获取窗口详细信息
hwnd = manager.find_window_by_title("记事本")
if hwnd:
    info = manager.get_window_info(hwnd)
    print(f"窗口信息: {info}")
```

## 最佳实践

### 1. 配置建议
- **测试环境**: 使用简单的窗口标题
- **生产环境**: 使用精确的窗口标识
- **游戏应用**: 增加激活延迟时间
- **办公应用**: 使用中心位置定位

### 2. 性能优化
- 合理设置激活延迟
- 避免频繁的窗口查找
- 使用缓存机制存储窗口句柄

### 3. 错误处理
- 添加窗口查找失败的处理
- 实现窗口激活的重试机制
- 记录窗口操作的日志

## 技术实现

### 1. 核心API
- **Windows API**: 使用ctypes调用Windows API
- **窗口查找**: FindWindow, FindWindowEx
- **窗口操作**: SetForegroundWindow, ShowWindow
- **鼠标控制**: SetCursorPos

### 2. 模块结构
```
puppeteer/
├── window_manager.py      # 窗口管理模块
├── controller.py          # 控制器（集成窗口管理）
└── config.py             # 配置管理

profiles/
├── simple_test.yaml      # 测试配置
└── example_game.yaml     # 游戏配置
```

### 3. 数据流
```
配置文件 → 控制器 → 窗口管理器 → Windows API → 目标窗口
```

## 总结

Puppeteer的窗口管理功能提供了完整的窗口自动化解决方案：

- **智能查找**: 多种方式查找目标窗口
- **自动激活**: 确保窗口处于活跃状态
- **精确定位**: 鼠标自动定位到窗口内
- **灵活配置**: 支持各种使用场景
- **易于集成**: 自动集成到现有工作流

通过合理配置和使用窗口管理功能，可以确保自动化程序在正确的窗口环境中执行，提高自动化操作的准确性和可靠性。
