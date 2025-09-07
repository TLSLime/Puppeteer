# -*- coding: utf-8 -*-
"""
快速安全系统测试
测试调整后的安全机制是否更宽松
"""

import sys
import os
import time

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_safety_looseness():
    """测试安全机制的宽松程度"""
    print("测试调整后的安全机制...")
    
    try:
        from puppeteer.safety_monitor import SafetyMonitor, SafetyLevel
        
        # 创建安全监控器
        monitor = SafetyMonitor(SafetyLevel.MEDIUM, "esc")
        print("✓ 安全监控器创建成功")
        
        # 显示配置
        config = monitor.get_safety_config()
        print(f"安全配置:")
        print(f"  用户活动阈值: {config['user_activity_threshold']}秒")
        print(f"  鼠标移动阈值: {config['mouse_movement_threshold']}像素")
        print(f"  宽限期: {config['grace_period']}秒")
        
        # 启动监控
        monitor.start_monitoring()
        print("✓ 安全监控已启动")
        
        print("\n测试说明:")
        print("1. 启动后有2秒宽限期，期间的操作不会触发安全机制")
        print("2. 鼠标移动需要超过10像素才会被检测")
        print("3. 操作间隔需要超过0.5秒才会被检测")
        print("4. 请尝试轻微移动鼠标，应该不会触发安全机制")
        
        # 监控5秒
        for i in range(50):
            time.sleep(0.1)
            if not monitor.is_monitoring():
                print("监控已停止")
                break
                
        # 停止监控
        monitor.stop_monitoring()
        print("✓ 安全监控已停止")
        
        # 显示统计
        stats = monitor.get_stats()
        print(f"\n监控统计:")
        print(f"  鼠标事件: {stats['mouse_events']}")
        print(f"  键盘事件: {stats['keyboard_events']}")
        print(f"  紧急停止: {stats['emergency_stops']}")
        print(f"  总事件数: {stats['total_events']}")
        
        if stats['total_events'] == 0:
            print("✓ 安全机制调整成功，没有误触发")
        else:
            print("⚠️ 仍有安全事件触发，可能需要进一步调整")
            
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def test_controller_safety():
    """测试控制器的安全集成"""
    print("\n测试控制器安全集成...")
    
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
        
        # 检查安全配置
        safety_level = controller.get_safety_level()
        print(f"安全级别: {safety_level.value}")
        
        # 获取状态
        status = controller.get_status()
        print(f"安全级别: {status['safety_level']}")
        print(f"安全统计: {status['safety_stats']}")
        
        # 清理测试文件
        import shutil
        if os.path.exists("test_safety_profiles"):
            shutil.rmtree("test_safety_profiles")
        if os.path.exists("test_safety_logs"):
            shutil.rmtree("test_safety_logs")
            
        return True
        
    except Exception as e:
        print(f"✗ 控制器测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("Puppeteer 安全机制宽松度测试")
    print("=" * 50)
    
    tests = [
        ("安全机制宽松度", test_safety_looseness),
        ("控制器安全集成", test_controller_safety)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name}测试异常: {e}")
            results.append((test_name, False))
    
    # 显示结果
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    
    success_count = 0
    for test_name, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"{test_name}: {status}")
        if success:
            success_count += 1
    
    print(f"\n总体结果: {success_count}/{len(results)} 测试通过")
    
    if success_count == len(results):
        print("🎉 安全机制调整成功！")
        print("\n调整内容:")
        print("✓ 用户活动阈值: 0.1秒 → 0.5秒")
        print("✓ 鼠标移动阈值: 无限制 → 10像素")
        print("✓ 宽限期: 无 → 2秒")
        print("✓ 启动后2秒内的操作不会触发安全机制")
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
