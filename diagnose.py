# -*- coding: utf-8 -*-
"""
问题诊断脚本 - 帮助诊断Puppeteer运行问题
"""

import sys
import os
import subprocess

def check_python_version():
    """检查Python版本"""
    print("1. 检查Python版本...")
    version = sys.version_info
    print(f"   Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 7:
        print("   ✓ Python版本符合要求")
        return True
    else:
        print("   ✗ Python版本过低，需要Python 3.7+")
        return False

def check_dependencies():
    """检查依赖包"""
    print("\n2. 检查依赖包...")
    required_packages = [
        'mss', 'opencv-python', 'numpy', 'Pillow',
        'pyautogui', 'pynput', 'PyYAML', 'pytesseract'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == 'opencv-python':
                import cv2
            elif package == 'Pillow':
                import PIL
            elif package == 'PyYAML':
                import yaml
            else:
                __import__(package.replace('-', '_'))
            print(f"   ✓ {package}")
        except ImportError:
            print(f"   ✗ {package} - 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n   缺少依赖包: {', '.join(missing_packages)}")
        print("   请运行: pip install -r requirements.txt")
        return False
    else:
        print("   ✓ 所有依赖包已安装")
        return True

def check_files():
    """检查必要文件"""
    print("\n3. 检查必要文件...")
    required_files = [
        'main.py',
        'puppeteer/__init__.py',
        'puppeteer/capture.py',
        'puppeteer/vision.py',
        'puppeteer/input_provider.py',
        'puppeteer/config.py',
        'puppeteer/controller.py',
        'puppeteer/logger.py',
        'puppeteer/ui.py',
        'profiles/simple_test.yaml'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✓ {file_path}")
        else:
            print(f"   ✗ {file_path} - 文件不存在")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n   缺少文件: {', '.join(missing_files)}")
        return False
    else:
        print("   ✓ 所有必要文件存在")
        return True

def check_permissions():
    """检查权限"""
    print("\n4. 检查权限...")
    try:
        # 测试文件写入权限
        test_file = "test_permission.tmp"
        with open(test_file, 'w') as f:
            f.write("test")
        os.remove(test_file)
        print("   ✓ 文件写入权限正常")
        
        # 测试截屏权限
        try:
            import mss
            with mss.mss() as sct:
                sct.grab(sct.monitors[1])
            print("   ✓ 截屏权限正常")
        except Exception as e:
            print(f"   ⚠ 截屏权限可能有问题: {e}")
        
        return True
    except Exception as e:
        print(f"   ✗ 权限检查失败: {e}")
        return False

def test_basic_functionality():
    """测试基本功能"""
    print("\n5. 测试基本功能...")
    try:
        # 测试模块导入
        from puppeteer import ConfigManager, PuppeteerLogger
        print("   ✓ 模块导入正常")
        
        # 测试配置加载
        config_manager = ConfigManager("test_diagnose")
        if config_manager.create_default_profile("test"):
            print("   ✓ 配置管理正常")
        else:
            print("   ✗ 配置管理异常")
            return False
        
        # 测试日志记录
        logger = PuppeteerLogger("test_diagnose_logs")
        logger.log_system("INFO", "诊断测试")
        print("   ✓ 日志记录正常")
        
        # 清理测试文件
        import shutil
        if os.path.exists("test_diagnose"):
            shutil.rmtree("test_diagnose")
        if os.path.exists("test_diagnose_logs"):
            shutil.rmtree("test_diagnose_logs")
        
        return True
    except Exception as e:
        print(f"   ✗ 基本功能测试失败: {e}")
        return False

def test_ui():
    """测试UI功能"""
    print("\n6. 测试UI功能...")
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # 隐藏窗口
        root.destroy()
        print("   ✓ Tkinter UI可用")
        return True
    except Exception as e:
        print(f"   ✗ UI测试失败: {e}")
        return False

def provide_solutions():
    """提供解决方案"""
    print("\n" + "="*60)
    print("解决方案建议")
    print("="*60)
    print("1. 如果依赖包缺失:")
    print("   pip install -r requirements.txt")
    print()
    print("2. 如果文件缺失:")
    print("   请重新下载完整的项目文件")
    print()
    print("3. 如果权限问题:")
    print("   请以管理员身份运行命令提示符")
    print()
    print("4. 如果UI问题:")
    print("   请检查是否安装了tkinter: pip install tk")
    print()
    print("5. 推荐启动方式:")
    print("   - 图形界面: python main.py --mode ui")
    print("   - 命令行: python main.py --mode cli --profile simple_test")
    print("   - 批处理: start_puppeteer.bat")
    print()
    print("6. 如果仍有问题:")
    print("   请运行: python quick_test.py")

def main():
    """主函数"""
    print("="*60)
    print("Puppeteer 问题诊断工具")
    print("="*60)
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_files(),
        check_permissions(),
        test_basic_functionality(),
        test_ui()
    ]
    
    passed = sum(checks)
    total = len(checks)
    
    print("\n" + "="*60)
    print("诊断结果")
    print("="*60)
    print(f"通过检查: {passed}/{total}")
    
    if passed == total:
        print("✓ 所有检查通过! 程序应该可以正常运行")
        print("\n推荐启动方式:")
        print("1. 双击 start_puppeteer.bat")
        print("2. 或运行: python main.py --mode ui")
    else:
        print("✗ 发现问题，请查看上面的错误信息")
        provide_solutions()
    
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
