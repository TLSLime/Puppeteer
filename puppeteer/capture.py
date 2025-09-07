# -*- coding: utf-8 -*-
"""
截屏模块 - 高效截取屏幕图像
使用 mss 库实现高性能截屏，支持指定区域和缩放
"""

import mss
import numpy as np
import cv2
from typing import Optional, Tuple, Union
import time


class ScreenCapture:
    """屏幕截取器，支持全屏或指定区域截取"""
    
    def __init__(self, monitor_id: int = 1):
        """
        初始化截屏器
        
        Args:
            monitor_id: 显示器ID，1为主显示器
        """
        self.monitor_id = monitor_id
        self.sct = None
        self._last_capture_time = 0
        self._fps_limit = 10  # 默认10fps限制
        
    def __enter__(self):
        """上下文管理器入口"""
        self.sct = mss.mss()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        if self.sct:
            self.sct.close()
            
    def capture(self, region: Optional[Tuple[int, int, int, int]] = None, 
                grayscale: bool = False) -> np.ndarray:
        """
        截取屏幕图像
        
        Args:
            region: 截取区域 (x, y, width, height)，None为全屏
            grayscale: 是否转换为灰度图
            
        Returns:
            BGR格式的numpy数组图像
        """
        if not self.sct:
            raise RuntimeError("ScreenCapture not initialized. Use with statement.")
            
        # FPS限制
        current_time = time.time()
        if current_time - self._last_capture_time < 1.0 / self._fps_limit:
            time.sleep(1.0 / self._fps_limit - (current_time - self._last_capture_time))
        self._last_capture_time = time.time()
        
        try:
            if region:
                # 指定区域截取
                monitor = {
                    "top": region[1],
                    "left": region[0], 
                    "width": region[2],
                    "height": region[3]
                }
            else:
                # 全屏截取
                monitor = self.sct.monitors[self.monitor_id]
                
            # 截取屏幕
            screenshot = self.sct.grab(monitor)
            
            # 转换为numpy数组
            img = np.array(screenshot)
            
            # 转换颜色格式 BGR -> RGB (mss返回BGRA格式)
            if len(img.shape) == 3 and img.shape[2] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            elif len(img.shape) == 3 and img.shape[2] == 3:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2BGR)
                
            # 转换为灰度图
            if grayscale:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
            return img
            
        except Exception as e:
            raise RuntimeError(f"Screen capture failed: {e}")
            
    def set_fps_limit(self, fps: int):
        """设置截屏帧率限制"""
        self._fps_limit = max(1, min(60, fps))  # 限制在1-60fps之间
        
    def get_screen_size(self) -> Tuple[int, int]:
        """获取屏幕尺寸"""
        if not self.sct:
            raise RuntimeError("ScreenCapture not initialized. Use with statement.")
            
        monitor = self.sct.monitors[self.monitor_id]
        return monitor["width"], monitor["height"]


def test_capture():
    """测试截屏功能"""
    print("测试截屏功能...")
    
    with ScreenCapture() as capture:
        # 测试全屏截取
        print("截取全屏...")
        img = capture.capture()
        print(f"全屏图像尺寸: {img.shape}")
        
        # 测试区域截取
        print("截取指定区域...")
        region_img = capture.capture(region=(100, 100, 400, 300))
        print(f"区域图像尺寸: {region_img.shape}")
        
        # 测试灰度图
        print("截取灰度图...")
        gray_img = capture.capture(grayscale=True)
        print(f"灰度图像尺寸: {gray_img.shape}")
        
        # 获取屏幕尺寸
        width, height = capture.get_screen_size()
        print(f"屏幕尺寸: {width}x{height}")
        
    print("截屏测试完成!")


if __name__ == "__main__":
    test_capture()
