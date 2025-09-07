# -*- coding: utf-8 -*-
"""
依赖安装脚本 - 安装Puppeteer所需的所有依赖
支持Windows系统，自动检测并安装缺失的包
"""

import subprocess
import sys
import os
import platform
from typing import List, Dict, Tuple


def run_command(command: str, description: str = "") -> Tuple[bool, str]:
    """
    运行命令并返回结果
    
    Args:
        command: 要执行的命令
        description: 命令描述
        
    Returns:
        (是否成功, 输出信息)
    """
    try:
        print(f"执行: {description or command}")
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            print(f"✓ 成功: {description or command}")
            return True, result.stdout
        else:
            print(f"✗ 失败: {description or command}")
            print(f"错误: {result.stderr}")
            return False, result.stderr
            
    except Exception as e:
        print(f"✗ 异常: {description or command} - {e}")
        return False, str(e)


def check_python_version() -> bool:
    """检查Python版本"""
    version = sys.version_info
    print(f"当前Python版本: {version.major}.{version.minor}.{version.micro}")
    print(f"Python安装路径: {sys.executable}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ 需要Python 3.7或更高版本")
        return False
    
    print("✓ Python版本符合要求（支持Python 3.7+）")
    return True


def check_pip() -> bool:
    """检查pip是否可用"""
    success, output = run_command("pip --version", "检查pip版本")
    if success:
        print(f"✓ pip可用: {output.strip()}")
        return True
    else:
        print("❌ pip不可用，尝试使用python -m pip")
        success, output = run_command("python -m pip --version", "检查python -m pip")
        if success:
            print(f"✓ python -m pip可用: {output.strip()}")
            return True
        else:
            print("❌ pip完全不可用")
            return False


def install_package(package: str, description: str = "") -> bool:
    """
    安装单个包
    
    Args:
        package: 包名
        description: 包描述
        
    Returns:
        是否安装成功
    """
    print(f"\n安装包: {package} ({description})")
    
    # 尝试使用pip安装
    success, _ = run_command(f"pip install {package}", f"安装{package}")
    if success:
        return True
    
    # 如果失败，尝试使用python -m pip
    success, _ = run_command(f"python -m pip install {package}", f"使用python -m pip安装{package}")
    if success:
        return True
    
    # 如果还是失败，尝试升级pip后重试
    print(f"尝试升级pip后重新安装{package}")
    run_command("python -m pip install --upgrade pip", "升级pip")
    success, _ = run_command(f"python -m pip install {package}", f"重新安装{package}")
    
    return success


def install_requirements() -> bool:
    """安装requirements.txt中的依赖"""
    print("\n=== 安装requirements.txt依赖 ===")
    
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt文件不存在")
        return False
    
    # 读取requirements.txt
    with open("requirements.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    packages = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            packages.append(line)
    
    print(f"找到{len(packages)}个包需要安装")
    
    success_count = 0
    failed_packages = []
    
    for package in packages:
        if install_package(package):
            success_count += 1
        else:
            failed_packages.append(package)
    
    print(f"\n安装结果: {success_count}/{len(packages)} 成功")
    
    if failed_packages:
        print("失败的包:")
        for package in failed_packages:
            print(f"  - {package}")
        return False
    
    return True


def install_windows_specific() -> bool:
    """安装Windows特定依赖"""
    print("\n=== 安装Windows特定依赖 ===")
    
    if platform.system() != "Windows":
        print("非Windows系统，跳过Windows特定依赖")
        return True
    
    windows_packages = [
        ("pywin32", "Windows API支持"),
        ("wmi", "Windows管理接口"),
        ("psutil", "系统进程管理"),
    ]
    
    success_count = 0
    for package, description in windows_packages:
        if install_package(package, description):
            success_count += 1
    
    print(f"Windows特定依赖安装结果: {success_count}/{len(windows_packages)} 成功")
    return success_count == len(windows_packages)


def test_imports() -> bool:
    """测试关键模块导入"""
    print("\n=== 测试模块导入 ===")
    
    test_modules = [
        ("mss", "屏幕截图"),
        ("cv2", "OpenCV图像处理"),
        ("numpy", "数值计算"),
        ("PIL", "图像处理"),
        ("pyautogui", "自动化输入"),
        ("yaml", "YAML配置"),
        ("tkinter", "GUI界面"),
    ]
    
    # Windows特定模块
    if platform.system() == "Windows":
        test_modules.extend([
            ("win32api", "Windows API"),
            ("psutil", "系统信息"),
        ])
    
    success_count = 0
    failed_modules = []
    
    for module, description in test_modules:
        try:
            __import__(module)
            print(f"✓ {module} ({description})")
            success_count += 1
        except ImportError as e:
            print(f"✗ {module} ({description}) - {e}")
            failed_modules.append(module)
    
    print(f"\n导入测试结果: {success_count}/{len(test_modules)} 成功")
    
    if failed_modules:
        print("导入失败的模块:")
        for module in failed_modules:
            print(f"  - {module}")
        return False
    
    return True


def main():
    """主函数"""
    print("=" * 60)
    print("Puppeteer 依赖安装脚本")
    print("=" * 60)
    
    # 检查Python版本
    if not check_python_version():
        return False
    
    # 检查pip
    if not check_pip():
        return False
    
    # 安装requirements.txt依赖
    if not install_requirements():
        print("❌ requirements.txt依赖安装失败")
        return False
    
    # 安装Windows特定依赖
    if not install_windows_specific():
        print("⚠️ Windows特定依赖安装部分失败，但可以继续")
    
    # 测试导入
    if not test_imports():
        print("❌ 模块导入测试失败")
        return False
    
    print("\n" + "=" * 60)
    print("✓ 所有依赖安装完成！")
    print("现在可以运行Puppeteer程序了")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ 安装过程中遇到问题，请检查错误信息")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n用户中断安装")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 安装过程中发生异常: {e}")
        sys.exit(1)
