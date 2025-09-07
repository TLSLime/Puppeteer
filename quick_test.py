# -*- coding: utf-8 -*-
"""
快速验证脚本 - 验证Puppeteer在Windows上的基本功能
"""

import sys
import os

def test_imports():
    """测试所有模块导入"""
    print("测试模块导入...")
    try:
        from puppeteer import ScreenCapture, VisionProcessor, InputProvider
        from puppeteer import ConfigManager, PuppeteerLogger, PuppeteerController
        from puppeteer.ui import PuppeteerUI
        print("✓ 所有模块导入成功")
        return True
    except Exception as e:
        print(f"✗ 模块导入失败: {e}")
        return False

def test_basic_functionality():
    """测试基本功能"""
    print("\n测试基本功能...")
    try:
        # 测试配置管理
        from puppeteer import ConfigManager
        cm = ConfigManager("test_configs")
        if cm.create_default_profile("test"):
            print("✓ 配置管理功能正常")
        else:
            print("✗ 配置管理功能异常")
            return False
            
        # 测试日志记录
        from puppeteer import PuppeteerLogger
        logger = PuppeteerLogger("test_logs")
        logger.log_system("INFO", "测试消息")
        print("✓ 日志记录功能正常")
        
        # 测试截屏功能
        from puppeteer import ScreenCapture
        with ScreenCapture() as capture:
            img = capture.capture(region=(0, 0, 100, 100))
            print(f"✓ 截屏功能正常 (图像尺寸: {img.shape})")
            
        # 测试输入控制
        from puppeteer import InputProvider
        provider = InputProvider()
        print("✓ 输入控制功能正常")
        
        # 测试视觉处理
        from puppeteer import VisionProcessor
        processor = VisionProcessor()
        print("✓ 视觉处理功能正常")
        
        return True
        
    except Exception as e:
        print(f"✗ 基本功能测试失败: {e}")
        return False

def test_ui_availability():
    """测试UI可用性"""
    print("\n测试UI可用性...")
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # 隐藏窗口
        root.destroy()
        print("✓ Tkinter UI可用")
        return True
    except Exception as e:
        print(f"✗ UI不可用: {e}")
        return False

def cleanup_test_files():
    """清理测试文件"""
    print("\n清理测试文件...")
    try:
        import shutil
        if os.path.exists("test_configs"):
            shutil.rmtree("test_configs")
        if os.path.exists("test_logs"):
            shutil.rmtree("test_logs")
        print("✓ 测试文件清理完成")
    except Exception as e:
        print(f"✗ 清理失败: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("Puppeteer Windows 快速验证测试")
    print("=" * 60)
    
    success_count = 0
    total_tests = 3
    
    # 测试模块导入
    if test_imports():
        success_count += 1
    
    # 测试基本功能
    if test_basic_functionality():
        success_count += 1
    
    # 测试UI可用性
    if test_ui_availability():
        success_count += 1
    
    # 清理测试文件
    cleanup_test_files()
    
    # 输出结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    print(f"通过测试: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("✓ 所有测试通过! Puppeteer 可以在 Windows 上正常运行")
        print("\n使用方法:")
        print("1. 双击 start_puppeteer.bat 启动程序")
        print("2. 或运行: python main.py")
        print("3. 或运行: python main.py --mode cli --profile simple_test")
        return 0
    else:
        print("✗ 部分测试失败，请检查依赖安装")
        print("\n请确保已安装所有依赖:")
        print("pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
