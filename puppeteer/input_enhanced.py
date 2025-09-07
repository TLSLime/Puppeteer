# -*- coding: utf-8 -*-
"""
增强输入模块 - 支持多种Windows输入方案
提供更强大的鼠标键盘控制功能
"""

import time
import random
import threading
from typing import Dict, List, Optional, Tuple, Any, Union
import json

# 基础输入库
import pyautogui
import pynput
from pynput import mouse, keyboard

# Windows系统库
try:
    import win32api
    import win32con
    import win32gui
    import win32clipboard
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

# 系统信息
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class EnhancedInputProvider:
    """增强输入提供器，支持多种Windows输入方案"""
    
    def __init__(self, input_method: str = "auto", humanize_enabled: bool = True):
        """
        初始化增强输入提供器
        
        Args:
            input_method: 输入方法 ("auto", "pyautogui", "pynput", "win32")
            humanize_enabled: 是否启用人性化参数
        """
        self.input_method = input_method
        self.humanize_enabled = humanize_enabled
        self.last_action_time = 0
        self.action_cooldown = 0.1
        self._lock = threading.Lock()
        
        # 人性化参数
        self.humanize_config = {
            "mouse_delay_range": (0.05, 0.15),
            "key_delay_range": (0.08, 0.14),
            "click_delay_range": (0.02, 0.08),
            "movement_jitter": 2,
            "timing_jitter": 0.02
        }
        
        # 初始化输入方法
        self._init_input_method()
        
        # 禁用PyAutoGUI的安全检查
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0
        
    def _init_input_method(self):
        """初始化输入方法"""
        if self.input_method == "auto":
            if WIN32_AVAILABLE:
                self.input_method = "win32"
            else:
                self.input_method = "pyautogui"
                
        print(f"使用输入方法: {self.input_method}")
        
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
            duration: 移动持续时间
            
        Returns:
            是否执行成功
        """
        try:
            with self._lock:
                self._wait_cooldown()
                
                # 应用抖动
                target_x, target_y = self._apply_movement_jitter(x, y)
                
                if self.input_method == "win32" and WIN32_AVAILABLE:
                    return self._move_mouse_win32(target_x, target_y, duration)
                elif self.input_method == "pynput":
                    return self._move_mouse_pynput(target_x, target_y, duration)
                else:
                    return self._move_mouse_pyautogui(target_x, target_y, duration)
                    
        except Exception as e:
            print(f"鼠标移动失败: {e}")
            return False
            
    def _move_mouse_win32(self, x: int, y: int, duration: Optional[float]) -> bool:
        """使用Win32 API移动鼠标"""
        if not WIN32_AVAILABLE:
            return False
            
        try:
            # 计算移动时间
            if duration is None:
                current_x, current_y = win32gui.GetCursorPos()
                distance = ((x - current_x) ** 2 + (y - current_y) ** 2) ** 0.5
                duration = min(0.5, max(0.1, distance / 1000))
                
            # 应用人性化延迟
            duration = self._apply_humanize_delay(duration)
            
            # 平滑移动
            steps = max(1, int(duration * 60))  # 60fps
            current_x, current_y = win32gui.GetCursorPos()
            
            for i in range(steps + 1):
                progress = i / steps
                new_x = int(current_x + (x - current_x) * progress)
                new_y = int(current_y + (y - current_y) * progress)
                
                win32api.SetCursorPos((new_x, new_y))
                time.sleep(duration / steps)
                
            return True
            
        except Exception as e:
            print(f"Win32鼠标移动失败: {e}")
            return False
            
    def _move_mouse_pynput(self, x: int, y: int, duration: Optional[float]) -> bool:
        """使用pynput移动鼠标"""
        try:
            if duration is None:
                duration = 0.1
                
            duration = self._apply_humanize_delay(duration)
            
            # pynput不支持平滑移动，使用pyautogui作为备选
            pyautogui.moveTo(x, y, duration=duration)
            return True
            
        except Exception as e:
            print(f"pynput鼠标移动失败: {e}")
            return False
            
    def _move_mouse_pyautogui(self, x: int, y: int, duration: Optional[float]) -> bool:
        """使用pyautogui移动鼠标"""
        try:
            if duration is None:
                current_x, current_y = pyautogui.position()
                distance = ((x - current_x) ** 2 + (y - current_y) ** 2) ** 0.5
                duration = min(0.5, max(0.1, distance / 1000))
                
            duration = self._apply_humanize_delay(duration)
            pyautogui.moveTo(x, y, duration=duration)
            return True
            
        except Exception as e:
            print(f"pyautogui鼠标移动失败: {e}")
            return False
            
    def click(self, x: Optional[int] = None, y: Optional[int] = None, 
              button: str = "left", clicks: int = 1) -> bool:
        """
        执行点击操作
        
        Args:
            x, y: 点击坐标
            button: 鼠标按钮 ("left", "right", "middle")
            clicks: 点击次数
            
        Returns:
            是否执行成功
        """
        try:
            with self._lock:
                self._wait_cooldown()
                
                if x is not None and y is not None:
                    if not self.move_mouse(x, y):
                        return False
                        
                # 应用点击延迟
                delay = random.uniform(*self.humanize_config["click_delay_range"])
                delay = self._apply_humanize_delay(delay)
                time.sleep(delay)
                
                if self.input_method == "win32" and WIN32_AVAILABLE:
                    return self._click_win32(button, clicks)
                elif self.input_method == "pynput":
                    return self._click_pynput(button, clicks)
                else:
                    return self._click_pyautogui(button, clicks)
                    
        except Exception as e:
            print(f"点击操作失败: {e}")
            return False
            
    def _click_win32(self, button: str, clicks: int) -> bool:
        """使用Win32 API点击"""
        if not WIN32_AVAILABLE:
            return False
            
        try:
            # 映射按钮
            button_map = {
                "left": win32con.MOUSEEVENTF_LEFTDOWN,
                "right": win32con.MOUSEEVENTF_RIGHTDOWN,
                "middle": win32con.MOUSEEVENTF_MIDDLEDOWN
            }
            
            if button not in button_map:
                return False
                
            button_flag = button_map[button]
            
            for _ in range(clicks):
                # 按下
                win32api.mouse_event(button_flag, 0, 0, 0, 0)
                time.sleep(0.01)  # 短暂延迟
                
                # 释放
                win32api.mouse_event(button_flag << 1, 0, 0, 0, 0)
                time.sleep(0.01)
                
            return True
            
        except Exception as e:
            print(f"Win32点击失败: {e}")
            return False
            
    def _click_pynput(self, button: str, clicks: int) -> bool:
        """使用pynput点击"""
        try:
            # 映射按钮
            button_map = {
                "left": mouse.Button.left,
                "right": mouse.Button.right,
                "middle": mouse.Button.middle
            }
            
            if button not in button_map:
                return False
                
            button_obj = button_map[button]
            
            with mouse.Controller() as controller:
                for _ in range(clicks):
                    controller.click(button_obj, 1)
                    time.sleep(0.01)
                    
            return True
            
        except Exception as e:
            print(f"pynput点击失败: {e}")
            return False
            
    def _click_pyautogui(self, button: str, clicks: int) -> bool:
        """使用pyautogui点击"""
        try:
            pyautogui.click(clicks=clicks, button=button)
            return True
            
        except Exception as e:
            print(f"pyautogui点击失败: {e}")
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
                
                # 应用按键延迟
                delay = random.uniform(*self.humanize_config["key_delay_range"])
                delay = self._apply_humanize_delay(delay)
                time.sleep(delay)
                
                if self.input_method == "win32" and WIN32_AVAILABLE:
                    return self._press_key_win32(key, presses)
                elif self.input_method == "pynput":
                    return self._press_key_pynput(key, presses)
                else:
                    return self._press_key_pyautogui(key, presses)
                    
        except Exception as e:
            print(f"按键操作失败: {e}")
            return False
            
    def _press_key_win32(self, key: str, presses: int) -> bool:
        """使用Win32 API按键"""
        if not WIN32_AVAILABLE:
            return False
            
        try:
            # 虚拟键码映射
            vk_map = {
                'a': 0x41, 'b': 0x42, 'c': 0x43, 'd': 0x44, 'e': 0x45,
                'f': 0x46, 'g': 0x47, 'h': 0x48, 'i': 0x49, 'j': 0x4A,
                'k': 0x4B, 'l': 0x4C, 'm': 0x4D, 'n': 0x4E, 'o': 0x4F,
                'p': 0x50, 'q': 0x51, 'r': 0x52, 's': 0x53, 't': 0x54,
                'u': 0x55, 'v': 0x56, 'w': 0x57, 'x': 0x58, 'y': 0x59,
                'z': 0x5A,
                'space': win32con.VK_SPACE,
                'enter': win32con.VK_RETURN,
                'tab': win32con.VK_TAB,
                'shift': win32con.VK_SHIFT,
                'ctrl': win32con.VK_CONTROL,
                'alt': win32con.VK_MENU,
                'esc': win32con.VK_ESCAPE,
                'f1': win32con.VK_F1, 'f2': win32con.VK_F2, 'f3': win32con.VK_F3,
                'f4': win32con.VK_F4, 'f5': win32con.VK_F5, 'f6': win32con.VK_F6,
                'f7': win32con.VK_F7, 'f8': win32con.VK_F8, 'f9': win32con.VK_F9,
                'f10': win32con.VK_F10, 'f11': win32con.VK_F11, 'f12': win32con.VK_F12,
            }
            
            vk_code = vk_map.get(key.lower())
            if vk_code is None:
                return False
                
            for _ in range(presses):
                # 按下
                win32api.keybd_event(vk_code, 0, 0, 0)
                time.sleep(0.01)
                
                # 释放
                win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)
                time.sleep(0.01)
                
            return True
            
        except Exception as e:
            print(f"Win32按键失败: {e}")
            return False
            
    def _press_key_pynput(self, key: str, presses: int) -> bool:
        """使用pynput按键"""
        try:
            with keyboard.Controller() as controller:
                for _ in range(presses):
                    controller.press(key)
                    controller.release(key)
                    time.sleep(0.01)
                    
            return True
            
        except Exception as e:
            print(f"pynput按键失败: {e}")
            return False
            
    def _press_key_pyautogui(self, key: str, presses: int) -> bool:
        """使用pyautogui按键"""
        try:
            pyautogui.press(key, presses=presses)
            return True
            
        except Exception as e:
            print(f"pyautogui按键失败: {e}")
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
                
                if interval is None:
                    interval = random.uniform(0.05, 0.15)
                    
                if self.input_method == "win32" and WIN32_AVAILABLE:
                    return self._type_text_win32(text, interval)
                elif self.input_method == "pynput":
                    return self._type_text_pynput(text, interval)
                else:
                    return self._type_text_pyautogui(text, interval)
                    
        except Exception as e:
            print(f"文本输入失败: {e}")
            return False
            
    def _type_text_win32(self, text: str, interval: float) -> bool:
        """使用Win32 API输入文本"""
        if not WIN32_AVAILABLE:
            return False
            
        try:
            for char in text:
                # 使用剪贴板方式输入（更可靠）
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(char)
                win32clipboard.CloseClipboard()
                
                # 模拟Ctrl+V
                win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
                win32api.keybd_event(ord('V'), 0, 0, 0)
                win32api.keybd_event(ord('V'), 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
                
                time.sleep(interval)
                
            return True
            
        except Exception as e:
            print(f"Win32文本输入失败: {e}")
            return False
            
    def _type_text_pynput(self, text: str, interval: float) -> bool:
        """使用pynput输入文本"""
        try:
            with keyboard.Controller() as controller:
                for char in text:
                    controller.type(char)
                    time.sleep(interval)
                    
            return True
            
        except Exception as e:
            print(f"pynput文本输入失败: {e}")
            return False
            
    def _type_text_pyautogui(self, text: str, interval: float) -> bool:
        """使用pyautogui输入文本"""
        try:
            pyautogui.typewrite(text, interval=interval)
            return True
            
        except Exception as e:
            print(f"pyautogui文本输入失败: {e}")
            return False
            
    def get_mouse_position(self) -> Tuple[int, int]:
        """获取当前鼠标位置"""
        try:
            if self.input_method == "win32" and WIN32_AVAILABLE:
                return win32gui.GetCursorPos()
            else:
                return pyautogui.position()
        except Exception as e:
            print(f"获取鼠标位置失败: {e}")
            return (0, 0)
            
    def get_screen_size(self) -> Tuple[int, int]:
        """获取屏幕尺寸"""
        try:
            if self.input_method == "win32" and WIN32_AVAILABLE:
                return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
            else:
                return pyautogui.size()
        except Exception as e:
            print(f"获取屏幕尺寸失败: {e}")
            return (1920, 1080)
            
    def set_humanize_config(self, config: Dict[str, Any]):
        """设置人性化配置"""
        self.humanize_config.update(config)
        
    def set_cooldown(self, cooldown: float):
        """设置动作冷却时间"""
        self.action_cooldown = max(0, cooldown)
        
    def set_input_method(self, method: str):
        """设置输入方法"""
        if method in ["auto", "pyautogui", "pynput", "win32"]:
            self.input_method = method
            self._init_input_method()
        else:
            print(f"不支持的输入方法: {method}")


def test_enhanced_input():
    """测试增强输入功能"""
    print("测试增强输入功能...")
    
    provider = EnhancedInputProvider(input_method="auto", humanize_enabled=True)
    
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
    success = provider.type_text("Hello World")
    print(f"文本输入: {'成功' if success else '失败'}")
    
    # 获取信息
    pos = provider.get_mouse_position()
    size = provider.get_screen_size()
    print(f"鼠标位置: {pos}")
    print(f"屏幕尺寸: {size}")
    
    print("增强输入测试完成!")


if __name__ == "__main__":
    test_enhanced_input()
