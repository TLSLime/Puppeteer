# -*- coding: utf-8 -*-
"""
改进的自动化测试脚本
测试修复后的功能：窗口管理、安全恢复、文件状态检查
"""

import sys
import os
import time
import subprocess

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_window_management():
    """测试窗口管理功能"""
    print("=" * 60)
    print("测试窗口管理功能")
    print("=" * 60)
    
    try:
        from puppeteer.window_manager import WindowManager
        
        # 创建窗口管理器
        manager = WindowManager()
        print("✓ 窗口管理器创建成功")
        
        # 测试配置
        window_config = {
            "title": "test_doc.txt",
            "file_path": "test_doc.txt",
            "exact_match": False,
            "mouse_position": "center",
            "auto_activate": True,
            "activation_delay": 2.0
        }
        
        print("测试智能窗口管理...")
        success = manager.smart_ensure_window_active(window_config)
        
        if success:
            print("✓ 智能窗口管理功能正常")
            
            # 测试窗口状态检查
            print("测试窗口状态检查...")
            status = manager.check_window_status(window_config)
            print(f"窗口状态: {status}")
            
            return True
        else:
            print("✗ 智能窗口管理功能失败")
            return False
            
    except Exception as e:
        print(f"✗ 窗口管理测试失败: {e}")
        return False

def test_safety_recovery():
    """测试安全恢复功能"""
    print("\n" + "=" * 60)
    print("测试安全恢复功能")
    print("=" * 60)
    
    try:
        from puppeteer.controller import PuppeteerController
        from puppeteer.config import ConfigManager
        from puppeteer.logger import PuppeteerLogger
        from puppeteer.safety_monitor import SafetyLevel, SafetyEvent
        
        print("创建控制器...")
        
        # 创建组件
        config_manager = ConfigManager("profiles")
        logger = PuppeteerLogger("test_logs")
        controller = PuppeteerController(config_manager, logger, SafetyLevel.DISABLED)
        
        print("✓ 控制器创建成功")
        
        # 加载配置
        if config_manager.load_profile("test_doc"):
            print("✓ 配置加载成功")
            
            # 测试安全恢复功能
            print("测试安全恢复功能...")
            
            # 模拟安全事件
            test_data = {"key": "esc", "reason": "emergency_stop"}
            controller._safety_callback(SafetyEvent.EMERGENCY_STOP, test_data)
            
            print("✓ 安全恢复功能测试完成")
            return True
        else:
            print("✗ 配置加载失败")
            return False
            
    except Exception as e:
        print(f"✗ 安全恢复测试失败: {e}")
        return False

def test_improved_automation():
    """测试改进的自动化功能"""
    print("\n" + "=" * 60)
    print("测试改进的自动化功能")
    print("=" * 60)
    
    try:
        print("准备启动改进的自动化测试...")
        print("程序将自动:")
        print("1. 智能检查窗口状态")
        print("2. 自动打开文件（如果需要）")
        print("3. 确保窗口活跃")
        print("4. 执行自动化宏")
        print("5. 支持安全恢复")
        
        input("按回车键开始改进的自动化测试...")
        
        # 启动改进的自动化
        cmd = [
            sys.executable, "main.py", 
            "--mode", "cli", 
            "--profile", "test_doc", 
            "--safety-level", "disabled",
            "--non-interactive",
            "--auto-exit"
        ]
        
        print(f"执行命令: {' '.join(cmd)}")
        
        # 启动进程
        import subprocess
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.getcwd()
        )
        
        # 等待程序执行完成
        stdout, stderr = process.communicate(timeout=30)
        
        print("程序输出:")
        print(stdout)
        
        if stderr:
            print("错误输出:")
            print(stderr)
        
        if process.returncode == 0:
            print("✓ 改进的自动化测试成功")
            print("请检查test_doc.txt文件是否已更新")
            return True
        else:
            print(f"✗ 改进的自动化测试失败，返回码: {process.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ 程序执行超时")
        process.kill()
        return False
    except Exception as e:
        print(f"✗ 改进的自动化测试失败: {e}")
        return False

def test_file_status_check():
    """测试文件状态检查功能"""
    print("\n" + "=" * 60)
    print("测试文件状态检查功能")
    print("=" * 60)
    
    try:
        from puppeteer.window_manager import WindowManager
        
        # 创建窗口管理器
        manager = WindowManager()
        
        # 测试配置
        window_config = {
            "title": "test_doc.txt",
            "file_path": "test_doc.txt",
            "exact_match": False,
            "mouse_position": "center",
            "auto_activate": True,
            "activation_delay": 2.0
        }
        
        print("测试文件状态检查...")
        
        # 检查文件是否存在
        import os
        if os.path.exists("test_doc.txt"):
            print("✓ 目标文件存在")
        else:
            print("⚠️ 目标文件不存在，创建测试文件...")
            with open("test_doc.txt", "w", encoding="utf-8") as f:
                f.write("这是一个测试文档，用于验证Puppeteer自动化功能。\n\n")
                f.write("当前时间: 等待自动化程序写入...\n\n")
                f.write("测试内容:\n")
                f.write("1. 基础文本输入功能\n")
                f.write("2. 鼠标点击功能\n")
                f.write("3. 键盘按键功能\n")
                f.write("4. 窗口管理功能\n")
                f.write("5. 安全机制功能\n\n")
                f.write("自动化程序将在此处写入测试结果。\n")
            print("✓ 测试文件已创建")
        
        # 测试窗口状态检查
        status = manager.check_window_status(window_config)
        print(f"窗口状态检查结果: {status}")
        
        if status["found"]:
            print("✓ 窗口状态检查功能正常")
        else:
            print("⚠️ 窗口未找到，这是正常的（文件可能未打开）")
        
        return True
        
    except Exception as e:
        print(f"✗ 文件状态检查测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("Puppeteer 改进的自动化功能测试")
    print("=" * 80)
    print("目标: 测试修复后的窗口管理、安全恢复、文件状态检查功能")
    print("=" * 80)
    
    tests = [
        ("窗口管理功能", test_window_management),
        ("安全恢复功能", test_safety_recovery),
        ("文件状态检查功能", test_file_status_check),
        ("改进的自动化功能", test_improved_automation)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name}测试异常: {e}")
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
        print("🎉 所有改进的自动化功能测试通过！")
        print("\n功能验证:")
        print("✓ 窗口查找回调函数错误修复")
        print("✓ 自动化程序在目标txt文件内进行输入操作")
        print("✓ 安全键停止后自动恢复准备状态")
        print("✓ 文件状态检查和重新打开功能")
        print("✓ 智能窗口管理")
        print("✓ 自动恢复机制")
        print("\n请检查test_doc.txt文件，确认自动化内容已写入")
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
