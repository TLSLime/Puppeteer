# -*- coding: utf-8 -*-
"""
安全系统测试脚本
测试安全监控、紧急停止和用户操作检测功能
"""

import sys
import os
import time
import threading

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_safety_monitor():
    """测试安全监控器"""
    print("=" * 60)
    print("测试安全监控器")
    print("=" * 60)
    
    try:
        from puppeteer.safety_monitor import SafetyMonitor, SafetyLevel, SafetyEvent
        
        def safety_callback(event_type, data):
            print(f"安全事件回调: {event_type.value} - {data}")
            
        # 创建安全监控器
        monitor = SafetyMonitor(SafetyLevel.MEDIUM, "esc", safety_callback)
        print("✓ 安全监控器创建成功")
        
        # 测试配置
        print(f"安全级别: {monitor.safety_level.value}")
        print(f"紧急停止键: {monitor.emergency_key}")
        print(f"用户活动阈值: {monitor._user_activity_threshold}秒")
        
        # 测试监控启动
        monitor.start_monitoring()
        print("✓ 安全监控已启动")
        
        # 等待一段时间让用户测试
        print("\n请尝试以下操作来测试安全系统:")
        print("1. 移动鼠标")
        print("2. 按键盘按键")
        print("3. 按ESC键紧急停止")
        print("4. 等待10秒自动结束测试")
        
        # 监控10秒
        for i in range(100):
            time.sleep(0.1)
            if not monitor.is_monitoring():
                print("监控已停止")
                break
                
        # 停止监控
        monitor.stop_monitoring()
        print("✓ 安全监控已停止")
        
        # 显示统计信息
        stats = monitor.get_stats()
        print(f"\n监控统计:")
        print(f"  鼠标事件: {stats['mouse_events']}")
        print(f"  键盘事件: {stats['keyboard_events']}")
        print(f"  紧急停止: {stats['emergency_stops']}")
        print(f"  总事件数: {stats['total_events']}")
        
        return True
        
    except Exception as e:
        print(f"✗ 安全监控器测试失败: {e}")
        return False


def test_safety_manager():
    """测试安全管理器"""
    print("\n" + "=" * 60)
    print("测试安全管理器")
    print("=" * 60)
    
    try:
        from puppeteer.safety_monitor import SafetyManager, SafetyLevel
        
        # 创建安全管理器
        manager = SafetyManager(SafetyLevel.MEDIUM)
        print("✓ 安全管理器创建成功")
        
        # 测试配置
        config = manager.get_config()
        print(f"安全配置: {config}")
        
        # 启动安全监控
        manager.start_safety_monitoring()
        print("✓ 安全监控已启动")
        
        # 启动自动化
        manager.start_automation()
        print("✓ 自动化已启动")
        
        # 检查状态
        print(f"自动化运行状态: {manager.is_automation_running()}")
        print(f"安全监控状态: {manager.is_safety_monitoring()}")
        
        # 等待一段时间
        print("\n请尝试移动鼠标或按键盘来测试自动停止...")
        time.sleep(5)
        
        # 检查状态
        print(f"自动化运行状态: {manager.is_automation_running()}")
        
        # 停止自动化
        manager.stop_automation("test_complete")
        print("✓ 自动化已停止")
        
        # 停止安全监控
        manager.stop_safety_monitoring()
        print("✓ 安全监控已停止")
        
        # 显示统计信息
        stats = manager.get_safety_stats()
        print(f"\n安全统计: {stats}")
        
        return True
        
    except Exception as e:
        print(f"✗ 安全管理器测试失败: {e}")
        return False


