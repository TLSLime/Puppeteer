# -*- coding: utf-8 -*-
"""
自动执行测试脚本
测试修改后的自动执行功能，避免二次确认和控制台卡死
"""

import sys
import os
import time

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_auto_file_opening():
    """测试自动打开文件功能"""
    print("=" * 60)
    print("测试自动打开文件功能")
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
        
        print("测试自动打开文件...")
        success = manager.ensure_window_active(window_config)
        
        if success:
            print("✓ 自动打开文件功能正常")
            return True
        else:
            print("✗ 自动打开文件功能失败")
            return False
            
    except Exception as e:
        print(f"✗ 自动打开文件测试失败: {e}")
        return False

def test_non_interactive_mode():
    """测试非交互模式"""
    print("\n" + "=" * 60)
    print("测试非交互模式")
    print("=" * 60)
    
    try:
        import subprocess
        
        print("启动非交互模式测试...")
        
        # 使用subprocess启动程序
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
            print("✓ 非交互模式测试成功")
            return True
        else:
            print(f"✗ 非交互模式测试失败，返回码: {process.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ 程序执行超时")
        process.kill()
        return False
    except Exception as e:
        print(f"✗ 非交互模式测试失败: {e}")
        return False

def test_auto_macro_execution():
    """测试自动宏执行"""
    print("\n" + "=" * 60)
    print("测试自动宏执行")
    print("=" * 60)
    
    try:
        from puppeteer.controller import PuppeteerController
        from puppeteer.config import ConfigManager
        from puppeteer.logger import PuppeteerLogger
        from puppeteer.safety_monitor import SafetyLevel
        
        print("创建控制器...")
        
        # 创建组件
        config_manager = ConfigManager("profiles")
        logger = PuppeteerLogger("test_logs")
        controller = PuppeteerController(config_manager, logger, SafetyLevel.DISABLED)
        
        print("✓ 控制器创建成功")
        
        # 加载配置
        if config_manager.load_profile("test_doc"):
            print("✓ 配置加载成功")
            
            # 获取策略配置
            config = config_manager.get_config()
            strategy = config.get("strategy", {})
            auto_macro = strategy.get("auto_execute_macro")
            
            if auto_macro:
                print(f"✓ 找到自动执行宏: {auto_macro}")
                
                # 测试宏执行
                print("测试宏执行...")
                success = controller.execute_macro(auto_macro)
                
                if success:
                    print("✓ 宏执行成功")
                    return True
                else:
                    print("✗ 宏执行失败")
                    return False
            else:
                print("⚠️ 未配置自动执行宏")
                return False
        else:
            print("✗ 配置加载失败")
            return False
            
    except Exception as e:
        print(f"✗ 自动宏执行测试失败: {e}")
        return False

def test_full_automation():
    """测试完整自动化流程"""
    print("\n" + "=" * 60)
    print("测试完整自动化流程")
    print("=" * 60)
    
    try:
        print("准备启动完整自动化测试...")
        print("程序将自动:")
        print("1. 打开test_doc.txt文件")
        print("2. 激活记事本窗口")
        print("3. 执行自动化宏")
        print("4. 自动退出")
        
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
            print("请检查test_doc.txt文件是否已更新")
            return True
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
    print("Puppeteer 自动执行功能测试")
    print("=" * 80)
    print("目标: 测试修改后的自动执行功能，避免二次确认和控制台卡死")
    print("=" * 80)
    
    tests = [
        ("自动打开文件功能", test_auto_file_opening),
        ("非交互模式", test_non_interactive_mode),
        ("自动宏执行", test_auto_macro_execution),
        ("完整自动化流程", test_full_automation)
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
        print("🎉 所有自动执行功能测试通过！")
        print("\n功能验证:")
        print("✓ 自动打开文件功能")
        print("✓ 非交互模式运行")
        print("✓ 自动宏执行")
        print("✓ 完整自动化流程")
        print("✓ 避免二次确认")
        print("✓ 避免控制台卡死")
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
