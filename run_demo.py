# -*- coding: utf-8 -*-
"""
Puppeteer 演示脚本
展示完整的自动化流程：截屏 -> 识别 -> 决策 -> 动作
"""

import sys
import os
import time
import numpy as np
import cv2

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from puppeteer import ScreenCapture, VisionProcessor, InputProvider, ConfigManager, PuppeteerLogger


def create_demo_template():
    """创建演示用的模板图片"""
    print("创建演示模板...")
    
    # 确保assets目录存在
    os.makedirs("assets", exist_ok=True)
    
    # 创建一个简单的演示模板
    template = np.ones((50, 100), dtype=np.uint8) * 255
    cv2.rectangle(template, (10, 10), (90, 40), (0, 0, 0), -1)
    cv2.putText(template, "DEMO", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    cv2.imwrite("assets/demo_template.png", template)
    print("演示模板已创建: assets/demo_template.png")


def run_demo():
    """运行演示"""
    print("=" * 60)
    print("Puppeteer 演示程序")
    print("=" * 60)
    
    try:
        # 1. 创建演示模板
        create_demo_template()
        
        # 2. 初始化组件
        print("初始化组件...")
        config_manager = ConfigManager("demo_profiles")
        logger = PuppeteerLogger("demo_logs")
        
        # 创建演示配置
        demo_config = {
            "profile": "demo",
            "description": "演示配置",
            "screen_region": [0, 0, 800, 600],
            "keymap": {
                "attack": "q",
                "jump": "space"
            },
            "templates": {
                "enemies": ["demo_template.png"],
                "items": [],
                "ui_elements": []
            },
            "rois": {
                "demo_template.png": [100, 100, 600, 400]
            },
            "detection": {
                "scene": "demo",
                "templates": {
                    "enemies": ["demo_template.png"],
                    "items": [],
                    "ui_elements": []
                },
                "self_status": {}
            },
            "macros": {
                "demo_combo": ["attack", "jump", "attack"]
            },
            "humanize": {
                "enabled": True,
                "mouse_delay_range": [50, 150],
                "key_delay_range": [80, 140]
            },
            "controller": {
                "fps_limit": 5,
                "action_cooldown": 0.2,
                "confidence_threshold": 0.7
            }
        }
        
        # 保存演示配置
        config_manager.save_profile("demo", demo_config)
        config_manager.load_profile("demo")
        
        # 3. 初始化视觉处理器
        vision = VisionProcessor(confidence_threshold=0.7)
        vision.load_template("demo_template", "assets/demo_template.png")
        
        # 4. 初始化输入提供器
        input_provider = InputProvider(humanize_enabled=True)
        
        # 5. 演示循环
        print("开始演示循环...")
        print("按 Ctrl+C 停止演示")
        
        cycle_count = 0
        max_cycles = 10  # 最多运行10个循环
        
        with ScreenCapture() as capture:
            while cycle_count < max_cycles:
                try:
                    print(f"\n--- 循环 {cycle_count + 1} ---")
                    
                    # 截屏
                    print("1. 截屏...")
                    image = capture.capture(region=[0, 0, 800, 600])
                    print(f"   截屏完成，图像尺寸: {image.shape}")
                    
                    # 视觉识别
                    print("2. 视觉识别...")
                    detection_config = config_manager.get_detection_config()
                    observation = vision.process_observation(image, detection_config)
                    
                    enemies = observation.get("enemies", [])
                    print(f"   检测到 {len(enemies)} 个目标")
                    
                    # 记录观察日志
                    logger.log_observation(observation)
                    
                    # 简单决策：如果检测到目标就执行动作
                    if enemies:
                        print("3. 执行动作...")
                        action = {
                            "type": "press",
                            "key": "q",
                            "humanize": {"delay_ms": [100, 200]}
                        }
                        
                        result = input_provider.execute_action(action)
                        logger.log_action(action, result)
                        
                        if result["success"]:
                            print("   动作执行成功")
                        else:
                            print(f"   动作执行失败: {result.get('error', 'unknown')}")
                    else:
                        print("3. 无目标，跳过动作")
                    
                    # 等待一段时间
                    time.sleep(1.0)
                    cycle_count += 1
                    
                except KeyboardInterrupt:
                    print("\n收到停止信号...")
                    break
                except Exception as e:
                    print(f"循环异常: {e}")
                    logger.log_error(e, {"cycle": cycle_count})
                    time.sleep(1.0)
                    cycle_count += 1
        
        print("\n演示完成!")
        
        # 6. 显示统计信息
        recent_logs = logger.get_recent_logs(20)
        action_logs = [log for log in recent_logs if log.get("type") == "action"]
        observation_logs = [log for log in recent_logs if log.get("type") == "observation"]
        
        print(f"总循环数: {cycle_count}")
        print(f"动作执行次数: {len(action_logs)}")
        print(f"观察记录次数: {len(observation_logs)}")
        
        # 7. 清理演示文件
        print("\n清理演示文件...")
        import shutil
        
        if os.path.exists("demo_profiles"):
            shutil.rmtree("demo_profiles")
        if os.path.exists("demo_logs"):
            shutil.rmtree("demo_logs")
        if os.path.exists("assets/demo_template.png"):
            os.remove("assets/demo_template.png")
            
        print("演示文件已清理")
        
    except Exception as e:
        print(f"演示失败: {e}")
        return 1
        
    return 0


if __name__ == "__main__":
    print("Puppeteer 演示程序")
    print("这个演示将展示完整的自动化流程")
    print("注意：演示过程中会执行实际的鼠标和键盘操作")
    
    response = input("是否继续？(y/N): ").strip().lower()
    if response in ['y', 'yes']:
        sys.exit(run_demo())
    else:
        print("演示已取消")
        sys.exit(0)
