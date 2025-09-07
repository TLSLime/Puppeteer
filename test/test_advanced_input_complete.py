# -*- coding: utf-8 -*-
"""
完整的高级输入功能测试脚本
测试键盘、鼠标、游戏手柄等所有高级输入功能
"""

import sys
import os
import time
import json

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_advanced_input_manager():
    """测试高级输入管理器"""
    print("=" * 60)
    print("测试高级输入管理器")
    print("=" * 60)
    
    try:
        from puppeteer.advanced_input import AdvancedInputManager
        
        manager = AdvancedInputManager(humanize_enabled=True)
        print(f"✓ 高级输入管理器初始化成功")
        print(f"  使用方法: {manager.get_input_method()}")
        
        # 测试键盘操作
        print("\n测试键盘操作...")
        
        # 单次按键
        success = manager.press_key("space")
        print(f"  单次按键 (space): {'✓' if success else '✗'}")
        
        # 长按按键
        success = manager.press_key("a", duration=0.3)
        print(f"  长按按键 (a, 0.3s): {'✓' if success else '✗'}")
        
        # 组合键
        success = manager.press_key_combination(["ctrl", "c"])
        print(f"  组合键 (Ctrl+C): {'✓' if success else '✗'}")
        
        # 同时按键
        success = manager.press_key_simultaneous(["shift", "tab"])
        print(f"  同时按键 (Shift+Tab): {'✓' if success else '✗'}")
        
        # 文本输入
        success = manager.type_text_with_delay("Hello World")
        print(f"  文本输入: {'✓' if success else '✗'}")
        
        # 测试鼠标操作
        print("\n测试鼠标操作...")
        
        # 普通点击
        success = manager.click(400, 300)
        print(f"  普通点击 (400,300): {'✓' if success else '✗'}")
        
        # 长按点击
        success = manager.click(400, 300, duration=0.3)
        print(f"  长按点击 (400,300, 0.3s): {'✓' if success else '✗'}")
        
        # 拖拽
        success = manager.drag(100, 100, 200, 200)
        print(f"  拖拽 (100,100 -> 200,200): {'✓' if success else '✗'}")
        
        # 滚轮
        success = manager.scroll(400, 300, "up", 3)
        print(f"  滚轮 (向上3次): {'✓' if success else '✗'}")
        
        # 测试游戏手柄操作
        print("\n测试游戏手柄操作...")
        
        # 游戏手柄按钮
        success = manager.press_gamepad_button("a")
        print(f"  游戏手柄按钮 (A): {'✓' if success else '✗'}")
        
        # 游戏手柄长按
        success = manager.press_gamepad_button("b", duration=0.3)
        print(f"  游戏手柄长按 (B, 0.3s): {'✓' if success else '✗'}")
        
        # 摇杆操作
        success = manager.move_gamepad_stick("left", "up", 0.5)
        print(f"  摇杆操作 (左摇杆向上): {'✓' if success else '✗'}")
        
        # 测试宏操作
        print("\n测试宏操作...")
        
        macro = [
            {"type": "key_press", "key": "space"},
            {"type": "delay", "delay": 0.1},
            {"type": "mouse_click", "x": 400, "y": 300},
            {"type": "delay", "delay": 0.1},
            {"type": "type_text", "text": "Test"},
            {"type": "delay", "delay": 0.1},
            {"type": "gamepad_button", "button": "a"}
        ]
        
        results = manager.execute_macro(macro)
        success_count = sum(1 for r in results if r["success"])
        print(f"  宏操作: {success_count}/{len(results)} 成功")
        
        # 显示配置
        config = manager.get_humanize_config()
        print(f"\n人性化配置: {len(config)} 项")
        
        return True
        
    except Exception as e:
        print(f"✗ 高级输入管理器测试失败: {e}")
        return False


