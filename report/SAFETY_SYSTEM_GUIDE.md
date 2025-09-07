# Puppeteer 安全系统使用指南

## 概述

Puppeteer现在集成了强大的安全系统，能够检测用户主动操作并自动停止自动化程序，防止造成非预期损失。

## 安全功能特性

### 1. 用户操作检测
- **鼠标操作检测**: 检测鼠标移动、点击等操作
- **键盘操作检测**: 检测键盘按键输入
- **实时监控**: 10ms间隔的实时监控
- **智能过滤**: 避免误判自动化程序的操作

### 2. 紧急停止功能
- **紧急停止键**: 支持ESC、F1、F12等按键
- **即时响应**: 按下紧急键立即停止程序
- **控制台提示**: 显示停止原因和操作说明

### 3. 多级安全配置
- **低安全级别**: 仅检测紧急停止键
- **中等安全级别**: 检测鼠标和键盘操作
- **高安全级别**: 检测所有用户操作

### 4. 安全事件记录
- **事件日志**: 记录所有安全事件
- **统计信息**: 提供详细的安全统计
- **调试支持**: 便于问题排查和优化

## 使用方法

### 1. 基本使用

```python
from puppeteer.safety_monitor import SafetyMonitor, SafetyLevel, SafetyEvent

# 创建安全监控器
monitor = SafetyMonitor(
    safety_level=SafetyLevel.MEDIUM,  # 安全级别
    emergency_key="esc",              # 紧急停止键
    callback=None                     # 回调函数
)

# 开始监控
monitor.start_monitoring()

# 停止监控
monitor.stop_monitoring()
```

### 2. 安全管理器

```python
from puppeteer.safety_monitor import SafetyManager, SafetyLevel

# 创建安全管理器
manager = SafetyManager(SafetyLevel.MEDIUM)

# 启动安全监控
manager.start_safety_monitoring()

# 启动自动化
manager.start_automation()

# 检查状态
if manager.is_automation_running():
    print("自动化正在运行")
    
if manager.is_safety_monitoring():
    print("安全监控已启动")

# 停止自动化
manager.stop_automation("manual_stop")

# 停止安全监控
manager.stop_safety_monitoring()
```

### 3. 控制器集成

```python
from puppeteer.controller import PuppeteerController
from puppeteer.safety_monitor import SafetyLevel

# 创建带安全系统的控制器
controller = PuppeteerController(
    config_manager=config_manager,
    logger=logger,
    safety_level=SafetyLevel.MEDIUM
)

# 启动控制器（自动启动安全监控）
controller.start("profile_name")

# 获取安全统计
safety_stats = controller.get_safety_stats()
print(f"安全统计: {safety_stats}")

# 设置安全级别
controller.set_safety_level(SafetyLevel.HIGH)
```

## 安全级别说明

### LOW (低安全级别)
- **功能**: 仅检测紧急停止键
- **适用场景**: 完全受控环境，用户不会意外操作
- **性能影响**: 最小
- **使用建议**: 测试环境或完全自动化场景

### MEDIUM (中等安全级别)
- **功能**: 检测紧急停止键 + 鼠标和键盘操作
- **适用场景**: 一般使用场景，平衡安全性和性能
- **性能影响**: 中等
- **使用建议**: 推荐用于大多数场景

### HIGH (高安全级别)
- **功能**: 检测所有用户操作
- **适用场景**: 高风险环境，需要最高安全性
- **性能影响**: 较高
- **使用建议**: 生产环境或关键任务

## 紧急停止键配置

### 支持的按键
```python
# 功能键
"esc"    # ESC键（推荐）
"f1"     # F1键
"f12"    # F12键

# 常用键
"space"  # 空格键
"enter"  # 回车键
"tab"    # Tab键

# 修饰键
"shift"  # Shift键
"ctrl"   # Ctrl键
"alt"    # Alt键
```

### 配置示例
```python
# 使用ESC键作为紧急停止
monitor = SafetyMonitor(SafetyLevel.MEDIUM, "esc")

# 使用F1键作为紧急停止
monitor = SafetyMonitor(SafetyLevel.MEDIUM, "f1")

# 使用空格键作为紧急停止
monitor = SafetyMonitor(SafetyLevel.MEDIUM, "space")
```

## 安全事件处理

### 1. 事件类型
```python
from puppeteer.safety_monitor import SafetyEvent

# 鼠标移动事件
SafetyEvent.MOUSE_MOVE

# 鼠标点击事件
SafetyEvent.MOUSE_CLICK

# 键盘输入事件
SafetyEvent.KEYBOARD_INPUT

# 紧急停止事件
SafetyEvent.EMERGENCY_STOP
```

