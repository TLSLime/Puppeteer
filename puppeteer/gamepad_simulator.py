# -*- coding: utf-8 -*-
"""
游戏手柄模拟器 - 专业的游戏手柄输入模拟
支持Xbox、PlayStation等主流手柄的按键和摇杆模拟
"""

import time
import random
import threading
import ctypes
import ctypes.wintypes
from typing import Dict, List, Optional, Tuple, Any, Union
from enum import Enum
import math


class GamepadType(Enum):
    """游戏手柄类型"""
    XBOX = "xbox"
    PLAYSTATION = "playstation"
    GENERIC = "generic"


class GamepadButton(Enum):
    """游戏手柄按钮"""
    # Xbox按钮
    A = "a"
    B = "b"
    X = "x"
    Y = "y"
    LB = "lb"  # Left Bumper
    RB = "rb"  # Right Bumper
    LT = "lt"  # Left Trigger
    RT = "rt"  # Right Trigger
    START = "start"
    SELECT = "select"
    L3 = "l3"  # Left Stick
    R3 = "r3"  # Right Stick
    DPAD_UP = "dpad_up"
    DPAD_DOWN = "dpad_down"
    DPAD_LEFT = "dpad_left"
    DPAD_RIGHT = "dpad_right"
    
    # PlayStation按钮
    CROSS = "cross"      # A
    CIRCLE = "circle"    # B
    SQUARE = "square"    # X
    TRIANGLE = "triangle" # Y
    L1 = "l1"            # LB
    R1 = "r1"            # RB
    L2 = "l2"            # LT
    R2 = "r2"            # RT
    OPTIONS = "options"  # START
    SHARE = "share"      # SELECT
    L3_PS = "l3_ps"      # Left Stick
    R3_PS = "r3_ps"      # Right Stick


class GamepadStick(Enum):
    """游戏手柄摇杆"""
    LEFT = "left"
    RIGHT = "right"