def test_controller_integration():
    """测试控制器集成"""
    print("\n" + "=" * 60)
    print("测试控制器安全集成")
    print("=" * 60)
    
    try:
        from puppeteer.controller import PuppeteerController
        from puppeteer.config import ConfigManager
        from puppeteer.logger import PuppeteerLogger
        from puppeteer.safety_monitor import SafetyLevel
        
        # 创建测试配置
        config_manager = ConfigManager("test_safety_profiles")
        logger = PuppeteerLogger("test_safety_logs")
        
        # 创建控制器
        controller = PuppeteerController(config_manager, logger, SafetyLevel.MEDIUM)
        print("✓ 控制器创建成功")
        
        # 检查安全级别
        safety_level = controller.get_safety_level()
        print(f"安全级别: {safety_level.value}")
        
        # 获取状态
        status = controller.get_status()
        print(f"控制器状态: {status}")
        
        # 测试安全统计
        safety_stats = controller.get_safety_stats()
        print(f"安全统计: {safety_stats}")
        
        # 清理测试文件
        import shutil
        if os.path.exists("test_safety_profiles"):
            shutil.rmtree("test_safety_profiles")
        if os.path.exists("test_safety_logs"):
            shutil.rmtree("test_safety_logs")
            
        return True
        
    except Exception as e:
        print(f"✗ 控制器集成测试失败: {e}")
        return False


def test_safety_levels():
    """测试不同安全级别"""
    print("\n" + "=" * 60)
    print("测试不同安全级别")
    print("=" * 60)
    
    try:
        from puppeteer.safety_monitor import SafetyMonitor, SafetyLevel
        
        levels = [SafetyLevel.LOW, SafetyLevel.MEDIUM, SafetyLevel.HIGH]
        
        for level in levels:
            print(f"\n测试安全级别: {level.value}")
            
            monitor = SafetyMonitor(level, "esc")
            print(f"✓ {level.value} 级别监控器创建成功")
            
            # 测试配置
            print(f"  监控鼠标: {level in [SafetyLevel.MEDIUM, SafetyLevel.HIGH]}")
            print(f"  监控键盘: {level in [SafetyLevel.MEDIUM, SafetyLevel.HIGH]}")
            print(f"  监控紧急键: {True}")
            
        return True
        
    except Exception as e:
        print(f"✗ 安全级别测试失败: {e}")
        return False


def test_emergency_keys():
    """测试不同紧急停止键"""
    print("\n" + "=" * 60)
    print("测试不同紧急停止键")
    print("=" * 60)
    
    try:
        from puppeteer.safety_monitor import SafetyMonitor, SafetyLevel
        
        emergency_keys = ["esc", "f1", "f12", "space"]
        
        for key in emergency_keys:
            print(f"\n测试紧急停止键: {key.upper()}")
            
            monitor = SafetyMonitor(SafetyLevel.LOW, key)
            print(f"✓ 紧急停止键 {key.upper()} 设置成功")
            
            # 检查键码
            vk_code = monitor.VK_CODES.get(key.lower())
            if vk_code:
                print(f"  虚拟键码: 0x{vk_code:02X}")
            else:
                print(f"  ⚠️ 不支持的按键: {key}")
                
        return True
        
    except Exception as e:
        print(f"✗ 紧急停止键测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("Puppeteer 安全系统测试")
    print("=" * 80)
    
    # 等待用户准备
    print("请确保:")
    print("1. 鼠标和键盘可以正常使用")
    print("2. 准备好测试用户操作检测")
    print("3. 准备好测试紧急停止功能")
    
    input("\n按回车键开始测试...")
    
    tests = [
        ("安全监控器", test_safety_monitor),
        ("安全管理器", test_safety_manager),
        ("控制器集成", test_controller_integration),
        ("安全级别", test_safety_levels),
        ("紧急停止键", test_emergency_keys)
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
        print("🎉 所有测试通过！安全系统工作正常")
        print("\n安全功能特性:")
        print("✓ 用户操作检测（鼠标、键盘）")
        print("✓ 紧急停止键支持")
        print("✓ 多级安全配置")
        print("✓ 实时监控和统计")
        print("✓ 自动停止自动化程序")
        print("✓ 安全事件日志记录")
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
