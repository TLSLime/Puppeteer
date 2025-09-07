# 人偶师（Puppeteer） — MVP 整合设计（供 AI 阅读与构建）

> 目的：把“人偶师”设计蓝图中的“MVP 面向新手”的实现方案整合成一份清晰的 Markdown 文档，便于 AI 或自动化工具按块读取、理解与生成代码。文档已分块、标注 TODO，并包含示例代码与验收标准。

---

## 0. 快速概要（1 段）

目标是构建一个面向 Windows 的闭环 MVP：能够**截屏感知（CV）→ 基于配置的决策 → 模拟输入执行（鼠标/键盘）→ 日志记录与最小 UI 控制**。核心要求：对新手友好、优先使用 Python 开源库、实现可配置的 Profile 驱动流程并保证审计与回放能力。

---

## 1. 设计原则（若干要点，便于 AI/工程师快速抓住核心）

1. 手臂与大脑分离：动作执行（低延迟、可回放）与策略（配置/简单规则/后续可接 LLM）分离。
2. Profile 驱动：每个游戏通过 YAML 配置文件描述 UI 区域、键位映射、模板路径与宏，降低针对每个游戏编写脚本的成本。
3. 屏幕级感知优先：以屏幕截图 + OpenCV（模板匹配）作为 MVP 感知方式，后续支持模型检测或插件扩展。
4. 可观测与审计：所有动作/观测/意图写入日志，支持回放与简单分析。
5. 新手友好：首选 Python 生态（mss、OpenCV、PyAutoGUI、Tkinter、PyYAML、logging）。

---

## 2. MVP 模块概览（分条，便于 AI 模块化读取）

以下每一条为一个可独立实现的模块块，AI 或开发者可按此顺序实现或并行开发。

### 2.1 capture（截屏模块）
- 功能：高效截取前台游戏窗口或指定屏幕区域并返回 NumPy 图像数组。
- 推荐库：mss（首选），备选 pyautogui.screenshot / Pillow。
- 输入：profile.screen_region 或 full screen。
- 输出：BGR/灰度图像数组。
- 关键点：支持 ROI、缩放选项、帧率控制。

### 2.2 vision（视觉识别模块）
- 功能：模板匹配、简单的颜色/HSV 分割、OCR（可选）并输出结构化 Observation。
- 推荐库：OpenCV（cv2）、Tesseract（OCR 可选）。
- 输入：图像数组、profile.templates
- 输出：Observation JSON（见 §5 数据契约简化版）。
- 关键点：使用模板置信度阈值、ROI 优先处理、时序平滑（简单过滤）。

### 2.3 input_provider（输入合成模块）
- 功能：封装鼠标/键盘动作（move, click, press, combo），并支持 humanize 参数（延迟/抖动）。
- 推荐库：PyAutoGUI（首选），必要时 PyDirectInput / pynput。
- 输入：Action JSON / macro sequence
- 输出：动作执行结果（success/fail/latency），并写入日志。
- 关键点：提供 APM 节流、按键冷却、前台窗口校验。

### 2.4 config（配置系统）
- 功能：读取/解析 YAML Profile（UI 区域、模板路径、按键映射、宏、场景/行为树引用）。
- 推荐库：PyYAML
- 输入：profile.yaml
- 输出：程序可直接调用的配置对象/字典。

### 2.5 controller（主循环/逻辑）
- 功能：驱动截屏→识别→决策→动作的主循环，支持启动/停止/暂停/恢复。
- 关键点：时间步长（默认 100–200 ms）、失败恢复（弹窗、卡死）、与 UI 通信。

### 2.6 ui（最小控制面板）
- 功能：提供启动/停止、切换 Profile、显示当前状态/日志的最小 GUI。
- 推荐框架：Tkinter（内置，零依赖）或 PySimpleGUI（更简单的封装）。
- 关键点：与 controller 使用线程或队列通信（避免阻塞 UI）。

### 2.7 logging（日志与审计）
- 功能：记录 Action/Observation/System 日志（JSONL 格式可选），支持实时推送到 UI 控制台。
- 推荐：内置 logging，JSON 格式化（可使用 python-json-logger）。
- 输出：`puppeteer-YYYY-MM-DD.jsonl` 或 plain text 日志，包含 timestamp、type、payload。

---

## 3. 简化的数据契约（供模块间通信，JSON 格式示例）

