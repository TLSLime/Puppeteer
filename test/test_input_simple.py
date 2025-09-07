# -*- coding: utf-8 -*-
"""
简化的输入测试脚本
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_basic_imports():
    """测试基本导入"""
    print("测试基本导入...")
    
    try:
        from puppeteer.input_provider import InputProvider
        print("✓ InputProvider导入成功")
        
        from puppeteer.windows_core import WindowsCoreInput
        print("✓ WindowsCoreInput导入成功")
        
        from puppeteer.input_enhanced import EnhancedInputProvider
        print("✓ EnhancedInputProvider导入成功")
        
        # 将导入的类存储到全局变量中
        globals()['InputProvider'] = InputProvider
        globals()['WindowsCoreInput'] = WindowsCoreInput
        globals()['EnhancedInputProvider'] = EnhancedInputProvider
        
        return True
    except Exception as e:
        print(f"✗ 导入失败: {e}")
        return False

def test_input_provider():
    """测试输入提供器"""
    print("\n测试输入提供器...")
    
    try:
        provider = InputProvider(humanize_enabled=True, input_method="auto")
        print(f"✓ 输入提供器初始化成功，使用方法: {provider.get_input_method()}")
        
        # 测试获取信息
        pos = provider.get_mouse_position()
        size = provider.get_screen_size()
        print(f"✓ 鼠标位置: {pos}")
        print(f"✓ 屏幕尺寸: {size}")
        
        return True
    except Exception as e:
        print(f"✗ 输入提供器测试失败: {e}")
        return False

def test_windows_core():
    """测试Windows核心输入"""
    print("\n测试Windows核心输入...")
    
    try:
        provider = WindowsCoreInput(humanize_enabled=True)
        print("✓ Windows核心输入初始化成功")
        
        # 测试获取信息
        pos = provider.get_mouse_position()
        size = provider.get_screen_size()
        print(f"✓ 鼠标位置: {pos}")
        print(f"✓ 屏幕尺寸: {size}")
        
        # 测试按键支持
        keys = provider.get_available_keys()
        print(f"✓ 支持的按键数量: {len(keys)}")
        
        return True
    except Exception as e:
        print(f"✗ Windows核心输入测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("Puppeteer 输入功能简化测试")
    print("=" * 40)
    
    tests = [
        ("基本导入", test_basic_imports),
        ("输入提供器", test_input_provider),
        ("Windows核心输入", test_windows_core),
    ]
    
    success_count = 0
    for test_name, test_func in tests:
        try:
            if test_func():
                success_count += 1
        except Exception as e:
            print(f"✗ {test_name}测试异常: {e}")
    
    print(f"\n测试结果: {success_count}/{len(tests)} 通过")
    
    if success_count == len(tests):
        print("🎉 所有测试通过！")
        return True
    else:
        print("⚠️ 部分测试失败")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n用户中断测试")
        sys.exit(1)
    except Exception as e:
        print(f"\n测试异常: {e}")
        sys.exit(1)
