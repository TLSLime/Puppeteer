# 高级输入功能使用示例

## 概述

Puppeteer现在支持强大的高级输入功能，包括：
- 单次按键和长按操作
- 组合键和同时按键
- 鼠标点击、拖拽、滚轮
- 游戏手柄按钮和摇杆模拟
- 宏操作和组合操作

## 基本使用

### 1. 高级输入管理器

```python
from puppeteer.advanced_input import AdvancedInputManager

# 创建管理器
manager = AdvancedInputManager(humanize_enabled=True)

# 单次按键
manager.press_key("space")

# 长按按键（0.5秒）
manager.press_key("a", duration=0.5)

# 组合键
manager.press_key_combination(["ctrl", "c"])

# 同时按键
manager.press_key_simultaneous(["shift", "tab"])

# 文本输入
manager.type_text_with_delay("Hello World")
```

### 2. 鼠标操作

```python
# 普通点击
manager.click(400, 300)

# 长按点击（0.5秒）
manager.click(400, 300, duration=0.5)

# 拖拽
manager.drag(100, 100, 200, 200)

# 滚轮
manager.scroll(400, 300, "up", 3)
```

### 3. 游戏手柄操作

```python
# 游戏手柄按钮
manager.press_gamepad_button("a")
manager.press_gamepad_button("b", duration=0.5)

# 摇杆操作
manager.move_gamepad_stick("left", "up", 0.5)
```

## 游戏手柄模拟器

### 1. Xbox手柄

```python
from puppeteer.gamepad_simulator import GamepadSimulator, GamepadType, GamepadButton, GamepadStick

# 创建Xbox手柄模拟器
xbox = GamepadSimulator(GamepadType.XBOX, humanize_enabled=True)

# 按钮操作
xbox.press_button(GamepadButton.A)  # A按钮
xbox.press_button(GamepadButton.B, duration=0.5)  # 长按B按钮
xbox.press_button(GamepadButton.X)  # X按钮
xbox.press_button(GamepadButton.Y)  # Y按钮

# 肩键和扳机
xbox.press_button(GamepadButton.LB)  # 左肩键
xbox.press_button(GamepadButton.RB)  # 右肩键
xbox.set_trigger("lt", 0.8)  # 左扳机
xbox.set_trigger("rt", 0.6)  # 右扳机

# 摇杆操作
xbox.move_stick(GamepadStick.LEFT, 0.5, 0.5)  # 左摇杆
xbox.move_stick(GamepadStick.RIGHT, -0.3, 0.7)  # 右摇杆

# 方向键
xbox.press_button(GamepadButton.DPAD_UP)
xbox.press_button(GamepadButton.DPAD_DOWN)
xbox.press_button(GamepadButton.DPAD_LEFT)
xbox.press_button(GamepadButton.DPAD_RIGHT)
```

### 2. PlayStation手柄

```python
# 创建PlayStation手柄模拟器
ps = GamepadSimulator(GamepadType.PLAYSTATION, humanize_enabled=True)

# PlayStation按钮
ps.press_button(GamepadButton.CROSS)    # X按钮
ps.press_button(GamepadButton.CIRCLE)   # O按钮
ps.press_button(GamepadButton.SQUARE)   # □按钮
ps.press_button(GamepadButton.TRIANGLE) # △按钮

# 肩键
ps.press_button(GamepadButton.L1)  # L1
ps.press_button(GamepadButton.R1)  # R1
ps.press_button(GamepadButton.L2)  # L2
ps.press_button(GamepadButton.R2)  # R2
```

## 宏操作

### 1. 基本宏操作

```python
# 定义宏
macro = [
    {"type": "key_press", "key": "space"},
    {"type": "delay", "delay": 0.1},
    {"type": "mouse_click", "x": 400, "y": 300},
    {"type": "delay", "delay": 0.1},
    {"type": "type_text", "text": "Hello"},
    {"type": "delay", "delay": 0.1},
    {"type": "key_press", "key": "enter"}
]

# 执行宏
results = manager.execute_macro(macro)
```

### 2. 游戏手柄组合操作

```python
# 游戏手柄组合操作
combo = [
    {"type": "button_press", "button": "a"},
    {"type": "delay", "delay": 0.1},
    {"type": "stick_move", "stick": "left", "x": 1.0, "y": 0.0},
    {"type": "delay", "delay": 0.2},
    {"type": "button_press", "button": "b"},
    {"type": "delay", "delay": 0.1},
    {"type": "trigger_set", "trigger": "lt", "value": 0.5}
]

# 执行组合操作
success = xbox.execute_combo(combo)
```

## 游戏场景示例

### 1. 动作游戏

