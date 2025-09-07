# -*- coding: utf-8 -*-
"""
Puppeteer 主程序入口
启动用户界面或命令行模式
"""

import sys
import os
import argparse
import yaml
import time
from puppeteer import PuppeteerController, ConfigManager, PuppeteerLogger
from puppeteer.ui import PuppeteerUI
from puppeteer.safety_monitor import SafetyLevel


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Puppeteer - 桌面程序自动化操控系统")
    parser.add_argument("--mode", choices=["ui", "cli"], default="ui", 
                       help="运行模式: ui(图形界面) 或 cli(命令行)")
    parser.add_argument("--profile", type=str, help="配置文件名称")
    parser.add_argument("--config-dir", type=str, default="profiles", 
                       help="配置文件目录")
    parser.add_argument("--log-dir", type=str, default="logs", 
                       help="日志目录")
    parser.add_argument("--log-format", choices=["jsonl", "text"], default="jsonl",
                       help="日志格式")
    parser.add_argument("--safety-level", choices=["disabled", "low", "medium", "high"], 
                       help="安全级别")
    parser.add_argument("--safety-config", type=str, default="safety_config.yaml",
                       help="安全配置文件路径")
    parser.add_argument("--non-interactive", action="store_true",
                       help="非交互模式，不等待用户输入")
    parser.add_argument("--auto-exit", action="store_true",
                       help="自动退出模式，执行完成后自动退出")
    
    args = parser.parse_args()
    
    # 加载安全配置
    safety_level = SafetyLevel.DISABLED  # 默认值
    if args.safety_level:
        safety_level = SafetyLevel(args.safety_level)
    elif os.path.exists(args.safety_config):
        try:
            with open(args.safety_config, 'r', encoding='utf-8') as f:
                safety_config = yaml.safe_load(f)
                if 'safety_level' in safety_config:
                    safety_level = SafetyLevel(safety_config['safety_level'])
        except Exception as e:
            print(f"加载安全配置失败: {e}")
            print("使用默认安全级别: disabled")
    
    print(f"安全级别: {safety_level.value}")
    
    try:
        if args.mode == "ui":
            # 图形界面模式
            print("启动图形界面...")
            app = PuppeteerUI()
            app.run()
            
        elif args.mode == "cli":
            # 命令行模式
            if not args.profile:
                print("错误: 命令行模式需要指定配置文件")
                print("使用 --profile <配置名> 参数")
                return 1
                
            print(f"启动命令行模式，配置文件: {args.profile}")
            
            # 初始化组件
            config_manager = ConfigManager(args.config_dir)
            logger = PuppeteerLogger(args.log_dir, args.log_format)
            controller = PuppeteerController(config_manager, logger, safety_level)
            
            # 启动控制器
            if controller.start(args.profile):
                if args.non_interactive:
                    print("控制器启动成功，非交互模式运行")
                    # 非交互模式：等待一段时间后自动停止
                    if args.auto_exit:
                        print("自动退出模式，等待10秒后自动停止...")
                        time.sleep(10)
                        controller.stop()
                    else:
                        # 保持运行直到被外部停止
                        try:
                            while controller.is_running:
                                time.sleep(1)
                        except KeyboardInterrupt:
                            print("\n用户中断，正在停止...")
                        finally:
                            controller.stop()
                else:
                    print("控制器启动成功，按 Ctrl+C 停止")
                    try:
                        # 保持运行
                        while controller.is_running:
                            time.sleep(1)
                    except KeyboardInterrupt:
                        print("\n收到停止信号...")
                        controller.stop()
                        print("控制器已停止")
            else:
                print("控制器启动失败")
                return 1
                
    except Exception as e:
        print(f"程序运行失败: {e}")
        return 1
        
    return 0


if __name__ == "__main__":
    sys.exit(main())
