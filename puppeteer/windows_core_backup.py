# -*- coding: utf-8 -*-
"""
Windows核心输入模块 - 使用原生Windows API
提供最稳定和高效的Windows系统输入控制
"""

import time
import random
import threading
import ctypes
import ctypes.wintypes
from typing import Dict, List, Optional, Tuple, Any, Union
from ctypes import wintypes

# Windows API常量
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

# 鼠标事件常量
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_ABSOLUTE = 0x8000

# 键盘事件常量
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_SCANCODE = 0x0008

# 虚拟键码
VK_CODES = {
    # 字母键
    'a': 0x41, 'b': 0x42, 'c': 0x43, 'd': 0x44, 'e': 0x45,
    'f': 0x46, 'g': 0x47, 'h': 0x48, 'i': 0x49, 'j': 0x4A,
    'k': 0x4B, 'l': 0x4C, 'm': 0x4D, 'n': 0x4E, 'o': 0x4F,
    'p': 0x50, 'q': 0x51, 'r': 0x52, 's': 0x53, 't': 0x54,
    'u': 0x55, 'v': 0x56, 'w': 0x57, 'x': 0x58, 'y': 0x59,
    'z': 0x5A,
    
    # 数字键
    '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34,
    '5': 0x35, '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39,
    
    # 功能键
    'f1': 0x70, 'f2': 0x71, 'f3': 0x72, 'f4': 0x73,
    'f5': 0x74, 'f6': 0x75, 'f7': 0x76, 'f8': 0x77,
    'f9': 0x78, 'f10': 0x79, 'f11': 0x7A, 'f12': 0x7B,
    
    # 特殊键
    'space': 0x20, 'enter': 0x0D, 'tab': 0x09, 'shift': 0x10,
    'ctrl': 0x11, 'alt': 0x12, 'esc': 0x1B, 'backspace': 0x08,
    'delete': 0x2E, 'insert': 0x2D, 'home': 0x24, 'end': 0x23,
    'pageup': 0x21, 'pagedown': 0x22,
    
    # 方向键
    'up': 0x26, 'down': 0x28, 'left': 0x25, 'right': 0x27,
    
    # 符号键
    'plus': 0xBB, 'minus': 0xBD, 'equals': 0xBB,
    'comma': 0xBC, 'period': 0xBE, 'slash': 0xBF,
    'backslash': 0xDC, 'semicolon': 0xBA, 'quote': 0xDE,
    'bracket_left': 0xDB, 'bracket_right': 0xDD,
    'grave': 0xC0, 'tilde': 0xC0,
}


class POINT(ctypes.Structure):
    """Windows POINT结构"""
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class MOUSEINPUT(ctypes.Structure):
    """Windows MOUSEINPUT结构"""
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG))
    ]


class KEYBDINPUT(ctypes.Structure):
    """Windows KEYBDINPUT结构"""
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG))
    ]


class HARDWAREINPUT(ctypes.Structure):
    """Windows HARDWAREINPUT结构"""
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD)
    ]


class INPUT_UNION(ctypes.Union):
    """Windows INPUT联合体"""
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT)
    ]


class INPUT(ctypes.Structure):
    """Windows INPUT结构"""
    _fields_ = [
        ("type", wintypes.DWORD),
        ("ii", INPUT_UNION)
    ]


