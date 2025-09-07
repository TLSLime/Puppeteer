# -*- coding: utf-8 -*-
"""
直接输入测试
测试输入提供器的基本功能
"""

import sys
import os
import time

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_input_provider():
    """测试输入提供器"""
    print("=" * 60)
    print("输入提供器测试")
    print("=" * 60)
    
    try:
        from puppeteer.input_provider import InputProvider
        
        # 创建输入提供器
        input_provider = InputProvider()
        print("✓ 输入提供器创建成功")
        
        # 测试基本功能
        print("测试基本功能...")
        
        # 获取鼠标位置
        mouse_pos = input_provider.get_mouse_position()
        print(f"✓ 当前鼠标位置: {mouse_pos}")
        
        # 获取屏幕大小
        screen_size = input_provider.get_screen_size()
        print(f"✓ 屏幕大小: {screen_size}")
        
        # 测试按键检测
        space_pressed = input_provider.is_key_pressed("space")
        print(f"✓ 空格键检测: {space_pressed}")
        
        return True
        
    except Exception as e:
        print(f"✗ 输入提供器测试失败: {e}")
        return False

def test_text_input():
    """测试文本输入"""
    print("\n" + "=" * 60)
    print("文本输入测试")
    print("=" * 60)
    
    try:
        from puppeteer.input_provider import InputProvider
        
        print("请确保记事本程序已打开，并且光标在可输入位置")
        input("按回车键开始文本输入测试...")
        
        # 创建输入提供器
        input_provider = InputProvider()
        
        # 等待2秒
        print("等待2秒...")
        time.sleep(2)
        
        # 输入测试文本
        test_text = "Puppeteer自动化测试 - 文本输入功能正常！"
        print(f"输入文本: {test_text}")
        input_provider.type_text(test_text)
        time.sleep(1)
        
        # 换行
        print("换行...")
        input_provider.press_key("enter")
        time.sleep(1)
        
        # 输入时间戳
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_text = f"测试时间: {timestamp}"
        print(f"输入时间: {time_text}")
        input_provider.type_text(time_text)
        time.sleep(1)
        
        # 换行
        input_provider.press_key("enter")
        time.sleep(1)
        
        # 保存文档
        print("保存文档...")
        input_provider.press_key("ctrl+s")
        time.sleep(1)
        
        print("✓ 文本输入测试完成")
        return True
        
    except Exception as e:
        print(f"✗ 文本输入测试失败: {e}")
        return False

def test_keyboard_operations():
    """测试键盘操作"""
    print("\n" + "=" * 60)
    print("键盘操作测试")
    print("=" * 60)
    
    try:
        from puppeteer.input_provider import InputProvider
        
        print("请确保记事本程序已打开，并且光标在可输入位置")
        input("按回车键开始键盘操作测试...")
        
        # 创建输入提供器
        input_provider = InputProvider()
        
        # 等待2秒
        print("等待2秒...")
        time.sleep(2)
        
        # 输入测试文本
        test_text = "键盘操作测试开始"
        print(f"输入文本: {test_text}")
        input_provider.type_text(test_text)
        time.sleep(1)
        
        # 测试各种键盘操作
        operations = [
            ("换行", "enter"),
            ("移动到行首", "home"),
            ("移动到行尾", "end"),
            ("全选", "ctrl+a"),
            ("复制", "ctrl+c"),
            ("移动到行尾", "end"),
            ("换行", "enter"),
            ("粘贴", "ctrl+v"),
            ("换行", "enter"),
            ("删除", "delete"),
            ("退格", "backspace")
        ]
        
        for desc, key in operations:
            print(f"执行: {desc} ({key})")
            input_provider.press_key(key)
            time.sleep(0.5)
        
        # 保存文档
        print("保存文档...")
        input_provider.press_key("ctrl+s")
        time.sleep(1)
        
        print("✓ 键盘操作测试完成")
        return True
        
    except Exception as e:
        print(f"✗ 键盘操作测试失败: {e}")
        return False

def test_mouse_operations():
    """测试鼠标操作"""
    print("\n" + "=" * 60)
    print("鼠标操作测试")
    print("=" * 60)
    
    try:
        from puppeteer.input_provider import InputProvider
        
        print("请确保记事本程序已打开")
        input("按回车键开始鼠标操作测试...")
        
        # 创建输入提供器
        input_provider = InputProvider()
        
        # 等待2秒
        print("等待2秒...")
        time.sleep(2)
        
        # 获取当前鼠标位置
        current_pos = input_provider.get_mouse_position()
        print(f"当前鼠标位置: {current_pos}")
        
        # 测试鼠标移动
        print("测试鼠标移动...")
        input_provider.move_mouse(400, 300)
        time.sleep(1)
        
        # 测试鼠标点击
        print("测试鼠标点击...")
        input_provider.click(400, 300)
        time.sleep(1)
        
        # 输入测试文本
        test_text = "鼠标操作测试完成"
        print(f"输入文本: {test_text}")
        input_provider.type_text(test_text)
        time.sleep(1)
        
        # 保存文档
        print("保存文档...")
        input_provider.press_key("ctrl+s")
        time.sleep(1)
        
        print("✓ 鼠标操作测试完成")
        return True
        
    except Exception as e:
        print(f"✗ 鼠标操作测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("Puppeteer 直接输入测试")
    print("=" * 80)
    print("目标: 验证输入提供器的基本功能")
    print("=" * 80)
    
    tests = [
        ("输入提供器测试", test_input_provider),
        ("文本输入测试", test_text_input),
        ("键盘操作测试", test_keyboard_operations),
        ("鼠标操作测试", test_mouse_operations)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name}异常: {e}")
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
        print("🎉 所有输入测试通过！")
        print("\n功能验证:")
        print("✓ 输入提供器基本功能")
        print("✓ 文本输入功能")
        print("✓ 键盘操作功能")
        print("✓ 鼠标操作功能")
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
