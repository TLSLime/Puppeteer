# -*- coding: utf-8 -*-
"""
安全监控模块 - 检测用户主动操作并停止自动化程序
防止自动化程序造成非预期损失
"""

import time
import threading
import ctypes
import ctypes.wintypes
from typing import Dict, List, Optional, Tuple, Any, Callable
from enum import Enum
import queue


class SafetyEvent(Enum):
    """安全事件类型"""
    MOUSE_MOVE = "mouse_move"
    MOUSE_CLICK = "mouse_click"
    KEYBOARD_INPUT = "keyboard_input"
    EMERGENCY_STOP = "emergency_stop"


class SafetyLevel(Enum):
    """安全级别"""
    DISABLED = "disabled"  # 完全禁用安全机制
    LOW = "low"           # 仅检测紧急停止键
    MEDIUM = "medium"     # 检测鼠标和键盘
    HIGH = "high"         # 检测所有用户操作


class SafetyMonitor:
    """安全监控器"""
    
    def __init__(self, safety_level: SafetyLevel = SafetyLevel.MEDIUM, 
                 emergency_key: str = "esc", callback: Optional[Callable] = None):
        """
        初始化安全监控器
        
        Args:
            safety_level: 安全级别
            emergency_key: 紧急停止键
            callback: 安全事件回调函数
        """
        self.safety_level = safety_level
        self.emergency_key = emergency_key
        self.callback = callback
        
        # 监控状态
        self._monitoring = False
        self._stop_requested = False
        self._monitor_thread = None
        self._lock = threading.Lock()
        
        # 事件队列
        self._event_queue = queue.Queue()
        
        # 用户操作检测
        self._last_mouse_pos = (0, 0)
        self._last_mouse_time = 0
        self._last_key_time = 0
        self._user_activity_threshold = 1.0  # 1秒内的操作认为是用户操作
        self._mouse_movement_threshold = 50  # 鼠标移动超过50像素才认为是用户操作
        self._automation_start_time = time.time()  # 自动化开始时间
        self._grace_period = 5.0  # 启动后5秒内的操作不认为是用户操作
        
        # 统计信息
        self._stats = {
            "mouse_events": 0,
            "keyboard_events": 0,
            "emergency_stops": 0,
            "total_events": 0
        }
        
        # 初始化Windows API
        self._init_windows_api()
        
        print(f"安全监控器初始化完成 - 安全级别: {safety_level.value}, 紧急键: {emergency_key}")
        
    def _init_windows_api(self):
        """初始化Windows API"""
        try:
            self.user32 = ctypes.windll.user32
            self.kernel32 = ctypes.windll.kernel32
            
            # 设置函数原型
            self.user32.GetCursorPos.argtypes = [ctypes.POINTER(ctypes.wintypes.POINT)]
            self.user32.GetCursorPos.restype = ctypes.c_bool
            
            self.user32.GetAsyncKeyState.argtypes = [ctypes.c_int]
            self.user32.GetAsyncKeyState.restype = ctypes.c_short
            
            self.user32.GetSystemMetrics.argtypes = [ctypes.c_int]
            self.user32.GetSystemMetrics.restype = ctypes.c_int
            
            # 虚拟键码
            self.VK_CODES = {
                'esc': 0x1B, 'space': 0x20, 'enter': 0x0D, 'tab': 0x09,
                'shift': 0x10, 'ctrl': 0x11, 'alt': 0x12,
                'f1': 0x70, 'f2': 0x71, 'f3': 0x72, 'f4': 0x73,
                'f5': 0x74, 'f6': 0x75, 'f7': 0x76, 'f8': 0x77,
                'f9': 0x78, 'f10': 0x79, 'f11': 0x7A, 'f12': 0x7B,
                'a': 0x41, 'b': 0x42, 'c': 0x43, 'd': 0x44, 'e': 0x45,
                'f': 0x46, 'g': 0x47, 'h': 0x48, 'i': 0x49, 'j': 0x4A,
                'k': 0x4B, 'l': 0x4C, 'm': 0x4D, 'n': 0x4E, 'o': 0x4F,
                'p': 0x50, 'q': 0x51, 'r': 0x52, 's': 0x53, 't': 0x54,
                'u': 0x55, 'v': 0x56, 'w': 0x57, 'x': 0x58, 'y': 0x59, 'z': 0x5A
            }
            
            print("Windows API初始化成功")
            
        except Exception as e:
            print(f"Windows API初始化失败: {e}")
            raise
            
    def start_monitoring(self):
        """开始监控"""
        if self._monitoring:
            print("安全监控已在运行")
            return
            
        with self._lock:
            self._monitoring = True
            self._stop_requested = False
            self._automation_start_time = time.time()  # 重置启动时间
            self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self._monitor_thread.start()
            
        print("安全监控已启动")
        
    def stop_monitoring(self):
        """停止监控"""
        if not self._monitoring:
            print("安全监控未在运行")
            return
            
        with self._lock:
            self._monitoring = False
            self._stop_requested = True
            
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=1.0)
            
        print("安全监控已停止")
        
    def _monitor_loop(self):
        """监控循环"""
        print("安全监控循环开始")
        
        while self._monitoring and not self._stop_requested:
            try:
                current_time = time.time()
                
                # 检测紧急停止键
                if self._check_emergency_key():
                    self._handle_emergency_stop()
                    break
                    
                # 根据安全级别检测用户操作
                if self.safety_level == SafetyLevel.DISABLED:
                    # 完全禁用安全机制
                    pass
                elif self.safety_level in [SafetyLevel.MEDIUM, SafetyLevel.HIGH]:
                    # 检测鼠标操作
                    if self._check_mouse_activity(current_time):
                        self._handle_user_activity(SafetyEvent.MOUSE_MOVE)
                        break
                        
                    # 检测键盘操作
                    if self._check_keyboard_activity(current_time):
                        self._handle_user_activity(SafetyEvent.KEYBOARD_INPUT)
                        break
                        
                # 短暂休眠
                time.sleep(0.01)  # 10ms检测间隔
                
            except Exception as e:
                print(f"安全监控循环异常: {e}")
                time.sleep(0.1)
                
        print("安全监控循环结束")
        
    def _check_emergency_key(self) -> bool:
        """检查紧急停止键"""
        try:
            vk_code = self.VK_CODES.get(self.emergency_key.lower())
            if vk_code is None:
                return False
                
            state = self.user32.GetAsyncKeyState(vk_code)
            return bool(state & 0x8000)  # 检查最高位（按下状态）
            
        except Exception as e:
            print(f"检查紧急停止键失败: {e}")
            return False
            
    def _check_mouse_activity(self, current_time: float) -> bool:
        """检查鼠标活动"""
        try:
            # 检查是否在宽限期内
            if current_time - self._automation_start_time < self._grace_period:
                return False
                
            # 获取当前鼠标位置
            point = ctypes.wintypes.POINT()
            if not self.user32.GetCursorPos(ctypes.byref(point)):
                return False
                
            current_pos = (point.x, point.y)
            
            # 检查鼠标是否移动超过阈值
            if current_pos != self._last_mouse_pos:
                # 计算移动距离
                distance = ((current_pos[0] - self._last_mouse_pos[0]) ** 2 + 
                           (current_pos[1] - self._last_mouse_pos[1]) ** 2) ** 0.5
                
                # 只有移动距离超过阈值且时间间隔足够才认为是用户操作
                if (distance > self._mouse_movement_threshold and 
                    current_time - self._last_mouse_time > self._user_activity_threshold):
                    self._last_mouse_pos = current_pos
                    self._last_mouse_time = current_time
                    return True
                else:
                    # 更新位置但不触发事件
                    self._last_mouse_pos = current_pos
                    
            # 检查鼠标点击
            mouse_buttons = [0x01, 0x02, 0x04]  # 左键、右键、中键
            for button in mouse_buttons:
                state = self.user32.GetAsyncKeyState(button)
                if state & 0x8000:  # 按下状态
                    if current_time - self._last_mouse_time > self._user_activity_threshold:
                        self._last_mouse_time = current_time
                        return True
                        
            return False
            
        except Exception as e:
            print(f"检查鼠标活动失败: {e}")
            return False
            
    def _check_keyboard_activity(self, current_time: float) -> bool:
        """检查键盘活动"""
        try:
            # 检查是否在宽限期内
            if current_time - self._automation_start_time < self._grace_period:
                return False
                
            # 检查常用按键
            common_keys = [0x20, 0x0D, 0x09, 0x10, 0x11, 0x12]  # 空格、回车、Tab、Shift、Ctrl、Alt
            
            for key in common_keys:
                state = self.user32.GetAsyncKeyState(key)
                if state & 0x8000:  # 按下状态
                    if current_time - self._last_key_time > self._user_activity_threshold:
                        self._last_key_time = current_time
                        return True
                        
            # 检查字母键
            for i in range(0x41, 0x5B):  # A-Z
                state = self.user32.GetAsyncKeyState(i)
                if state & 0x8000:  # 按下状态
                    if current_time - self._last_key_time > self._user_activity_threshold:
                        self._last_key_time = current_time
                        return True
                        
            return False
            
        except Exception as e:
            print(f"检查键盘活动失败: {e}")
            return False
            
    def _handle_emergency_stop(self):
        """处理紧急停止"""
        print(f"\n🚨 紧急停止触发！用户按下了 {self.emergency_key.upper()} 键")
        self._stats["emergency_stops"] += 1
        self._stats["total_events"] += 1
        
        self._trigger_callback(SafetyEvent.EMERGENCY_STOP, {
            "reason": "emergency_key_pressed",
            "key": self.emergency_key,
            "timestamp": time.time()
        })
        
    def _handle_user_activity(self, event_type: SafetyEvent):
        """处理用户活动"""
        if event_type == SafetyEvent.MOUSE_MOVE:
            print(f"\n⚠️ 检测到用户鼠标操作，自动化程序已停止")
            self._stats["mouse_events"] += 1
        elif event_type == SafetyEvent.KEYBOARD_INPUT:
            print(f"\n⚠️ 检测到用户键盘操作，自动化程序已停止")
            self._stats["keyboard_events"] += 1
            
        self._stats["total_events"] += 1
        
        self._trigger_callback(event_type, {
            "reason": "user_activity_detected",
            "event_type": event_type.value,
            "timestamp": time.time()
        })
        
    def _trigger_callback(self, event_type: SafetyEvent, data: Dict[str, Any]):
        """触发回调函数"""
        if self.callback:
            try:
                self.callback(event_type, data)
            except Exception as e:
                print(f"安全回调函数执行失败: {e}")
                
    def is_monitoring(self) -> bool:
        """检查是否正在监控"""
        return self._monitoring
        
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return self._stats.copy()
        
    def reset_stats(self):
        """重置统计信息"""
        self._stats = {
            "mouse_events": 0,
            "keyboard_events": 0,
            "emergency_stops": 0,
            "total_events": 0
        }
        
    def set_safety_level(self, level: SafetyLevel):
        """设置安全级别"""
        self.safety_level = level
        print(f"安全级别已更改为: {level.value}")
        
    def set_emergency_key(self, key: str):
        """设置紧急停止键"""
        if key.lower() in self.VK_CODES:
            self.emergency_key = key
            print(f"紧急停止键已更改为: {key.upper()}")
        else:
            print(f"不支持的按键: {key}")
            
    def set_user_activity_threshold(self, threshold: float):
        """设置用户活动检测阈值"""
        self._user_activity_threshold = max(0.01, threshold)
        print(f"用户活动检测阈值已设置为: {self._user_activity_threshold}秒")
        
    def set_mouse_movement_threshold(self, threshold: int):
        """设置鼠标移动阈值"""
        self._mouse_movement_threshold = max(1, threshold)
        print(f"鼠标移动阈值已设置为: {self._mouse_movement_threshold}像素")
        
    def set_grace_period(self, period: float):
        """设置宽限期"""
        self._grace_period = max(0.0, period)
        print(f"宽限期已设置为: {self._grace_period}秒")
        
    def get_safety_config(self) -> Dict[str, Any]:
        """获取安全配置"""
        return {
            "safety_level": self.safety_level.value,
            "emergency_key": self.emergency_key,
            "user_activity_threshold": self._user_activity_threshold,
            "mouse_movement_threshold": self._mouse_movement_threshold,
            "grace_period": self._grace_period
        }


