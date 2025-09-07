# -*- coding: utf-8 -*-
"""
主控制器模块 - 协调各个模块的主循环
负责截屏、识别、决策、动作执行的完整流程
"""

import time
import threading
import os
from typing import Dict, Any, Optional, List
from .capture import ScreenCapture
from .vision import VisionProcessor
from .input_provider import InputProvider
from .config import ConfigManager
from .logger import PuppeteerLogger
from .safety_monitor import SafetyManager, SafetyLevel, SafetyEvent
from .window_manager import WindowManager
from .dialog_handler import DialogHandler


class PuppeteerController:
    """Puppeteer主控制器，协调各个模块工作"""
    
    def __init__(self, config_manager: ConfigManager, logger: PuppeteerLogger, 
                 safety_level: SafetyLevel = SafetyLevel.DISABLED):
        """
        初始化控制器
        
        Args:
            config_manager: 配置管理器
            logger: 日志记录器
            safety_level: 安全级别
        """
        self.config_manager = config_manager
        self.logger = logger
        
        # 核心模块
        self.capture = None
        self.vision = VisionProcessor()
        self.input_provider = InputProvider()
        
        # 安全系统
        self.safety_manager = SafetyManager(safety_level)
        
        # 窗口管理
        self.window_manager = WindowManager()
        
        # 对话框处理（稍后在start方法中初始化）
        self.dialog_handler = None
        
        # 控制状态
        self.is_running = False
        self.is_paused = False
        self.current_profile = None
        self.main_thread = None
        
        # 运行参数
        self.fps_limit = 10
        self.action_cooldown = 0.1
        self.confidence_threshold = 0.8
        
        # 统计信息
        self.stats = {
            "start_time": 0,
            "actions_executed": 0,
            "observations_made": 0,
            "errors_count": 0
        }
        
    def start(self, profile_name: str) -> bool:
        """
        启动控制器
        
        Args:
            profile_name: 配置文件名
            
        Returns:
            是否启动成功
        """
        if self.is_running:
            print("控制器已在运行中")
            return False
            
        try:
            # 加载配置
            if not self.config_manager.load_profile(profile_name):
                print(f"加载配置失败: {profile_name}")
                return False
                
            self.current_profile = profile_name
            config = self.config_manager.get_config()
            
            # 应用配置参数
            self._apply_config(config)
            
            # 初始化截屏器
            self.capture = ScreenCapture()
            self.capture.set_fps_limit(self.fps_limit)
            
            # 启动安全监控
            self.safety_manager.start_safety_monitoring(self._safety_callback)
            
            # 激活目标窗口
            self._activate_target_window(config)
            
            # 加载模板
            self._load_templates(config)
            
            # 设置输入提供器
            self._setup_input_provider(config)
            
            # 记录会话开始
            self.logger.log_session_start(profile_name, config)
            self.stats["start_time"] = time.time()
            
            # 初始化对话框处理器
            print("🔧 初始化对话框处理器...")
            dialog_config = config.get("dialog_handler", {})
            self.dialog_handler = DialogHandler(dialog_config)
            self.dialog_handler.set_dialog_callback(self._dialog_callback)
            print("✅ 对话框处理器初始化完成")
            
            # 显示用户提醒
            self._show_user_reminder()
            
            # 启动对话框检测
            print("🔍 启动对话框检测...")
            self.dialog_handler.start_dialog_detection()
            print("✅ 对话框检测已启动")
            
            # 启动自动化
            print("🚀 启动自动化系统...")
            self.safety_manager.start_automation()
            print("✅ 自动化系统已启动")
            
            # 自动执行宏（如果配置了）
            print("📋 准备执行自动宏...")
            self._auto_execute_macro(config)
            
            # 启动主循环
            self.is_running = True
            self.is_paused = False
            self.main_thread = threading.Thread(target=self._main_loop, daemon=True)
            self.main_thread.start()
            print("✅ 主循环已启动")
            
            print(f"控制器启动成功: {profile_name}")
            return True
            
        except Exception as e:
            print(f"启动控制器失败: {e}")
            self.logger.log_error(e, {"action": "start", "profile": profile_name})
            return False
            
    def stop(self):
        """停止控制器"""
        if not self.is_running:
            print("控制器未在运行")
            return
            
        try:
            self.is_running = False
            
            # 等待主线程结束
            if self.main_thread and self.main_thread.is_alive():
                self.main_thread.join(timeout=2.0)
                
            # 记录会话结束
            if self.stats["start_time"] > 0:
                duration = time.time() - self.stats["start_time"]
                self.logger.log_session_end(self.current_profile, duration, self.stats)
                
            # 停止对话框检测
            if self.dialog_handler:
                print("🔍 停止对话框检测...")
                try:
                    self.dialog_handler.stop_dialog_detection()
                    print("✅ 对话框检测已停止")
                except Exception as e:
                    print(f"⚠️ 停止对话框检测时出现异常: {e}")
            
            # 停止安全监控
            print("🛡️ 停止安全监控...")
            try:
                self.safety_manager.stop_safety_monitoring()
                print("✅ 安全监控已停止")
            except Exception as e:
                print(f"⚠️ 停止安全监控时出现异常: {e}")
            
            # 清理资源
            if self.capture:
                self.capture = None
                
            print("控制器已停止")
            
        except Exception as e:
            print(f"停止控制器失败: {e}")
            self.logger.log_error(e, {"action": "stop"})
            
    def pause(self):
        """暂停控制器"""
        if self.is_running:
            self.is_paused = True
            print("控制器已暂停")
            
    def resume(self):
        """恢复控制器"""
        if self.is_running and self.is_paused:
            self.is_paused = False
            print("控制器已恢复")
            
    def _apply_config(self, config: Dict[str, Any]):
        """应用配置参数"""
        controller_config = config.get("controller", {})
        self.fps_limit = controller_config.get("fps_limit", 10)
        self.action_cooldown = controller_config.get("action_cooldown", 0.1)
        self.confidence_threshold = controller_config.get("confidence_threshold", 0.8)
        
        # 设置视觉处理器
        self.vision.set_confidence_threshold(self.confidence_threshold)
        
        # 设置输入提供器
        self.input_provider.set_cooldown(self.action_cooldown)
        
    def _load_templates(self, config: Dict[str, Any]):
        """加载模板"""
        templates_config = config.get("templates", {})
        template_dir = "assets"  # 默认模板目录
        
        # 加载所有模板
        for category, template_list in templates_config.items():
            for template_name in template_list:
                template_path = os.path.join(template_dir, template_name)
                self.vision.load_template(template_name, template_path)
                
    def _setup_input_provider(self, config: Dict[str, Any]):
        """设置输入提供器"""
        humanize_config = config.get("humanize", {})
        if humanize_config:
            self.input_provider.set_humanize_config(humanize_config)
            
    def _main_loop(self):
        """主循环"""
        print("🔄 主循环开始")
        loop_count = 0
        
        try:
            while self.is_running:
                loop_count += 1
                
                if self.is_paused:
                    print("⏸️ 主循环已暂停")
                    time.sleep(0.1)
                    continue
                    
                # 检查安全状态
                try:
                    if not self.safety_manager.is_automation_running():
                        print("🛡️ 检测到安全事件，停止自动化")
                        self.is_running = False
                        break
                except Exception as e:
                    print(f"⚠️ 检查安全状态异常: {e}")
                    
                # 执行一个循环
                try:
                    self._execute_cycle()
                except Exception as e:
                    print(f"⚠️ 执行循环异常: {e}")
                    self.stats["errors_count"] += 1
                
                # 控制帧率，但确保最小响应性
                sleep_time = max(0.01, 1.0 / self.fps_limit)
                time.sleep(sleep_time)
                
                # 每100次循环显示一次状态（可选）
                if loop_count % 100 == 0:
                    print(f"🔄 主循环运行中... (第{loop_count}次)")
                
        except KeyboardInterrupt:
            print("🔄 主循环被用户中断")
        except Exception as e:
            print(f"❌ 主循环异常: {e}")
            self.logger.log_error(e, {"action": "main_loop"})
            self.stats["errors_count"] += 1
            
        print("🔄 主循环结束")
        
    def _execute_cycle(self):
        """执行一个完整的循环：截屏 -> 识别 -> 决策 -> 动作"""
        try:
            # 1. 截屏
            if not self.capture:
                return
                
            with self.capture as capture:
                screen_region = self.config_manager.get_screen_region()
                image = capture.capture(region=screen_region, grayscale=False)
                
            # 2. 视觉识别
            detection_config = self.config_manager.get_detection_config()
            if not detection_config:
                return
                
            observation = self.vision.process_observation(image, detection_config)
            self.stats["observations_made"] += 1
            
            # 记录观察日志
            self.logger.log_observation(observation)
            
            # 3. 决策和动作执行
            self._make_decision_and_act(observation)
            
        except Exception as e:
            print(f"执行循环异常: {e}")
            self.logger.log_error(e, {"action": "execute_cycle"})
            self.stats["errors_count"] += 1
            
    def _make_decision_and_act(self, observation: Dict[str, Any]):
        """基于观察做出决策并执行动作"""
        try:
            # 简单的决策逻辑：检测到敌人就攻击
            enemies = observation.get("enemies", [])
            if enemies:
                # 找到最近的敌人
                closest_enemy = min(enemies, key=lambda e: e["confidence"], reverse=True)
                
                # 执行攻击动作
                action = {
                    "type": "press",
                    "key": "q",  # 默认攻击键
                    "humanize": {"delay_ms": [80, 140]}
                }
                
                # 获取配置中的攻击键
                keymap = self.config_manager.get_keymap()
                if keymap and "attack" in keymap:
                    action["key"] = keymap["attack"]
                    
                # 执行动作
                result = self.input_provider.execute_action(action)
                self.stats["actions_executed"] += 1
                
                # 记录动作日志
                self.logger.log_action(action, result)
                
                if result["success"]:
                    print(f"执行攻击动作: {action['key']}")
                else:
                    print(f"攻击动作失败: {result.get('error', 'unknown')}")
                    
        except Exception as e:
            print(f"决策执行异常: {e}")
            self.logger.log_error(e, {"action": "make_decision"})
            self.stats["errors_count"] += 1
            
    def get_status(self) -> Dict[str, Any]:
        """获取控制器状态"""
        return {
            "is_running": self.is_running,
            "is_paused": self.is_paused,
            "current_profile": self.current_profile,
            "stats": self.stats.copy(),
            "loaded_templates": self.vision.get_loaded_templates() if self.vision else [],
            "safety_level": self.safety_manager.safety_level.value,
            "safety_stats": self.safety_manager.get_safety_stats()
        }
        
    def execute_macro(self, macro_name: str) -> bool:
        """
        执行宏操作
        
        Args:
            macro_name: 宏名称
            
        Returns:
            是否执行成功
        """
        try:
            macros = self.config_manager.get_macros()
            if not macros or macro_name not in macros:
                print(f"宏不存在: {macro_name}")
                return False
                
            # 确保目标窗口处于活跃状态
            config = self.config_manager.get_config()
            self._ensure_window_active(config)
                
            macro_keys = macros[macro_name]
            keymap = self.config_manager.get_keymap()
            
            # 转换为动作序列
            actions = []
            for macro_item in macro_keys:
                if isinstance(macro_item, str):
                    # 解析宏项
                    if macro_item.startswith("type: "):
                        # 文本输入动作
                        text = macro_item[6:]  # 移除 "type: " 前缀
                        action = {
                            "type": "type",
                            "text": text,
                            "humanize": {"delay_ms": [50, 100]}
                        }
                        actions.append(action)
                    elif macro_item.startswith("key: "):
                        # 按键动作
                        key_name = macro_item[5:]  # 移除 "key: " 前缀
                        if keymap and key_name in keymap:
                            action = {
                                "type": "press",
                                "key": keymap[key_name],
                                "humanize": {"delay_ms": [50, 100]}
                            }
                            actions.append(action)
                        else:
                            # 直接使用按键名称
                            action = {
                                "type": "press",
                                "key": key_name,
                                "humanize": {"delay_ms": [50, 100]}
                            }
                            actions.append(action)
                    else:
                        # 默认作为按键处理
                        if keymap and macro_item in keymap:
                            action = {
                                "type": "press",
                                "key": keymap[macro_item],
                                "humanize": {"delay_ms": [50, 100]}
                            }
                            actions.append(action)
                    
            # 执行宏
            results = self.input_provider.execute_macro(actions)
            
            # 记录日志
            for i, (action, result) in enumerate(zip(actions, results)):
                self.logger.log_action(action, result)
                self.stats["actions_executed"] += 1
                
            success_count = sum(1 for r in results if r["success"])
            print(f"执行宏 {macro_name}: {success_count}/{len(results)} 成功")
            
            return success_count == len(results)
            
        except Exception as e:
            print(f"执行宏失败: {e}")
            self.logger.log_error(e, {"action": "execute_macro", "macro": macro_name})
            return False
            
    def _safety_callback(self, event_type: SafetyEvent, data: Dict[str, Any]):
        """安全事件回调函数"""
        try:
            # 记录安全事件
            self.logger.log_safety_event(event_type.value, data)
            
            # 根据事件类型处理
            if event_type == SafetyEvent.EMERGENCY_STOP:
                print(f"紧急停止触发: {data.get('key', 'unknown')}")
                self.safety_manager.stop_automation("emergency_stop")
                # 自动恢复准备状态
                self._auto_recovery()
            elif event_type in [SafetyEvent.MOUSE_MOVE, SafetyEvent.KEYBOARD_INPUT]:
                print(f"用户操作检测: {event_type.value}")
                self.safety_manager.stop_automation("user_activity")
                # 自动恢复准备状态
                self._auto_recovery()
                
        except Exception as e:
            print(f"安全回调函数异常: {e}")
            
    def _auto_recovery(self):
        """自动恢复准备状态"""
        try:
            print("自动恢复准备状态...")
            
            # 等待一段时间让用户完成操作
            time.sleep(2.0)
            
            # 重新激活目标窗口
            config = self.config_manager.get_config()
            self._ensure_window_active(config)
            
            # 重新启动安全监控
            if not self.safety_manager.is_monitoring():
                print("重新启动安全监控...")
                self.safety_manager.start_safety_monitoring(self._safety_callback)
            
            # 重新启动自动化
            if not self.safety_manager.is_automation_running():
                print("重新启动自动化...")
                self.safety_manager.start_automation()
                
            print("自动恢复完成，准备继续执行")
            
        except Exception as e:
            print(f"自动恢复异常: {e}")
            self.logger.log_error(e, {"action": "auto_recovery"})
            
    def get_safety_stats(self) -> Dict[str, Any]:
        """获取安全统计信息"""
        return self.safety_manager.get_safety_stats()
        
    def set_safety_level(self, level: SafetyLevel):
        """设置安全级别"""
        self.safety_manager.safety_level = level
        if self.safety_manager.monitor:
            self.safety_manager.monitor.set_safety_level(level)
            
    def get_safety_level(self) -> SafetyLevel:
        """获取安全级别"""
        return self.safety_manager.safety_level
        
    def _activate_target_window(self, config: Dict[str, Any]):
        """激活目标窗口"""
        try:
            window_config = config.get("window", {})
            if not window_config.get("enabled", False):
                print("窗口管理已禁用")
                return
                
            print("激活目标窗口...")
            
            # 激活窗口
            success = self.window_manager.ensure_window_active(window_config)
            if success:
                print("目标窗口激活成功")
                
                # 添加激活延迟
                activation_delay = window_config.get("activation_delay", 0.5)
                if activation_delay > 0:
                    print(f"等待 {activation_delay} 秒...")
                    time.sleep(activation_delay)
            else:
                print("目标窗口激活失败")
                
        except Exception as e:
            print(f"激活目标窗口异常: {e}")
            self.logger.log_error(e, {"action": "activate_target_window"})
            
    def _auto_execute_macro(self, config: Dict[str, Any]):
        """自动执行宏"""
        try:
            strategy = config.get("strategy", {})
            auto_macro = strategy.get("auto_execute_macro")
            execution_delay = strategy.get("execution_delay", 1.0)
            
            if auto_macro:
                print(f"自动执行宏: {auto_macro}")
                
                # 等待执行延迟
                if execution_delay > 0:
                    print(f"等待 {execution_delay} 秒后执行...")
                    time.sleep(execution_delay)
                
                # 执行宏
                success = self.execute_macro(auto_macro)
                if success:
                    print(f"✓ 宏 {auto_macro} 执行成功")
                else:
                    print(f"✗ 宏 {auto_macro} 执行失败")
            else:
                print("未配置自动执行宏")
                
        except Exception as e:
            print(f"自动执行宏异常: {e}")
            self.logger.log_error(e, {"action": "auto_execute_macro"})
            
    def _ensure_window_active(self, config: Dict[str, Any]):
        """确保目标窗口处于活跃状态"""
        try:
            window_config = config.get("window", {})
            if not window_config.get("enabled", False):
                return
                
            # 使用智能目标管理
            print("🎯 开始智能目标管理...")
            success = self.window_manager.smart_ensure_target_active(window_config)
            if success:
                print("✅ 目标程序已确保活跃")
            else:
                print("❌ 无法确保目标程序活跃")
                # 如果无法确保目标活跃，停止自动化
                print("🛑 自动化程序终止：无法激活目标程序")
                self.stop()
                
        except Exception as e:
            print(f"确保窗口活跃异常: {e}")
            self.logger.log_error(e, {"action": "ensure_window_active"})
            
    def _show_user_reminder(self):
        """显示用户提醒"""
        print("\n" + "=" * 80)
        print("重要提醒：自动化程序即将开始运行")
        print("=" * 80)
        print("请勿进行以下操作，以免影响自动化运行：")
        print("   • 不要移动鼠标")
        print("   • 不要点击键盘")
        print("   • 不要切换窗口")
        print("   • 不要关闭目标程序")
        print("   • 不要进行其他手动操作")
        print("")
        print("安全机制已启用，如检测到用户操作将自动停止")
        print("如需停止程序，请按 ESC 键或 Ctrl+C")
        print("=" * 80)
        print("")
        
        # 倒计时提醒
        for i in range(3, 0, -1):
            print(f"自动化将在 {i} 秒后开始...", end="\r")
            time.sleep(1)
        print("自动化开始运行！                    ")
        print("")
        
    def _dialog_callback(self, dialog_info: Dict[str, Any]):
        """对话框处理回调"""
        try:
            action = dialog_info.get("action")
            
            if action == "terminate_program":
                # 终止程序
                reason = dialog_info.get("reason", "unknown")
                dialog_info_detail = dialog_info.get("dialog_info", {})
                
                print(f"\n 程序终止: {reason}")
                print(f"对话框信息: {dialog_info_detail.get('title', 'Unknown')}")
                print(f"对话框内容: {dialog_info_detail.get('content', 'Unknown')}")
                
                # 停止自动化
                self.stop()
                return
                
            # 处理对话框信息
            title = dialog_info.get("title", "Unknown")
            content = dialog_info.get("content", "Unknown")
            dialog_type = dialog_info.get("type", "unknown")
            is_expected = dialog_info.get("is_expected", False)
            
            print(f"\n📋 对话框处理回调:")
            print(f"   📋 标题: {title}")
            print(f"   📄 内容: {content}")
            print(f"   🏷️  类型: {dialog_type}")
            print(f"   ✅ 预期: {'是' if is_expected else '否'}")
            print(f"   🕐 时间: {time.strftime('%H:%M:%S')}")
            
        except Exception as e:
            print(f"对话框回调异常: {e}")


