# -*- coding: utf-8 -*-
"""
模块测试脚本
用于测试各个模块的基本功能
"""

import sys
import os
import time

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from puppeteer.capture import ScreenCapture
from puppeteer.vision import VisionProcessor
from puppeteer.input_provider import InputProvider
from puppeteer.config import ConfigManager
from puppeteer.logger import PuppeteerLogger


def test_capture():
    """测试截屏模块"""
    print("=" * 50)
    print("测试截屏模块")
    print("=" * 50)
    
    try:
        with ScreenCapture() as capture:
            # 测试全屏截取
            print("测试全屏截取...")
            img = capture.capture()
            print(f"全屏图像尺寸: {img.shape}")
            
            # 测试区域截取
            print("测试区域截取...")
            region_img = capture.capture(region=(100, 100, 400, 300))
            print(f"区域图像尺寸: {region_img.shape}")
            
            # 测试灰度图
            print("测试灰度图...")
            gray_img = capture.capture(grayscale=True)
            print(f"灰度图像尺寸: {gray_img.shape}")
            
            # 获取屏幕尺寸
            width, height = capture.get_screen_size()
            print(f"屏幕尺寸: {width}x{height}")
            
        print("截屏模块测试通过!")
        return True
        
    except Exception as e:
        print(f"截屏模块测试失败: {e}")
        return False


def test_vision():
    """测试视觉识别模块"""
    print("=" * 50)
    print("测试视觉识别模块")
    print("=" * 50)
    
    try:
        processor = VisionProcessor(confidence_threshold=0.7)
        
        # 创建测试图像
        import numpy as np
        import cv2
        
        test_image = np.zeros((400, 600, 3), dtype=np.uint8)
        cv2.rectangle(test_image, (100, 100), (200, 150), (255, 255, 255), -1)
        
        # 创建测试模板
        template = np.ones((50, 100), dtype=np.uint8) * 255
        
        # 保存测试模板
        os.makedirs("test_assets", exist_ok=True)
        cv2.imwrite("test_assets/test_template.png", template)
        
        # 加载模板
        if processor.load_template("test_template", "test_assets/test_template.png"):
            print("模板加载成功")
            
            # 测试匹配
            matches = processor.match_template(test_image, "test_template")
            print(f"找到 {len(matches)} 个匹配")
            
            for match in matches:
                print(f"位置: {match['position']}, 置信度: {match['confidence']:.3f}")
                
        # 清理测试文件
        if os.path.exists("test_assets/test_template.png"):
            os.remove("test_assets/test_template.png")
            os.rmdir("test_assets")
            
        print("视觉识别模块测试通过!")
        return True
        
    except Exception as e:
        print(f"视觉识别模块测试失败: {e}")
        return False


def test_input():
    """测试输入控制模块"""
    print("=" * 50)
    print("测试输入控制模块")
    print("=" * 50)
    
    try:
        provider = InputProvider(humanize_enabled=True)
        
        # 测试鼠标移动（移动到屏幕中央）
        print("测试鼠标移动...")
        success = provider.move_mouse(400, 300)
        print(f"鼠标移动: {'成功' if success else '失败'}")
        
        # 测试按键
        print("测试按键...")
        success = provider.press_key("space")
        print(f"按键: {'成功' if success else '失败'}")
        
        # 测试动作对象
        print("测试动作对象...")
        action = {
            "type": "press",
            "key": "q",
            "humanize": {"delay_ms": [50, 100]}
        }
        result = provider.execute_action(action)
        print(f"动作执行: {result}")
        
        print("输入控制模块测试通过!")
        return True
        
    except Exception as e:
        print(f"输入控制模块测试失败: {e}")
        return False


def test_config():
    """测试配置管理模块"""
    print("=" * 50)
    print("测试配置管理模块")
    print("=" * 50)
    
    try:
        manager = ConfigManager("test_profiles")
        
        # 创建测试配置
        test_profile = "test_game"
        if manager.create_default_profile(test_profile, [0, 0, 800, 600]):
            print("创建测试配置成功")
            
            # 加载配置
            if manager.load_profile(test_profile):
                print("加载配置成功")
                
                # 测试各种配置获取
                screen_region = manager.get_screen_region()
                print(f"屏幕区域: {screen_region}")
                
                keymap = manager.get_keymap()
                print(f"按键映射: {keymap}")
                
                templates = manager.get_templates()
                print(f"模板配置: {templates}")
                
                detection_config = manager.get_detection_config()
                print(f"检测配置: {detection_config}")
                
            # 列出配置文件
            profiles = manager.list_profiles()
            print(f"可用配置: {profiles}")
            
        # 清理测试文件
        import shutil
        if os.path.exists("test_profiles"):
            shutil.rmtree("test_profiles")
            
        print("配置管理模块测试通过!")
        return True
        
    except Exception as e:
        print(f"配置管理模块测试失败: {e}")
        return False


def test_logger():
    """测试日志记录模块"""
    print("=" * 50)
    print("测试日志记录模块")
    print("=" * 50)
    
    try:
        # 测试JSONL格式
        logger = PuppeteerLogger("test_logs", "jsonl")
        
        # 记录各种类型的日志
        logger.log_system("INFO", "系统启动")
        
        action = {"type": "press", "key": "q"}
        result = {"success": True, "timestamp": time.time()}
        logger.log_action(action, result)
        
        observation = {
            "timestamp": time.time(),
            "scene": "test",
            "enemies": [{"id": "e1", "pos": [100, 200], "confidence": 0.9}],
            "items": []
        }
        logger.log_observation(observation)
        
        logger.log_error(Exception("测试错误"), {"context": "test"})
        
        # 获取最近日志
        recent_logs = logger.get_recent_logs(5)
        print(f"最近日志数量: {len(recent_logs)}")
        
        # 导出日志
        logger.export_session_logs("test_export.json")
        
        # 清理测试文件
        import shutil
        if os.path.exists("test_logs"):
            shutil.rmtree("test_logs")
        if os.path.exists("test_export.json"):
            os.remove("test_export.json")
            
        print("日志记录模块测试通过!")
        return True
        
    except Exception as e:
        print(f"日志记录模块测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("Puppeteer 模块测试开始")
    print("=" * 60)
    
    test_results = []
    
    # 运行所有测试
    test_results.append(("截屏模块", test_capture()))
    test_results.append(("视觉识别模块", test_vision()))
    test_results.append(("输入控制模块", test_input()))
    test_results.append(("配置管理模块", test_config()))
    test_results.append(("日志记录模块", test_logger()))
    
    # 输出测试结果
    print("=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for module_name, result in test_results:
        status = "通过" if result else "失败"
        print(f"{module_name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("=" * 60)
    print(f"总计: {passed} 个模块通过, {failed} 个模块失败")
    
    if failed == 0:
        print("所有模块测试通过! 系统可以正常使用。")
        return 0
    else:
        print("部分模块测试失败，请检查相关依赖和配置。")
        return 1


if __name__ == "__main__":
    sys.exit(main())
