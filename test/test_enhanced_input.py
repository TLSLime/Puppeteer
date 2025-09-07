# -*- coding: utf-8 -*-
"""
增强输入功能测试脚本
测试Windows核心输入、增强输入和原有输入功能
"""

import time
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from puppeteer.input_provider import InputProvider
from puppeteer.windows_core import WindowsCoreInput
from puppeteer.input_enhanced import EnhancedInputProvider


def test_windows_core():
    """测试Windows核心输入"""
    print("\n" + "="*50)
    print("测试Windows核心输入")
    print("="*50)
    
    try:
        provider = WindowsCoreInput(humanize_enabled=True)
        
        # 获取屏幕信息
        size = provider.get_screen_size()
        pos = provider.get_mouse_position()
        print(f"屏幕尺寸: {size}")
        print(f"当前鼠标位置: {pos}")
        
        # 测试鼠标移动
        print("\n测试鼠标移动...")
        center_x, center_y = size[0] // 2, size[1] // 2
        success = provider.move_mouse(center_x, center_y)
        print(f"移动到屏幕中心: {'成功' if success else '失败'}")
        
        # 测试点击
        print("\n测试点击...")
        success = provider.click(center_x, center_y)
        print(f"点击屏幕中心: {'成功' if success else '失败'}")
        
        # 测试按键
        print("\n测试按键...")
        success = provider.press_key("space")
        print(f"按下空格键: {'成功' if success else '失败'}")
        
        # 测试文本输入
        print("\n测试文本输入...")
        success = provider.type_text("Hello World")
        print(f"输入文本: {'成功' if success else '失败'}")
        
        # 测试按键状态
        print("\n测试按键状态...")
        space_pressed = provider.is_key_pressed("space")
        print(f"空格键状态: {'按下' if space_pressed else '未按下'}")
        
        # 显示支持的按键
        keys = provider.get_available_keys()
        print(f"支持的按键数量: {len(keys)}")
        print(f"部分按键示例: {keys[:10]}")
        
        return True
        
    except Exception as e:
        print(f"Windows核心输入测试失败: {e}")
        return False


def test_enhanced_input():
    """测试增强输入"""
    print("\n" + "="*50)
    print("测试增强输入")
    print("="*50)
    
    try:
        provider = EnhancedInputProvider(input_method="auto", humanize_enabled=True)
        
        # 获取屏幕信息
        size = provider.get_screen_size()
        pos = provider.get_mouse_position()
        print(f"屏幕尺寸: {size}")
        print(f"当前鼠标位置: {pos}")
        
        # 测试鼠标移动
        print("\n测试鼠标移动...")
        center_x, center_y = size[0] // 2, size[1] // 2
        success = provider.move_mouse(center_x, center_y)
        print(f"移动到屏幕中心: {'成功' if success else '失败'}")
        
        # 测试点击
        print("\n测试点击...")
        success = provider.click(center_x, center_y)
        print(f"点击屏幕中心: {'成功' if success else '失败'}")
        
        # 测试按键
        print("\n测试按键...")
        success = provider.press_key("space")
        print(f"按下空格键: {'成功' if success else '失败'}")
        
        # 测试文本输入
        print("\n测试文本输入...")
        success = provider.type_text("Hello World")
        print(f"输入文本: {'成功' if success else '失败'}")
        
        return True
        
    except Exception as e:
        print(f"增强输入测试失败: {e}")
        return False


def test_input_provider():
    """测试输入提供器"""
    print("\n" + "="*50)
    print("测试输入提供器")
    print("="*50)
    
    try:
        # 测试自动选择
        provider = InputProvider(humanize_enabled=True, input_method="auto")
        print(f"自动选择的输入方法: {provider.get_input_method()}")
        
        # 获取屏幕信息
        size = provider.get_screen_size()
        pos = provider.get_mouse_position()
        print(f"屏幕尺寸: {size}")
        print(f"当前鼠标位置: {pos}")
        
        # 测试鼠标移动
        print("\n测试鼠标移动...")
        center_x, center_y = size[0] // 2, size[1] // 2
        success = provider.move_mouse(center_x, center_y)
        print(f"移动到屏幕中心: {'成功' if success else '失败'}")
        
        # 测试点击
        print("\n测试点击...")
        success = provider.click(center_x, center_y)
        print(f"点击屏幕中心: {'成功' if success else '失败'}")
        
        # 测试按键
        print("\n测试按键...")
        success = provider.press_key("space")
        print(f"按下空格键: {'成功' if success else '失败'}")
        
        # 测试文本输入
        print("\n测试文本输入...")
        success = provider.type_text("Hello World")
        print(f"输入文本: {'成功' if success else '失败'}")
        
        # 测试按键状态
        print("\n测试按键状态...")
        space_pressed = provider.is_key_pressed("space")
        print(f"空格键状态: {'按下' if space_pressed else '未按下'}")
        
        # 测试动作对象
        print("\n测试动作对象...")
        action = {
            "type": "press",
            "key": "q",
            "humanize": {"delay_ms": [50, 100]}
        }
        result = provider.execute_action(action)
        print(f"动作执行结果: {result['success']}")
        
        return True
        
    except Exception as e:
        print(f"输入提供器测试失败: {e}")
        return False


def test_performance():
    """测试性能"""
    print("\n" + "="*50)
    print("性能测试")
    print("="*50)
    
    try:
        provider = InputProvider(humanize_enabled=False, input_method="auto")
        
        # 测试鼠标移动性能
        print("测试鼠标移动性能...")
        start_time = time.time()
        for i in range(10):
            provider.move_mouse(100 + i * 10, 100 + i * 10)
        end_time = time.time()
        print(f"10次鼠标移动耗时: {end_time - start_time:.3f}秒")
        
        # 测试按键性能
        print("测试按键性能...")
        start_time = time.time()
        for i in range(10):
            provider.press_key("space")
        end_time = time.time()
        print(f"10次按键耗时: {end_time - start_time:.3f}秒")
        
        return True
        
    except Exception as e:
        print(f"性能测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("Puppeteer 增强输入功能测试")
    print("=" * 60)
    
    # 等待用户准备
    print("请确保:")
    print("1. 有一个文本编辑器或记事本打开")
    print("2. 鼠标和键盘可以正常使用")
    print("3. 准备好观察测试结果")
    
    input("\n按回车键开始测试...")
    
    test_results = []
    
    # 测试Windows核心输入
    result = test_windows_core()
    test_results.append(("Windows核心输入", result))
    
    # 测试增强输入
    result = test_enhanced_input()
    test_results.append(("增强输入", result))
    
    # 测试输入提供器
    result = test_input_provider()
    test_results.append(("输入提供器", result))
    
    # 测试性能
    result = test_performance()
    test_results.append(("性能测试", result))
    
    # 显示测试结果
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    success_count = 0
    for test_name, success in test_results:
        status = "✓ 成功" if success else "✗ 失败"
        print(f"{test_name}: {status}")
        if success:
            success_count += 1
    
    print(f"\n总体结果: {success_count}/{len(test_results)} 测试通过")
    
    if success_count == len(test_results):
        print("🎉 所有测试通过！增强输入功能工作正常")
    else:
        print("⚠️ 部分测试失败，请检查错误信息")
    
    return success_count == len(test_results)


if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n用户中断测试")
        sys.exit(1)
    except Exception as e:
        print(f"\n测试过程中发生异常: {e}")
        sys.exit(1)
