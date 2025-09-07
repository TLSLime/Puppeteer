# -*- coding: utf-8 -*-
"""
日志记录模块 - 结构化日志记录和审计
支持JSONL格式日志，便于回放和分析
"""

import json
import logging
import os
import time
from datetime import datetime
from typing import Dict, Any, Optional, List
import threading


class PuppeteerLogger:
    """Puppeteer日志记录器，支持结构化日志和审计功能"""
    
    def __init__(self, log_dir: str = "logs", log_format: str = "jsonl"):
        """
        初始化日志记录器
        
        Args:
            log_dir: 日志目录
            log_format: 日志格式 ("jsonl" 或 "text")
        """
        self.log_dir = log_dir
        self.log_format = log_format
        self._lock = threading.Lock()
        
        # 确保日志目录存在
        os.makedirs(log_dir, exist_ok=True)
        
        # 初始化日志文件
        self._init_log_files()
        
        # 设置标准日志记录器
        self._setup_standard_logger()
        
    def _init_log_files(self):
        """初始化日志文件"""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        
        if self.log_format == "jsonl":
            self.log_file = os.path.join(self.log_dir, f"puppeteer-{timestamp}.jsonl")
        else:
            self.log_file = os.path.join(self.log_dir, f"puppeteer-{timestamp}.log")
            
        # 创建日志文件（如果不存在）
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write("")
                
    def _setup_standard_logger(self):
        """设置标准日志记录器"""
        self.logger = logging.getLogger("puppeteer")
        self.logger.setLevel(logging.INFO)
        
        # 清除现有处理器
        self.logger.handlers.clear()
        
        # 文件处理器
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 设置格式
        if self.log_format == "jsonl":
            formatter = logging.Formatter('%(message)s')
        else:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def _write_jsonl(self, data: Dict[str, Any]):
        """写入JSONL格式日志"""
        try:
            with self._lock:
                with open(self.log_file, 'a', encoding='utf-8', buffering=1) as f:
                    f.write(json.dumps(data, ensure_ascii=False) + '\n')
                    f.flush()  # 强制刷新缓冲区
                    # 文件句柄会在with语句结束时自动关闭
        except Exception as e:
            print(f"写入日志失败: {e}")
            
    def _write_text(self, level: str, message: str, extra: Optional[Dict[str, Any]] = None):
        """写入文本格式日志"""
        try:
            if extra:
                message = f"{message} | {json.dumps(extra, ensure_ascii=False)}"
            self.logger.info(message)
        except Exception as e:
            print(f"写入日志失败: {e}")
            
    def log_action(self, action: Dict[str, Any], result: Dict[str, Any]):
        """
        记录动作日志
        
        Args:
            action: 动作对象
            result: 执行结果
        """
        log_data = {
            "timestamp": time.time(),
            "type": "action",
            "action": action,
            "result": result
        }
        
        if self.log_format == "jsonl":
            self._write_jsonl(log_data)
        else:
            self._write_text("INFO", f"执行动作: {action.get('type', 'unknown')}", log_data)
            
    def log_observation(self, observation: Dict[str, Any]):
        """
        记录观察日志
        
        Args:
            observation: 观察数据
        """
        log_data = {
            "timestamp": time.time(),
            "type": "observation",
            "observation": observation
        }
        
        if self.log_format == "jsonl":
            self._write_jsonl(log_data)
        else:
            scene = observation.get("scene", "unknown")
            enemies_count = len(observation.get("enemies", []))
            items_count = len(observation.get("items", []))
            self._write_text("INFO", f"观察场景: {scene}, 敌人: {enemies_count}, 物品: {items_count}", log_data)
            
    def log_system(self, level: str, message: str, extra: Optional[Dict[str, Any]] = None):
        """
        记录系统日志
        
        Args:
            level: 日志级别
            message: 日志消息
            extra: 额外数据
        """
        log_data = {
            "timestamp": time.time(),
            "type": "system",
            "level": level,
            "message": message
        }
        
        if extra:
            log_data["extra"] = extra
            
        if self.log_format == "jsonl":
            self._write_jsonl(log_data)
        else:
            self._write_text(level, message, extra)
            
    def log_error(self, error: Exception, context: Optional[Dict[str, Any]] = None):
        """
        记录错误日志
        
        Args:
            error: 异常对象
            context: 错误上下文
        """
        log_data = {
            "timestamp": time.time(),
            "type": "error",
            "error": str(error),
            "error_type": type(error).__name__
        }
        
        if context:
            log_data["context"] = context
            
        if self.log_format == "jsonl":
            self._write_jsonl(log_data)
        else:
            self._write_text("ERROR", f"错误: {error}", log_data)
            
    def log_session_start(self, profile_name: str, config: Dict[str, Any]):
        """记录会话开始"""
        log_data = {
            "timestamp": time.time(),
            "type": "session_start",
            "profile": profile_name,
            "config": config
        }
        
        if self.log_format == "jsonl":
            self._write_jsonl(log_data)
        else:
            self._write_text("INFO", f"会话开始: {profile_name}", log_data)
            
    def log_session_end(self, profile_name: str, duration: float, stats: Optional[Dict[str, Any]] = None):
        """记录会话结束"""
        log_data = {
            "timestamp": time.time(),
            "type": "session_end",
            "profile": profile_name,
            "duration": duration
        }
        
        if stats:
            log_data["stats"] = stats
            
        if self.log_format == "jsonl":
            self._write_jsonl(log_data)
        else:
            self._write_text("INFO", f"会话结束: {profile_name}, 持续时间: {duration:.2f}秒", log_data)
            
    def log_safety_event(self, event_type: str, data: Dict[str, Any]):
        """
        记录安全事件日志
        
        Args:
            event_type: 安全事件类型
            data: 事件数据
        """
        log_data = {
            "timestamp": time.time(),
            "type": "safety_event",
            "event_type": event_type,
            "data": data
        }
        
        if self.log_format == "jsonl":
            self._write_jsonl(log_data)
        else:
            self._write_text("WARNING", f"安全事件: {event_type} - {data}", log_data)
            
    def get_recent_logs(self, count: int = 100, log_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取最近的日志记录
        
        Args:
            count: 获取数量
            log_type: 日志类型过滤
            
        Returns:
            日志记录列表
        """
        logs = []
        
        try:
            if not os.path.exists(self.log_file):
                return logs
                
            with open(self.log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            # 从后往前读取指定数量的行
            recent_lines = lines[-count:] if len(lines) > count else lines
            
            for line in recent_lines:
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    if self.log_format == "jsonl":
                        log_data = json.loads(line)
                    else:
                        # 对于文本格式，简单解析
                        log_data = {"raw": line}
                        
                    if log_type is None or log_data.get("type") == log_type:
                        logs.append(log_data)
                        
                except json.JSONDecodeError:
                    continue
                    
        except Exception as e:
            print(f"读取日志失败: {e}")
            
        return logs
        
    def export_session_logs(self, output_path: str, start_time: Optional[float] = None, 
                          end_time: Optional[float] = None) -> bool:
        """
        导出会话日志
        
        Args:
            output_path: 输出文件路径
            start_time: 开始时间戳
            end_time: 结束时间戳
            
        Returns:
            是否导出成功
        """
        try:
            logs = self.get_recent_logs(count=10000)  # 获取大量日志
            
            # 时间过滤
            if start_time or end_time:
                filtered_logs = []
                for log in logs:
                    timestamp = log.get("timestamp", 0)
                    if start_time and timestamp < start_time:
                        continue
                    if end_time and timestamp > end_time:
                        continue
                    filtered_logs.append(log)
                logs = filtered_logs
                
            # 导出为JSON
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
                
            print(f"导出日志到: {output_path}")
            return True
            
        except Exception as e:
            print(f"导出日志失败: {e}")
            return False


def test_logger():
    """测试日志记录功能"""
    print("测试日志记录功能...")
    
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
        
    print("日志记录测试完成!")


if __name__ == "__main__":
    test_logger()