class WindowsCoreInput:
    """Windows核心输入控制器"""
    
    def __init__(self, humanize_enabled: bool = True):
        """
        初始化Windows核心输入控制器
        
        Args:
            humanize_enabled: 是否启用人性化参数
        """
        self.humanize_enabled = humanize_enabled
        self.last_action_time = 0
        self.action_cooldown = 0.05
        self._lock = threading.Lock()
        
        # 人性化参数
        self.humanize_config = {
            "mouse_delay_range": (0.02, 0.08),
            "key_delay_range": (0.05, 0.12),
            "click_delay_range": (0.01, 0.05),
            "movement_jitter": 1,
            "timing_jitter": 0.01
        }
        
        # 加载Windows API
        self._load_windows_api()
        
        # 获取屏幕信息
        self.screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        self.screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        
        print(f"Windows核心输入初始化完成 - 屏幕尺寸: {self.screen_width}x{self.screen_height}")
        
    def _load_windows_api(self):
        """加载Windows API函数"""
        try:
            # 用户32.dll
            self.user32 = ctypes.windll.user32
            self.kernel32 = ctypes.windll.kernel32
            
            # 设置函数原型
            self.user32.SetCursorPos.argtypes = [ctypes.c_int, ctypes.c_int]
            self.user32.SetCursorPos.restype = ctypes.c_bool
            
            self.user32.GetCursorPos.argtypes = [ctypes.POINTER(POINT)]
            self.user32.GetCursorPos.restype = ctypes.c_bool
            
            self.user32.SendInput.argtypes = [wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int]
            self.user32.SendInput.restype = wintypes.UINT
            
            self.user32.GetSystemMetrics.argtypes = [ctypes.c_int]
            self.user32.GetSystemMetrics.restype = ctypes.c_int
            
            self.user32.GetAsyncKeyState.argtypes = [ctypes.c_int]
            self.user32.GetAsyncKeyState.restype = ctypes.c_short
            
            print("Windows API加载成功")
            
        except Exception as e:
            print(f"Windows API加载失败: {e}")
            raise
            
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
                
                # 计算移动时间
                if duration is None:
                    current_pos = self.get_mouse_position()
                    distance = ((target_x - current_pos[0]) ** 2 + (target_y - current_pos[1]) ** 2) ** 0.5
                    duration = min(0.3, max(0.05, distance / 2000))
                    
                # 应用人性化延迟
                duration = self._apply_humanize_delay(duration)
                
                # 平滑移动
                steps = max(1, int(duration * 120))  # 120fps
                current_pos = self.get_mouse_position()
                
                for i in range(steps + 1):
                    progress = i / steps
                    # 使用缓动函数
                    progress = self._ease_in_out_cubic(progress)
                    
                    new_x = int(current_pos[0] + (target_x - current_pos[0]) * progress)
                    new_y = int(current_pos[1] + (target_y - current_pos[1]) * progress)
                    
                    self.user32.SetCursorPos(new_x, new_y)
                    time.sleep(duration / steps)
                    
                return True
                
        except Exception as e:
            print(f"鼠标移动失败: {e}")
            return False
            
    def _ease_in_out_cubic(self, t: float) -> float:
        """三次缓动函数"""
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 3) / 2
            
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
                
                # 映射按钮
                button_map = {
                    "left": (MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP),
                    "right": (MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP),
                    "middle": (MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP)
                }
                
                if button not in button_map:
                    return False
                    
                down_flag, up_flag = button_map[button]
                
                for _ in range(clicks):
                    # 创建鼠标输入结构
                    mouse_input = INPUT()
                    mouse_input.type = INPUT_MOUSE
                    mouse_input.ii.mi.dx = 0
                    mouse_input.ii.mi.dy = 0
                    mouse_input.ii.mi.mouseData = 0
                    mouse_input.ii.mi.time = 0
                    mouse_input.ii.mi.dwExtraInfo = None
                    
                    # 按下
                    mouse_input.ii.mi.dwFlags = down_flag
                    self.user32.SendInput(1, ctypes.byref(mouse_input), ctypes.sizeof(INPUT))
                    time.sleep(0.01)
                    
                    # 释放
                    mouse_input.ii.mi.dwFlags = up_flag
                    self.user32.SendInput(1, ctypes.byref(mouse_input), ctypes.sizeof(INPUT))
                    time.sleep(0.01)
                    
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
                
                # 应用按键延迟
                delay = random.uniform(*self.humanize_config["key_delay_range"])
                delay = self._apply_humanize_delay(delay)
                time.sleep(delay)
                
                # 检查是否是组合键
                if '+' in key:
                    return self._press_combo_key(key, presses)
                else:
                    return self._press_single_key(key, presses)
                
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
                
                if interval is None:
                    interval = random.uniform(0.05, 0.12)
                    
                for char in text:
                    if char == ' ':
                        self.press_key('space')
                    elif char == '\n':
                        self.press_key('enter')
                    elif char == '\t':
                        self.press_key('tab')
                    else:
                        # 对于其他字符，使用Unicode输入
                        self._send_unicode_char(char)
                        
                    time.sleep(interval)
                    
                return True
                
        except Exception as e:
            print(f"文本输入失败: {e}")
            return False
            
    def _send_unicode_char(self, char: str) -> bool:
        """发送Unicode字符"""
        try:
            # 创建键盘输入结构
            key_input = INPUT()
            key_input.type = INPUT_KEYBOARD
            key_input.ii.ki.wVk = 0
            key_input.ii.ki.wScan = ord(char)
            key_input.ii.ki.time = 0
            key_input.ii.ki.dwExtraInfo = None
            
            # 按下
            key_input.ii.ki.dwFlags = KEYEVENTF_UNICODE
            self.user32.SendInput(1, ctypes.byref(key_input), ctypes.sizeof(INPUT))
            time.sleep(0.01)
            
            # 释放
            key_input.ii.ki.dwFlags = KEYEVENTF_UNICODE | KEYEVENTF_KEYUP
            self.user32.SendInput(1, ctypes.byref(key_input), ctypes.sizeof(INPUT))
            time.sleep(0.01)
            
            return True
            
        except Exception as e:
            print(f"Unicode字符输入失败: {e}")
            return False
            
    def get_mouse_position(self) -> Tuple[int, int]:
        """获取当前鼠标位置"""
        try:
            point = POINT()
            if self.user32.GetCursorPos(ctypes.byref(point)):
                return (point.x, point.y)
            else:
                return (0, 0)
        except Exception as e:
            print(f"获取鼠标位置失败: {e}")
            return (0, 0)
            
    def get_screen_size(self) -> Tuple[int, int]:
        """获取屏幕尺寸"""
        return (self.screen_width, self.screen_height)
        
    def is_key_pressed(self, key: str) -> bool:
        """检查按键是否被按下"""
        try:
            vk_code = VK_CODES.get(key.lower())
            if vk_code is None:
                return False
                
            state = self.user32.GetAsyncKeyState(vk_code)
            return bool(state & 0x8000)
            
        except Exception as e:
            print(f"检查按键状态失败: {e}")
            return False
            
    def _press_single_key(self, key: str, presses: int = 1) -> bool:
        """按下单个按键"""
        try:
            # 获取虚拟键码
            vk_code = VK_CODES.get(key.lower())
            if vk_code is None:
                print(f"不支持的按键: {key}")
                return False
                
            for _ in range(presses):
                # 创建键盘输入结构
                key_input = INPUT()
                key_input.type = INPUT_KEYBOARD
                key_input.ii.ki.wVk = vk_code
                key_input.ii.ki.wScan = 0
                key_input.ii.ki.time = 0
                key_input.ii.ki.dwExtraInfo = None
                
                # 按下
                key_input.ii.ki.dwFlags = 0
                self.user32.SendInput(1, ctypes.byref(key_input), ctypes.sizeof(INPUT))
                time.sleep(0.01)
                
                # 释放
                key_input.ii.ki.dwFlags = KEYEVENTF_KEYUP
                self.user32.SendInput(1, ctypes.byref(key_input), ctypes.sizeof(INPUT))
                time.sleep(0.01)
            
            return True
            
        except Exception as e:
            print(f"单个按键操作失败: {e}")
            return False
            
    def _press_combo_key(self, combo_key: str, presses: int = 1) -> bool:
        """按下组合键"""
        try:
            # 解析组合键
            keys = combo_key.split('+')
            if len(keys) != 2:
                print(f"不支持的组合键格式: {combo_key}")
                return False
                
            modifier_key = keys[0].strip().lower()
            main_key = keys[1].strip().lower()
            
            # 获取虚拟键码
            modifier_vk = VK_CODES.get(modifier_key)
            main_vk = VK_CODES.get(main_key)
            
            if modifier_vk is None:
                print(f"不支持的修饰键: {modifier_key}")
                return False
            if main_vk is None:
                print(f"不支持的按键: {main_key}")
                return False
            
            for _ in range(presses):
                # 按下修饰键
                modifier_input = INPUT()
                modifier_input.type = INPUT_KEYBOARD
                modifier_input.ii.ki.wVk = modifier_vk
                modifier_input.ii.ki.wScan = 0
                modifier_input.ii.ki.time = 0
                modifier_input.ii.ki.dwExtraInfo = None
                modifier_input.ii.ki.dwFlags = 0  # 按下
                
                self.user32.SendInput(1, ctypes.byref(modifier_input), ctypes.sizeof(INPUT))
                time.sleep(0.01)
                
                # 按下主键
                main_input = INPUT()
                main_input.type = INPUT_KEYBOARD
                main_input.ii.ki.wVk = main_vk
                main_input.ii.ki.wScan = 0
                main_input.ii.ki.time = 0
                main_input.ii.ki.dwExtraInfo = None
                main_input.ii.ki.dwFlags = 0  # 按下
                
                self.user32.SendInput(1, ctypes.byref(main_input), ctypes.sizeof(INPUT))
                time.sleep(0.01)
                
                # 释放主键
                main_input.ii.ki.dwFlags = KEYEVENTF_KEYUP
                self.user32.SendInput(1, ctypes.byref(main_input), ctypes.sizeof(INPUT))
                time.sleep(0.01)
                
                # 释放修饰键
                modifier_input.ii.ki.dwFlags = KEYEVENTF_KEYUP
                self.user32.SendInput(1, ctypes.byref(modifier_input), ctypes.sizeof(INPUT))
                time.sleep(0.01)
            
            return True
            
        except Exception as e:
            print(f"组合键操作失败: {e}")
            return False
            
    def set_humanize_config(self, config: Dict[str, Any]):
        """设置人性化配置"""
        self.humanize_config.update(config)
        
    def set_cooldown(self, cooldown: float):
        """设置动作冷却时间"""
        self.action_cooldown = max(0, cooldown)
        
    def get_available_keys(self) -> List[str]:
        """获取支持的按键列表"""
        return list(VK_CODES.keys())