class GamepadSimulator:
    """游戏手柄模拟器"""
    
    def __init__(self, gamepad_type: GamepadType = GamepadType.XBOX, 
                 humanize_enabled: bool = True):
        """
        初始化游戏手柄模拟器
        
        Args:
            gamepad_type: 游戏手柄类型
            humanize_enabled: 是否启用人性化参数
        """
        self.gamepad_type = gamepad_type
        self.humanize_enabled = humanize_enabled
        self._lock = threading.Lock()
        
        # 按键状态跟踪
        self._button_states = {}
        self._stick_states = {}
        
        # 按键映射
        self._init_button_mappings()
        
        # 人性化配置
        self.humanize_config = {
            "button_delay_range": (0.05, 0.12),
            "stick_delay_range": (0.02, 0.08),
            "trigger_delay_range": (0.01, 0.05),
            "movement_jitter": 0.05,
            "timing_jitter": 0.01
        }
        
        print(f"游戏手柄模拟器初始化完成 - 类型: {gamepad_type.value}")
        
    def _init_button_mappings(self):
        """初始化按键映射"""
        # Xbox到键盘的映射
        self.xbox_mapping = {
            GamepadButton.A: "space",
            GamepadButton.B: "esc",
            GamepadButton.X: "x",
            GamepadButton.Y: "y",
            GamepadButton.LB: "q",
            GamepadButton.RB: "e",
            GamepadButton.LT: "shift",
            GamepadButton.RT: "ctrl",
            GamepadButton.START: "enter",
            GamepadButton.SELECT: "tab",
            GamepadButton.L3: "f1",
            GamepadButton.R3: "f2",
            GamepadButton.DPAD_UP: "up",
            GamepadButton.DPAD_DOWN: "down",
            GamepadButton.DPAD_LEFT: "left",
            GamepadButton.DPAD_RIGHT: "right"
        }
        
        # PlayStation到键盘的映射
        self.playstation_mapping = {
            GamepadButton.CROSS: "space",
            GamepadButton.CIRCLE: "esc",
            GamepadButton.SQUARE: "x",
            GamepadButton.TRIANGLE: "y",
            GamepadButton.L1: "q",
            GamepadButton.R1: "e",
            GamepadButton.L2: "shift",
            GamepadButton.R2: "ctrl",
            GamepadButton.OPTIONS: "enter",
            GamepadButton.SHARE: "tab",
            GamepadButton.L3_PS: "f1",
            GamepadButton.R3_PS: "f2",
            GamepadButton.DPAD_UP: "up",
            GamepadButton.DPAD_DOWN: "down",
            GamepadButton.DPAD_LEFT: "left",
            GamepadButton.DPAD_RIGHT: "right"
        }
        
        # 通用映射
        self.generic_mapping = {
            GamepadButton.A: "space",
            GamepadButton.B: "esc",
            GamepadButton.X: "x",
            GamepadButton.Y: "y",
            GamepadButton.LB: "q",
            GamepadButton.RB: "e",
            GamepadButton.LT: "shift",
            GamepadButton.RT: "ctrl",
            GamepadButton.START: "enter",
            GamepadButton.SELECT: "tab",
            GamepadButton.L3: "f1",
            GamepadButton.R3: "f2",
            GamepadButton.DPAD_UP: "up",
            GamepadButton.DPAD_DOWN: "down",
            GamepadButton.DPAD_LEFT: "left",
            GamepadButton.DPAD_RIGHT: "right"
        }
        
    def _get_button_mapping(self) -> Dict[GamepadButton, str]:
        """获取当前手柄类型的按键映射"""
        if self.gamepad_type == GamepadType.XBOX:
            return self.xbox_mapping
        elif self.gamepad_type == GamepadType.PLAYSTATION:
            return self.playstation_mapping
        else:
            return self.generic_mapping
            
    def _apply_humanize_delay(self, base_delay: float) -> float:
        """应用人性化延迟"""
        if not self.humanize_enabled:
            return base_delay
            
        jitter = random.uniform(-self.humanize_config["timing_jitter"], 
                               self.humanize_config["timing_jitter"])
        return max(0, base_delay + jitter)
        
    def _press_key(self, key: str, duration: Optional[float] = None) -> bool:
        """按下键盘按键（内部方法）"""
        try:
            # 这里应该调用实际的键盘输入方法
            # 为了简化，我们使用模拟的方式
            if duration is None:
                print(f"模拟按下按键: {key}")
                time.sleep(0.01)
            else:
                print(f"模拟长按按键: {key} ({duration}秒)")
                time.sleep(duration)
            return True
        except Exception as e:
            print(f"按键操作失败: {e}")
            return False
            
    def press_button(self, button: GamepadButton, duration: Optional[float] = None) -> bool:
        """
        按下游戏手柄按钮
        
        Args:
            button: 按钮类型
            duration: 按住时长，None为单次按下
            
        Returns:
            是否执行成功
        """
        try:
            with self._lock:
                # 获取按键映射
                mapping = self._get_button_mapping()
                key = mapping.get(button)
                
                if key is None:
                    print(f"不支持的按钮: {button.value}")
                    return False
                    
                # 应用延迟
                if duration is None:
                    delay = random.uniform(*self.humanize_config["button_delay_range"])
                else:
                    delay = random.uniform(*self.humanize_config["trigger_delay_range"])
                    
                delay = self._apply_humanize_delay(delay)
                time.sleep(delay)
                
                # 执行按键操作
                success = self._press_key(key, duration)
                
                if success:
                    # 记录状态
                    self._button_states[button] = {
                        "pressed": True,
                        "timestamp": time.time(),
                        "duration": duration
                    }
                    
                return success
                
        except Exception as e:
            print(f"按钮操作失败: {e}")
            return False
            
    def release_button(self, button: GamepadButton) -> bool:
        """
        释放游戏手柄按钮
        
        Args:
            button: 按钮类型
            
        Returns:
            是否执行成功
        """
        try:
            with self._lock:
                if button in self._button_states:
                    del self._button_states[button]
                    print(f"释放按钮: {button.value}")
                    return True
                else:
                    print(f"按钮未被按下: {button.value}")
                    return False
                    
        except Exception as e:
            print(f"释放按钮失败: {e}")
            return False
            
    def move_stick(self, stick: GamepadStick, x: float, y: float, 
                   duration: Optional[float] = None) -> bool:
        """
        移动游戏手柄摇杆
        
        Args:
            stick: 摇杆类型
            x: X轴值 (-1.0 到 1.0)
            y: Y轴值 (-1.0 到 1.0)
            duration: 移动时长
            
        Returns:
            是否执行成功
        """
        try:
            with self._lock:
                # 限制值范围
                x = max(-1.0, min(1.0, x))
                y = max(-1.0, min(1.0, y))
                
                # 应用人性化抖动
                if self.humanize_enabled:
                    jitter = self.humanize_config["movement_jitter"]
                    x += random.uniform(-jitter, jitter)
                    y += random.uniform(-jitter, jitter)
                    x = max(-1.0, min(1.0, x))
                    y = max(-1.0, min(1.0, y))
                
                # 计算移动方向
                if abs(x) > 0.1 or abs(y) > 0.1:
                    # 确定主要方向
                    if abs(x) > abs(y):
                        direction = "right" if x > 0 else "left"
                    else:
                        direction = "up" if y > 0 else "down"
                        
                    # 计算强度
                    intensity = math.sqrt(x*x + y*y)
                    
                    # 映射到键盘按键
                    key_mapping = {
                        GamepadStick.LEFT: {
                            "up": "w",
                            "down": "s",
                            "left": "a",
                            "right": "d"
                        },
                        GamepadStick.RIGHT: {
                            "up": "i",
                            "down": "k",
                            "left": "j",
                            "right": "l"
                        }
                    }
                    
                    key = key_mapping.get(stick, {}).get(direction)
                    if key is None:
                        print(f"不支持的摇杆操作: {stick.value} {direction}")
                        return False
                        
                    # 应用延迟
                    delay = random.uniform(*self.humanize_config["stick_delay_range"])
                    delay = self._apply_humanize_delay(delay)
                    time.sleep(delay)
                    
                    # 根据强度调整按键时长
                    if duration is None:
                        duration = 0.1 * intensity
                        
                    # 执行按键操作
                    success = self._press_key(key, duration)
                    
                    if success:
                        # 记录状态
                        self._stick_states[stick] = {
                            "x": x,
                            "y": y,
                            "timestamp": time.time(),
                            "duration": duration
                        }
                        
                    return success
                else:
                    # 摇杆回到中心位置
                    if stick in self._stick_states:
                        del self._stick_states[stick]
                    return True
                    
        except Exception as e:
            print(f"摇杆操作失败: {e}")
            return False
            
    def set_trigger(self, trigger: str, value: float) -> bool:
        """
        设置扳机值
        
        Args:
            trigger: 扳机类型 ("lt", "rt")
            value: 扳机值 (0.0 到 1.0)
            
        Returns:
            是否执行成功
        """
        try:
            with self._lock:
                # 限制值范围
                value = max(0.0, min(1.0, value))
                
                # 映射到按键
                key_mapping = {
                    "lt": "shift",
                    "rt": "ctrl"
                }
                
                key = key_mapping.get(trigger.lower())
                if key is None:
                    print(f"不支持的扳机: {trigger}")
                    return False
                    
                # 根据值调整按键时长
                duration = 0.1 * value
                
                # 应用延迟
                delay = random.uniform(*self.humanize_config["trigger_delay_range"])
                delay = self._apply_humanize_delay(delay)
                time.sleep(delay)
                
                # 执行按键操作
                success = self._press_key(key, duration)
                
                if success:
                    # 记录状态
                    self._button_states[trigger] = {
                        "value": value,
                        "timestamp": time.time(),
                        "duration": duration
                    }
                    
                return success
                
        except Exception as e:
            print(f"扳机操作失败: {e}")
            return False
            
    def execute_combo(self, combo: List[Dict[str, Any]]) -> bool:
        """
        执行组合操作
        
        Args:
            combo: 组合操作列表
            
        Returns:
            是否执行成功
        """
        try:
            with self._lock:
                for action in combo:
                    action_type = action.get("type", "")
                    
                    if action_type == "button_press":
                        button = GamepadButton(action.get("button", ""))
                        duration = action.get("duration")
                        if not self.press_button(button, duration):
                            return False
                            
                    elif action_type == "button_release":
                        button = GamepadButton(action.get("button", ""))
                        if not self.release_button(button):
                            return False
                            
                    elif action_type == "stick_move":
                        stick = GamepadStick(action.get("stick", ""))
                        x = action.get("x", 0.0)
                        y = action.get("y", 0.0)
                        duration = action.get("duration")
                        if not self.move_stick(stick, x, y, duration):
                            return False
                            
                    elif action_type == "trigger_set":
                        trigger = action.get("trigger", "")
                        value = action.get("value", 0.0)
                        if not self.set_trigger(trigger, value):
                            return False
                            
                    elif action_type == "delay":
                        delay = action.get("delay", 0.1)
                        time.sleep(delay)
                        
                    else:
                        print(f"未知操作类型: {action_type}")
                        return False
                        
                return True
                
        except Exception as e:
            print(f"组合操作失败: {e}")
            return False
            
    def get_button_state(self, button: GamepadButton) -> Optional[Dict[str, Any]]:
        """获取按钮状态"""
        return self._button_states.get(button)
        
    def get_stick_state(self, stick: GamepadStick) -> Optional[Dict[str, Any]]:
        """获取摇杆状态"""
        return self._stick_states.get(stick)
        
    def is_button_pressed(self, button: GamepadButton) -> bool:
        """检查按钮是否被按下"""
        return button in self._button_states
        
    def get_all_states(self) -> Dict[str, Any]:
        """获取所有状态"""
        return {
            "buttons": {btn.value: state for btn, state in self._button_states.items()},
            "sticks": {stick.value: state for stick, state in self._stick_states.items()},
            "gamepad_type": self.gamepad_type.value,
            "humanize_enabled": self.humanize_enabled
        }
        
    def reset(self):
        """重置所有状态"""
        with self._lock:
            self._button_states.clear()
            self._stick_states.clear()
            
    def set_gamepad_type(self, gamepad_type: GamepadType):
        """设置游戏手柄类型"""
        self.gamepad_type = gamepad_type
        print(f"游戏手柄类型已更改为: {gamepad_type.value}")
        
    def set_humanize_config(self, config: Dict[str, Any]):
        """设置人性化配置"""
        self.humanize_config.update(config)
        
    def get_humanize_config(self) -> Dict[str, Any]:
        """获取人性化配置"""
        return self.humanize_config.copy()


