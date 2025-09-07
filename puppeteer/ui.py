# -*- coding: utf-8 -*-
"""
用户界面模块 - 最小控制面板
使用Tkinter提供启动/停止、配置切换等基本功能
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
from typing import Optional, Dict, Any
from .controller import PuppeteerController
from .config import ConfigManager
from .logger import PuppeteerLogger


class PuppeteerUI:
    """Puppeteer用户界面"""
    
    def __init__(self):
        """初始化用户界面"""
        self.root = tk.Tk()
        self.root.title("Puppeteer - 桌面程序自动化操控系统")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # 核心组件
        self.config_manager = ConfigManager()
        self.logger = PuppeteerLogger()
        self.controller = PuppeteerController(self.config_manager, self.logger)
        
        # UI状态
        self.is_running = False
        self.current_profile = None
        self.status_update_thread = None
        
        # 创建界面
        self._create_widgets()
        self._setup_layout()
        self._start_status_updates()
        
    def _create_widgets(self):
        """创建界面组件"""
        # 主框架
        self.main_frame = ttk.Frame(self.root, padding="10")
        
        # 标题
        self.title_label = ttk.Label(self.main_frame, text="Puppeteer 控制面板", 
                                   font=("Arial", 16, "bold"))
        
        # 配置选择框架
        self.config_frame = ttk.LabelFrame(self.main_frame, text="配置管理", padding="5")
        
        self.profile_label = ttk.Label(self.config_frame, text="当前配置:")
        self.profile_var = tk.StringVar()
        self.profile_combo = ttk.Combobox(self.config_frame, textvariable=self.profile_var,
                                        state="readonly", width=30)
        
        self.refresh_btn = ttk.Button(self.config_frame, text="刷新配置", 
                                    command=self._refresh_profiles)
        self.create_btn = ttk.Button(self.config_frame, text="创建配置", 
                                   command=self._create_profile)
        
        # 控制框架
        self.control_frame = ttk.LabelFrame(self.main_frame, text="运行控制", padding="5")
        
        self.start_btn = ttk.Button(self.control_frame, text="开始", 
                                  command=self._start_controller, style="Accent.TButton")
        self.stop_btn = ttk.Button(self.control_frame, text="停止", 
                                 command=self._stop_controller, state="disabled")
        self.pause_btn = ttk.Button(self.control_frame, text="暂停", 
                                  command=self._pause_controller, state="disabled")
        self.resume_btn = ttk.Button(self.control_frame, text="恢复", 
                                   command=self._resume_controller, state="disabled")
        
        # 状态框架
        self.status_frame = ttk.LabelFrame(self.main_frame, text="运行状态", padding="5")
        
        self.status_label = ttk.Label(self.status_frame, text="状态: 空闲")
        self.profile_status_label = ttk.Label(self.status_frame, text="配置: 无")
        self.stats_label = ttk.Label(self.status_frame, text="统计: 无")
        
        # 日志框架
        self.log_frame = ttk.LabelFrame(self.main_frame, text="运行日志", padding="5")
        
        # 创建日志文本框和滚动条
        self.log_text = tk.Text(self.log_frame, height=15, width=70, wrap=tk.WORD)
        self.log_scrollbar = ttk.Scrollbar(self.log_frame, orient=tk.VERTICAL, 
                                         command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=self.log_scrollbar.set)
        
        self.clear_log_btn = ttk.Button(self.log_frame, text="清空日志", 
                                      command=self._clear_log)
        self.export_log_btn = ttk.Button(self.log_frame, text="导出日志", 
                                       command=self._export_log)
        
        # 宏控制框架
        self.macro_frame = ttk.LabelFrame(self.main_frame, text="宏控制", padding="5")
        
        self.macro_label = ttk.Label(self.macro_frame, text="可用宏:")
        self.macro_var = tk.StringVar()
        self.macro_combo = ttk.Combobox(self.macro_frame, textvariable=self.macro_var,
                                      state="readonly", width=20)
        
        self.execute_macro_btn = ttk.Button(self.macro_frame, text="执行宏", 
                                          command=self._execute_macro, state="disabled")
        
    def _setup_layout(self):
        """设置布局"""
        # 主框架
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        
        # 标题
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # 配置管理
        self.config_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        self.config_frame.columnconfigure(1, weight=1)
        
        self.profile_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.profile_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        self.refresh_btn.grid(row=0, column=2, padx=(0, 5))
        self.create_btn.grid(row=0, column=3)
        
        # 运行控制
        self.control_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.start_btn.grid(row=0, column=0, padx=(0, 5))
        self.stop_btn.grid(row=0, column=1, padx=(0, 5))
        self.pause_btn.grid(row=0, column=2, padx=(0, 5))
        self.resume_btn.grid(row=0, column=3)
        
        # 运行状态
        self.status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.status_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 20))
        self.profile_status_label.grid(row=0, column=1, sticky=tk.W, padx=(0, 20))
        self.stats_label.grid(row=0, column=2, sticky=tk.W)
        
        # 宏控制
        self.macro_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.macro_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.macro_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        self.execute_macro_btn.grid(row=0, column=2)
        
        # 日志
        self.log_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 5))
        self.log_frame.columnconfigure(0, weight=1)
        self.log_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(5, weight=1)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        self.log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        self.clear_log_btn.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.export_log_btn.grid(row=1, column=0, sticky=tk.E, pady=(5, 0))
        
        # 初始化
        self._refresh_profiles()
        self._log_message("系统启动完成")
        
    def _refresh_profiles(self):
        """刷新配置文件列表"""
        try:
            profiles = self.config_manager.list_profiles()
            self.profile_combo['values'] = profiles
            
            if profiles and not self.profile_var.get():
                self.profile_var.set(profiles[0])
                self.current_profile = profiles[0]
                self._update_macro_list()
                
        except Exception as e:
            self._log_message(f"刷新配置失败: {e}")
            
    def _create_profile(self):
        """创建新配置文件"""
        try:
            # 简单的输入对话框
            dialog = tk.Toplevel(self.root)
            dialog.title("创建配置")
            dialog.geometry("300x150")
            dialog.resizable(False, False)
            dialog.transient(self.root)
            dialog.grab_set()
            
            # 居中显示
            dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
            
            ttk.Label(dialog, text="配置名称:").pack(pady=10)
            name_entry = ttk.Entry(dialog, width=30)
            name_entry.pack(pady=5)
            name_entry.focus()
            
            def create():
                name = name_entry.get().strip()
                if name:
                    if self.config_manager.create_default_profile(name):
                        self._refresh_profiles()
                        self.profile_var.set(name)
                        self._log_message(f"创建配置成功: {name}")
                    else:
                        messagebox.showerror("错误", "创建配置失败")
                    dialog.destroy()
                else:
                    messagebox.showwarning("警告", "请输入配置名称")
                    
            ttk.Button(dialog, text="创建", command=create).pack(pady=10)
            
            # 回车键绑定
            name_entry.bind('<Return>', lambda e: create())
            
        except Exception as e:
            self._log_message(f"创建配置失败: {e}")
            
    def _start_controller(self):
        """启动控制器"""
        try:
            profile_name = self.profile_var.get()
            if not profile_name:
                messagebox.showwarning("警告", "请选择配置文件")
                return
                
            if self.controller.start(profile_name):
                self.is_running = True
                self.current_profile = profile_name
                self._update_ui_state()
                self._log_message(f"启动控制器: {profile_name}")
            else:
                messagebox.showerror("错误", "启动控制器失败")
                
        except Exception as e:
            self._log_message(f"启动失败: {e}")
            messagebox.showerror("错误", f"启动失败: {e}")
            
    def _stop_controller(self):
        """停止控制器"""
        try:
            self.controller.stop()
            self.is_running = False
            self.current_profile = None
            self._update_ui_state()
            self._log_message("停止控制器")
            
        except Exception as e:
            self._log_message(f"停止失败: {e}")
            
    def _pause_controller(self):
        """暂停控制器"""
        try:
            self.controller.pause()
            self._update_ui_state()
            self._log_message("暂停控制器")
            
        except Exception as e:
            self._log_message(f"暂停失败: {e}")
            
    def _resume_controller(self):
        """恢复控制器"""
        try:
            self.controller.resume()
            self._update_ui_state()
            self._log_message("恢复控制器")
            
        except Exception as e:
            self._log_message(f"恢复失败: {e}")
            
    def _execute_macro(self):
        """执行宏"""
        try:
            macro_name = self.macro_var.get()
            if not macro_name:
                messagebox.showwarning("警告", "请选择宏")
                return
                
            if self.controller.execute_macro(macro_name):
                self._log_message(f"执行宏成功: {macro_name}")
            else:
                self._log_message(f"执行宏失败: {macro_name}")
                
        except Exception as e:
            self._log_message(f"执行宏失败: {e}")
            
    def _update_ui_state(self):
        """更新UI状态"""
        if self.is_running:
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
            self.pause_btn.config(state="normal")
            self.resume_btn.config(state="normal")
            self.execute_macro_btn.config(state="normal")
        else:
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")
            self.pause_btn.config(state="disabled")
            self.resume_btn.config(state="disabled")
            self.execute_macro_btn.config(state="disabled")
            
    def _update_macro_list(self):
        """更新宏列表"""
        try:
            if self.current_profile:
                macros = self.config_manager.get_macros()
                if macros:
                    self.macro_combo['values'] = list(macros.keys())
                    if not self.macro_var.get() and macros:
                        self.macro_var.set(list(macros.keys())[0])
                else:
                    self.macro_combo['values'] = []
                    self.macro_var.set("")
            else:
                self.macro_combo['values'] = []
                self.macro_var.set("")
                
        except Exception as e:
            self._log_message(f"更新宏列表失败: {e}")
            
    def _start_status_updates(self):
        """启动状态更新线程"""
        def update_status():
            while True:
                try:
                    if self.is_running:
                        status = self.controller.get_status()
                        self._update_status_display(status)
                    time.sleep(1)  # 每秒更新一次
                except:
                    break
                    
        self.status_update_thread = threading.Thread(target=update_status, daemon=True)
        self.status_update_thread.start()
        
    def _update_status_display(self, status: Dict[str, Any]):
        """更新状态显示"""
        try:
            # 更新状态标签
            if status["is_running"]:
                if status["is_paused"]:
                    self.status_label.config(text="状态: 暂停")
                else:
                    self.status_label.config(text="状态: 运行中")
            else:
                self.status_label.config(text="状态: 空闲")
                
            # 更新配置状态
            profile = status.get("current_profile", "无")
            self.profile_status_label.config(text=f"配置: {profile}")
            
            # 更新统计信息
            stats = status.get("stats", {})
            actions = stats.get("actions_executed", 0)
            observations = stats.get("observations_made", 0)
            errors = stats.get("errors_count", 0)
            self.stats_label.config(text=f"统计: 动作{actions} 观察{observations} 错误{errors}")
            
        except Exception as e:
            pass  # 忽略状态更新错误
            
    def _log_message(self, message: str):
        """添加日志消息"""
        try:
            timestamp = time.strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {message}\n"
            
            self.log_text.insert(tk.END, log_entry)
            self.log_text.see(tk.END)
            
            # 限制日志行数
            lines = self.log_text.get("1.0", tk.END).count('\n')
            if lines > 1000:
                self.log_text.delete("1.0", "100.0")
                
        except Exception as e:
            print(f"日志记录失败: {e}")
            
    def _clear_log(self):
        """清空日志"""
        self.log_text.delete("1.0", tk.END)
        
    def _export_log(self):
        """导出日志"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get("1.0", tk.END))
                self._log_message(f"日志已导出到: {filename}")
                
        except Exception as e:
            self._log_message(f"导出日志失败: {e}")
            
    def run(self):
        """运行界面"""
        try:
            self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
            self.root.mainloop()
        except Exception as e:
            print(f"界面运行失败: {e}")
            
    def _on_closing(self):
        """关闭窗口时的处理"""
        try:
            if self.is_running:
                self.controller.stop()
            self.root.destroy()
        except Exception as e:
            print(f"关闭失败: {e}")


def main():
    """主函数"""
    try:
        app = PuppeteerUI()
        app.run()
    except Exception as e:
        print(f"启动失败: {e}")


if __name__ == "__main__":
    main()
