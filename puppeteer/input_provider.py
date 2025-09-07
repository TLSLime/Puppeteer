# -*- coding: utf-8 -*-
"""
输入提供模块 - 鼠标和键盘输入控制
支持多种输入方法：Windows核心API、PyAutoGUI、pynput
自动选择最佳输入方案，提供humanized输入
"""

import pyautogui
import time
import random
import threading
from typing import Dict, List, Optional, Tuple, Any, Union
import json

# 尝试导入增强输入模块
try:
    from .windows_core import WindowsCoreInput
    WINDOWS_CORE_AVAILABLE = True
except ImportError:
    WINDOWS_CORE_AVAILABLE = False

try:
    from .input_enhanced import EnhancedInputProvider
    ENHANCED_INPUT_AVAILABLE = True
except ImportError:
    ENHANCED_INPUT_AVAILABLE = False


class InputProvider:
    """输入提供器，负责执行鼠标和键盘操作"""
    
    def __init__(self, humanize_enabled: bool = True, input_method: str = "auto"):
        """
        初始化输入提供器
        
        Args:
            humanize_enabled: 是否启用人性化参数
            input_method: 输入方法 ("auto", "windows_core", "enhanced", "pyautogui")
        """
        self.humanize_enabled = humanize_enabled
        self.input_method = input_method
        self.last_action_time = 0
        self.action_cooldown = 0.1  # 最小动作间隔
        self._lock = threading.Lock()
        
        # 人性化参数
        self.humanize_config = {
            "mouse_delay_range": (0.05, 0.15),  # 鼠标移动延迟范围
            "key_delay_range": (0.08, 0.14),    # 按键延迟范围
            "click_delay_range": (0.02, 0.08),  # 点击延迟范围
            "movement_jitter": 2,               # 移动抖动像素
            "timing_jitter": 0.02               # 时间抖动
        }
        
        # 初始化输入后端
        self._init_input_backend()
        
        # 禁用PyAutoGUI的安全检查
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0
        
    def _init_input_backend(self):
        """初始化输入后端"""
        if self.input_method == "auto":
            # 自动选择最佳输入方法
            if WINDOWS_CORE_AVAILABLE:
                self.input_method = "windows_core"
                self.backend = WindowsCoreInput(humanize_enabled=self.humanize_enabled)
                print("使用Windows核心输入API")
            elif ENHANCED_INPUT_AVAILABLE:
                self.input_method = "enhanced"
                self.backend = EnhancedInputProvider(input_method="auto", humanize_enabled=self.humanize_enabled)
                print("使用增强输入提供器")
            else:
                self.input_method = "pyautogui"
                self.backend = None
                print("使用PyAutoGUI输入")
        elif self.input_method == "windows_core" and WINDOWS_CORE_AVAILABLE:
            self.backend = WindowsCoreInput(humanize_enabled=self.humanize_enabled)
            print("使用Windows核心输入API")
        elif self.input_method == "enhanced" and ENHANCED_INPUT_AVAILABLE:
            self.backend = EnhancedInputProvider(input_method="auto", humanize_enabled=self.humanize_enabled)
            print("使用增强输入提供器")
        else:
            self.input_method = "pyautogui"
            self.backend = None
            print("使用PyAutoGUI输入")
        
    def _apply_humanize_delay(self, base_delay: float) -> float:
        """应用人性化延迟"""
        if not self.humanize_enabled:
            return base_delay
            
        jitter = random.uniform(-self.humanize_config["timing_jitter"], 
                               self.humanize_config["timing_jitter"])
        return max(0, base_delay + jitter)
        
    def _apply_movement_jitter(self, x: int, y: int) -> Tuple[int, int]:
        """应用移动抖动"""
        if not self.humanize_enabled:
            return x, y
            
        jitter = self.humanize_config["movement_jitter"]
        jitter_x = random.randint(-jitter, jitter)
        jitter_y = random.randint(-jitter, jitter)
        return x + jitter_x, y + jitter_y
        
    def _wait_cooldown(self):
        """等待冷却时间"""
        current_time = time.time()
        elapsed = current_time - self.last_action_time
        if elapsed < self.action_cooldown:
            time.sleep(self.action_cooldown - elapsed)
        self.last_action_time = time.time()
        
    def move_mouse(self, x: int, y: int, duration: Optional[float] = None) -> bool:
        """
        移动鼠标到指定位置
        
        Args:
            x, y: 目标坐标
            duration: 移动持续时间，None为自动计算
            
        Returns:
            是否执行成功
        """
        try:
            with self._lock:
                self._wait_cooldown()
                
                # 如果有后端，使用后端
                if self.backend is not None:
                    return self.backend.move_mouse(x, y, duration)
                
                # 否则使用PyAutoGUI
                # 应用抖动
                target_x, target_y = self._apply_movement_jitter(x, y)
                
                # 计算移动时间
                if duration is None:
                    current_x, current_y = pyautogui.position()
                    distance = ((target_x - current_x) ** 2 + (target_y - current_y) ** 2) ** 0.5
                    duration = min(0.5, max(0.1, distance / 1000))  # 基于距离计算时间
                    
                # 应用人性化延迟
                duration = self._apply_humanize_delay(duration)
                
                pyautogui.moveTo(target_x, target_y, duration=duration)
                return True
                
        except Exception as e:
            print(f"鼠标移动失败: {e}")
            return False
            
    def click(self, x: Optional[int] = None, y: Optional[int] = None, 
              button: str = "left", clicks: int = 1) -> bool:
        """
        执行点击操作
        
        Args:
            x, y: 点击坐标，None为当前位置
            button: 鼠标按钮 ("left", "right", "middle")
            clicks: 点击次数
            
        Returns:
            是否执行成功
        """
        try:
            with self._lock:
                self._wait_cooldown()
                
                # 如果有后端，使用后端
                if self.backend is not None:
                    return self.backend.click(x, y, button, clicks)
                
                # 否则使用PyAutoGUI
                if x is not None and y is not None:
                    # 移动到目标位置并点击
                    if not self.move_mouse(x, y):
                        return False
                        
                # 应用点击延迟
                delay = random.uniform(*self.humanize_config["click_delay_range"])
                delay = self._apply_humanize_delay(delay)
                time.sleep(delay)
                
                pyautogui.click(x, y, clicks=clicks, button=button)
                return True
                
        except Exception as e:
            print(f"点击操作失败: {e}")
            return False
            
    def press_key(self, key: str, presses: int = 1) -> bool:
        """
        按下键盘按键
        
        Args:
            key: 按键名称
            presses: 按下次数
            
        Returns:
            是否执行成功
        """
        try:
            with self._lock:
                self._wait_cooldown()
                
                # 如果有后端，使用后端
                if self.backend is not None:
                    return self.backend.press_key(key, presses)
                
                # 否则使用PyAutoGUI
                # 应用按键延迟
                delay = random.uniform(*self.humanize_config["key_delay_range"])
                delay = self._apply_humanize_delay(delay)
                time.sleep(delay)
                
                # 检查是否是组合键
                if '+' in key:
                    # 处理组合键，如 ctrl+a, alt+tab 等
                    keys = key.split('+')
                    if len(keys) == 2:
                        pyautogui.hotkey(keys[0].strip(), keys[1].strip())
                        return True
                    else:
                        print(f"不支持的组合键格式: {key}")
                        return False
                else:
                    # 单个按键
                    pyautogui.press(key, presses=presses)
                    return True
                
        except Exception as e:
            print(f"按键操作失败: {e}")
            return False
            
    def type_text(self, text: str, interval: Optional[float] = None) -> bool:
        """
        输入文本
        
        Args:
            text: 要输入的文本
            interval: 字符间隔时间
            
        Returns:
            是否执行成功
        """
        try:
            with self._lock:
                self._wait_cooldown()
                
                # 如果有后端，使用后端
                if self.backend is not None:
                    return self.backend.type_text(text, interval)
                
                # 否则使用PyAutoGUI
                if interval is None:
                    interval = random.uniform(0.05, 0.15)
                    
                pyautogui.typewrite(text, interval=interval)
                return True
                
        except Exception as e:
            print(f"文本输入失败: {e}")
            return False
            
    def execute_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行动作对象
        
        Args:
            action: 动作字典，包含type, key, pos等字段
            
        Returns:
            执行结果
        """
        result = {
            "success": False,
            "action": action,
            "timestamp": time.time(),
            "error": None
        }
        
        try:
            action_type = action.get("type", "")
            humanize = action.get("humanize", {})
            
            # 应用自定义人性化参数
            if humanize:
                delay_ms = humanize.get("delay_ms", [80, 140])
                if isinstance(delay_ms, list) and len(delay_ms) == 2:
                    delay = random.uniform(delay_ms[0] / 1000.0, delay_ms[1] / 1000.0)
                    time.sleep(delay)
                    
            if action_type == "press":
                key = action.get("key", "")
                result["success"] = self.press_key(key)
                
            elif action_type == "click":
                pos = action.get("pos", [])
                if len(pos) >= 2:
                    result["success"] = self.click(pos[0], pos[1])
                else:
                    result["success"] = self.click()
                    
            elif action_type == "move":
                pos = action.get("pos", [])
                if len(pos) >= 2:
                    result["success"] = self.move_mouse(pos[0], pos[1])
                    
            elif action_type == "combo":
                keys = action.get("keys", [])
                for key in keys:
                    if not self.press_key(key):
                        result["success"] = False
                        break
                else:
                    result["success"] = True
                    
            elif action_type == "type":
                text = action.get("text", "")
                result["success"] = self.type_text(text)
                    
            else:
                result["error"] = f"未知动作类型: {action_type}"
                
        except Exception as e:
            result["error"] = str(e)
            
        return result
        
    def execute_macro(self, macro: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        执行宏操作序列
        
        Args:
            macro: 动作序列
            
        Returns:
            执行结果列表
        """
        results = []
        for action in macro:
            result = self.execute_action(action)
            results.append(result)
            
            # 如果某个动作失败，可以选择是否继续
            if not result["success"]:
                print(f"宏执行失败: {result['error']}")
                
        return results
        
    def set_humanize_config(self, config: Dict[str, Any]):
        """设置人性化配置"""
        self.humanize_config.update(config)
        
    def set_cooldown(self, cooldown: float):
        """设置动作冷却时间"""
        self.action_cooldown = max(0, cooldown)
        
    def get_mouse_position(self) -> Tuple[int, int]:
        """获取当前鼠标位置"""
        try:
            if self.backend is not None:
                return self.backend.get_mouse_position()
            else:
                return pyautogui.position()
        except Exception as e:
            print(f"获取鼠标位置失败: {e}")
            return (0, 0)
            
    def get_screen_size(self) -> Tuple[int, int]:
        """获取屏幕尺寸"""
        try:
            if self.backend is not None:
                return self.backend.get_screen_size()
            else:
                return pyautogui.size()
        except Exception as e:
            print(f"获取屏幕尺寸失败: {e}")
            return (1920, 1080)
            
    def is_key_pressed(self, key: str) -> bool:
        """检查按键是否被按下"""
        try:
            if self.backend is not None and hasattr(self.backend, 'is_key_pressed'):
                return self.backend.is_key_pressed(key)
            else:
                # 使用PyAutoGUI的备用方法
                return pyautogui.isPressed(key)
        except Exception as e:
            print(f"检查按键状态失败: {e}")
            return False
            
    def get_input_method(self) -> str:
        """获取当前使用的输入方法"""
        return self.input_method
        
    def set_input_method(self, method: str):
        """设置输入方法"""
        if method in ["auto", "windows_core", "enhanced", "pyautogui"]:
            self.input_method = method
            self._init_input_backend()
        else:
            print(f"不支持的输入方法: {method}")


