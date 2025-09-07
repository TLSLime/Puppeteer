# -*- coding: utf-8 -*-
"""
窗口管理模块 - 处理目标窗口的激活、定位和状态管理
确保自动化程序执行时目标窗口处于活跃状态
"""

import time
import ctypes
import ctypes.wintypes
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import psutil


class WindowState(Enum):
    """窗口状态"""
    ACTIVE = "active"
    MINIMIZED = "minimized"
    MAXIMIZED = "maximized"
    NORMAL = "normal"
    HIDDEN = "hidden"


class WindowManager:
    """窗口管理器"""
    
    def __init__(self):
        """初始化窗口管理器"""
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32
        
        # 设置函数原型
        self.user32.FindWindowW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p]
        self.user32.FindWindowW.restype = ctypes.wintypes.HWND
        
        self.user32.FindWindowExW.argtypes = [
            ctypes.wintypes.HWND, ctypes.wintypes.HWND, 
            ctypes.c_wchar_p, ctypes.c_wchar_p
        ]
        self.user32.FindWindowExW.restype = ctypes.wintypes.HWND
        
        self.user32.GetWindowTextW.argtypes = [ctypes.wintypes.HWND, ctypes.c_wchar_p, ctypes.c_int]
        self.user32.GetWindowTextW.restype = ctypes.c_int
        
        self.user32.GetClassNameW.argtypes = [ctypes.wintypes.HWND, ctypes.c_wchar_p, ctypes.c_int]
        self.user32.GetClassNameW.restype = ctypes.c_int
        
        self.user32.SetForegroundWindow.argtypes = [ctypes.wintypes.HWND]
        self.user32.SetForegroundWindow.restype = ctypes.c_bool
        
        self.user32.ShowWindow.argtypes = [ctypes.wintypes.HWND, ctypes.c_int]
        self.user32.ShowWindow.restype = ctypes.c_bool
        
        self.user32.GetWindowRect.argtypes = [ctypes.wintypes.HWND, ctypes.POINTER(ctypes.wintypes.RECT)]
        self.user32.GetWindowRect.restype = ctypes.c_bool
        
        self.user32.IsWindowVisible.argtypes = [ctypes.wintypes.HWND]
        self.user32.IsWindowVisible.restype = ctypes.c_bool
        
        self.user32.IsIconic.argtypes = [ctypes.wintypes.HWND]
        self.user32.IsIconic.restype = ctypes.c_bool
        
        self.user32.IsZoomed.argtypes = [ctypes.wintypes.HWND]
        self.user32.IsZoomed.restype = ctypes.c_bool
        
        # 窗口状态常量
        self.SW_HIDE = 0
        self.SW_SHOWNORMAL = 1
        self.SW_SHOWMINIMIZED = 2
        self.SW_SHOWMAXIMIZED = 3
        self.SW_SHOWNOACTIVATE = 4
        self.SW_SHOW = 5
        self.SW_MINIMIZE = 6
        self.SW_SHOWMINNOACTIVE = 7
        self.SW_SHOWNA = 8
        self.SW_RESTORE = 9
        
        print("窗口管理器初始化完成")
        
    def find_window_by_title(self, title: str, exact_match: bool = False) -> Optional[ctypes.wintypes.HWND]:
        """
        根据窗口标题查找窗口
        
        Args:
            title: 窗口标题
            exact_match: 是否精确匹配
            
        Returns:
            窗口句柄，如果未找到返回None
        """
        try:
            if exact_match:
                # 精确匹配
                hwnd = self.user32.FindWindowW(None, title)
                if hwnd and self.user32.IsWindowVisible(hwnd):
                    return hwnd
            else:
                # 模糊匹配 - 优先匹配记事本窗口
                hwnd = self.user32.FindWindowW(None, None)
                notepad_windows = []
                other_windows = []
                
                while hwnd:
                    if self.user32.IsWindowVisible(hwnd):
                        window_title = ctypes.create_unicode_buffer(256)
                        self.user32.GetWindowTextW(hwnd, window_title, 256)
                        window_title_str = window_title.value
                        
                        if title.lower() in window_title_str.lower():
                            # 检查是否是记事本窗口
                            if "记事本" in window_title_str or "Notepad" in window_title_str:
                                notepad_windows.append(hwnd)
                            else:
                                other_windows.append(hwnd)
                    hwnd = self.user32.FindWindowExW(None, hwnd, None, None)
                
                # 优先返回记事本窗口
                if notepad_windows:
                    return notepad_windows[0]
                elif other_windows:
                    return other_windows[0]
                
            return None
            
        except Exception as e:
            print(f"查找窗口失败: {e}")
            return None
            
    def find_window_by_class(self, class_name: str) -> Optional[ctypes.wintypes.HWND]:
        """
        根据窗口类名查找窗口
        
        Args:
            class_name: 窗口类名
            
        Returns:
            窗口句柄，如果未找到返回None
        """
        try:
            hwnd = self.user32.FindWindowW(class_name, None)
            if hwnd and self.user32.IsWindowVisible(hwnd):
                return hwnd
            return None
            
        except Exception as e:
            print(f"根据类名查找窗口失败: {e}")
            return None
            
    def find_window_by_process(self, process_name: str) -> Optional[ctypes.wintypes.HWND]:
        """
        根据进程名查找窗口
        
        Args:
            process_name: 进程名
            
        Returns:
            窗口句柄，如果未找到返回None
        """
        try:
            # 查找进程
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'].lower() == process_name.lower():
                    pid = proc.info['pid']
                    
                    # 根据PID查找窗口
                    def enum_windows_proc(hwnd, lparam):
                        if self.user32.IsWindowVisible(hwnd):
                            _, window_pid = ctypes.c_ulong(), ctypes.c_ulong()
                            self.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(window_pid))
                            if window_pid.value == pid:
                                lparam.append(hwnd)
                        return True
                    
                    # 手动查找窗口
                    hwnd = self.user32.FindWindowW(None, None)
                    while hwnd:
                        if self.user32.IsWindowVisible(hwnd):
                            _, window_pid = ctypes.c_ulong(), ctypes.c_ulong()
                            self.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(window_pid))
                            if window_pid.value == pid:
                                return hwnd
                        hwnd = self.user32.FindWindowExW(None, hwnd, None, None)
                        
            return None
            
        except Exception as e:
            print(f"根据进程名查找窗口失败: {e}")
            return None
            
    def get_window_info(self, hwnd: ctypes.wintypes.HWND) -> Dict[str, Any]:
        """
        获取窗口信息
        
        Args:
            hwnd: 窗口句柄
            
        Returns:
            窗口信息字典
        """
        try:
            # 获取窗口标题
            title = ctypes.create_unicode_buffer(256)
            self.user32.GetWindowTextW(hwnd, title, 256)
            
            # 获取窗口类名
            class_name = ctypes.create_unicode_buffer(256)
            self.user32.GetClassNameW(hwnd, class_name, 256)
            
            # 获取窗口位置和大小
            rect = ctypes.wintypes.RECT()
            self.user32.GetWindowRect(hwnd, ctypes.byref(rect))
            
            # 获取窗口状态
            is_visible = self.user32.IsWindowVisible(hwnd)
            is_minimized = self.user32.IsIconic(hwnd)
            is_maximized = self.user32.IsZoomed(hwnd)
            
            # 获取进程信息
            _, pid = ctypes.c_ulong(), ctypes.c_ulong()
            self.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            
            return {
                "hwnd": hwnd,
                "title": title.value,
                "class_name": class_name.value,
                "pid": pid.value,
                "position": {
                    "left": rect.left,
                    "top": rect.top,
                    "right": rect.right,
                    "bottom": rect.bottom,
                    "width": rect.right - rect.left,
                    "height": rect.bottom - rect.top
                },
                "state": {
                    "visible": bool(is_visible),
                    "minimized": bool(is_minimized),
                    "maximized": bool(is_maximized)
                }
            }
            
        except Exception as e:
            print(f"获取窗口信息失败: {e}")
            return {}
            
    def activate_window(self, hwnd: ctypes.wintypes.HWND) -> bool:
        """
        激活窗口
        
        Args:
            hwnd: 窗口句柄
            
        Returns:
            是否成功激活
        """
        try:
            if not hwnd:
                return False
                
            # 检查窗口是否最小化
            if self.user32.IsIconic(hwnd):
                self.user32.ShowWindow(hwnd, self.SW_RESTORE)
                time.sleep(0.1)
                
            # 激活窗口
            result = self.user32.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            
            return bool(result)
            
        except Exception as e:
            print(f"激活窗口失败: {e}")
            return False
            
    def move_mouse_to_window(self, hwnd: ctypes.wintypes.HWND, 
                           position: str = "center") -> bool:
        """
        将鼠标移动到窗口内指定位置
        
        Args:
            hwnd: 窗口句柄
            position: 位置 ("center", "top_left", "top_right", "bottom_left", "bottom_right")
            
        Returns:
            是否成功移动
        """
        try:
            if not hwnd:
                return False
                
            # 获取窗口位置
            rect = ctypes.wintypes.RECT()
            if not self.user32.GetWindowRect(hwnd, ctypes.byref(rect)):
                return False
                
            # 计算目标位置
            width = rect.right - rect.left
            height = rect.bottom - rect.top
            
            if position == "center":
                x = rect.left + width // 2
                y = rect.top + height // 2
            elif position == "top_left":
                x = rect.left + width // 4
                y = rect.top + height // 4
            elif position == "top_right":
                x = rect.left + width * 3 // 4
                y = rect.top + height // 4
            elif position == "bottom_left":
                x = rect.left + width // 4
                y = rect.top + height * 3 // 4
            elif position == "bottom_right":
                x = rect.left + width * 3 // 4
                y = rect.top + height * 3 // 4
            else:
                x = rect.left + width // 2
                y = rect.top + height // 2
                
            # 移动鼠标
            self.user32.SetCursorPos(x, y)
            time.sleep(0.1)
            
            return True
            
        except Exception as e:
            print(f"移动鼠标到窗口失败: {e}")
            return False
            
    def ensure_window_active(self, window_config: Dict[str, Any]) -> bool:
        """
        确保目标窗口处于活跃状态
        
        Args:
            window_config: 窗口配置
            
        Returns:
            是否成功激活窗口
        """
        try:
            hwnd = None
            
            # 根据配置查找窗口
            if "title" in window_config:
                hwnd = self.find_window_by_title(
                    window_config["title"], 
                    window_config.get("exact_match", False)
                )
            elif "class_name" in window_config:
                hwnd = self.find_window_by_class(window_config["class_name"])
            elif "process_name" in window_config:
                hwnd = self.find_window_by_process(window_config["process_name"])
                
            if not hwnd:
                print(f"未找到目标窗口: {window_config}")
                # 尝试自动打开文件
                if self._auto_open_file(window_config):
                    # 重新查找窗口
                    if "title" in window_config:
                        hwnd = self.find_window_by_title(
                            window_config["title"], 
                            window_config.get("exact_match", False)
                        )
                    if not hwnd:
                        print("自动打开文件后仍未找到窗口")
                        return False
                else:
                    return False
                
            # 获取窗口信息
            window_info = self.get_window_info(hwnd)
            print(f"找到目标窗口: {window_info['title']}")
            
            # 激活窗口
            if not self.activate_window(hwnd):
                print("激活窗口失败")
                return False
                
            # 移动鼠标到窗口内
            mouse_position = window_config.get("mouse_position", "center")
            if not self.move_mouse_to_window(hwnd, mouse_position):
                print("移动鼠标到窗口失败")
                return False
                
            print(f"窗口已激活，鼠标已移动到 {mouse_position}")
            return True
            
        except Exception as e:
            print(f"确保窗口活跃失败: {e}")
            return False
            
    def _auto_open_file(self, window_config: Dict[str, Any]) -> bool:
        """
        自动打开文件
        
        Args:
            window_config: 窗口配置
            
        Returns:
            是否成功打开文件
        """
        try:
            import subprocess
            import os
            
            # 获取文件路径和程序路径
            file_path = window_config.get("file_path")
            program_path = window_config.get("program_path")
            file_type = window_config.get("file_type", "auto")
            
            if not file_path:
                # 从标题中提取文件名
                title = window_config.get("title", "")
                if "." in title:
                    file_path = title
                else:
                    print("无法确定文件路径")
                    return False
                    
            # 检查文件是否存在
            if not os.path.exists(file_path):
                print(f"文件不存在: {file_path}")
                return False
                
            print(f"自动打开文件: {file_path}")
            
            # 根据文件类型选择打开方式
            success = self._open_file_by_type(file_path, program_path, file_type)
            
            if success:
                time.sleep(3)  # 等待文件打开
                print("文件已成功打开")
                return True
            else:
                print("文件打开失败")
                return False
                
        except Exception as e:
            print(f"自动打开文件异常: {e}")
            return False
            
    def _open_file_by_type(self, file_path: str, program_path: str = None, file_type: str = "auto") -> bool:
        """根据文件类型打开文件"""
        try:
            import subprocess
            import os
            
            # 获取文件扩展名
            _, ext = os.path.splitext(file_path.lower())
            
            # 如果指定了程序路径，优先使用
            if program_path and os.path.exists(program_path):
                print(f"使用指定程序打开: {program_path}")
                subprocess.Popen([program_path, file_path], shell=True)
                return True
            
            # 根据文件类型选择默认程序
            if file_type == "auto":
                file_type = ext[1:] if ext else "txt"
            
            # 文件类型映射
            type_mapping = {
                "txt": "notepad.exe",
                "doc": "winword.exe",
                "docx": "winword.exe", 
                "xls": "excel.exe",
                "xlsx": "excel.exe",
                "ppt": "powerpnt.exe",
                "pptx": "powerpnt.exe",
                "pdf": "AcroRd32.exe",
                "html": "chrome.exe",
                "htm": "chrome.exe",
                "jpg": "mspaint.exe",
                "jpeg": "mspaint.exe",
                "png": "mspaint.exe",
                "bmp": "mspaint.exe",
                "gif": "mspaint.exe",
                "mp3": "wmplayer.exe",
                "mp4": "wmplayer.exe",
                "avi": "wmplayer.exe",
                "zip": "explorer.exe",
                "rar": "explorer.exe"
            }
            
            # 获取对应的程序
            program = type_mapping.get(file_type.lower())
            
            if program:
                print(f"使用 {program} 打开 {file_type} 文件")
                subprocess.Popen([program, file_path], shell=True)
                return True
            else:
                # 使用系统默认程序打开
                print(f"使用系统默认程序打开文件")
                os.startfile(file_path)
                return True
                
        except Exception as e:
            print(f"按类型打开文件失败: {e}")
            return False
            
    def _close_existing_notepad_windows(self):
        """关闭现有的记事本窗口"""
        try:
            hwnd = self.user32.FindWindowW(None, None)
            while hwnd:
                if self.user32.IsWindowVisible(hwnd):
                    window_title = ctypes.create_unicode_buffer(256)
                    self.user32.GetWindowTextW(hwnd, window_title, 256)
                    window_title_str = window_title.value
                    
                    # 检查是否是记事本窗口
                    if "记事本" in window_title_str or "Notepad" in window_title_str:
                        print(f"关闭现有记事本窗口: {window_title_str}")
                        self.user32.PostMessageW(hwnd, 0x0010, 0, 0)  # WM_CLOSE
                        time.sleep(0.5)
                        
                hwnd = self.user32.FindWindowExW(None, hwnd, None, None)
                
        except Exception as e:
            print(f"关闭记事本窗口异常: {e}")
            
    def check_running_processes(self, process_names: List[str]) -> Dict[str, bool]:
        """
        检查指定进程是否正在运行
        
        Args:
            process_names: 进程名称列表
            
        Returns:
            进程运行状态字典
        """
        try:
            import psutil
            
            running_processes = {}
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name'].lower()
                    for target_name in process_names:
                        target_name_lower = target_name.lower()
                        if target_name_lower in proc_name or proc_name in target_name_lower:
                            running_processes[target_name] = True
                            break
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            
            # 标记未找到的进程
            for process_name in process_names:
                if process_name not in running_processes:
                    running_processes[process_name] = False
                    
            return running_processes
            
        except ImportError:
            print("警告: psutil 未安装，无法检测进程状态")
            return {name: False for name in process_names}
        except Exception as e:
            print(f"检查进程状态失败: {e}")
            return {name: False for name in process_names}
            
    def find_process_by_name(self, process_name: str) -> Optional[ctypes.wintypes.HWND]:
        """
        根据进程名查找窗口
        
        Args:
            process_name: 进程名称
            
        Returns:
            窗口句柄
        """
        try:
            hwnd = self.user32.FindWindowW(None, None)
            while hwnd:
                if self.user32.IsWindowVisible(hwnd):
                    window_title = ctypes.create_unicode_buffer(256)
                    self.user32.GetWindowTextW(hwnd, window_title, 256)
                    window_title_str = window_title.value
                    
                    # 检查窗口标题是否包含进程名
                    if process_name.lower() in window_title_str.lower():
                        return hwnd
                        
                hwnd = self.user32.FindWindowExW(None, hwnd, None, None)
                
            return None
            
        except Exception as e:
            print(f"根据进程名查找窗口失败: {e}")
            return None
            
    def smart_ensure_target_active(self, window_config: Dict[str, Any]) -> bool:
        """
        智能确保目标程序活跃
        
        Args:
            window_config: 窗口配置
            
        Returns:
            是否成功确保目标活跃
        """
        try:
            print("智能检查目标程序状态...")
            
            # 检查进程状态
            process_names = window_config.get("process_names", [])
            if process_names:
                print(f"🔍 检查进程状态: {process_names}")
                process_status = self.check_running_processes(process_names)
                
                running_processes = [name for name, running in process_status.items() if running]
                if running_processes:
                    print(f"✅ 发现运行中的进程: {running_processes}")
                else:
                    print("⚠️ 未发现运行中的目标进程")
            
            # 检查窗口状态
            status = self.check_window_status(window_config)
            
            if status["found"] and status["hwnd"]:
                print("✅ 找到目标窗口")
                print(f"   📋 窗口标题: {status.get('title', 'Unknown')}")
                print(f"   🆔 窗口句柄: {status['hwnd']}")
                
                # 激活窗口
                if not status["active"]:
                    print("🔄 激活目标窗口...")
                    self.activate_window(status["hwnd"])
                    time.sleep(0.5)
                    print("✅ 窗口已激活")
                else:
                    print("✅ 窗口已处于活跃状态")
                
                # 移动鼠标到窗口内
                mouse_position = window_config.get("mouse_position", "center")
                print(f"🖱️ 移动鼠标到窗口位置: {mouse_position}")
                self.move_mouse_to_window(status["hwnd"], mouse_position)
                print("✅ 鼠标已移动到目标位置")
                
                print("✅ 目标程序已确保活跃")
                return True
            else:
                print("⚠️ 未找到目标窗口，尝试打开...")
                
                # 尝试打开文件或程序
                print("📂 尝试打开目标文件或程序...")
                if self._auto_open_file(window_config):
                    print("✅ 文件打开命令已执行")
                    time.sleep(2)
                    
                    # 重新检查窗口状态
                    print("🔍 重新检查窗口状态...")
                    status = self.check_window_status(window_config)
                    if status["found"] and status["hwnd"]:
                        print("✅ 成功打开并激活目标程序")
                        print(f"   📋 窗口标题: {status.get('title', 'Unknown')}")
                        return True
                    else:
                        print("❌ 打开程序后仍未找到窗口")
                        return False
                else:
                    print("❌ 无法打开目标程序")
                    return False
                    
        except Exception as e:
            print(f"智能确保目标活跃异常: {e}")
            return False
            
    def check_window_status(self, window_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        检查窗口状态
        
        Args:
            window_config: 窗口配置
            
        Returns:
            窗口状态信息
        """
        try:
            status = {
                "found": False,
                "active": False,
                "visible": False,
                "hwnd": None,
                "title": "",
                "needs_reopen": False
            }
            
            # 查找窗口
            hwnd = self.find_window_by_title(
                window_config["title"], 
                window_config.get("exact_match", False)
            )
            
            if hwnd:
                status["found"] = True
                status["hwnd"] = hwnd
                
                # 获取窗口信息
                window_info = self.get_window_info(hwnd)
                status["title"] = window_info.get("title", "")
                
                # 检查窗口是否可见
                status["visible"] = self.user32.IsWindowVisible(hwnd)
                
                # 检查窗口是否活跃
                foreground_hwnd = self.user32.GetForegroundWindow()
                status["active"] = (hwnd == foreground_hwnd)
                
                # 判断是否需要重新打开
                if not status["visible"] or not status["active"]:
                    status["needs_reopen"] = True
            else:
                status["needs_reopen"] = True
                
            return status
            
        except Exception as e:
            print(f"检查窗口状态异常: {e}")
            return {"found": False, "active": False, "visible": False, "hwnd": None, "title": "", "needs_reopen": True}
            
    def smart_ensure_window_active(self, window_config: Dict[str, Any]) -> bool:
        """
        智能确保窗口活跃
        
        Args:
            window_config: 窗口配置
            
        Returns:
            是否成功确保窗口活跃
        """
        try:
            print("智能检查窗口状态...")
            
            # 检查窗口状态
            status = self.check_window_status(window_config)
            
            if not status["found"]:
                print("窗口未找到，尝试打开文件...")
                if self._auto_open_file(window_config):
                    time.sleep(2)
                    status = self.check_window_status(window_config)
                else:
                    return False
            
            if status["found"] and status["hwnd"]:
                # 如果窗口不可见，尝试恢复
                if not status["visible"]:
                    print("窗口不可见，尝试恢复...")
                    self.user32.ShowWindow(status["hwnd"], 9)  # SW_RESTORE
                    time.sleep(1)
                
                # 激活窗口
                if not status["active"]:
                    print("激活窗口...")
                    self.activate_window(status["hwnd"])
                    time.sleep(0.5)
                
                # 移动鼠标到窗口内
                mouse_position = window_config.get("mouse_position", "center")
                self.move_mouse_to_window(status["hwnd"], mouse_position)
                
                print(f"✅ 窗口状态: 找到={status['found']}, 活跃={status['active']}, 可见={status['visible']}")
                return True
            else:
                print("❌ 无法确保窗口活跃")
                return False
                
        except Exception as e:
            print(f"智能确保窗口活跃异常: {e}")
            return False
            
    def list_windows(self, filter_title: str = "") -> List[Dict[str, Any]]:
        """
        列出所有可见窗口
        
        Args:
            filter_title: 标题过滤器
            
        Returns:
            窗口信息列表
        """
        try:
            windows = []
            
            def enum_windows_proc(hwnd, lparam):
                if self.user32.IsWindowVisible(hwnd):
                    window_info = self.get_window_info(hwnd)
                    if window_info and window_info.get("title"):
                        if not filter_title or filter_title.lower() in window_info["title"].lower():
                            windows.append(window_info)
                return True
                
            # 手动枚举窗口
            hwnd = self.user32.FindWindowW(None, None)
            while hwnd:
                if self.user32.IsWindowVisible(hwnd):
                    window_info = self.get_window_info(hwnd)
                    if window_info and window_info.get("title"):
                        if not filter_title or filter_title.lower() in window_info["title"].lower():
                            windows.append(window_info)
                hwnd = self.user32.FindWindowExW(None, hwnd, None, None)
                
            return windows
            
        except Exception as e:
            print(f"列出窗口失败: {e}")
            return []


def test_window_manager():
    """测试窗口管理器"""
    print("测试窗口管理器...")
    
    try:
        manager = WindowManager()
        
        # 列出所有窗口
        print("\n所有可见窗口:")
        windows = manager.list_windows()
        for i, window in enumerate(windows[:10]):  # 只显示前10个
            print(f"{i+1}. {window['title']} ({window['class_name']})")
            
        # 测试查找记事本窗口
        print("\n查找记事本窗口:")
        notepad_hwnd = manager.find_window_by_title("记事本")
        if notepad_hwnd:
            window_info = manager.get_window_info(notepad_hwnd)
            print(f"找到记事本: {window_info}")
            
            # 测试激活窗口
            if manager.activate_window(notepad_hwnd):
                print("记事本窗口已激活")
                
                # 测试移动鼠标
                if manager.move_mouse_to_window(notepad_hwnd, "center"):
                    print("鼠标已移动到记事本窗口中心")
        else:
            print("未找到记事本窗口")
            
        return True
        
    except Exception as e:
        print(f"窗口管理器测试失败: {e}")
        return False


if __name__ == "__main__":
    test_window_manager()