def test_gamepad_simulator():
    """测试游戏手柄模拟器"""
    print("\n" + "=" * 60)
    print("测试游戏手柄模拟器")
    print("=" * 60)
    
    try:
        from puppeteer.gamepad_simulator import GamepadSimulator, GamepadType, GamepadButton, GamepadStick
        
        # 测试Xbox手柄
        print("\n测试Xbox手柄...")
        xbox = GamepadSimulator(GamepadType.XBOX, humanize_enabled=True)
        print(f"✓ Xbox手柄模拟器初始化成功")
        
        # 按钮操作
        success = xbox.press_button(GamepadButton.A)
        print(f"  按下A按钮: {'✓' if success else '✗'}")
        
        success = xbox.press_button(GamepadButton.B, duration=0.3)
        print(f"  长按B按钮 (0.3s): {'✓' if success else '✗'}")
        
        success = xbox.press_button(GamepadButton.X)
        print(f"  按下X按钮: {'✓' if success else '✗'}")
        
        success = xbox.press_button(GamepadButton.Y)
        print(f"  按下Y按钮: {'✓' if success else '✗'}")
        
        # 肩键和扳机
        success = xbox.press_button(GamepadButton.LB)
        print(f"  按下LB按钮: {'✓' if success else '✗'}")
        
        success = xbox.press_button(GamepadButton.RB)
        print(f"  按下RB按钮: {'✓' if success else '✗'}")
        
        success = xbox.set_trigger("lt", 0.8)
        print(f"  设置左扳机 (0.8): {'✓' if success else '✗'}")
        
        success = xbox.set_trigger("rt", 0.6)
        print(f"  设置右扳机 (0.6): {'✓' if success else '✗'}")
        
        # 摇杆操作
        success = xbox.move_stick(GamepadStick.LEFT, 0.5, 0.5)
        print(f"  移动左摇杆 (0.5, 0.5): {'✓' if success else '✗'}")
        
        success = xbox.move_stick(GamepadStick.RIGHT, -0.3, 0.7)
        print(f"  移动右摇杆 (-0.3, 0.7): {'✓' if success else '✗'}")
        
        # 方向键
        success = xbox.press_button(GamepadButton.DPAD_UP)
        print(f"  按下上方向键: {'✓' if success else '✗'}")
        
        success = xbox.press_button(GamepadButton.DPAD_DOWN)
        print(f"  按下下方向键: {'✓' if success else '✗'}")
        
        success = xbox.press_button(GamepadButton.DPAD_LEFT)
        print(f"  按下左方向键: {'✓' if success else '✗'}")
        
        success = xbox.press_button(GamepadButton.DPAD_RIGHT)
        print(f"  按下右方向键: {'✓' if success else '✗'}")
        
        # 测试PlayStation手柄
        print("\n测试PlayStation手柄...")
        ps = GamepadSimulator(GamepadType.PLAYSTATION, humanize_enabled=True)
        print(f"✓ PlayStation手柄模拟器初始化成功")
        
        # PlayStation按钮
        success = ps.press_button(GamepadButton.CROSS)
        print(f"  按下X按钮: {'✓' if success else '✗'}")
        
        success = ps.press_button(GamepadButton.CIRCLE)
        print(f"  按下O按钮: {'✓' if success else '✗'}")
        
        success = ps.press_button(GamepadButton.SQUARE)
        print(f"  按下□按钮: {'✓' if success else '✗'}")
        
        success = ps.press_button(GamepadButton.TRIANGLE)
        print(f"  按下△按钮: {'✓' if success else '✗'}")
        
        # 测试组合操作
        print("\n测试组合操作...")
        combo = [
            {"type": "button_press", "button": "a"},
            {"type": "delay", "delay": 0.1},
            {"type": "stick_move", "stick": "left", "x": 1.0, "y": 0.0},
            {"type": "delay", "delay": 0.2},
            {"type": "button_press", "button": "b"},
            {"type": "delay", "delay": 0.1},
            {"type": "trigger_set", "trigger": "lt", "value": 0.5}
        ]
        
        success = xbox.execute_combo(combo)
        print(f"  组合操作: {'✓' if success else '✗'}")
        
        # 显示状态
        states = xbox.get_all_states()
        print(f"\n当前状态:")
        print(f"  按钮状态: {len(states['buttons'])} 个")
        print(f"  摇杆状态: {len(states['sticks'])} 个")
        print(f"  手柄类型: {states['gamepad_type']}")
        print(f"  人性化: {states['humanize_enabled']}")
        
        return True
        
    except Exception as e:
        print(f"✗ 游戏手柄模拟器测试失败: {e}")
        return False


