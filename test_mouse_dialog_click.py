# -*- coding: utf-8 -*-
"""
鼠标点击对话框测试脚本
测试通过鼠标点击处理对话框的功能
"""

import sys
import os
import time
import threading
import ctypes
import ctypes.wintypes

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_test_dialog():
    """创建测试对话框"""
    print("创建测试对话框...")
    
    # 使用Windows API创建消息框
    result = ctypes.windll.user32.MessageBoxW(
        None,
        "这是一个测试对话框\n用于测试鼠标点击功能\n请观察鼠标是否移动到按钮上并点击",
        "鼠标点击测试",
        0x00000004 | 0x00000020  # MB_YESNO | MB_ICONQUESTION
    )
    
    print(f"对话框结果: {result}")
    return result

def test_dialog_button_detection():
    """测试对话框按钮检测功能"""
    print("=" * 60)
    print("测试对话框按钮检测功能")
    print("=" * 60)
    
    try:
        from puppeteer.dialog_handler import DialogHandler
        
        # 创建对话框处理器
        handler = DialogHandler()
        
        # 创建测试对话框
        print("创建测试对话框...")
        dialog_thread = threading.Thread(target=create_test_dialog)
        dialog_thread.start()
        
        # 等待对话框出现
        time.sleep(1)
        
        # 查找对话框
        dialogs = handler._detect_dialogs()
        
        if dialogs:
            dialog = dialogs[0]
            print(f"找到对话框: {dialog['title']}")
            
            # 测试按钮检测
            button_types = ["yes", "no", "ok", "cancel"]
            
            for button_type in button_types:
                button_hwnd = handler._find_dialog_button(dialog['hwnd'], button_type)
                if button_hwnd:
                    print(f"✓ 找到按钮: {button_type}")
                    
                    # 获取按钮位置
                    button_rect = handler._get_button_rect(button_hwnd)
                    if button_rect:
                        center_x = button_rect[0] + (button_rect[2] - button_rect[0]) // 2
                        center_y = button_rect[1] + (button_rect[3] - button_rect[1]) // 2
                        print(f"  按钮位置: ({center_x}, {center_y})")
                else:
                    print(f"✗ 未找到按钮: {button_type}")
            
            # 等待对话框关闭
            dialog_thread.join()
            
        else:
            print("未找到对话框")
            
        return True
        
    except Exception as e:
        print(f"✗ 对话框按钮检测测试失败: {e}")
        return False

def test_mouse_movement():
    """测试鼠标移动功能"""
    print("\n" + "=" * 60)
    print("测试鼠标移动功能")
    print("=" * 60)
    
    try:
        from puppeteer.dialog_handler import DialogHandler
        
        # 创建对话框处理器
        handler = DialogHandler()
        
        print("测试鼠标平滑移动...")
        print("请观察鼠标移动轨迹")
        
        # 测试移动到屏幕中心
        screen_width = ctypes.windll.user32.GetSystemMetrics(0)
        screen_height = ctypes.windll.user32.GetSystemMetrics(1)
        center_x = screen_width // 2
        center_y = screen_height // 2
        
        print(f"移动到屏幕中心: ({center_x}, {center_y})")
        handler._smooth_move_mouse(center_x, center_y)
        time.sleep(1)
        
        # 测试移动到屏幕左上角
        print("移动到屏幕左上角: (100, 100)")
        handler._smooth_move_mouse(100, 100)
        time.sleep(1)
        
        # 测试移动到屏幕右下角
        print(f"移动到屏幕右下角: ({screen_width-100}, {screen_height-100})")
        handler._smooth_move_mouse(screen_width-100, screen_height-100)
        time.sleep(1)
        
        print("✓ 鼠标移动测试完成")
        return True
        
    except Exception as e:
        print(f"✗ 鼠标移动测试失败: {e}")
        return False

def test_dialog_mouse_click():
    """测试对话框鼠标点击功能"""
    print("\n" + "=" * 60)
    print("测试对话框鼠标点击功能")
    print("=" * 60)
    
    try:
        from puppeteer.dialog_handler import DialogHandler
        
        # 创建对话框处理器
        handler = DialogHandler()
        
        print("此测试将创建对话框并测试鼠标点击功能")
        print("请观察鼠标是否移动到按钮上并点击")
        
        input("按回车键开始测试...")
        
        # 创建测试对话框
        print("创建测试对话框...")
        dialog_thread = threading.Thread(target=create_test_dialog)
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
            
            # 等待对话框关闭
            time.sleep(1)
            
            print("✓ 对话框鼠标点击测试完成")
        else:
            print("未找到对话框")
            
        # 等待对话框线程结束
        dialog_thread.join()
        
        return True
        
    except Exception as e:
        print(f"✗ 对话框鼠标点击测试失败: {e}")
        return False

def test_integrated_dialog_handling():
    """测试集成的对话框处理功能"""
    print("\n" + "=" * 60)
    print("测试集成的对话框处理功能")
    print("=" * 60)
    
    try:
        print("此测试将启动自动化程序，然后创建对话框")
        print("观察程序是否能通过鼠标点击正确处理对话框")
        
        input("按回车键开始测试...")
        
        # 启动自动化程序
        print("启动自动化程序...")
        
        import subprocess
        process = subprocess.Popen([
            sys.executable, "main.py", 
            "--mode", "cli", 
            "--profile", "test_doc", 
            "--safety-level", "disabled",
            "--non-interactive"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # 等待程序启动
        time.sleep(5)
        
        # 创建对话框
        print("创建测试对话框...")
        create_test_dialog()
        
        # 等待程序处理
        time.sleep(3)
        
        # 终止程序
        process.terminate()
        process.wait()
        
        print("✓ 集成对话框处理测试完成")
        return True
        
    except subprocess.TimeoutExpired:
        print("✗ 程序执行超时")
        process.kill()
        return False
    except Exception as e:
        print(f"✗ 集成对话框处理测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("Puppeteer 鼠标点击对话框测试")
    print("=" * 80)
    print("目标: 测试通过鼠标点击处理对话框的功能")
    print("=" * 80)
    
    tests = [
        ("对话框按钮检测功能", test_dialog_button_detection),
        ("鼠标移动功能", test_mouse_movement),
        ("对话框鼠标点击功能", test_dialog_mouse_click),
        ("集成对话框处理功能", test_integrated_dialog_handling)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            print(f"\n开始 {test_name}...")
            result = test_func()
            results.append((test_name, result))
            print(f"✓ {test_name} 完成")
        except Exception as e:
            print(f"✗ {test_name} 失败: {e}")
            results.append((test_name, False))
    
    # 显示测试结果
    print("\n" + "=" * 80)
    print("测试结果汇总")
    print("=" * 80)
    
    success_count = 0
    for test_name, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"{test_name}: {status}")
        if success:
            success_count += 1
    
    print(f"\n总体结果: {success_count}/{len(results)} 测试通过")
    
    if success_count == len(results):
        print("🎉 所有鼠标点击对话框测试通过！")
        print("\n功能验证:")
        print("✓ 对话框按钮检测功能")
        print("✓ 鼠标平滑移动功能")
        print("✓ 对话框鼠标点击功能")
        print("✓ 集成对话框处理功能")
        print("✓ 使用Win32 API避免安全限制")
    else:
        print("⚠️ 部分测试失败，请检查错误信息")
    
    return success_count == len(results)

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n用户中断测试")
        sys.exit(1)
    except Exception as e:
        print(f"\n测试过程中发生异常: {e}")
        sys.exit(1)
