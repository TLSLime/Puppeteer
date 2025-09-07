# -*- coding: utf-8 -*-
"""
配置管理模块 - YAML配置文件解析和管理
负责加载和管理游戏配置文件
"""

import yaml
import os
from typing import Dict, List, Optional, Any, Union
import json


class ConfigManager:
    """配置管理器，负责加载和解析YAML配置文件"""
    
    def __init__(self, config_dir: str = "profiles"):
        """
        初始化配置管理器
        
        Args:
            config_dir: 配置文件目录
        """
        self.config_dir = config_dir
        self.current_profile = None
        self.profiles = {}
        
        # 确保配置目录存在
        os.makedirs(config_dir, exist_ok=True)
        
    def load_profile(self, profile_name: str) -> bool:
        """
        加载指定配置文件
        
        Args:
            profile_name: 配置文件名（不含扩展名）
            
        Returns:
            是否加载成功
        """
        try:
            profile_path = os.path.join(self.config_dir, f"{profile_name}.yaml")
            
            if not os.path.exists(profile_path):
                print(f"配置文件不存在: {profile_path}")
                return False
                
            with open(profile_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                
            # 验证配置结构
            if not self._validate_config(config):
                print(f"配置文件格式错误: {profile_path}")
                return False
                
            self.profiles[profile_name] = config
            self.current_profile = profile_name
            
            print(f"成功加载配置文件: {profile_name}")
            return True
            
        except Exception as e:
            print(f"加载配置文件失败 {profile_name}: {e}")
            return False
            
    def _validate_config(self, config: Dict[str, Any]) -> bool:
        """
        验证配置文件结构
        
        Args:
            config: 配置字典
            
        Returns:
            是否有效
        """
        required_fields = ["profile", "screen_region", "keymap"]
        
        for field in required_fields:
            if field not in config:
                print(f"缺少必需字段: {field}")
                return False
                
        return True
        
    def get_config(self, profile_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        获取配置对象
        
        Args:
            profile_name: 配置名称，None为当前配置
            
        Returns:
            配置字典
        """
        if profile_name is None:
            profile_name = self.current_profile
            
        if profile_name and profile_name in self.profiles:
            return self.profiles[profile_name]
            
        return None
        
    def get_screen_region(self, profile_name: Optional[str] = None) -> Optional[List[int]]:
        """获取屏幕区域配置"""
        config = self.get_config(profile_name)
        return config.get("screen_region") if config else None
        
    def get_keymap(self, profile_name: Optional[str] = None) -> Optional[Dict[str, str]]:
        """获取按键映射配置"""
        config = self.get_config(profile_name)
        return config.get("keymap") if config else None
        
    def get_templates(self, profile_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """获取模板配置"""
        config = self.get_config(profile_name)
        return config.get("templates") if config else None
        
    def get_macros(self, profile_name: Optional[str] = None) -> Optional[Dict[str, List[str]]]:
        """获取宏配置"""
        config = self.get_config(profile_name)
        return config.get("macros") if config else None
        
    def get_detection_config(self, profile_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """获取检测配置"""
        config = self.get_config(profile_name)
        return config.get("detection") if config else None
        
    def get_rois(self, profile_name: Optional[str] = None) -> Optional[Dict[str, List[int]]]:
        """获取ROI配置"""
        config = self.get_config(profile_name)
        return config.get("rois") if config else None
        
    def list_profiles(self) -> List[str]:
        """列出所有可用的配置文件"""
        profiles = []
        if os.path.exists(self.config_dir):
            for file in os.listdir(self.config_dir):
                if file.endswith('.yaml') or file.endswith('.yml'):
                    profiles.append(file[:-5])  # 移除扩展名
        return profiles
        
    def create_default_profile(self, profile_name: str, 
                             screen_region: List[int] = [0, 0, 1920, 1080]) -> bool:
        """
        创建默认配置文件
        
        Args:
            profile_name: 配置名称
            screen_region: 屏幕区域 [x, y, width, height]
            
        Returns:
            是否创建成功
        """
        try:
            default_config = {
                "profile": profile_name,
                "description": f"默认配置 - {profile_name}",
                "screen_region": screen_region,
                "keymap": {
                    "attack": "q",
                    "jump": "space",
                    "move_left": "a",
                    "move_right": "d",
                    "move_up": "w",
                    "move_down": "s"
                },
                "templates": {
                    "enemies": ["enemy1.png", "enemy2.png"],
                    "items": ["item1.png", "item2.png"],
                    "ui_elements": ["health_bar.png", "mana_bar.png"]
                },
                "rois": {
                    "enemy1.png": [100, 100, 800, 600],
                    "enemy2.png": [100, 100, 800, 600],
                    "item1.png": [0, 0, 1920, 1080],
                    "item2.png": [0, 0, 1920, 1080],
                    "health_bar.png": [50, 50, 200, 50],
                    "mana_bar.png": [50, 100, 200, 50]
                },
                "detection": {
                    "scene": "default",
                    "templates": {
                        "enemies": ["enemy1.png", "enemy2.png"],
                        "items": ["item1.png", "item2.png"],
                        "ui_elements": ["health_bar.png", "mana_bar.png"]
                    },
                    "self_status": {
                        "health": "health_bar.png",
                        "mana": "mana_bar.png"
                    }
                },
                "macros": {
                    "combo1": ["attack", "jump", "attack"],
                    "combo2": ["move_left", "attack", "move_right"]
                },
                "humanize": {
                    "enabled": True,
                    "mouse_delay_range": [50, 150],
                    "key_delay_range": [80, 140],
                    "click_delay_range": [20, 80],
                    "movement_jitter": 2,
                    "timing_jitter": 20
                },
                "controller": {
                    "fps_limit": 10,
                    "action_cooldown": 0.1,
                    "confidence_threshold": 0.8
                }
            }
            
            profile_path = os.path.join(self.config_dir, f"{profile_name}.yaml")
            with open(profile_path, 'w', encoding='utf-8') as f:
                yaml.dump(default_config, f, default_flow_style=False, 
                         allow_unicode=True, indent=2)
                         
            print(f"创建默认配置文件: {profile_path}")
            return True
            
        except Exception as e:
            print(f"创建配置文件失败: {e}")
            return False
            
    def save_profile(self, profile_name: str, config: Dict[str, Any]) -> bool:
        """
        保存配置文件
        
        Args:
            profile_name: 配置名称
            config: 配置字典
            
        Returns:
            是否保存成功
        """
        try:
            profile_path = os.path.join(self.config_dir, f"{profile_name}.yaml")
            with open(profile_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, 
                         allow_unicode=True, indent=2)
                         
            print(f"保存配置文件: {profile_path}")
            return True
            
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False


def test_config():
    """测试配置管理功能"""
    print("测试配置管理功能...")
    
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
        
    print("配置管理测试完成!")


if __name__ == "__main__":
    test_config()