### Observation（简化）
```json
{
  "timestamp": 0,
  "scene": "dungeon",
  "self": {"hp_pct": 0.85},
  "enemies": [{"id":"e1","pos":[x,y],"confidence":0.92}],
  "items": []
}
```

### Action（简化）
```json
{
  "type":"press", "key":"q", "humanize": {"delay_ms": [80,140]}
}
```

---

## 4. 参考示例代码（可直接复制运行 / 作为 AI 生成器的模板）

> 注意：示例为最小化可运行片段，用于快速验证模块功能，后续需包装成类/模块并加入异常处理、日志等。

### 4.1 截屏 + 模板匹配示例（capture + vision）

```python
import mss, cv2, numpy as np
with mss.mss() as sct:
    screen = np.array(sct.grab(sct.monitors[1]))
gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
template = cv2.imread('assets/enemy.png', cv2.IMREAD_GRAYSCALE)
res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
loc = np.where(res >= 0.8)
for pt in zip(*loc[::-1]):
    print('found enemy at', pt)
```

### 4.2 输入合成示例（input_provider）

```python
import pyautogui
pyautogui.moveTo(400,300, duration=0.12)
pyautogui.click()
pyautogui.press('q')
```

### 4.3 YAML 配置示例（profile.yaml）

```yaml
profile: example_game
screen_region: [0,0,800,600]
keymap:
  attack: 'q'
  jump: 'space'
templates:
  enemy: 'assets/enemy.png'
macros:
  combo1: ['attack','jump','attack']
```

### 4.4 最小 Tkinter 控制面板示例（ui.py）

```python
import tkinter as tk
from threading import Thread

def start_task():
    # 启动后台控制器线程
    Thread(target=controller.run, daemon=True).start()

def stop_task():
    controller.stop()

root = tk.Tk(); root.title('Puppeteer')
start_btn = tk.Button(root, text='开始', command=start_task)
stop_btn = tk.Button(root, text='停止', command=stop_task)
status = tk.Label(root, text='状态: 空闲')
start_btn.pack(); stop_btn.pack(); status.pack()
root.mainloop()
```

---

## 5. TODO 清单（分条/可读性强，含验收标准，便于 AI 或 CI 系统拆解）

> 说明：将 TODO 按优先级分组（High / Medium / Low）。每项包含：`id`、`title`、`priority`、`deps`、`input`、`output`、`acceptance`。

### 高优先（MVP 闭环）

- **T-MVP-001 — 初始化项目结构**
  - priority: HIGH
  - deps: []
  - input: None
  - output: 代码仓库框架（`capture.py, vision.py, input.py, config.py, controller.py, ui.py, logger.py, requirements.txt`）
  - acceptance: 项目能被 `python -m` 启动并打印欢迎信息

- **T-MVP-002 — capture: 实现基础截屏**
  - priority: HIGH
  - deps: [T-MVP-001]
  - input: mss 库
  - output: `capture.capture(region=None)` 返回 NumPy 图像数组
  - acceptance: 在目标机器上运行，函数能在 100 ms 内返回一帧 1080p 截图（或合适性能指标）

- **T-MVP-003 — vision: 模板匹配实现**
  - priority: HIGH
  - deps: [T-MVP-002]
  - input: 截图、模板图片
  - output: 简化 Observation（包含检测到的对象及置信度）
  - acceptance: 在给定样本集中，模板匹配能识别样本中指定元素，误报低于阈值（例如阈值 0.8）

- **T-MVP-004 — input_provider: 基本输入执行**
  - priority: HIGH
  - deps: [T-MVP-001]
  - input: Action 请求（按键/鼠标）
  - output: 执行动作并返回 success/fail
  - acceptance: 在前台窗口中执行按键/点击，目标控件能响应（可人工验证）

- **T-MVP-005 — config: YAML Profile 解析**
  - priority: HIGH
  - deps: [T-MVP-001]
  - input: example profile.yaml
  - output: 可在程序中访问的配置对象
  - acceptance: 切换 profile 后 controller 使用新配置

- **T-MVP-006 — controller: 主循环实现**
  - priority: HIGH
  - deps: [T-MVP-002, T-MVP-003, T-MVP-004, T-MVP-005]
  - input: Profile、Observation
  - output: 连续运行的主循环（截屏→识别→动作→日志）
  - acceptance: 程序在 UI 中点击“开始”后能按照配置对模拟场景做出动作（检测到 enemy 则按 attack）

