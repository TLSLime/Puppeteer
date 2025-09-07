# -*- coding: utf-8 -*-
"""
Puppeteer - 通用桌面程序自动化操控系统
MVP版本：截屏感知 + 配置驱动决策 + 输入执行 + 日志记录
"""

__version__ = "0.1.0"
__author__ = "Puppeteer Team"

# 导入核心模块
from .capture import ScreenCapture
from .vision import VisionProcessor
from .input_provider import InputProvider
from .config import ConfigManager
from .controller import PuppeteerController
from .logger import PuppeteerLogger

__all__ = [
    "ScreenCapture",
    "VisionProcessor", 
    "InputProvider",
    "ConfigManager",
    "PuppeteerController",
    "PuppeteerLogger"
]