```python
# 角色移动
def move_character(direction, duration=0.5):
    if direction == "forward":
        manager.move_gamepad_stick("left", "up", 1.0)
    elif direction == "backward":
        manager.move_gamepad_stick("left", "down", 1.0)
    elif direction == "left":
        manager.move_gamepad_stick("left", "left", 1.0)
    elif direction == "right":
        manager.move_gamepad_stick("left", "right", 1.0)

# 攻击组合
def attack_combo():
    combo = [
        {"type": "button_press", "button": "x"},  # 轻攻击
        {"type": "delay", "delay": 0.1},
        {"type": "button_press", "button": "y"},  # 重攻击
        {"type": "delay", "delay": 0.1},
        {"type": "button_press", "button": "a"},  # 跳跃
        {"type": "delay", "delay": 0.1},
        {"type": "button_press", "button": "x"}   # 空中攻击
    ]
    return xbox.execute_combo(combo)

# 使用示例
move_character("forward", 1.0)
attack_combo()
```

### 2. 策略游戏

```python
# 选择单位
def select_unit(x, y):
    manager.click(x, y)

# 移动单位
def move_unit(start_x, start_y, end_x, end_y):
    manager.drag(start_x, start_y, end_x, end_y)

# 快捷键操作
def use_hotkey(hotkey):
    if hotkey == "attack":
        manager.press_key_combination(["ctrl", "a"])
    elif hotkey == "move":
        manager.press_key_combination(["ctrl", "m"])
    elif hotkey == "stop":
        manager.press_key("s")

# 使用示例
select_unit(100, 100)
move_unit(100, 100, 200, 200)
use_hotkey("attack")
```

### 3. 射击游戏

```python
# 瞄准和射击
def aim_and_shoot(target_x, target_y):
    # 瞄准
    manager.move_mouse(target_x, target_y)
    # 射击
    manager.press_gamepad_button("rt", duration=0.1)

# 换弹
def reload():
    manager.press_gamepad_button("r")

# 切换武器
def switch_weapon():
    manager.press_gamepad_button("y")

# 使用示例
aim_and_shoot(400, 300)
reload()
switch_weapon()
```

## 配置和优化

### 1. 人性化配置

```python
# 设置人性化参数
config = {
    "key_delay_range": (0.05, 0.12),
    "mouse_delay_range": (0.02, 0.08),
    "click_delay_range": (0.01, 0.05),
    "hold_repeat_interval": 0.1,
    "movement_jitter": 1,
    "timing_jitter": 0.01
}

manager.set_humanize_config(config)
```

### 2. 性能优化

```python
# 关闭人性化以提高性能
manager = AdvancedInputManager(humanize_enabled=False)

# 批量操作
def batch_operations():
    operations = [
        {"type": "key_press", "key": "space"},
        {"type": "key_press", "key": "enter"},
        {"type": "key_press", "key": "tab"}
    ]
    return manager.execute_macro(operations)
```

## 状态管理

### 1. 检查状态

```python
# 检查按键状态
key_state = manager.get_key_state("space")
if key_state:
    print(f"按键被按住: {key_state['duration']}秒")

# 检查鼠标状态
mouse_state = manager.get_mouse_state("left", 400, 300)
if mouse_state:
    print(f"鼠标被按住: {mouse_state['duration']}秒")

# 检查游戏手柄状态
button_state = xbox.get_button_state(GamepadButton.A)
if button_state:
    print(f"按钮被按下: {button_state['timestamp']}")
```

### 2. 停止操作

```python
# 停止所有长按操作
manager.stop_all_holds()

# 重置游戏手柄状态
xbox.reset()
```

## 错误处理

```python
try:
    # 执行操作
    success = manager.press_key("space")
    if not success:
        print("按键操作失败")
        
    # 执行宏操作
    results = manager.execute_macro(macro)
    failed_count = sum(1 for r in results if not r["success"])
    if failed_count > 0:
        print(f"宏操作中有{failed_count}个步骤失败")
        
except Exception as e:
    print(f"操作异常: {e}")
```

## 测试和调试

```python
# 运行完整测试
python test_advanced_input_complete.py

# 运行简化测试
python test_input_simple.py

# 运行游戏手柄测试
python -c "from puppeteer.gamepad_simulator import test_gamepad_simulator; test_gamepad_simulator()"
```

## 总结

高级输入功能为Puppeteer提供了强大的桌面自动化能力：

- **键盘操作**: 支持单次、长按、组合键、同时按键
- **鼠标操作**: 支持点击、拖拽、滚轮、长按
- **游戏手柄**: 支持Xbox、PlayStation等主流手柄
- **宏操作**: 支持复杂的操作序列
- **人性化**: 可配置的延迟和抖动参数
- **高性能**: 优化的输入处理速度

这些功能使得Puppeteer能够适应各种复杂的桌面自动化场景，特别是游戏和应用程序的自动化操作。