def test_input():
    """测试输入功能"""
    print("测试输入功能...")
    
    provider = InputProvider(humanize_enabled=True, input_method="auto")
    
    # 显示使用的输入方法
    print(f"使用输入方法: {provider.get_input_method()}")
    
    # 测试鼠标移动
    print("测试鼠标移动...")
    success = provider.move_mouse(400, 300)
    print(f"鼠标移动: {'成功' if success else '失败'}")
    
    # 测试点击
    print("测试点击...")
    success = provider.click(400, 300)
    print(f"点击: {'成功' if success else '失败'}")
    
    # 测试按键
    print("测试按键...")
    success = provider.press_key("space")
    print(f"按键: {'成功' if success else '失败'}")
    
    # 测试文本输入
    print("测试文本输入...")
    success = provider.type_text("Hello")
    print(f"文本输入: {'成功' if success else '失败'}")
    
    # 获取信息
    pos = provider.get_mouse_position()
    size = provider.get_screen_size()
    print(f"鼠标位置: {pos}")
    print(f"屏幕尺寸: {size}")
    
    # 测试按键状态
    print("测试按键状态...")
    space_pressed = provider.is_key_pressed("space")
    print(f"空格键状态: {'按下' if space_pressed else '未按下'}")
    
    # 测试动作对象
    print("测试动作对象...")
    action = {
        "type": "press",
        "key": "q",
        "humanize": {"delay_ms": [50, 100]}
    }
    result = provider.execute_action(action)
    print(f"动作执行: {result}")
    
    print("输入测试完成!")


if __name__ == "__main__":
    test_input()
