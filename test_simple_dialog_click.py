# -*- coding: utf-8 -*-
"""
简单对话框点击测试
"""

import sys
import os
import time
import threading
import ctypes

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_dialog():
    """创建对话框"""
    print("创建对话框...")
    result = ctypes.windll.user32.MessageBoxW(
        None,
        "这是一个测试对话框\n请观察鼠标是否移动到按钮上并点击",
        "鼠标点击测试",
        0x00000004 | 0x00000020  # MB_YESNO | MB_ICONQUESTION
    )
    print(f"对话框结果: {result}")

def test_dialog_click():
    """测试对话框点击"""
    try:
        from puppeteer.dialog_handler import DialogHandler
        
        # 创建对话框处理器
        handler = DialogHandler()
        
        print("开始测试对话框鼠标点击功能...")
        print("请观察鼠标移动和点击过程")
        
        # 创建对话框
        dialog_thread = threading.Thread(target=create_dialog)
        dialog_thread.start()
        
        # 等待对话框出现
        time.sleep(1)
        
        # 查找对话框
        dialogs = handler._detect_dialogs()
        
        if dialogs:
            dialog = dialogs[0]
            print(f"找到对话框: {dialog['title']}")
            
            # 测试点击"是"按钮
            print("测试点击'是'按钮...")
            handler._click_dialog_button(dialog['hwnd'], "yes")
            
            print("✓ 对话框点击测试完成")
        else:
            print("未找到对话框")
            
        # 等待对话框线程结束
        dialog_thread.join()
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

if __name__ == "__main__":
    test_dialog_click()
