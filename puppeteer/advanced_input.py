# -*- coding: utf-8 -*-
"""
高级输入管理器 - 整合键盘、鼠标和游戏手柄操作
支持单次按键、长按、组合键、拖拽、滚轮和游戏手柄模拟
"""

import time
import random
import threading
import ctypes
import ctypes.wintypes
from typing import Dict, List, Optional, Tuple, Any, Union, Callable
from enum import Enum
import json

# 导入基础输入模块
from .windows_core import WindowsCoreInput
from .input_enhanced import EnhancedInputProvider
from .input_provider import InputProvider


class InputType(Enum):
    """输入类型枚举"""
    KEYBOARD = "keyboard"
    MOUSE = "mouse"
    GAMEPAD = "gamepad"


class KeyState(Enum):
    """按键状态枚举"""
    PRESS = "press"
    RELEASE = "release"
    HOLD = "hold"


class MouseButton(Enum):
    """鼠标按钮枚举"""
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"
    X1 = "x1"
    X2 = "x2"


class GamepadButton(Enum):
    """游戏手柄按钮枚举"""
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
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class AdvancedInputManager:
    """高级输入管理器"""
    
    def __init__(self, input_method: str = "auto", humanize_enabled: bool = True):
        """
        初始化高级输入管理器
        
        Args:
            input_method: 输入方法 ("auto", "windows_core", "enhanced", "pyautogui")
            humanize_enabled: 是否启用人性化参数
        """
        self.input_method = input_method
        self.humanize_enabled = humanize_enabled
        self._lock = threading.Lock()
        
        # 初始化输入提供器
        self._init_input_providers()
        
        # 按键状态跟踪
        self._key_states = {}
        self._mouse_states = {}
        self._gamepad_states = {}
        
        # 长按任务管理
        self._hold_tasks = {}
        self._hold_threads = {}
        
        # 人性化配置
        self.humanize_config = {
            "key_delay_range": (0.05, 0.12),
            "mouse_delay_range": (0.02, 0.08),
            "click_delay_range": (0.01, 0.05),
            "hold_repeat_interval": 0.1,
            "movement_jitter": 1,
            "timing_jitter": 0.01
        }
        
        print(f"高级输入管理器初始化完成 - 使用方法: {self.input_method}")
        
    def _init_input_providers(self):
        """初始化输入提供器"""
        try:
            self.provider = InputProvider(
                humanize_enabled=self.humanize_enabled,
                input_method=self.input_method
            )
            self.input_method = self.provider.get_input_method()
        except Exception as e:
            print(f"输入提供器初始化失败: {e}")
            raise
            
    def _apply_humanize_delay(self, base_delay: float) -> float:
        """应用人性化延迟"""
        if not self.humanize_enabled:
            return base_delay
            
        jitter = random.uniform(-self.humanize_config["timing_jitter"], 
                               self.humanize_config["timing_jitter"])
        return max(0, base_delay + jitter)
        
    # ==================== 键盘操作 ====================
    
    def press_key(self, key: str, duration: Optional[float] = None) -> bool:
        """
        按下键盘按键
        
        Args:
            key: 按键名称
            duration: 按住时长，None为单次按下
            
        Returns:
            是否执行成功
        """
        try:
            with self._lock:
                if duration is None:
                    # 单次按键
                    return self.provider.press_key(key)
                else:
                    # 长按
                    return self._hold_key(key, duration)
        except Exception as e:
            print(f"按键操作失败: {e}")
            return False
            
    def _hold_key(self, key: str, duration: float) -> bool:
        """长按按键"""
        try:
            # 按下按键
            if not self.provider.press_key(key):
                return False
                
            # 记录状态
            self._key_states[key] = {
                "state": KeyState.HOLD,
                "start_time": time.time(),
                "duration": duration
            }
            
            # 等待指定时间
            time.sleep(duration)
            
            # 释放按键（通过再次按下实现）
            self.provider.press_key(key)
            
            # 清除状态
            if key in self._key_states:
                del self._key_states[key]
                
            return True
            
        except Exception as e:
            print(f"长按按键失败: {e}")
            return False
            
    def press_key_combination(self, keys: List[str], interval: Optional[float] = None) -> bool:
        """
        按下组合键
        
        Args:
            keys: 按键列表，按顺序按下
            interval: 按键间隔时间
            
        Returns:
            是否执行成功
        """
        try:
            with self._lock:
                if interval is None:
                    interval = random.uniform(*self.humanize_config["key_delay_range"])
                    
                for key in keys:
                    if not self.provider.press_key(key):
                        return False
                    time.sleep(interval)
                    
                return True
                
        except Exception as e:
            print(f"组合键操作失败: {e}")
            return False
            
    def press_key_simultaneous(self, keys: List[str]) -> bool:
        """
        同时按下多个按键
        
        Args:
            keys: 按键列表
            
        Returns:
            是否执行成功
        """
        try:
            with self._lock:
                # 先按下所有按键
                for key in keys:
                    if not self.provider.press_key(key):
                        return False
                        
                # 短暂延迟后释放所有按键
                time.sleep(0.01)
                for key in keys:
                    self.provider.press_key(key)
                    
                return True
                
        except Exception as e:
            print(f"同时按键操作失败: {e}")
            return False
            
    def type_text_with_delay(self, text: str, base_interval: Optional[float] = None) -> bool:
        """
        输入文本，支持随机延迟
        
        Args:
            text: 要输入的文本
            base_interval: 基础间隔时间
            
        Returns:
            是否执行成功
        """
        try:
            with self._lock:
                if base_interval is None:
                    base_interval = random.uniform(0.05, 0.15)
                    
                for char in text:
                    # 应用人性化延迟
                    interval = self._apply_humanize_delay(base_interval)
                    
                    if not self.provider.type_text(char, interval):
                        return False
                        
                return True
                
        except Exception as e:
            print(f"文本输入失败: {e}")
            return False
            
    # ==================== 鼠标操作 ====================
    
    def click(self, x: Optional[int] = None, y: Optional[int] = None, 
              button: str = "left", clicks: int = 1, duration: Optional[float] = None) -> bool:
        """
        执行点击操作
        
        Args:
            x, y: 点击坐标
            button: 鼠标按钮
            clicks: 点击次数
            duration: 长按时长，None为普通点击
            
        Returns:
            是否执行成功
        """
        try:
            with self._lock:
                if duration is None:
                    # 普通点击
                    return self.provider.click(x, y, button, clicks)
                else:
                    # 长按
                    return self._hold_click(x, y, button, duration)
        except Exception as e:
            print(f"点击操作失败: {e}")
            return False
            
    def _hold_click(self, x: Optional[int], y: Optional[int], 
                   button: str, duration: float) -> bool:
        """长按鼠标"""
        try:
            # 移动到目标位置
            if x is not None and y is not None:
                if not self.provider.move_mouse(x, y):
                    return False
                    
            # 按下鼠标
            if not self.provider.click(x, y, button, 1):
                return False
                
            # 记录状态
            state_key = f"{button}_{x}_{y}"
            self._mouse_states[state_key] = {
                "state": KeyState.HOLD,
                "start_time": time.time(),
                "duration": duration,
                "button": button,
                "x": x,
                "y": y
            }
            
            # 等待指定时间
            time.sleep(duration)
            
            # 释放鼠标（通过再次点击实现）
            self.provider.click(x, y, button, 1)
            
            # 清除状态
            if state_key in self._mouse_states:
                del self._mouse_states[state_key]
                
            return True
            
        except Exception as e:
            print(f"长按鼠标失败: {e}")
            return False
            
    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, 
             button: str = "left", duration: Optional[float] = None) -> bool:
        """
        拖拽操作
        
        Args:
            start_x, start_y: 起始坐标
            end_x, end_y: 结束坐标
            button: 鼠标按钮
            duration: 拖拽时长
            
        Returns:
            是否执行成功
        """
        try:
            with self._lock:
                if duration is None:
                    duration = 0.5
                    
                # 移动到起始位置
                if not self.provider.move_mouse(start_x, start_y):
                    return False
                    
                # 按下鼠标
                if not self.provider.click(start_x, start_y, button, 1):
                    return False
                    
                # 拖拽到目标位置
                if not self.provider.move_mouse(end_x, end_y, duration):
                    return False
                    
                # 释放鼠标
                if not self.provider.click(end_x, end_y, button, 1):
                    return False
                    
                return True
                
        except Exception as e:
            print(f"拖拽操作失败: {e}")
            return False
            
    def scroll(self, x: int, y: int, direction: str = "up", clicks: int = 3) -> bool:
        """
        滚轮操作
        
        Args:
            x, y: 滚轮位置
            direction: 滚动方向 ("up", "down")
            clicks: 滚动次数
            
        Returns:
            是否执行成功
        """
        try:
            with self._lock:
                # 移动到目标位置
                if not self.provider.move_mouse(x, y):
                    return False
                    
                # 执行滚轮操作
                for _ in range(clicks):
                    if direction == "up":
                        self.provider.press_key("up")
                    else:
                        self.provider.press_key("down")
                    time.sleep(0.05)
                    
                return True
                
        except Exception as e:
            print(f"滚轮操作失败: {e}")
            return False
            
    # ==================== 游戏手柄操作 ====================
    
    def press_gamepad_button(self, button: str, duration: Optional[float] = None) -> bool:
        """
        按下游戏手柄按钮
        
        Args:
            button: 按钮名称
            duration: 按住时长
            
        Returns:
            是否执行成功
        """
        try:
            with self._lock:
                # 将游戏手柄按钮映射到键盘按键
                key_mapping = self._get_gamepad_key_mapping()
                key = key_mapping.get(button.lower())
                
                if key is None:
                    print(f"不支持的游戏手柄按钮: {button}")
                    return False
                    
                if duration is None:
                    return self.provider.press_key(key)
                else:
                    return self._hold_key(key, duration)
                    
        except Exception as e:
            print(f"游戏手柄按钮操作失败: {e}")
            return False
            
    def _get_gamepad_key_mapping(self) -> Dict[str, str]:
        """获取游戏手柄按钮到键盘的映射"""
        return {
            "a": "space",      # A按钮 -> 空格
            "b": "esc",        # B按钮 -> ESC
            "x": "x",          # X按钮 -> X
            "y": "y",          # Y按钮 -> Y
            "lb": "q",         # 左肩键 -> Q
            "rb": "e",         # 右肩键 -> E
            "lt": "shift",     # 左扳机 -> Shift
            "rt": "ctrl",      # 右扳机 -> Ctrl
            "start": "enter",  # 开始键 -> Enter
            "select": "tab",   # 选择键 -> Tab
            "l3": "f1",        # 左摇杆 -> F1
            "r3": "f2",        # 右摇杆 -> F2
            "up": "up",        # 上方向键 -> 上箭头
            "down": "down",    # 下方向键 -> 下箭头
            "left": "left",    # 左方向键 -> 左箭头
            "right": "right"   # 右方向键 -> 右箭头
        }
        
    def move_gamepad_stick(self, stick: str, direction: str, intensity: float = 1.0) -> bool:
        """
        移动游戏手柄摇杆
        
        Args:
            stick: 摇杆 ("left", "right")
            direction: 方向 ("up", "down", "left", "right")
            intensity: 强度 (0.0-1.0)
            
        Returns:
            是否执行成功
        """
        try:
            with self._lock:
                # 将摇杆移动映射到键盘按键
                key_mapping = {
                    "left": {
                        "up": "w",
                        "down": "s",
                        "left": "a",
                        "right": "d"
                    },
                    "right": {
                        "up": "i",
                        "down": "k",
                        "left": "j",
                        "right": "l"
                    }
                }
                
                key = key_mapping.get(stick, {}).get(direction)
                if key is None:
                    print(f"不支持的摇杆操作: {stick} {direction}")
                    return False
                    
                # 根据强度调整按键时长
                duration = 0.1 * intensity
                return self._hold_key(key, duration)
                
        except Exception as e:
            print(f"摇杆操作失败: {e}")
            return False
            
    # ==================== 宏操作 ====================
    
    def execute_macro(self, macro: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        执行宏操作序列
        
        Args:
            macro: 宏操作列表
            
        Returns:
            执行结果列表
        """
        results = []
        
        try:
            with self._lock:
                for i, action in enumerate(macro):
                    result = self._execute_single_action(action)
                    result["index"] = i
                    results.append(result)
                    
                    # 如果某个动作失败，可以选择是否继续
                    if not result["success"]:
                        print(f"宏操作第{i+1}步失败: {result.get('error', '未知错误')}")
                        
        except Exception as e:
            print(f"宏执行失败: {e}")
            
        return results
        
    def _execute_single_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """执行单个动作"""
        result = {
            "success": False,
            "action": action,
            "timestamp": time.time(),
            "error": None
        }
        
        try:
            action_type = action.get("type", "")
            
            if action_type == "key_press":
                key = action.get("key", "")
                duration = action.get("duration")
                result["success"] = self.press_key(key, duration)
                
            elif action_type == "key_combination":
                keys = action.get("keys", [])
                interval = action.get("interval")
                result["success"] = self.press_key_combination(keys, interval)
                
            elif action_type == "key_simultaneous":
                keys = action.get("keys", [])
                result["success"] = self.press_key_simultaneous(keys)
                
            elif action_type == "type_text":
                text = action.get("text", "")
                interval = action.get("interval")
                result["success"] = self.type_text_with_delay(text, interval)
                
            elif action_type == "mouse_click":
                x = action.get("x")
                y = action.get("y")
                button = action.get("button", "left")
                clicks = action.get("clicks", 1)
                duration = action.get("duration")
                result["success"] = self.click(x, y, button, clicks, duration)
                
            elif action_type == "mouse_drag":
                start_x = action.get("start_x", 0)
                start_y = action.get("start_y", 0)
                end_x = action.get("end_x", 0)
                end_y = action.get("end_y", 0)
                button = action.get("button", "left")
                duration = action.get("duration")
                result["success"] = self.drag(start_x, start_y, end_x, end_y, button, duration)
                
            elif action_type == "mouse_scroll":
                x = action.get("x", 0)
                y = action.get("y", 0)
                direction = action.get("direction", "up")
                clicks = action.get("clicks", 3)
                result["success"] = self.scroll(x, y, direction, clicks)
                
            elif action_type == "gamepad_button":
                button = action.get("button", "")
                duration = action.get("duration")
                result["success"] = self.press_gamepad_button(button, duration)
                
            elif action_type == "gamepad_stick":
                stick = action.get("stick", "left")
                direction = action.get("direction", "up")
                intensity = action.get("intensity", 1.0)
                result["success"] = self.move_gamepad_stick(stick, direction, intensity)
                
            elif action_type == "delay":
                delay = action.get("delay", 0.1)
                time.sleep(delay)
                result["success"] = True
                
            else:
                result["error"] = f"未知动作类型: {action_type}"
                
        except Exception as e:
            result["error"] = str(e)
            
        return result
        
    # ==================== 状态管理 ====================
    
    def get_key_state(self, key: str) -> Optional[Dict[str, Any]]:
        """获取按键状态"""
        return self._key_states.get(key)
        
    def get_mouse_state(self, button: str, x: int, y: int) -> Optional[Dict[str, Any]]:
        """获取鼠标状态"""
        state_key = f"{button}_{x}_{y}"
        return self._mouse_states.get(state_key)
        
    def get_gamepad_state(self, button: str) -> Optional[Dict[str, Any]]:
        """获取游戏手柄状态"""
        return self._gamepad_states.get(button)
        
    def is_key_held(self, key: str) -> bool:
        """检查按键是否被按住"""
        state = self._key_states.get(key)
        if state is None:
            return False
            
        elapsed = time.time() - state["start_time"]
        return elapsed < state["duration"]
        
    def stop_all_holds(self):
        """停止所有长按操作"""
        with self._lock:
            self._key_states.clear()
            self._mouse_states.clear()
            self._gamepad_states.clear()
            
    # ==================== 配置管理 ====================
    
    def set_humanize_config(self, config: Dict[str, Any]):
        """设置人性化配置"""
        self.humanize_config.update(config)
        
    def get_humanize_config(self) -> Dict[str, Any]:
        """获取人性化配置"""
        return self.humanize_config.copy()
        
    def set_input_method(self, method: str):
        """设置输入方法"""
        if method in ["auto", "windows_core", "enhanced", "pyautogui"]:
            self.input_method = method
            self._init_input_providers()
        else:
            print(f"不支持的输入方法: {method}")
            
    def get_input_method(self) -> str:
        """获取当前输入方法"""
        return self.input_method


def test_advanced_input():
    """测试高级输入功能"""
    print("测试高级输入功能...")
    
    manager = AdvancedInputManager(humanize_enabled=True)
    
    # 测试键盘操作
    print("\n测试键盘操作...")
    success = manager.press_key("space")
    print(f"单次按键: {'成功' if success else '失败'}")
    
    success = manager.press_key("a", duration=0.5)
    print(f"长按按键: {'成功' if success else '失败'}")
    
    success = manager.press_key_combination(["ctrl", "c"])
    print(f"组合键: {'成功' if success else '失败'}")
    
    success = manager.type_text_with_delay("Hello World")
    print(f"文本输入: {'成功' if success else '失败'}")
    
    # 测试鼠标操作
    print("\n测试鼠标操作...")
    success = manager.click(400, 300)
    print(f"普通点击: {'成功' if success else '失败'}")
    
    success = manager.click(400, 300, duration=0.5)
    print(f"长按点击: {'成功' if success else '失败'}")
    
    success = manager.drag(100, 100, 200, 200)
    print(f"拖拽操作: {'成功' if success else '失败'}")
    
    success = manager.scroll(400, 300, "up", 3)
    print(f"滚轮操作: {'成功' if success else '失败'}")
    
    # 测试游戏手柄操作
    print("\n测试游戏手柄操作...")
    success = manager.press_gamepad_button("a")
    print(f"游戏手柄按钮: {'成功' if success else '失败'}")
    
    success = manager.move_gamepad_stick("left", "up", 0.5)
    print(f"摇杆操作: {'成功' if success else '失败'}")
    
    # 测试宏操作
    print("\n测试宏操作...")
    macro = [
        {"type": "key_press", "key": "space"},
        {"type": "delay", "delay": 0.1},
        {"type": "mouse_click", "x": 400, "y": 300},
        {"type": "delay", "delay": 0.1},
        {"type": "type_text", "text": "Test"}
    ]
    
    results = manager.execute_macro(macro)
    success_count = sum(1 for r in results if r["success"])
    print(f"宏操作: {success_count}/{len(results)} 成功")
    
    print("高级输入测试完成!")


if __name__ == "__main__":
    test_advanced_input()
