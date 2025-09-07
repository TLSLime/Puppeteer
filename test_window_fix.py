# -*- coding: utf-8 -*-
"""
窗口管理修复测试脚本
测试修复后的窗口查找和自动打开功能
"""

import sys
import os
import time

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_window_detection():
    """测试窗口检测功能"""
    print("=" * 60)
    print("测试窗口检测功能")
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
        
        print("测试窗口查找...")
        
        # 查找窗口
        hwnd = manager.find_window_by_title(window_config["title"], window_config.get("exact_match", False))
        
        if hwnd:
            # 获取窗口信息
            window_info = manager.get_window_info(hwnd)
            print(f"找到窗口: {window_info['title']}")
            
            # 检查是否是记事本窗口
            if "记事本" in window_info['title'] or "Notepad" in window_info['title']:
                print("✓ 找到正确的记事本窗口")
                return True
            else:
                print(f"⚠️ 找到的窗口不是记事本: {window_info['title']}")
                return False
        else:
            print("⚠️ 未找到窗口")
            return False
            
    except Exception as e:
        print(f"✗ 窗口检测测试失败: {e}")
        return False

def test_auto_file_opening():
    """测试自动打开文件功能"""
    print("\n" + "=" * 60)
    print("测试自动打开文件功能")
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
        
        print("测试自动打开文件...")
        
        # 自动打开文件
        success = manager._auto_open_file(window_config)
        
        if success:
            print("✓ 文件打开成功")
            
            # 等待文件打开
            time.sleep(2)
            
            # 检查窗口
            hwnd = manager.find_window_by_title(window_config["title"], window_config.get("exact_match", False))
            if hwnd:
                window_info = manager.get_window_info(hwnd)
                print(f"打开的窗口: {window_info['title']}")
                
                if "记事本" in window_info['title'] or "Notepad" in window_info['title']:
                    print("✓ 成功打开记事本窗口")
                    return True
                else:
                    print(f"✗ 打开的窗口不是记事本: {window_info['title']}")
                    return False
            else:
                print("✗ 未找到打开的窗口")
                return False
        else:
            print("✗ 文件打开失败")
            return False
            
    except Exception as e:
        print(f"✗ 自动打开文件测试失败: {e}")
        return False

def test_smart_window_management():
    """测试智能窗口管理功能"""
    print("\n" + "=" * 60)
    print("测试智能窗口管理功能")
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
        
        print("测试智能窗口管理...")
        
        # 使用智能窗口管理
        success = manager.smart_ensure_window_active(window_config)
        
        if success:
            print("✓ 智能窗口管理成功")
            
            # 检查窗口状态
            status = manager.check_window_status(window_config)
            print(f"窗口状态: {status}")
            
            if status["found"] and status["hwnd"]:
                window_info = manager.get_window_info(status["hwnd"])
                print(f"管理的窗口: {window_info['title']}")
                
                if "记事本" in window_info['title'] or "Notepad" in window_info['title']:
                    print("✓ 成功管理记事本窗口")
                    return True
                else:
                    print(f"✗ 管理的窗口不是记事本: {window_info['title']}")
                    return False
            else:
                print("✗ 窗口状态检查失败")
                return False
        else:
            print("✗ 智能窗口管理失败")
            return False
            
    except Exception as e:
        print(f"✗ 智能窗口管理测试失败: {e}")
        return False

def test_complete_automation():
    """测试完整自动化流程"""
    print("\n" + "=" * 60)
    print("测试完整自动化流程")
    print("=" * 60)
    
    try:
        print("准备启动完整自动化测试...")
        print("程序将自动:")
        print("1. 智能检测窗口")
        print("2. 自动打开记事本文件")
        print("3. 确保窗口活跃")
        print("4. 执行自动化宏")
        
        input("按回车键开始完整自动化测试...")
        
        # 启动完整自动化
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
            print("✓ 完整自动化测试成功")
            
            # 检查文件内容
            if os.path.exists("test_doc.txt"):
                with open("test_doc.txt", "r", encoding="utf-8") as f:
                    content = f.read()
                print("文件内容:")
                print(content)
                
                if "这是一段自动程序生成的内容" in content:
                    print("✓ 文件内容正确更新")
                    return True
                else:
                    print("✗ 文件内容未正确更新")
                    return False
            else:
                print("✗ 文件不存在")
                return False
        else:
            print(f"✗ 完整自动化测试失败，返回码: {process.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ 程序执行超时")
        process.kill()
        return False
    except Exception as e:
        print(f"✗ 完整自动化测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("Puppeteer 窗口管理修复测试")
    print("=" * 80)
    print("目标: 测试修复后的窗口查找和自动打开功能")
    print("=" * 80)
    
    tests = [
        ("窗口检测功能", test_window_detection),
        ("自动打开文件功能", test_auto_file_opening),
        ("智能窗口管理功能", test_smart_window_management),
        ("完整自动化流程", test_complete_automation)
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
        print("🎉 所有窗口管理修复测试通过！")
        print("\n功能验证:")
        print("✓ 正确的窗口检测")
        print("✓ 自动打开记事本文件")
        print("✓ 智能窗口管理")
        print("✓ 完整自动化流程")
        print("✓ 避免错误窗口操作")
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
