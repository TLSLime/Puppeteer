# -*- coding: utf-8 -*-
"""
对话框处理器
处理自动化过程中遇到的确认弹窗和对话框
"""

import time
import ctypes
import ctypes.wintypes
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import threading
import re

# Windows API 常量
WM_CLOSE = 0x0010
WM_COMMAND = 0x0111
IDOK = 1
IDCANCEL = 2
IDYES = 6
IDNO = 7
IDABORT = 3
IDRETRY = 4
IDIGNORE = 5

# 对话框类型
class DialogType(Enum):
    """对话框类型枚举"""
    CONFIRMATION = "confirmation"  # 确认对话框
    WARNING = "warning"           # 警告对话框
    ERROR = "error"               # 错误对话框
    INFORMATION = "information"   # 信息对话框
    SAVE_CONFIRM = "save_confirm" # 保存确认
    EXIT_CONFIRM = "exit_confirm" # 退出确认
    DELETE_CONFIRM = "delete_confirm" # 删除确认
    UNKNOWN = "unknown"           # 未知对话框

class DialogHandler:
    """对话框处理器"""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化对话框处理器
        
        Args:
            config: 配置参数
        """
        self.config = config or {}
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32
        
        # 预期的对话框配置
        self.expected_dialogs = self.config.get("expected_dialogs", [])
        
        # 对话框检测间隔
        self.detection_interval = self.config.get("detection_interval", 0.5)
        
        # 对话框超时时间
        self.dialog_timeout = self.config.get("dialog_timeout", 10.0)
        
        # 是否启用对话框处理
        self.enabled = self.config.get("enabled", True)
        
        # 对话框检测线程
        self.detection_thread = None
        self.is_detecting = False
        
        # 对话框处理回调
        self.dialog_callback = None
        
        print("对话框处理器初始化完成")
        
    def set_dialog_callback(self, callback):
        """设置对话框处理回调函数"""
        self.dialog_callback = callback
        
    def start_dialog_detection(self):
        """开始对话框检测"""
        if not self.enabled:
            return
            
        if self.is_detecting:
            return
            
        self.is_detecting = True
        self.detection_thread = threading.Thread(target=self._detection_loop, daemon=True)
        self.detection_thread.start()
        print("对话框检测已启动")
        
    def stop_dialog_detection(self):
        """停止对话框检测"""
        print("🔍 正在停止对话框检测...")
        self.is_detecting = False
        
        if self.detection_thread and self.detection_thread.is_alive():
            print("🔍 等待检测线程结束...")
            self.detection_thread.join(timeout=2.0)
            
            if self.detection_thread.is_alive():
                print("⚠️ 检测线程未能在2秒内结束，强制继续")
            else:
                print("✅ 检测线程已正常结束")
        
        print("✅ 对话框检测已停止")
        
    def _detection_loop(self):
        """对话框检测循环"""
        print("🔍 对话框检测循环已启动")
        loop_count = 0
        
        while self.is_detecting:
            try:
                loop_count += 1
                
                # 每100次循环显示一次状态（可选）
                if loop_count % 100 == 0:
                    print(f"🔍 对话框检测循环运行中... (第{loop_count}次)")
                
                # 检测对话框
                dialogs = self._detect_dialogs()
                
                if dialogs:
                    print(f"🔍 检测到 {len(dialogs)} 个对话框")
                    for dialog in dialogs:
                        self._handle_dialog(dialog)
                        
                # 使用更短的睡眠时间，提高响应性
                time.sleep(min(self.detection_interval, 0.1))
                
            except KeyboardInterrupt:
                print("🔍 对话框检测循环被用户中断")
                break
            except Exception as e:
                print(f"❌ 对话框检测异常: {e}")
                # 异常时使用更长的睡眠时间，避免快速重试
                time.sleep(1.0)
                
        print("🔍 对话框检测循环已结束")
                
    def _detect_dialogs(self) -> List[Dict[str, Any]]:
        """
        检测当前系统中的对话框
        
        Returns:
            对话框信息列表
        """
        dialogs = []
        
        try:
            # 限制检测的窗口数量，避免长时间阻塞
            max_windows = 50
            window_count = 0
            
            # 枚举所有窗口
            hwnd = self.user32.FindWindowW(None, None)
            while hwnd and window_count < max_windows:
                window_count += 1
                
                try:
                    if self.user32.IsWindowVisible(hwnd):
                        # 获取窗口标题
                        window_title = ctypes.create_unicode_buffer(256)
                        self.user32.GetWindowTextW(hwnd, window_title, 256)
                        title = window_title.value
                        
                        # 检查是否是对话框
                        if self._is_dialog_window(hwnd, title):
                            dialog_info = self._analyze_dialog(hwnd, title)
                            if dialog_info:
                                dialogs.append(dialog_info)
                                
                except Exception as e:
                    # 单个窗口检测失败不影响整体检测
                    pass
                    
                hwnd = self.user32.FindWindowExW(None, hwnd, None, None)
                
        except Exception as e:
            print(f"❌ 检测对话框异常: {e}")
            
        return dialogs
        
    def _is_dialog_window(self, hwnd: ctypes.wintypes.HWND, title: str) -> bool:
        """
        判断窗口是否是对话框
        
        Args:
            hwnd: 窗口句柄
            title: 窗口标题
            
        Returns:
            是否是对话框
        """
        try:
            # 检查窗口类名
            class_name = ctypes.create_unicode_buffer(256)
            self.user32.GetClassNameW(hwnd, class_name, 256)
            class_name_str = class_name.value.lower()
            
            # 常见的对话框类名
            dialog_classes = [
                "#32770",  # 标准对话框
                "dialog",
                "messagebox",
                "msgbox",
                "confirm",
                "alert"
            ]
            
            # 检查类名
            for dialog_class in dialog_classes:
                if dialog_class in class_name_str:
                    return True
                    
            # 检查标题中的关键词
            dialog_keywords = [
                "确认", "确认删除", "确认保存", "确认退出",
                "警告", "错误", "提示", "信息",
                "确定", "取消", "是", "否",
                "confirm", "warning", "error", "alert",
                "ok", "cancel", "yes", "no",
                "save", "delete", "exit", "close"
            ]
            
            title_lower = title.lower()
            for keyword in dialog_keywords:
                if keyword in title_lower:
                    return True
                    
            return False
            
        except Exception as e:
            print(f"判断对话框窗口异常: {e}")
            return False
            
    def _analyze_dialog(self, hwnd: ctypes.wintypes.HWND, title: str) -> Optional[Dict[str, Any]]:
        """
        分析对话框信息
        
        Args:
            hwnd: 窗口句柄
            title: 窗口标题
            
        Returns:
            对话框信息字典
        """
        try:
            # 获取对话框文本内容
            content = self._get_dialog_content(hwnd)
            
            # 分析对话框类型
            dialog_type = self._classify_dialog(title, content)
            
            # 检查是否是预期的对话框
            is_expected = self._is_expected_dialog(title, content)
            
            dialog_info = {
                "hwnd": hwnd,
                "title": title,
                "content": content,
                "type": dialog_type,
                "is_expected": is_expected,
                "timestamp": time.time()
            }
            
            return dialog_info
            
        except Exception as e:
            print(f"分析对话框异常: {e}")
            return None
            
    def _get_dialog_content(self, hwnd: ctypes.wintypes.HWND) -> str:
        """
        获取对话框内容文本
        
        Args:
            hwnd: 窗口句柄
            
        Returns:
            对话框内容文本
        """
        try:
            content = ""
            
            # 查找静态文本控件
            static_hwnd = self.user32.FindWindowExW(hwnd, None, "Static", None)
            while static_hwnd:
                text = ctypes.create_unicode_buffer(256)
                self.user32.GetWindowTextW(static_hwnd, text, 256)
                if text.value:
                    content += text.value + "\n"
                static_hwnd = self.user32.FindWindowExW(hwnd, static_hwnd, "Static", None)
                
            return content.strip()
            
        except Exception as e:
            print(f"获取对话框内容异常: {e}")
            return ""
            
    def _classify_dialog(self, title: str, content: str) -> DialogType:
        """
        分类对话框类型
        
        Args:
            title: 对话框标题
            content: 对话框内容
            
        Returns:
            对话框类型
        """
        try:
            text = (title + " " + content).lower()
            
            # 保存确认
            if any(keyword in text for keyword in ["保存", "save", "是否保存", "do you want to save"]):
                return DialogType.SAVE_CONFIRM
                
            # 删除确认
            if any(keyword in text for keyword in ["删除", "delete", "确认删除", "confirm delete"]):
                return DialogType.DELETE_CONFIRM
                
            # 退出确认
            if any(keyword in text for keyword in ["退出", "exit", "关闭", "close", "确认退出"]):
                return DialogType.EXIT_CONFIRM
                
            # 错误对话框
            if any(keyword in text for keyword in ["错误", "error", "失败", "failed", "异常", "exception"]):
                return DialogType.ERROR
                
            # 警告对话框
            if any(keyword in text for keyword in ["警告", "warning", "注意", "attention", "caution"]):
                return DialogType.WARNING
                
            # 信息对话框
            if any(keyword in text for keyword in ["信息", "information", "提示", "info", "消息", "message"]):
                return DialogType.INFORMATION
                
            # 确认对话框
            if any(keyword in text for keyword in ["确认", "confirm", "确定", "ok", "是", "yes", "否", "no"]):
                return DialogType.CONFIRMATION
                
            return DialogType.UNKNOWN
            
        except Exception as e:
            print(f"分类对话框异常: {e}")
            return DialogType.UNKNOWN
            
    def _is_expected_dialog(self, title: str, content: str) -> bool:
        """
        检查是否是预期的对话框
        
        Args:
            title: 对话框标题
            content: 对话框内容
            
        Returns:
            是否是预期的对话框
        """
        try:
            # 检查配置中的预期对话框
            for expected in self.expected_dialogs:
                title_match = expected.get("title", "").lower() in title.lower()
                content_match = expected.get("content", "").lower() in content.lower()
                
                if title_match or content_match:
                    return True
                    
            # 默认预期一些常见的保存确认对话框
            default_expected = [
                "是否保存", "do you want to save", "保存文件", "save file",
                "文档已修改", "document has been modified"
            ]
            
            text = (title + " " + content).lower()
            for expected_text in default_expected:
                if expected_text in text:
                    return True
                    
            return False
            
        except Exception as e:
            print(f"检查预期对话框异常: {e}")
            return False
            
    def _handle_dialog(self, dialog_info: Dict[str, Any]):
        """
        处理对话框
        
        Args:
            dialog_info: 对话框信息
        """
        try:
            hwnd = dialog_info["hwnd"]
            title = dialog_info["title"]
            content = dialog_info["content"]
            dialog_type = dialog_info["type"]
            is_expected = dialog_info["is_expected"]
            
            print(f"\n🔍 检测到对话框:")
            print(f"   📋 标题: {title}")
            print(f"   📄 内容: {content}")
            print(f"   🏷️  类型: {dialog_type.value}")
            print(f"   ✅ 是否预期: {'是' if is_expected else '否'}")
            print(f"   🕐 时间: {time.strftime('%H:%M:%S')}")
            
            # 调用回调函数
            if self.dialog_callback:
                self.dialog_callback(dialog_info)
                
            # 根据对话框类型和预期状态处理
            if is_expected:
                # 预期的对话框，点击确定
                print(f"✅ 这是预期的对话框，准备点击确定按钮...")
                print(f"   🎯 操作: 点击确定按钮")
                print(f"   📍 目标: {title}")
                self._click_dialog_button(hwnd, "ok")
                print(f"   ✅ 操作完成: 已点击确定按钮")
            else:
                # 非预期的对话框，点击取消并终止程序
                print(f"❌ 这是非预期的对话框，准备点击取消按钮并终止程序...")
                print(f"   🎯 操作: 点击取消按钮")
                print(f"   📍 目标: {title}")
                print(f"   ⚠️  原因: 非预期对话框，安全终止")
                self._click_dialog_button(hwnd, "cancel")
                print(f"   ✅ 操作完成: 已点击取消按钮")
                
                # 通知程序终止
                if self.dialog_callback:
                    self.dialog_callback({
                        "action": "terminate_program",
                        "reason": "unexpected_dialog",
                        "dialog_info": dialog_info
                    })
                    
        except Exception as e:
            print(f"处理对话框异常: {e}")
            
    def _click_dialog_button(self, hwnd: ctypes.wintypes.HWND, button_type: str):
        """
        点击对话框按钮
        
        Args:
            hwnd: 对话框窗口句柄
            button_type: 按钮类型 ("ok", "cancel", "yes", "no")
        """
        try:
            # 查找按钮控件
            button_hwnd = self._find_dialog_button(hwnd, button_type)
            
            if button_hwnd:
                # 获取按钮位置
                button_rect = self._get_button_rect(button_hwnd)
                if button_rect:
                    # 计算按钮中心点
                    center_x = button_rect[0] + (button_rect[2] - button_rect[0]) // 2
                    center_y = button_rect[1] + (button_rect[3] - button_rect[1]) // 2
                    
                    print(f"   📍 按钮位置: ({center_x}, {center_y})")
                    print(f"   🖱️  开始移动鼠标到按钮位置...")
                    
                    # 平滑移动鼠标到按钮位置
                    self._smooth_move_mouse(center_x, center_y)
                    
                    # 等待一下确保鼠标到达
                    print(f"   ⏳ 等待鼠标到达目标位置...")
                    time.sleep(0.2)
                    
                    # 点击按钮
                    print(f"   👆 开始点击按钮...")
                    self._click_mouse(center_x, center_y)
                    
                    print(f"   ✅ 鼠标点击完成: {button_type}")
                else:
                    print(f"无法获取按钮 {button_type} 的位置")
            else:
                print(f"未找到按钮 {button_type}，尝试使用API方式")
                # 回退到API方式
                self._click_dialog_button_api(hwnd, button_type)
            
        except Exception as e:
            print(f"点击对话框按钮异常: {e}")
            
    def _find_dialog_button(self, hwnd: ctypes.wintypes.HWND, button_type: str) -> Optional[ctypes.wintypes.HWND]:
        """
        查找对话框中的按钮控件
        
        Args:
            hwnd: 对话框窗口句柄
            button_type: 按钮类型
            
        Returns:
            按钮控件句柄
        """
        try:
            # 按钮文本映射
            button_texts = {
                "ok": ["确定", "OK", "是", "Yes"],
                "cancel": ["取消", "Cancel", "否", "No"],
                "yes": ["是", "Yes", "确定", "OK"],
                "no": ["否", "No", "取消", "Cancel"],
                "abort": ["中止", "Abort"],
                "retry": ["重试", "Retry"],
                "ignore": ["忽略", "Ignore"]
            }
            
            target_texts = button_texts.get(button_type.lower(), [button_type])
            
            # 查找按钮控件
            button_hwnd = self.user32.FindWindowExW(hwnd, None, "Button", None)
            while button_hwnd:
                # 获取按钮文本
                button_text = ctypes.create_unicode_buffer(256)
                self.user32.GetWindowTextW(button_hwnd, button_text, 256)
                button_text_str = button_text.value
                
                # 检查是否匹配目标按钮
                for target_text in target_texts:
                    if target_text.lower() in button_text_str.lower():
                        print(f"   🔍 找到匹配按钮: '{button_text_str}' (匹配: '{target_text}')")
                        return button_hwnd
                
                # 查找下一个按钮
                button_hwnd = self.user32.FindWindowExW(hwnd, button_hwnd, "Button", None)
            
            return None
            
        except Exception as e:
            print(f"查找对话框按钮异常: {e}")
            return None
            
    def _get_button_rect(self, button_hwnd: ctypes.wintypes.HWND) -> Optional[Tuple[int, int, int, int]]:
        """
        获取按钮的屏幕坐标矩形
        
        Args:
            button_hwnd: 按钮控件句柄
            
        Returns:
            按钮矩形 (left, top, right, bottom)
        """
        try:
            rect = ctypes.wintypes.RECT()
            self.user32.GetWindowRect(button_hwnd, ctypes.byref(rect))
            
            return (rect.left, rect.top, rect.right, rect.bottom)
            
        except Exception as e:
            print(f"获取按钮位置异常: {e}")
            return None
            
    def _smooth_move_mouse(self, x: int, y: int):
        """
        平滑移动鼠标到指定位置
        
        Args:
            x, y: 目标坐标
        """
        try:
            # 获取当前鼠标位置
            current_pos = ctypes.wintypes.POINT()
            self.user32.GetCursorPos(ctypes.byref(current_pos))
            
            current_x, current_y = current_pos.x, current_pos.y
            
            # 计算距离
            distance = ((x - current_x) ** 2 + (y - current_y) ** 2) ** 0.5
            
            # 计算移动步数（每步最多5像素）
            steps = max(1, int(distance / 5))
            
            print(f"   📏 移动距离: {distance:.1f} 像素")
            print(f"   🚶 移动步数: {steps} 步")
            print(f"   🎯 目标位置: ({x}, {y})")
            
            # 平滑移动
            for i in range(steps + 1):
                progress = i / steps
                
                # 使用缓动函数
                progress = self._ease_in_out_cubic(progress)
                
                new_x = int(current_x + (x - current_x) * progress)
                new_y = int(current_y + (y - current_y) * progress)
                
                self.user32.SetCursorPos(new_x, new_y)
                time.sleep(0.01)  # 10ms间隔
                
        except Exception as e:
            print(f"平滑移动鼠标异常: {e}")
            
    def _ease_in_out_cubic(self, t: float) -> float:
        """三次缓动函数"""
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 3) / 2
            
    def _click_mouse(self, x: int, y: int):
        """
        在指定位置点击鼠标
        
        Args:
            x, y: 点击坐标
        """
        try:
            # 鼠标按下
            print(f"   👇 鼠标按下: ({x}, {y})")
            self.user32.mouse_event(0x0002, x, y, 0, 0)  # MOUSEEVENTF_LEFTDOWN
            time.sleep(0.05)
            
            # 鼠标释放
            print(f"   👆 鼠标释放: ({x}, {y})")
            self.user32.mouse_event(0x0004, x, y, 0, 0)  # MOUSEEVENTF_LEFTUP
            time.sleep(0.05)
            
        except Exception as e:
            print(f"鼠标点击异常: {e}")
            
    def _click_dialog_button_api(self, hwnd: ctypes.wintypes.HWND, button_type: str):
        """
        使用API方式点击对话框按钮（备用方法）
        
        Args:
            hwnd: 对话框窗口句柄
            button_type: 按钮类型
        """
        try:
            # 按钮ID映射
            button_ids = {
                "ok": IDOK,
                "cancel": IDCANCEL,
                "yes": IDYES,
                "no": IDNO,
                "abort": IDABORT,
                "retry": IDRETRY,
                "ignore": IDIGNORE
            }
            
            button_id = button_ids.get(button_type.lower(), IDCANCEL)
            
            # 发送按钮点击消息
            self.user32.SendMessageW(hwnd, WM_COMMAND, button_id, 0)
            
            print(f"已通过API点击对话框按钮: {button_type}")
            
        except Exception as e:
            print(f"API点击对话框按钮异常: {e}")
            
    def add_expected_dialog(self, title: str = "", content: str = "", dialog_type: str = ""):
        """
        添加预期的对话框
        
        Args:
            title: 对话框标题关键词
            content: 对话框内容关键词
            dialog_type: 对话框类型
        """
        expected_dialog = {
            "title": title,
            "content": content,
            "type": dialog_type
        }
        
        self.expected_dialogs.append(expected_dialog)
        print(f"已添加预期对话框: {expected_dialog}")
        
    def remove_expected_dialog(self, title: str = "", content: str = ""):
        """
        移除预期的对话框
        
        Args:
            title: 对话框标题关键词
            content: 对话框内容关键词
        """
        self.expected_dialogs = [
            dialog for dialog in self.expected_dialogs
            if not (dialog.get("title", "") == title and dialog.get("content", "") == content)
        ]
        print(f"已移除预期对话框: title={title}, content={content}")


def test_dialog_handler():
    """测试对话框处理器"""
    print("测试对话框处理器...")
    
    # 创建对话框处理器
    config = {
        "enabled": True,
        "detection_interval": 0.5,
        "dialog_timeout": 10.0,
        "expected_dialogs": [
            {"title": "保存", "content": "是否保存", "type": "save_confirm"}
        ]
    }
    
    handler = DialogHandler(config)
    
    # 设置回调函数
    def dialog_callback(dialog_info):
        print(f"对话框回调: {dialog_info}")
        
    handler.set_dialog_callback(dialog_callback)
    
    # 开始检测
    handler.start_dialog_detection()
    
    print("对话框检测已启动，等待10秒...")
    time.sleep(10)
    
    # 停止检测
    handler.stop_dialog_detection()
    
    print("对话框处理器测试完成!")


if __name__ == "__main__":
    test_dialog_handler()