class SafetyManager:
    """安全管理器 - 统一管理安全功能"""
    
    def __init__(self, safety_level: SafetyLevel = SafetyLevel.MEDIUM):
        """
        初始化安全管理器
        
        Args:
            safety_level: 安全级别
        """
        self.safety_level = safety_level
        self.monitor = None
        self._automation_running = False
        self._lock = threading.Lock()
        
        # 安全配置
        self.config = {
            "emergency_key": "esc",
            "user_activity_threshold": 1.0,  # 更宽松的阈值
            "mouse_movement_threshold": 50,   # 鼠标移动阈值
            "grace_period": 5.0,             # 宽限期
            "auto_restart": False,
            "log_safety_events": True
        }
        
        print(f"安全管理器初始化完成 - 安全级别: {safety_level.value}")
        
    def start_safety_monitoring(self, callback: Optional[Callable] = None):
        """开始安全监控"""
        if self.monitor and self.monitor.is_monitoring():
            print("安全监控已在运行")
            return
            
        self.monitor = SafetyMonitor(
            safety_level=self.safety_level,
            emergency_key=self.config["emergency_key"],
            callback=callback or self._default_safety_callback
        )
        
        self.monitor.set_user_activity_threshold(self.config["user_activity_threshold"])
        self.monitor.set_mouse_movement_threshold(self.config["mouse_movement_threshold"])
        self.monitor.set_grace_period(self.config["grace_period"])
        self.monitor.start_monitoring()
        
    def stop_safety_monitoring(self):
        """停止安全监控"""
        if self.monitor:
            self.monitor.stop_monitoring()
            
    def start_automation(self):
        """开始自动化"""
        with self._lock:
            if self._automation_running:
                print("自动化已在运行")
                return
                
            self._automation_running = True
            
        print("自动化已启动")
        
    def stop_automation(self, reason: str = "manual_stop"):
        """停止自动化"""
        with self._lock:
            if not self._automation_running:
                print("自动化未在运行")
                return
                
            self._automation_running = False
            
        print(f"自动化已停止 - 原因: {reason}")
        
    def is_automation_running(self) -> bool:
        """检查自动化是否在运行"""
        return self._automation_running
        
    def is_monitoring(self) -> bool:
        """检查安全监控是否正在运行"""
        return self.monitor is not None and self.monitor.is_running
        
    def is_safety_monitoring(self) -> bool:
        """检查安全监控是否在运行"""
        return self.monitor and self.monitor.is_monitoring()
        
    def _default_safety_callback(self, event_type: SafetyEvent, data: Dict[str, Any]):
        """默认安全回调函数"""
        if event_type == SafetyEvent.EMERGENCY_STOP:
            self.stop_automation("emergency_stop")
        elif event_type in [SafetyEvent.MOUSE_MOVE, SafetyEvent.KEYBOARD_INPUT]:
            self.stop_automation("user_activity")
            
    def get_safety_stats(self) -> Dict[str, Any]:
        """获取安全统计信息"""
        if self.monitor:
            return self.monitor.get_stats()
        return {}
        
    def set_config(self, config: Dict[str, Any]):
        """设置安全配置"""
        self.config.update(config)
        if self.monitor:
            self.monitor.set_emergency_key(self.config["emergency_key"])
            self.monitor.set_user_activity_threshold(self.config["user_activity_threshold"])
            
    def get_config(self) -> Dict[str, Any]:
        """获取安全配置"""
        return self.config.copy()


def test_safety_monitor():
    """测试安全监控器"""
    print("测试安全监控器...")
    
    def safety_callback(event_type, data):
        print(f"安全事件: {event_type.value} - {data}")
        
    # 创建安全监控器
    monitor = SafetyMonitor(SafetyLevel.MEDIUM, "esc", safety_callback)
    
    print("开始监控，请尝试移动鼠标或按键盘...")
    print("按ESC键可以紧急停止")
    
    try:
        monitor.start_monitoring()
        
        # 监控10秒
        for i in range(100):
            time.sleep(0.1)
            if not monitor.is_monitoring():
                break
                
    except KeyboardInterrupt:
        print("\n用户中断测试")
        
    finally:
        monitor.stop_monitoring()
        
    # 显示统计信息
    stats = monitor.get_stats()
    print(f"\n监控统计:")
    print(f"  鼠标事件: {stats['mouse_events']}")
    print(f"  键盘事件: {stats['keyboard_events']}")
    print(f"  紧急停止: {stats['emergency_stops']}")
    print(f"  总事件数: {stats['total_events']}")
    
    print("安全监控器测试完成!")


if __name__ == "__main__":
    test_safety_monitor()
