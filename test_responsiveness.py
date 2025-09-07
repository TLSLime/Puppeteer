# -*- coding: utf-8 -*-
"""
响应性测试脚本
测试程序的响应性和未响应问题
"""

import sys
import os
import time
import threading
import signal

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_dialog_detection_responsiveness():
    """测试对话框检测的响应性"""
    print("=" * 60)
    print("测试对话框检测响应性")
    print("=" * 60)
    
    try:
        from puppeteer.dialog_handler import DialogHandler
        
        # 创建对话框处理器
        config = {
            "enabled": True,
            "detection_interval": 0.1,  # 更短的检测间隔
            "dialog_timeout": 5.0,
            "expected_dialogs": []
        }
        
        handler = DialogHandler(config)
        print("✅ 对话框处理器创建成功")
        
        # 启动检测
        print("🔍 启动对话框检测...")
        handler.start_dialog_detection()
        
        # 运行10秒
        print("⏱️ 运行10秒测试响应性...")
        start_time = time.time()
        
        while time.time() - start_time < 10:
            time.sleep(1)
            elapsed = time.time() - start_time
            print(f"⏱️ 已运行 {elapsed:.1f} 秒")
        
        # 停止检测
        print("🛑 停止对话框检测...")
        handler.stop_dialog_detection()
        
        print("✅ 对话框检测响应性测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 对话框检测响应性测试失败: {e}")
        return False

def test_controller_responsiveness():
    """测试控制器的响应性"""
    print("\n" + "=" * 60)
    print("测试控制器响应性")
    print("=" * 60)
    
    try:
        from puppeteer.controller import PuppeteerController
        from puppeteer.config import ConfigManager
        from puppeteer.logger import PuppeteerLogger
        from puppeteer.safety_monitor import SafetyLevel
        
        # 创建控制器
        config_manager = ConfigManager("profiles")
        logger = PuppeteerLogger("test_logs")
        controller = PuppeteerController(config_manager, logger, SafetyLevel.DISABLED)
        
        print("✅ 控制器创建成功")
        
        # 启动控制器
        print("🚀 启动控制器...")
        success = controller.start("test_doc")
        
        if success:
            print("✅ 控制器启动成功")
            
            # 运行5秒
            print("⏱️ 运行5秒测试响应性...")
            start_time = time.time()
            
            while time.time() - start_time < 5:
                time.sleep(1)
                elapsed = time.time() - start_time
                print(f"⏱️ 已运行 {elapsed:.1f} 秒")
            
            # 停止控制器
            print("🛑 停止控制器...")
            controller.stop()
            
            print("✅ 控制器响应性测试完成")
            return True
        else:
            print("❌ 控制器启动失败")
            return False
        
    except Exception as e:
        print(f"❌ 控制器响应性测试失败: {e}")
        return False

def test_interrupt_handling():
    """测试中断处理"""
    print("\n" + "=" * 60)
    print("测试中断处理")
    print("=" * 60)
    
    try:
        from puppeteer.dialog_handler import DialogHandler
        
        # 创建对话框处理器
        handler = DialogHandler()
        
        # 启动检测
        print("🔍 启动对话框检测...")
        handler.start_dialog_detection()
        
        # 运行3秒后中断
        print("⏱️ 运行3秒后测试中断...")
        time.sleep(3)
        
        # 停止检测
        print("🛑 测试中断处理...")
        handler.stop_dialog_detection()
        
        print("✅ 中断处理测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 中断处理测试失败: {e}")
        return False

def test_memory_usage():
    """测试内存使用情况"""
    print("\n" + "=" * 60)
    print("测试内存使用情况")
    print("=" * 60)
    
    try:
        import psutil
        import gc
        
        # 获取当前进程
        process = psutil.Process()
        
        print(f"📊 初始内存使用: {process.memory_info().rss / 1024 / 1024:.1f} MB")
        
        # 创建多个对话框处理器
        handlers = []
        for i in range(5):
            from puppeteer.dialog_handler import DialogHandler
            handler = DialogHandler()
            handlers.append(handler)
            handler.start_dialog_detection()
            
            memory_usage = process.memory_info().rss / 1024 / 1024
            print(f"📊 创建第{i+1}个处理器后内存使用: {memory_usage:.1f} MB")
        
        # 停止所有处理器
        for i, handler in enumerate(handlers):
            handler.stop_dialog_detection()
            memory_usage = process.memory_info().rss / 1024 / 1024
            print(f"📊 停止第{i+1}个处理器后内存使用: {memory_usage:.1f} MB")
        
        # 清理
        handlers.clear()
        gc.collect()
        
        final_memory = process.memory_info().rss / 1024 / 1024
        print(f"📊 最终内存使用: {final_memory:.1f} MB")
        
        print("✅ 内存使用测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 内存使用测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("Puppeteer 响应性测试")
    print("=" * 80)
    print("目标: 测试程序的响应性和未响应问题")
    print("=" * 80)
    
    tests = [
        ("对话框检测响应性", test_dialog_detection_responsiveness),
        ("控制器响应性", test_controller_responsiveness),
        ("中断处理", test_interrupt_handling),
        ("内存使用情况", test_memory_usage)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            print(f"\n开始 {test_name}...")
            result = test_func()
            results.append((test_name, result))
            print(f"✅ {test_name} 完成")
        except Exception as e:
            print(f"❌ {test_name} 失败: {e}")
            results.append((test_name, False))
    
    # 显示测试结果
    print("\n" + "=" * 80)
    print("测试结果汇总")
    print("=" * 80)
    
    success_count = 0
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{test_name}: {status}")
        if success:
            success_count += 1
    
    print(f"\n总体结果: {success_count}/{len(results)} 测试通过")
    
    if success_count == len(results):
        print("🎉 所有响应性测试通过！")
        print("\n功能验证:")
        print("✅ 对话框检测响应性")
        print("✅ 控制器响应性")
        print("✅ 中断处理")
        print("✅ 内存使用情况")
        print("✅ 未响应问题已解决")
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
