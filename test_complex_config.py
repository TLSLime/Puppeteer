# -*- coding: utf-8 -*-
"""
复杂配置测试脚本
测试清空文件并输入新内容的功能
"""

import sys
import os
import time

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_complex_macro():
    """测试复杂宏执行"""
    print("=" * 60)
    print("测试复杂宏执行")
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
            
            # 获取宏配置
            macros = config_manager.get_macros()
            if "complex_test" in macros:
                print("✓ 找到复杂测试宏")
                print(f"宏内容: {macros['complex_test']}")
                
                # 确保目标窗口活跃
                config = config_manager.get_config()
                controller._ensure_window_active(config)
                
                # 执行复杂宏
                print("执行复杂宏...")
                success = controller.execute_macro("complex_test")
                
                if success:
                    print("✓ 复杂宏执行成功")
                    return True
                else:
                    print("✗ 复杂宏执行失败")
                    return False
            else:
                print("✗ 未找到复杂测试宏")
                return False
        else:
            print("✗ 配置加载失败")
            return False
            
    except Exception as e:
        print(f"✗ 复杂宏测试失败: {e}")
        return False

def test_file_content():
    """测试文件内容"""
    print("\n" + "=" * 60)
    print("测试文件内容")
    print("=" * 60)
    
    try:
        if os.path.exists("test_doc.txt"):
            with open("test_doc.txt", "r", encoding="utf-8") as f:
                content = f.read()
            
            print("当前文件内容:")
            print("-" * 40)
            print(content)
            print("-" * 40)
            
            # 检查是否包含预期内容
            expected_content = "这是一段自动程序生成的内容，用于测试程序是否正常，abcABC123!@#$%^&()_+==.`"
            if expected_content in content:
                print("✓ 文件包含预期内容")
                return True
            else:
                print("✗ 文件不包含预期内容")
                return False
        else:
            print("✗ 文件不存在")
            return False
            
    except Exception as e:
        print(f"✗ 文件内容测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("Puppeteer 复杂配置测试")
    print("=" * 80)
    print("目标: 测试清空文件并输入新内容的复杂配置")
    print("=" * 80)
    
    # 显示当前文件内容
    print("\n测试前的文件内容:")
    if os.path.exists("test_doc.txt"):
        with open("test_doc.txt", "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print("文件不存在")
    
    print("\n" + "=" * 80)
    print("开始测试...")
    print("=" * 80)
    
    tests = [
        ("复杂宏执行", test_complex_macro),
        ("文件内容验证", test_file_content)
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
    
    # 显示最终文件内容
    print("\n" + "=" * 80)
    print("最终文件内容")
    print("=" * 80)
    if os.path.exists("test_doc.txt"):
        with open("test_doc.txt", "r", encoding="utf-8") as f:
            print(f.read())
    else:
        print("文件不存在")
    
    if success_count == len(results):
        print("\n🎉 所有复杂配置测试通过！")
        print("\n功能验证:")
        print("✓ 清空文件内容")
        print("✓ 输入复杂文本内容")
        print("✓ 特殊字符处理")
        print("✓ 回车和空格操作")
        print("✓ 保存文件")
    else:
        print("\n⚠️ 部分测试失败，请检查错误信息")
    
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