def test_gamepad_simulator():
    """测试游戏手柄模拟器"""
    print("测试游戏手柄模拟器...")
    
    # 测试Xbox手柄
    print("\n测试Xbox手柄...")
    xbox = GamepadSimulator(GamepadType.XBOX, humanize_enabled=True)
    
    success = xbox.press_button(GamepadButton.A)
    print(f"按下A按钮: {'成功' if success else '失败'}")
    
    success = xbox.press_button(GamepadButton.B, duration=0.5)
    print(f"长按B按钮: {'成功' if success else '失败'}")
    
    success = xbox.move_stick(GamepadStick.LEFT, 0.5, 0.5)
    print(f"移动左摇杆: {'成功' if success else '失败'}")
    
    success = xbox.set_trigger("lt", 0.8)
    print(f"设置左扳机: {'成功' if success else '失败'}")
    
    # 测试PlayStation手柄
    print("\n测试PlayStation手柄...")
    ps = GamepadSimulator(GamepadType.PLAYSTATION, humanize_enabled=True)
    
    success = ps.press_button(GamepadButton.CROSS)
    print(f"按下X按钮: {'成功' if success else '失败'}")
    
    success = ps.press_button(GamepadButton.CIRCLE, duration=0.5)
    print(f"长按O按钮: {'成功' if success else '失败'}")
    
    success = ps.move_stick(GamepadStick.RIGHT, -0.3, 0.7)
    print(f"移动右摇杆: {'成功' if success else '失败'}")
    
    # 测试组合操作
    print("\n测试组合操作...")
    combo = [
        {"type": "button_press", "button": "a"},
        {"type": "delay", "delay": 0.1},
        {"type": "stick_move", "stick": "left", "x": 1.0, "y": 0.0},
        {"type": "delay", "delay": 0.2},
        {"type": "button_press", "button": "b"}
    ]
    
    success = xbox.execute_combo(combo)
    print(f"组合操作: {'成功' if success else '失败'}")
    
    # 显示状态
    print("\n当前状态:")
    states = xbox.get_all_states()
    print(f"按钮状态: {len(states['buttons'])} 个")
    print(f"摇杆状态: {len(states['sticks'])} 个")
    
    print("游戏手柄模拟器测试完成!")


if __name__ == "__main__":
    test_gamepad_simulator()
