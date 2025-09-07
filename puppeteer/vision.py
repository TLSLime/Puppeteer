# -*- coding: utf-8 -*-
"""
视觉识别模块 - 模板匹配和图像识别
使用OpenCV实现模板匹配，输出结构化Observation
"""

import cv2
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
import os
import json
import time


class VisionProcessor:
    """视觉处理器，负责模板匹配和图像识别"""
    
    def __init__(self, confidence_threshold: float = 0.8):
        """
        初始化视觉处理器
        
        Args:
            confidence_threshold: 模板匹配置信度阈值
        """
        self.confidence_threshold = confidence_threshold
        self.templates = {}  # 存储加载的模板
        self.template_cache = {}  # 模板缓存
        
    def load_template(self, name: str, template_path: str) -> bool:
        """
        加载模板图像
        
        Args:
            name: 模板名称
            template_path: 模板文件路径
            
        Returns:
            是否加载成功
        """
        try:
            if not os.path.exists(template_path):
                print(f"模板文件不存在: {template_path}")
                return False
                
            # 加载模板图像
            template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
            if template is None:
                print(f"无法加载模板图像: {template_path}")
                return False
                
            self.templates[name] = {
                "path": template_path,
                "image": template,
                "size": template.shape
            }
            
            print(f"成功加载模板: {name} ({template.shape})")
            return True
            
        except Exception as e:
            print(f"加载模板失败 {name}: {e}")
            return False
            
    def load_templates_from_config(self, templates_config: Dict[str, str]) -> int:
        """
        从配置加载多个模板
        
        Args:
            templates_config: 模板配置字典 {name: path}
            
        Returns:
            成功加载的模板数量
        """
        loaded_count = 0
        for name, path in templates_config.items():
            if self.load_template(name, path):
                loaded_count += 1
                
        return loaded_count
        
    def match_template(self, image: np.ndarray, template_name: str, 
                      roi: Optional[Tuple[int, int, int, int]] = None) -> List[Dict[str, Any]]:
        """
        在图像中匹配模板
        
        Args:
            image: 输入图像
            template_name: 模板名称
            roi: 感兴趣区域 (x, y, width, height)
            
        Returns:
            匹配结果列表，每个结果包含位置和置信度
        """
        if template_name not in self.templates:
            print(f"模板不存在: {template_name}")
            return []
            
        try:
            # 获取模板
            template_info = self.templates[template_name]
            template = template_info["image"]
            
            # 处理ROI
            if roi:
                x, y, w, h = roi
                search_image = image[y:y+h, x:x+w]
                offset_x, offset_y = x, y
            else:
                search_image = image
                offset_x, offset_y = 0, 0
                
            # 转换为灰度图
            if len(search_image.shape) == 3:
                search_gray = cv2.cvtColor(search_image, cv2.COLOR_BGR2GRAY)
            else:
                search_gray = search_image
                
            # 模板匹配
            result = cv2.matchTemplate(search_gray, template, cv2.TM_CCOEFF_NORMED)
            
            # 找到匹配位置
            locations = np.where(result >= self.confidence_threshold)
            
            matches = []
            for pt in zip(*locations[::-1]):  # 交换x,y坐标
                confidence = result[pt[1], pt[0]]
                center_x = pt[0] + template.shape[1] // 2 + offset_x
                center_y = pt[1] + template.shape[0] // 2 + offset_y
                
                matches.append({
                    "template": template_name,
                    "position": [center_x, center_y],
                    "confidence": float(confidence),
                    "bbox": [
                        pt[0] + offset_x,
                        pt[1] + offset_y,
                        template.shape[1],
                        template.shape[0]
                    ]
                })
                
            return matches
            
        except Exception as e:
            print(f"模板匹配失败 {template_name}: {e}")
            return []
            
    def process_observation(self, image: np.ndarray, 
                          detection_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理观察数据，生成结构化Observation
        
        Args:
            image: 输入图像
            detection_config: 检测配置
            
        Returns:
            结构化Observation数据
        """
        observation = {
            "timestamp": time.time(),
            "scene": detection_config.get("scene", "unknown"),
            "self": {},
            "enemies": [],
            "items": [],
            "ui_elements": []
        }
        
        try:
            # 处理各种检测任务
            templates = detection_config.get("templates", {})
            rois = detection_config.get("rois", {})
            
            for category, template_list in templates.items():
                if category == "enemies":
                    for template_name in template_list:
                        roi = rois.get(template_name)
                        matches = self.match_template(image, template_name, roi)
                        observation["enemies"].extend(matches)
                        
                elif category == "items":
                    for template_name in template_list:
                        roi = rois.get(template_name)
                        matches = self.match_template(image, template_name, roi)
                        observation["items"].extend(matches)
                        
                elif category == "ui_elements":
                    for template_name in template_list:
                        roi = rois.get(template_name)
                        matches = self.match_template(image, template_name, roi)
                        observation["ui_elements"].extend(matches)
                        
            # 处理自身状态检测（如血量等）
            self_status = detection_config.get("self_status", {})
            for status_name, template_name in self_status.items():
                roi = rois.get(template_name)
                matches = self.match_template(image, template_name, roi)
                if matches:
                    observation["self"][status_name] = matches[0]["confidence"]
                    
        except Exception as e:
            print(f"处理观察数据失败: {e}")
            
        return observation
        
    def set_confidence_threshold(self, threshold: float):
        """设置置信度阈值"""
        self.confidence_threshold = max(0.1, min(1.0, threshold))
        
    def get_loaded_templates(self) -> List[str]:
        """获取已加载的模板列表"""
        return list(self.templates.keys())


def test_vision():
    """测试视觉处理功能"""
    print("测试视觉处理功能...")
    
    processor = VisionProcessor(confidence_threshold=0.7)
    
    # 创建测试图像
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
        
    print("视觉处理测试完成!")


if __name__ == "__main__":
    test_vision()
