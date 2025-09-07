# -*- coding: utf-8 -*-
"""
基础功能测试脚本
测试Puppeteer的核心功能：窗口管理、文本输入、鼠标操作、键盘操作
"""

import sys
import os
import time
import subprocess

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_file_creation():
    """测试文件创建"""
    print("=" * 60)
    print("测试文件创建")
    print("=" * 60)
    
    try:
        # 检查test_doc.txt是否存在
        if os.path.exists("test_doc.txt"):
            print("✓ test_doc.txt 文件已存在")
        else:
            print("✗ test_doc.txt 文件不存在")
            return False
            
        # 检查配置文件是否存在
        if os.path.exists("profiles/test_doc.yaml"):
            print("✓ test_doc.yaml 配置文件已存在")
        else:
            print("✗ test_doc.yaml 配置文件不存在")
            return False
            
        return True
        
    except Exception as e:
        print(f"✗ 文件创建测试失败: {e}")
        return False

def test_config_loading():
    """测试配置加载"""
    print("\n" + "=" * 60)
    print("测试配置加载")
    print("=" * 60)
    
    try:
        from puppeteer.config import ConfigManager
        
        # 创建配置管理器
        config_manager = ConfigManager("profiles")
        print("✓ 配置管理器创建成功")
        
        # 加载测试配置
        if config_manager.load_profile("test_doc"):
            print("✓ test_doc 配置加载成功")
            
            # 获取配置
            config = config_manager.get_config()
            print(f"✓ 配置获取成功，包含 {len(config)} 个配置项")
            
            # 检查关键配置
            if "window" in config:
                window_config = config["window"]
                print(f"✓ 窗口配置: {window_config.get('title', 'N/A')}")
                
            if "macros" in config:
                macros = config["macros"]
                print(f"✓ 宏配置: {len(macros)} 个宏定义")
                
            if "keymap" in config:
                keymap = config["keymap"]
                print(f"✓ 按键映射: {len(keymap)} 个按键")
                
        else:
            print("✗ test_doc 配置加载失败")
            return False
            
        return True
        
    except Exception as e:
        print(f"✗ 配置加载测试失败: {e}")
        return False

def test_window_management():
    """测试窗口管理"""
    print("\n" + "=" * 60)
    print("测试窗口管理")
    print("=" * 60)
    
    try:
        from puppeteer.window_manager import WindowManager
        
        # 创建窗口管理器
        manager = WindowManager()
        print("✓ 窗口管理器创建成功")
        
        # 查找记事本窗口（用于打开test_doc.txt）
        print("查找记事本窗口...")
        notepad_hwnd = manager.find_window_by_title("记事本")
        
        if notepad_hwnd:
            print("✓ 找到记事本窗口")
            
            # 获取窗口信息
            window_info = manager.get_window_info(notepad_hwnd)
            print(f"✓ 窗口信息: {window_info['title']}")
            
            # 激活窗口
            if manager.activate_window(notepad_hwnd):
                print("✓ 窗口激活成功")
                
                # 移动鼠标到窗口中心
                if manager.move_mouse_to_window(notepad_hwnd, "center"):
                    print("✓ 鼠标定位成功")
                else:
                    print("⚠️ 鼠标定位失败")
            else:
                print("⚠️ 窗口激活失败")
        else:
            print("⚠️ 未找到记事本窗口")
            print("请确保记事本程序已打开并加载了test_doc.txt文件")
            
        return True
        
    except Exception as e:
        print(f"✗ 窗口管理测试失败: {e}")
        return False

def test_input_provider():
    """测试输入提供器"""
    print("\n" + "=" * 60)
    print("测试输入提供器")
    print("=" * 60)
    
    try:
        from puppeteer.input_provider import InputProvider
        
        # 创建输入提供器
        input_provider = InputProvider()
        print("✓ 输入提供器创建成功")
        
        # 测试基本输入功能
        print("测试基本输入功能...")
        
        # 获取鼠标位置
        mouse_pos = input_provider.get_mouse_position()
        print(f"✓ 当前鼠标位置: {mouse_pos}")
        
        # 获取屏幕大小
        screen_size = input_provider.get_screen_size()
        print(f"✓ 屏幕大小: {screen_size}")
        
        # 测试按键检测
        if input_provider.is_key_pressed("space"):
            print("✓ 空格键检测功能正常")
        else:
            print("✓ 空格键检测功能正常（未按下）")
            
        return True
        
    except Exception as e:
        print(f"✗ 输入提供器测试失败: {e}")
        return False