### 2. 事件回调
```python
def safety_callback(event_type, data):
    """安全事件回调函数"""
    if event_type == SafetyEvent.EMERGENCY_STOP:
        print(f"紧急停止: {data['key']}")
    elif event_type == SafetyEvent.MOUSE_MOVE:
        print("检测到鼠标操作")
    elif event_type == SafetyEvent.KEYBOARD_INPUT:
        print("检测到键盘操作")

# 创建带回调的监控器
monitor = SafetyMonitor(
    SafetyLevel.MEDIUM, 
    "esc", 
    safety_callback
)
```

## 配置选项

### 1. 安全管理器配置
```python
config = {
    "emergency_key": "esc",           # 紧急停止键
    "user_activity_threshold": 0.1,   # 用户活动检测阈值（秒）
    "auto_restart": False,            # 是否自动重启
    "log_safety_events": True         # 是否记录安全事件
}

manager.set_config(config)
```

### 2. 监控器配置
```python
# 设置用户活动检测阈值
monitor.set_user_activity_threshold(0.05)  # 50ms

# 设置安全级别
monitor.set_safety_level(SafetyLevel.HIGH)

# 设置紧急停止键
monitor.set_emergency_key("f1")
```

## 统计信息

### 1. 获取统计信息
```python
# 获取安全统计
stats = monitor.get_stats()
print(f"鼠标事件: {stats['mouse_events']}")
print(f"键盘事件: {stats['keyboard_events']}")
print(f"紧急停止: {stats['emergency_stops']}")
print(f"总事件数: {stats['total_events']}")

# 重置统计
monitor.reset_stats()
```

### 2. 控制器状态
```python
status = controller.get_status()
print(f"安全级别: {status['safety_level']}")
print(f"安全统计: {status['safety_stats']}")
```

## 日志记录

### 1. 安全事件日志
```python
# 安全事件会自动记录到日志
# 日志格式：
{
    "timestamp": 1234567890.123,
    "type": "safety_event",
    "event_type": "emergency_stop",
    "data": {
        "reason": "emergency_key_pressed",
        "key": "esc",
        "timestamp": 1234567890.123
    }
}
```

### 2. 查看日志
```python
# 获取最近的安全事件日志
recent_logs = logger.get_recent_logs(count=50, log_type="safety_event")
for log in recent_logs:
    print(f"安全事件: {log['event_type']} - {log['data']}")
```

## 最佳实践

### 1. 安全级别选择
- **开发测试**: 使用LOW级别
- **日常使用**: 使用MEDIUM级别
- **生产环境**: 使用HIGH级别

### 2. 紧急停止键选择
- **推荐**: ESC键（最常用，不易误触）
- **备选**: F1键（功能键，不易误触）
- **避免**: 常用字母键（容易误触）

### 3. 监控配置
- **检测阈值**: 0.1秒（100ms）适合大多数场景
- **回调函数**: 用于自定义处理逻辑
- **日志记录**: 建议开启，便于问题排查

### 4. 错误处理
```python
try:
    monitor.start_monitoring()
    # 执行自动化任务
except KeyboardInterrupt:
    print("用户中断")
    monitor.stop_monitoring()
except Exception as e:
    print(f"安全系统异常: {e}")
    monitor.stop_monitoring()
finally:
    # 确保监控停止
    if monitor.is_monitoring():
        monitor.stop_monitoring()
```

## 故障排除

### 1. 常见问题

**问题**: 安全监控无法启动
**解决**: 检查Windows API权限，确保程序有足够权限

**问题**: 误判用户操作
**解决**: 调整用户活动检测阈值，或降低安全级别

**问题**: 紧急停止键不响应
**解决**: 检查按键映射，确保使用支持的按键

### 2. 调试方法
```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 检查监控状态
print(f"监控状态: {monitor.is_monitoring()}")
print(f"统计信息: {monitor.get_stats()}")

# 测试按键检测
vk_code = monitor.VK_CODES.get("esc")
print(f"ESC键码: 0x{vk_code:02X}")
```

## 总结

Puppeteer的安全系统提供了全面的保护机制：

- **实时监控**: 10ms间隔的实时用户操作检测
- **多级安全**: 三种安全级别适应不同场景
- **紧急停止**: 支持多种紧急停止键
- **事件记录**: 完整的安全事件日志
- **统计信息**: 详细的安全统计和监控
- **易于集成**: 简单的API和配置选项

通过合理配置和使用安全系统，可以确保Puppeteer在自动化过程中不会造成非预期的系统损失，为用户提供安全可靠的桌面自动化体验。
