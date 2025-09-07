# IDEA：人偶师（Puppeteer） — 核心构想（供 AI 与工程师快速理解）

> 简短一句话：构建一个轻量化、可配置的通用“操控臂”（Puppeteer），通过屏幕级感知 + 通用控制库 + 配置驱动的策略，实现对桌面程序/2D 游戏的自动化操控，后续扩展为行为树/状态机/LLM 驱动的智能决策层。

---

## 1. 核心目标（为什么做）
- 减少玩家/测试人员在重复性、低价值操作上的时间投入；
- 提供一个通用、可复用的操控层（输入合成 + 人类化参数），避免为每款游戏从零开始实现脚本；
- 以 Profile/配置驱动实现快速适配不同游戏/软件，并通过配置调整操控策略；
- 为未来接入更高级的决策（行为树、状态机、LLM）预留标准化的数据契约与接口。

---

## 2. 一句话 MVP（最小可行产物）
实现一个 Windows 上的轻量化闭环：**截屏（mss）→ 模板匹配（OpenCV）→ 配置驱动决策（YAML profile）→ 输入执行（PyAutoGUI/PyDirectInput）→ 日志（JSONL）**，并提供最小 UI 用于启动/停止与切换 Profile。

---

## 3. 核心构件（概念级）
- **控制库（Core Action Library）**：封装按键、鼠标、组合动作、节流与 humanize 参数；对外暴露简单同步/异步接口供上层调用。
- **感知层（Perception）**：以屏幕截取 + 模板匹配为 MVP，输出结构化 Observation（坐标、置信度、UI 状态）；后期可置换为模型检测或插件接入。
- **配置层（Profile）**：YAML/JSON 格式，描述 UI ROI、模板、按键映射、宏、策略权重（平衡/收益最大化/仅通关 等）。
- **决策层（Decision）**：初期为规则/阈值触发器与简单行为树片段；中期接入行为树或状态机引擎；长期可由 LLM 输出高层 Intent。
- **运行编排（Controller/Scheduler）**：任务队列、启动/停止、异常恢复与日志记录。
- **UI（Minimal Control Panel）**：启动/停止、Profile 切换、简易 overlay（日后可换为 Web Dashboard）。

---

## 4. 数据契约（最小版，供模块互操作）
- **Observation**：`{timestamp, scene, self:{hp_pct,...}, enemies:[{pos,confidence}], items:[]}`
- **Action**：`{type: press|click|combo, key, pos, humanize:{delay_ms,jitter}}`
- **Intent（后期）**：`{goal, policy_weights, time_budget_s}`

（要求：模块之间仅通过这些 JSON 结构通信，便于替换实现与审计）

---

## 5. 使用场景与策略示例
- 单机挂机：优先保证收益最大化，容错高，可用内存/注入方式（若合规）。
- 多人陪玩：优先玩家体验（humanize 严格、行为更自然、响应更稳定）。
- 通关导向：优先求生存/通关，速度优先。

策略通过 Profile 中的 policy_weights/模式字段调整。

---

## 6. MVP 主要任务（极简版 TODO）
- T1：项目骨架与依赖管理（Python venv，requirements）
- T2：实现 capture（mss）模块
- T3：实现 vision（OpenCV 模板匹配）模块
- T4：实现 input_provider（PyAutoGUI）库并封装 humanize
- T5：实现 Profile 加载（YAML）与示例 profile
- T6：实现 controller 主循环并能基于 Observation 触发 Action
- T7：实现最小 GUI（Tkinter）以启动/停止、切换 profile
- T8：实现日志（JSONL）与简单回放包导出

---

## 7. 发展路线（后续功能）
- 行为树 / 状态机 引擎（可视化编辑）
- 更健壮的感知（轻量检测器、ONNX 加速）
- LLM Adapter：高层 Intent 生成（带 Schema 校验与安全过滤）
- 插件系统与 profile 市场
- 更低延迟的输入实现（C++/Rust 层）

---

## 8. 风险与合规考量（要点）
- 避免未经授权的内存读写/注入、反作弊冲突；将内存/注入等高风险能力设为可选、需明确授权。
- 日志敏感信息隐私处理，不默认上传云端。
- 在多人在线场景中注意伦理/社区规则，不鼓励破坏游戏公平性的自动化行为。

---

## 9. 给 AI 的指令（如何用这份 IDEA）
1. 将文档中列出的 TODO 按序分解为代码任务，每个任务产出：实现文件、函数接口、简单注释、测试或手动验证步骤。
2. 生成的代码应严格遵守“数据契约”接口，便于模块替换与单元测试。
3. 每完成一个任务，记录日志样例与运行截图，便于回放与进一步调试。

---

## 10. 结语
该 IDEA 把你的设计思路抽象为短小、可执行的工程级指令，便于 AI 或工程师按步实现。需要我把某个 TODO 直接开始实现成代码、或把 IDEA 转为任务板（Trello/GitHub Issues）吗？