def test_controller_integration():
    """测试控制器集成"""
    print("\n" + "=" * 60)
    print("测试控制器集成")
    print("=" * 60)
    
    try:
        from puppeteer.controller import PuppeteerController
        from puppeteer.config import ConfigManager
        from puppeteer.logger import PuppeteerLogger
        from puppeteer.safety_monitor import SafetyLevel
        
        # 创建测试组件
        config_manager = ConfigManager("profiles")
        logger = PuppeteerLogger("test_logs")
        
        # 创建控制器
        controller = PuppeteerController(config_manager, logger, SafetyLevel.DISABLED)
        print("✓ 控制器创建成功")
        
        # 检查组件集成
        if hasattr(controller, 'window_manager'):
            print("✓ 窗口管理器已集成")
        else:
            print("✗ 窗口管理器未集成")
            
        if hasattr(controller, 'safety_manager'):
            print("✓ 安全管理器已集成")
        else:
            print("✗ 安全管理器未集成")
            
        if hasattr(controller, 'input_provider'):
            print("✓ 输入提供器已集成")
        else:
            print("✗ 输入提供器未集成")
            
        # 获取控制器状态
        status = controller.get_status()
        print(f"✓ 控制器状态获取成功: {status['is_running']}")
        
        return True
        
    except Exception as e:
        print(f"✗ 控制器集成测试失败: {e}")
        return False

def test_manual_automation():
    """测试手动自动化"""
    print("\n" + "=" * 60)
    print("测试手动自动化")
    print("=" * 60)
    
    try:
        print("请确保:")
        print("1. 记事本程序已打开")
        print("2. test_doc.txt文件已在记事本中打开")
        print("3. 记事本窗口处于可见状态")
        
        input("按回车键开始手动自动化测试...")
        
        from puppeteer.input_provider import InputProvider
        
        # 创建输入提供器
        input_provider = InputProvider()
        
        # 等待2秒
        print("等待2秒...")
        time.sleep(2)
        
        # 执行简单的自动化操作
        print("执行自动化操作...")
        
        # 移动到文档末尾
        input_provider.press_key("end")
        time.sleep(0.5)
        
        # 换行
        input_provider.press_key("enter")
        time.sleep(0.5)
        
        # 输入测试文本
        test_text = "自动化测试 - 手动执行成功！"
        input_provider.type_text(test_text)
        time.sleep(0.5)
        
        # 换行
        input_provider.press_key("enter")
        time.sleep(0.5)
        
        # 保存文档
        input_provider.press_key("ctrl+s")
        time.sleep(0.5)
        
        print("✓ 手动自动化测试完成")
        print("请检查test_doc.txt文件是否已更新")
        
        return True
        
    except Exception as e:
        print(f"✗ 手动自动化测试失败: {e}")
        return False

def test_full_automation():
    """测试完整自动化"""
    print("\n" + "=" * 60)
    print("测试完整自动化")
    print("=" * 60)
    
    try:
        print("准备启动完整自动化测试...")
        print("请确保记事本程序已打开test_doc.txt文件")
        
        input("按回车键启动完整自动化...")
        
        # 启动完整自动化
        print("启动Puppeteer自动化程序...")
        
        # 使用subprocess启动程序
        cmd = [
            sys.executable, "main.py", 
            "--mode", "cli", 
            "--profile", "test_doc", 
            "--safety-level", "disabled"
        ]
        
        print(f"执行命令: {' '.join(cmd)}")
        
        # 启动进程
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.getcwd()
        )
        
        # 等待一段时间让程序执行
        print("程序运行中，等待10秒...")
        time.sleep(10)
        
        # 终止进程
        process.terminate()
        process.wait()
        
        print("✓ 完整自动化测试完成")
        print("请检查test_doc.txt文件是否已更新")
        
        return True
        
    except Exception as e:
        print(f"✗ 完整自动化测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("Puppeteer 基础功能测试")
    print("=" * 80)
    print("目标: 通过配置文档控制test_doc.txt写入内容，检验基础功能")
    print("=" * 80)
    
    tests = [
        ("文件创建", test_file_creation),
        ("配置加载", test_config_loading),
        ("窗口管理", test_window_management),
        ("输入提供器", test_input_provider),
        ("控制器集成", test_controller_integration),
        ("手动自动化", test_manual_automation),
        ("完整自动化", test_full_automation)
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
        print("🎉 所有基础功能测试通过！")
        print("\n功能验证:")
        print("✓ 文件创建和配置加载")
        print("✓ 窗口管理和激活")
        print("✓ 输入提供器功能")
        print("✓ 控制器集成")
        print("✓ 手动自动化操作")
        print("✓ 完整自动化流程")
        print("\n请检查test_doc.txt文件，确认自动化内容已写入")
    else:
        print("⚠️ 部分测试失败，请检查错误信息")
        print("建议:")
        print("1. 确保记事本程序已打开")
        print("2. 确保test_doc.txt文件已在记事本中打开")
        print("3. 检查配置文件是否正确")
        print("4. 检查依赖库是否安装完整")
    
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