def test_controller():
    """测试控制器功能"""
    print("测试控制器功能...")
    
    # 创建测试配置
    config_manager = ConfigManager("test_profiles")
    logger = PuppeteerLogger("test_logs")
    
    # 创建默认配置
    if config_manager.create_default_profile("test_game"):
        print("创建测试配置成功")
        
        # 创建控制器
        controller = PuppeteerController(config_manager, logger)
        
        # 测试状态
        status = controller.get_status()
        print(f"初始状态: {status}")
        
        # 测试启动（需要实际的屏幕环境）
        print("注意：实际启动需要屏幕环境，这里只测试配置加载")
        
    # 清理测试文件
    import shutil
    if os.path.exists("test_profiles"):
        shutil.rmtree("test_profiles")
    if os.path.exists("test_logs"):
        shutil.rmtree("test_logs")
        
        print("控制器测试完成!")


def test_controller():
    """测试控制器功能"""
    print("测试控制器功能...")
    
    # 创建测试配置
    config_manager = ConfigManager("test_profiles")
    logger = PuppeteerLogger("test_logs")
    
    # 创建默认配置
    if config_manager.create_default_profile("test_game"):
        print("创建测试配置成功")
        
        # 创建控制器
        controller = PuppeteerController(config_manager, logger)
        
        # 测试状态
        status = controller.get_status()
        print(f"初始状态: {status}")
        
        # 测试启动（需要实际的屏幕环境）
        print("注意：实际启动需要屏幕环境，这里只测试配置加载")
        
    # 清理测试文件
    import shutil
    if os.path.exists("test_profiles"):
        shutil.rmtree("test_profiles")
    if os.path.exists("test_logs"):
        shutil.rmtree("test_logs")
        
    print("控制器测试完成!")


    def _safety_callback(self, event_type: SafetyEvent, data: Dict[str, Any]):
        """安全事件回调函数"""
        try:
            # 记录安全事件
            self.logger.log_safety_event(event_type.value, data)
            
            # 根据事件类型处理
            if event_type == SafetyEvent.EMERGENCY_STOP:
                print(f"紧急停止触发: {data.get('key', 'unknown')}")
                self.safety_manager.stop_automation("emergency_stop")
            elif event_type in [SafetyEvent.MOUSE_MOVE, SafetyEvent.KEYBOARD_INPUT]:
                print(f"用户操作检测: {event_type.value}")
                self.safety_manager.stop_automation("user_activity")
                
        except Exception as e:
            print(f"安全回调函数异常: {e}")
            
    def get_safety_stats(self) -> Dict[str, Any]:
        """获取安全统计信息"""
        return self.safety_manager.get_safety_stats()
        
    def set_safety_level(self, level: SafetyLevel):
        """设置安全级别"""
        self.safety_manager.safety_level = level
        if self.safety_manager.monitor:
            self.safety_manager.monitor.set_safety_level(level)
            
    def get_safety_level(self) -> SafetyLevel:
        """获取安全级别"""
        return self.safety_manager.safety_level


if __name__ == "__main__":
    import os
    test_controller()