def test_windows_core():
    """测试Windows核心输入功能"""
    print("测试Windows核心输入功能...")
    
    provider = WindowsCoreInput(humanize_enabled=True)
    
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
    
    print("Windows核心输入测试完成!")


def test_windows_core():
    """测试Windows核心输入功能"""
    print("测试Windows核心输入功能...")
    
    provider = WindowsCoreInput()
    
    # 测试鼠标移动
    print("测试鼠标移动...")
    provider.move_mouse(100, 100)
    time.sleep(1)
    
    # 测试鼠标点击
    print("测试鼠标点击...")
    provider.click(200, 200)
    time.sleep(1)
    
    # 测试按键
    print("测试按键...")
    provider.press_key("space")
    time.sleep(1)
    
    # 测试文本输入
    print("测试文本输入...")
    provider.type_text("Hello World!")
    time.sleep(1)
    
    # 测试按键状态
    print("测试按键状态...")
    space_pressed = provider.is_key_pressed("space")
    print(f"空格键状态: {'按下' if space_pressed else '未按下'}")
    
    print("Windows核心输入测试完成!")


if __name__ == "__main__":
    test_windows_core()
        self._lock = threading.Lock()
        self.humanize_config = {
            "mouse_delay_range": [80, 140],
            "key_delay_range": [80, 140],
            "type_delay_range": [50, 100]
        }
        
        # 获取屏幕尺寸
        self.screen_width = self.user32.GetSystemMetrics(0)
        self.screen_height = self.user32.GetSystemMetrics(1)
        print(f"Windows核心输入初始化完成 - 屏幕尺寸: {self.screen_width}x{self.screen_height}")
    
    def _wait_cooldown(self):
        """等待冷却时间"""
        time.sleep(0.01)
    
    def _apply_humanize_delay(self, delay: float) -> float:
        """应用人性化延迟"""
        return delay * random.uniform(0.8, 1.2)
    
    def move_mouse(self, x: int, y: int) -> bool:
        """移动鼠标"""
        try:
            with self._lock:
                self._wait_cooldown()
                
                # 应用人性化延迟
                delay = random.uniform(*self.humanize_config["mouse_delay_range"])
                delay = self._apply_humanize_delay(delay)
                time.sleep(delay / 1000.0)
                
                # 使用Windows API移动鼠标
                self.user32.SetCursorPos(x, y)
                return True
                
        except Exception as e:
            print(f"鼠标移动失败: {e}")
            return False
    
    def click(self, x: int = None, y: int = None, button: str = "left") -> bool:
        """点击鼠标"""
        try:
            with self._lock:
                self._wait_cooldown()
                
                # 如果指定了坐标，先移动鼠标
                if x is not None and y is not None:
                    self.move_mouse(x, y)
                
                # 应用人性化延迟
                delay = random.uniform(*self.humanize_config["mouse_delay_range"])
                delay = self._apply_humanize_delay(delay)
                time.sleep(delay / 1000.0)
                
                # 确定鼠标事件类型
                if button.lower() == "left":
                    down_flag = MOUSEEVENTF_LEFTDOWN
                    up_flag = MOUSEEVENTF_LEFTUP
                elif button.lower() == "right":
                    down_flag = MOUSEEVENTF_RIGHTDOWN
                    up_flag = MOUSEEVENTF_RIGHTUP
                elif button.lower() == "middle":
                    down_flag = MOUSEEVENTF_MIDDLEDOWN
                    up_flag = MOUSEEVENTF_MIDDLEUP
                else:
                    print(f"不支持的鼠标按键: {button}")
                    return False
                
                # 创建鼠标输入结构
                mouse_input = INPUT()
                mouse_input.type = INPUT_MOUSE
                mouse_input.mi.dx = 0
                mouse_input.mi.dy = 0
                mouse_input.mi.mouseData = 0
                mouse_input.mi.dwFlags = down_flag
                mouse_input.mi.time = 0
                mouse_input.mi.dwExtraInfo = None
                
                # 发送鼠标按下事件
                self.user32.SendInput(1, ctypes.byref(mouse_input), ctypes.sizeof(INPUT))
                time.sleep(0.01)
                
                # 发送鼠标释放事件
                mouse_input.mi.dwFlags = up_flag
                self.user32.SendInput(1, ctypes.byref(mouse_input), ctypes.sizeof(INPUT))
                
                return True
                
        except Exception as e:
            print(f"鼠标点击失败: {e}")
            return False
    
    def press_key(self, key: str, presses: int = 1) -> bool:
        """按下键盘按键"""
        try:
            with self._lock:
                self._wait_cooldown()
                
                # 应用按键延迟
                delay = random.uniform(*self.humanize_config["key_delay_range"])
                delay = self._apply_humanize_delay(delay)
                time.sleep(delay / 1000.0)
                
                # 检查是否是组合键
                if '+' in key:
                    return self._press_combo_key(key, presses)
                else:
                    return self._press_single_key(key, presses)
                    
        except Exception as e:
            print(f"按键操作失败: {e}")
            return False
    
    def _press_single_key(self, key: str, presses: int = 1) -> bool:
        """按下单个按键"""
        try:
            # 获取虚拟键码
            vk_code = VK_CODES.get(key.lower())
            if vk_code is None:
                print(f"不支持的按键: {key}")
                return False
                
            for _ in range(presses):
                # 创建键盘输入结构
                key_input = INPUT()
                key_input.type = INPUT_KEYBOARD
                key_input.ii.ki.wVk = vk_code
                key_input.ii.ki.wScan = 0
                key_input.ii.ki.time = 0
                key_input.ii.ki.dwExtraInfo = None
                
                # 按下
                key_input.ii.ki.dwFlags = 0
                self.user32.SendInput(1, ctypes.byref(key_input), ctypes.sizeof(INPUT))
                time.sleep(0.01)
                
                # 释放
                key_input.ii.ki.dwFlags = KEYEVENTF_KEYUP
                self.user32.SendInput(1, ctypes.byref(key_input), ctypes.sizeof(INPUT))
                time.sleep(0.01)
            
            return True
            
        except Exception as e:
            print(f"单个按键操作失败: {e}")
            return False
            
    def _press_combo_key(self, combo_key: str, presses: int = 1) -> bool:
        """按下组合键"""
        try:
            # 解析组合键
            keys = combo_key.split('+')
            if len(keys) != 2:
                print(f"不支持的组合键格式: {combo_key}")
                return False
                
            modifier_key = keys[0].strip().lower()
            main_key = keys[1].strip().lower()
            
            # 获取虚拟键码
            modifier_vk = VK_CODES.get(modifier_key)
            main_vk = VK_CODES.get(main_key)
            
            if modifier_vk is None:
                print(f"不支持的修饰键: {modifier_key}")
                return False
            if main_vk is None:
                print(f"不支持的按键: {main_key}")
                return False
            
            for _ in range(presses):
                # 按下修饰键
                modifier_input = INPUT()
                modifier_input.type = INPUT_KEYBOARD
                modifier_input.ii.ki.wVk = modifier_vk
                modifier_input.ii.ki.wScan = 0
                modifier_input.ii.ki.time = 0
                modifier_input.ii.ki.dwExtraInfo = None
                modifier_input.ii.ki.dwFlags = 0  # 按下
                
                self.user32.SendInput(1, ctypes.byref(modifier_input), ctypes.sizeof(INPUT))
                time.sleep(0.01)
                
                # 按下主键
                main_input = INPUT()
                main_input.type = INPUT_KEYBOARD
                main_input.ii.ki.wVk = main_vk
                main_input.ii.ki.wScan = 0
                main_input.ii.ki.time = 0
                main_input.ii.ki.dwExtraInfo = None
                main_input.ii.ki.dwFlags = 0  # 按下
                
                self.user32.SendInput(1, ctypes.byref(main_input), ctypes.sizeof(INPUT))
                time.sleep(0.01)
                
                # 释放主键
                main_input.ii.ki.dwFlags = KEYEVENTF_KEYUP
                self.user32.SendInput(1, ctypes.byref(main_input), ctypes.sizeof(INPUT))
                time.sleep(0.01)
                
                # 释放修饰键
                modifier_input.ii.ki.dwFlags = KEYEVENTF_KEYUP
                self.user32.SendInput(1, ctypes.byref(modifier_input), ctypes.sizeof(INPUT))
                time.sleep(0.01)
            
            return True
            
        except Exception as e:
            print(f"组合键操作失败: {e}")
            return False


if __name__ == "__main__":
    test_windows_core()