- **T-MVP-007 — ui: 最小控制面板**
  - priority: HIGH
  - deps: [T-MVP-006]
  - input: controller 状态
  - output: 启动/停止按钮，状态显示，简单日志输出区域
  - acceptance: 用户能通过 UI 启停主循环并看到实时状态/日志

- **T-MVP-008 — logger: JSONL 或文本日志实现**
  - priority: HIGH
  - deps: [T-MVP-006]
  - input: 模块事件（action/observation/system）
  - output: `logs/puppeteer-YYYY-MM-DD.jsonl`（或 .log）
  - acceptance: 每次动作和关键观测写入日志并可被检索

### 中优先（增强与易用性）

- **T-MVP-010 — humanize 参数与节流**
  - priority: MEDIUM
  - deps: [T-MVP-004]
  - input: humanize config（delay distributions, jitter）
  - output: 实际动作加入随机延时与轨迹
  - acceptance: 人为可视化轨迹并验证延时在预期范围

- **T-MVP-011 — ROI 配置与多模板支持**
  - priority: MEDIUM
  - deps: [T-MVP-003, T-MVP-005]
  - input: profile.ui_templates（多模板）
  - output: 更高鲁棒性的检测结果
  - acceptance: 在不同分辨率/场景下识别率提高

- **T-MVP-012 — 回放包导出（日志+视频/截图）**
  - priority: MEDIUM
  - deps: [T-MVP-008]
  - input: session logs + screenshots
  - output: zip 回放包（logs + screenshots + metadata）
  - acceptance: 能从回放包里重建运行过程并逐步查看日志

### 低优先（长期/可选）

- **T-MVP-020 — 使用轻量目标检测模型提升感知**
  - priority: LOW
  - deps: [T-MVP-003]
  - input: 训练数据或预训练模型（YOLOv8/ONNX）
  - output: 更鲁棒的检测 pipeline
  - acceptance: 在噪声场景下检测率明显提升

- **T-MVP-021 — 替换 UI 为 Web Dashboard（Flask + Bootstrap）**
  - priority: LOW
  - deps: [T-MVP-007]
  - input: 程序内 WebSocket / REST 端点
  - output: 可远程控制的 Web UI
  - acceptance: 可通过浏览器进行启动/停止并查看日志

---

## 6. 迭代建议与时间线（适合单人/小团队）

- Sprint 0（准备）：1–2 天，初始化 repo、环境与依赖（requirements.txt）。
- Sprint 1（核心功能）：2 周，实现 capture、vision（模板匹配）与 input_provider，写出示例脚本并验证。完成 T-MVP-001 ~ T-MVP-004。
- Sprint 2（集成与 UI）：1 周，完成 config、controller、ui、logger（T-MVP-005 ~ T-MVP-008）。验证完整闭环。
- Sprint 3（稳固与优化）：1 周，加入 humanize、ROI 与回放导出（T-MVP-010 ~ T-MVP-012）。

总体 MVP 预计 4–6 周（单人完整开发）或 2–4 周（2 人小组并行）。

---

## 7. 给 AI 的说明（如何按块生成代码）

- 优先顺序：按 TODO 高优先级顺序逐条生成代码并运行测试。每个 TODO 应当输出：实现文件、函数签名、简要注释、单元/集成测试样例（或手动测试步骤）。
- 接口契约：各模块之间使用简化 JSON 数据契约（见 §3），AI 在生成代码时必须遵守该输入/输出格式。
- 可执行示例：至少生成一套能运行的 demo（`run_demo.py`），演示从读取 profile、截屏、检测模板到触发按键的完整闭环。
- 日志要求：每次动作与观测都至少写入日志（INFO 级别），以便审计与回放。

---

## 8. 后续扩展建议（简要）

- LLM Adapter：将来可加入 LLM 仅输出高层 Intent（JSON），由本地 Decision Layer 将 Intent 分解为 Action。
- 插件/Profile 市场：Profile 继承机制与社区共享平台。
- Windows 原生低延迟输入替换模块（C++/Rust）以支持更高精度需求。

---

## 9. 结语

该 Markdown 文件已将“新手友好”的实现路线、模块划分、示例代码与 TODO 清单合并成一份便于 AI 读取与自动生成的蓝图。你可以让 AI 直接根据 `T-MVP-00x` 任务逐条生成代码、测试用例与文档，也可以指示我直接开始为某个 TODO 输出实现代码。



