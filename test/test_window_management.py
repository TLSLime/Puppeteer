# -*- coding: utf-8 -*-
"""
窗口管理功能测试脚本
测试目标窗口激活、鼠标定位等功能
"""

import sys
import os
import time

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_window_manager():
    """测试窗口管理器基本功能"""
    print("=" * 60)
    print("测试窗口管理器基本功能")
    print("=" * 60)
    
    try:
        from puppeteer.window_manager import WindowManager
        
        # 创建窗口管理器
        manager = WindowManager()
        print("✓ 窗口管理器创建成功")
        
        # 列出所有窗口
        print("\n列出所有可见窗口:")
        windows = manager.list_windows()
        for i, window in enumerate(windows[:5]):  # 只显示前5个
            print(f"{i+1}. {window['title']} ({window['class_name']})")
            
        # 测试查找记事本窗口
        print("\n测试查找记事本窗口:")
        notepad_hwnd = manager.find_window_by_title("记事本")
        if notepad_hwnd:
            window_info = manager.get_window_info(notepad_hwnd)
            print(f"✓ 找到记事本: {window_info['title']}")
            print(f"  窗口状态: {window_info['state']}")
            print(f"  窗口位置: {window_info['position']}")
            
            # 测试激活窗口
            if manager.activate_window(notepad_hwnd):
                print("✓ 记事本窗口已激活")
                
                # 测试移动鼠标到不同位置
                positions = ["center", "top_left", "top_right", "bottom_left", "bottom_right"]
                for pos in positions:
                    if manager.move_mouse_to_window(notepad_hwnd, pos):
                        print(f"✓ 鼠标已移动到 {pos}")
                        time.sleep(0.5)
        else:
            print("⚠️ 未找到记事本窗口")
            
        return True
        
    except Exception as e:
        print(f"✗ 窗口管理器测试失败: {e}")
        return False

def test_window_config():
    """测试窗口配置功能"""
    print("\n" + "=" * 60)
    print("测试窗口配置功能")
    print("=" * 60)
    
    try:
        from puppeteer.window_manager import WindowManager
        
        manager = WindowManager()
        
        # 测试不同的窗口配置
        configs = [
            {
                "title": "记事本",
                "exact_match": False,
                "mouse_position": "center",
                "auto_activate": True,
                "activation_delay": 0.5
            },
            {
                "title": "新建文本文档",
                "exact_match": False,
                "mouse_position": "top_left",
                "auto_activate": True,
                "activation_delay": 0.3
            }
        ]
        
        for i, config in enumerate(configs):
            print(f"\n测试配置 {i+1}: {config['title']}")
            success = manager.ensure_window_active(config)
            if success:
                print(f"✓ 配置 {i+1} 测试成功")
            else:
                print(f"✗ 配置 {i+1} 测试失败")
                
        return True
        
    except Exception as e:
        print(f"✗ 窗口配置测试失败: {e}")
        return False

def test_controller_integration():
    """测试控制器集成"""
    print("\n" + "=" * 60)
    print("测试控制器窗口管理集成")
    print("=" * 60)
    
    try:
        from puppeteer.controller import PuppeteerController
        from puppeteer.config import ConfigManager
        from puppeteer.logger import PuppeteerLogger
        from puppeteer.safety_monitor import SafetyLevel
        
        # 创建测试配置
        config_manager = ConfigManager("test_window_profiles")
        logger = PuppeteerLogger("test_window_logs")
        
        # 创建控制器
        controller = PuppeteerController(config_manager, logger, SafetyLevel.DISABLED)
        print("✓ 控制器创建成功")
        
        # 检查窗口管理器
        if hasattr(controller, 'window_manager'):
            print("✓ 窗口管理器已集成")
        else:
            print("✗ 窗口管理器未集成")
            return False
            
        # 清理测试文件
        import shutil
        if os.path.exists("test_window_profiles"):
            shutil.rmtree("test_window_profiles")
        if os.path.exists("test_window_logs"):
            shutil.rmtree("test_window_logs")
            
        return True
        
    except Exception as e:
        print(f"✗ 控制器集成测试失败: {e}")
        return False

def test_config_files():
    """测试配置文件"""
    print("\n" + "=" * 60)
    print("测试配置文件")
    print("=" * 60)
    
    try:
        import yaml
        
        # 测试simple_test.yaml
        with open("profiles/simple_test.yaml", 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            
        if "window" in config:
            window_config = config["window"]
            print("✓ simple_test.yaml 包含窗口配置")
            print(f"  窗口标题: {window_config.get('title', 'N/A')}")
            print(f"  鼠标位置: {window_config.get('mouse_position', 'N/A')}")
            print(f"  自动激活: {window_config.get('auto_activate', 'N/A')}")
        else:
            print("✗ simple_test.yaml 缺少窗口配置")
            return False
            
        # 测试example_game.yaml
        with open("profiles/example_game.yaml", 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            
        if "window" in config:
            window_config = config["window"]
            print("✓ example_game.yaml 包含窗口配置")
            print(f"  窗口标题: {window_config.get('title', 'N/A')}")
            print(f"  鼠标位置: {window_config.get('mouse_position', 'N/A')}")
            print(f"  自动激活: {window_config.get('auto_activate', 'N/A')}")
        else:
            print("✗ example_game.yaml 缺少窗口配置")
            return False
            
        return True
        
    except Exception as e:
        print(f"✗ 配置文件测试失败: {e}")
        return False

def test_full_workflow():
    """测试完整工作流程"""
    print("\n" + "=" * 60)
    print("测试完整工作流程")
    print("=" * 60)
    
    try:
        print("请确保记事本程序已打开...")
        input("按回车键继续...")
        
        # 测试完整流程
        from puppeteer.window_manager import WindowManager
        
        manager = WindowManager()
        
        # 查找并激活记事本
        config = {
            "title": "记事本",
            "exact_match": False,
            "mouse_position": "center",
            "auto_activate": True,
            "activation_delay": 1.0
        }
        
        print("激活目标窗口...")
        success = manager.ensure_window_active(config)
        
        if success:
            print("✓ 完整工作流程测试成功")
            print("  目标窗口已激活")
            print("  鼠标已定位到窗口中心")
            print("  可以开始自动化操作")
        else:
            print("✗ 完整工作流程测试失败")
            
        return success
        
    except Exception as e:
        print(f"✗ 完整工作流程测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("Puppeteer 窗口管理功能测试")
    print("=" * 80)
    
    tests = [
        ("窗口管理器基本功能", test_window_manager),
        ("窗口配置功能", test_window_config),
        ("控制器集成", test_controller_integration),
        ("配置文件", test_config_files),
        ("完整工作流程", test_full_workflow)
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
        print("🎉 窗口管理功能测试全部通过！")
        print("\n功能特性:")
        print("✓ 目标窗口查找和激活")
        print("✓ 鼠标自动定位到窗口内")
        print("✓ 配置文件支持")
        print("✓ 控制器集成")
        print("✓ 多种窗口查找方式")
        print("✓ 灵活的鼠标位置配置")
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
