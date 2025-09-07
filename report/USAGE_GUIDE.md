# Puppeteer 使用指南

## 问题解决

如果您遇到"控制台直接结束"的问题，请按照以下步骤操作：

### 1. 运行诊断工具

```bash
python diagnose.py
```

这将检查所有依赖和配置是否正确。

### 2. 推荐启动方式

**方式一：使用批处理文件（推荐）**
```bash
# 英文版
start_puppeteer.bat

# 中文版
start_puppeteer_cn.bat

# 简化版
start.bat
```

**方式二：直接运行Python**
```bash
# 图形界面（推荐新手）
python main.py --mode ui

# 命令行模式
python main.py --mode cli --profile simple_test
```

**方式三：运行测试**
```bash
# 快速验证
python quick_test.py

# 完整测试
python test_modules.py
```

### 3. 常见问题解决

#### 问题1：批处理文件立即退出
**原因**：可能是编码问题或Python路径问题
**解决**：
1. 确保Python已正确安装
2. 使用 `python main.py --mode ui` 直接启动
3. 检查控制台编码设置

#### 问题2：依赖包缺失
**解决**：
```bash
pip install -r requirements.txt
```

#### 问题3：权限问题
**解决**：
1. 以管理员身份运行命令提示符
2. 确保有文件写入权限

#### 问题4：UI无法启动
**解决**：
```bash
pip install tk
```

### 4. 启动模式说明

#### 图形界面模式（推荐）
- 适合新手用户
- 提供友好的操作界面
- 支持配置管理和实时监控

#### 命令行模式
- 适合高级用户
- 支持脚本化操作
- 需要配置文件

#### 测试模式
- 验证系统功能
- 检查依赖和配置
- 诊断问题

### 5. 配置文件说明

#### simple_test.yaml
- 简化配置，无需模板文件
- 适合测试和验证
- 推荐新手使用

#### example_game.yaml
- 完整配置示例
- 需要模板文件
- 适合实际游戏使用

### 6. 使用步骤

1. **首次使用**：
   ```bash
   python diagnose.py  # 检查环境
   python quick_test.py  # 快速验证
   ```

2. **启动程序**：
   ```bash
   python main.py --mode ui  # 图形界面
   ```

3. **配置游戏**：
   - 在图形界面中创建配置文件
   - 或手动编辑 `profiles/` 目录下的YAML文件

4. **开始自动化**：
   - 选择配置文件
   - 点击"开始"按钮
   - 观察日志输出

### 7. 故障排除

如果程序仍然无法正常运行：

1. **检查Python版本**：
   ```bash
   python --version  # 需要Python 3.7+
   ```

2. **检查依赖**：
   ```bash
   pip list | findstr "mss opencv numpy pyautogui"
   ```

3. **重新安装依赖**：
   ```bash
   pip uninstall -r requirements.txt -y
   pip install -r requirements.txt
   ```

4. **清理缓存**：
   ```bash
   # 删除 __pycache__ 目录
   # 删除 .pyc 文件
   ```

### 8. 技术支持

如果问题仍然存在：

1. 运行 `python diagnose.py` 获取详细诊断信息
2. 检查 `logs/` 目录下的日志文件
3. 确保所有文件完整且未损坏
4. 尝试在干净的Python环境中重新安装

### 9. 注意事项

- 确保以管理员权限运行（用于输入控制）
- 避免在游戏运行时修改配置文件
- 定期备份配置文件
- 遵守游戏服务条款

## 快速开始

1. 双击 `start_puppeteer.bat`
2. 选择 "1. GUI Mode"
3. 在图形界面中创建配置
4. 点击"开始"按钮

就这么简单！
