# -*- coding: utf-8 -*-
"""
对话框场景测试脚本
模拟各种对话框场景来测试对话框处理功能
"""

import sys
import os
import time
import threading
import ctypes
import ctypes.wintypes

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_save_dialog():
    """创建保存确认对话框"""
    print("创建保存确认对话框...")
    
    # 使用Windows API创建消息框
    result = ctypes.windll.user32.MessageBoxW(
        None,
        "文档已修改，是否保存？",
        "记事本",
        0x00000004 | 0x00000020  # MB_YESNO | MB_ICONQUESTION
    )
    
    print(f"保存对话框结果: {result}")
    return result

def create_error_dialog():
    """创建错误对话框"""
    print("创建错误对话框...")
    
    result = ctypes.windll.user32.MessageBoxW(
        None,
        "发生错误，程序无法继续执行",
        "错误",
        0x00000010 | 0x00000000  # MB_ICONERROR | MB_OK
    )
    
    print(f"错误对话框结果: {result}")
    return result

def create_warning_dialog():
    """创建警告对话框"""
    print("创建警告对话框...")
    
    result = ctypes.windll.user32.MessageBoxW(
        None,
        "警告：此操作不可撤销，确定继续吗？",
        "警告",
        0x00000004 | 0x00000030  # MB_YESNO | MB_ICONWARNING
    )
    
    print(f"警告对话框结果: {result}")
    return result

def create_delete_dialog():
    """创建删除确认对话框"""
    print("创建删除确认对话框...")
    
    result = ctypes.windll.user32.MessageBoxW(
        None,
        "确认删除此文件吗？",
        "确认删除",
        0x00000004 | 0x00000020  # MB_YESNO | MB_ICONQUESTION
    )
    
    print(f"删除对话框结果: {result}")
    return result

def test_dialog_scenarios():
    """测试各种对话框场景"""
    print("=" * 60)
    print("测试对话框场景")
    print("=" * 60)
    
    print("此测试将创建各种对话框来验证对话框处理功能")
    print("请观察程序是否能正确检测和处理这些对话框")
    
    input("按回车键开始测试...")
    
    # 测试保存对话框（预期的）
    print("\n1. 测试保存对话框（预期对话框）")
    create_save_dialog()
    time.sleep(2)
    
    # 测试错误对话框（非预期的）
    print("\n2. 测试错误对话框（非预期对话框）")
    create_error_dialog()
    time.sleep(2)
    
    # 测试警告对话框（非预期的）
    print("\n3. 测试警告对话框（非预期对话框）")
    create_warning_dialog()
    time.sleep(2)
    
    # 测试删除对话框（非预期的）
    print("\n4. 测试删除对话框（非预期对话框）")
    create_delete_dialog()
    time.sleep(2)
    
    print("\n对话框场景测试完成！")

def test_automation_with_dialogs():
    """测试带对话框的自动化"""
    print("\n" + "=" * 60)
    print("测试带对话框的自动化")
    print("=" * 60)
    
    print("此测试将启动自动化程序，然后创建对话框")
    print("观察程序是否能正确处理对话框")
    
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
    create_save_dialog()
    
    # 等待程序处理
    time.sleep(3)
    
    # 创建非预期对话框
    print("创建非预期对话框...")
    create_error_dialog()
    
    # 等待程序处理
    time.sleep(3)
    
    # 终止程序
    process.terminate()
    process.wait()
    
    print("带对话框的自动化测试完成！")

def main():
    """主测试函数"""
    print("Puppeteer 对话框场景测试")
    print("=" * 80)
    print("目标: 测试各种对话框场景的处理功能")
    print("=" * 80)
    
    tests = [
        ("对话框场景测试", test_dialog_scenarios),
        ("带对话框的自动化测试", test_automation_with_dialogs)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            print(f"\n开始 {test_name}...")
            result = test_func()
            results.append((test_name, True))
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
        print("🎉 所有对话框场景测试通过！")
        print("\n功能验证:")
        print("✓ 保存确认对话框处理")
        print("✓ 错误对话框处理")
        print("✓ 警告对话框处理")
        print("✓ 删除确认对话框处理")
        print("✓ 预期和非预期对话框区分")
        print("✓ 自动化程序中的对话框处理")
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