def test_input_integration():
    """测试输入集成"""
    print("\n" + "=" * 60)
    print("测试输入集成")
    print("=" * 60)
    
    try:
        from puppeteer.advanced_input import AdvancedInputManager
        from puppeteer.gamepad_simulator import GamepadSimulator, GamepadType
        
        # 创建管理器
        manager = AdvancedInputManager(humanize_enabled=True)
        gamepad = GamepadSimulator(GamepadType.XBOX, humanize_enabled=True)
        
        print("✓ 输入管理器集成成功")
        
        # 测试混合操作
        print("\n测试混合操作...")
        
        # 键盘 + 鼠标
        success1 = manager.press_key("space")
        success2 = manager.click(400, 300)
        print(f"  键盘+鼠标: {'✓' if success1 and success2 else '✗'}")
        
        # 游戏手柄 + 键盘
        success1 = gamepad.press_button(GamepadButton.A)
        success2 = manager.press_key("enter")
        print(f"  游戏手柄+键盘: {'✓' if success1 and success2 else '✗'}")
        
        # 复杂宏操作
        complex_macro = [
            {"type": "key_press", "key": "ctrl"},
            {"type": "mouse_click", "x": 400, "y": 300},
            {"type": "delay", "delay": 0.1},
            {"type": "type_text", "text": "Complex"},
            {"type": "delay", "delay": 0.1},
            {"type": "key_press", "key": "enter"}
        ]
        
        results = manager.execute_macro(complex_macro)
        success_count = sum(1 for r in results if r["success"])
        print(f"  复杂宏操作: {success_count}/{len(results)} 成功")
        
        return True
        
    except Exception as e:
        print(f"✗ 输入集成测试失败: {e}")
        return False


def test_performance():
    """测试性能"""
    print("\n" + "=" * 60)
    print("性能测试")
    print("=" * 60)
    
    try:
        from puppeteer.advanced_input import AdvancedInputManager
        
        manager = AdvancedInputManager(humanize_enabled=False)  # 关闭人性化以提高性能
        
        # 测试键盘性能
        print("测试键盘性能...")
        start_time = time.time()
        for i in range(20):
            manager.press_key("space")
        end_time = time.time()
        keyboard_time = end_time - start_time
        print(f"  20次按键耗时: {keyboard_time:.3f}秒")
        print(f"  平均每次: {keyboard_time/20*1000:.1f}ms")
        
        # 测试鼠标性能
        print("\n测试鼠标性能...")
        start_time = time.time()
        for i in range(10):
            manager.click(100 + i * 10, 100 + i * 10)
        end_time = time.time()
        mouse_time = end_time - start_time
        print(f"  10次点击耗时: {mouse_time:.3f}秒")
        print(f"  平均每次: {mouse_time/10*1000:.1f}ms")
        
        # 测试宏操作性能
        print("\n测试宏操作性能...")
        macro = [
            {"type": "key_press", "key": "space"},
            {"type": "mouse_click", "x": 400, "y": 300},
            {"type": "type_text", "text": "Test"}
        ]
        
        start_time = time.time()
        for i in range(5):
            manager.execute_macro(macro)
        end_time = time.time()
        macro_time = end_time - start_time
        print(f"  5次宏操作耗时: {macro_time:.3f}秒")
        print(f"  平均每次: {macro_time/5*1000:.1f}ms")
        
        return True
        
    except Exception as e:
        print(f"✗ 性能测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("Puppeteer 高级输入功能完整测试")
    print("=" * 80)
    
    # 等待用户准备
    print("请确保:")
    print("1. 有一个文本编辑器或记事本打开")
    print("2. 鼠标和键盘可以正常使用")
    print("3. 准备好观察测试结果")
    
    input("\n按回车键开始测试...")
    
    tests = [
        ("高级输入管理器", test_advanced_input_manager),
        ("游戏手柄模拟器", test_gamepad_simulator),
        ("输入集成", test_input_integration),
        ("性能测试", test_performance)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name}测试异常: {e}")
            results.append((test_name, False))
    
    # 显示测试结果
    print("\n" + "=" * 80)
    print("测试结果汇总")
    print("=" * 80)
    
    success_count = 0
    for test_name, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"{test_name}: {status}")
        if success:
            success_count += 1
    
    print(f"\n总体结果: {success_count}/{len(results)} 测试通过")
    
    if success_count == len(results):
        print("🎉 所有测试通过！高级输入功能工作正常")
        print("\n功能特性:")
        print("✓ 单次按键和长按支持")
        print("✓ 组合键和同时按键")
        print("✓ 鼠标点击、拖拽、滚轮")
        print("✓ 游戏手柄按钮和摇杆模拟")
        print("✓ 宏操作和组合操作")
        print("✓ 人性化参数配置")
        print("✓ 高性能输入处理")
    else:
        print("⚠️ 部分测试失败，请检查错误信息")
    
    return success_count == len(results)


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n用户中断测试")
        sys.exit(1)
    except Exception as e:
        print(f"\n测试过程中发生异常: {e}")
        sys.exit(1)
