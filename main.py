import csv
# 用于日志记录
import logging
# 类型提示
from typing import List, Optional


# 日志配置，既输出到文件也输出到控制台
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler('test_report.log', encoding='utf-8'), logging.StreamHandler()]
)


# 角色最大等级
MAX_LEVEL = 100


class Effect:
    """
    技能或效果类，表示对角色属性的增益/减益效果
    attack_bonus_percent/defense_bonus_percent/health_bonus_percent: 百分比加成
    duration: 持续回合数（可扩展）
    """
    def __init__(self, name: str, attack_bonus_percent: float = 0.0, defense_bonus_percent: float = 0.0, health_bonus_percent: float = 0.0, duration: int = 1):
        self.name = name
        self.attack_bonus_percent = attack_bonus_percent
        self.defense_bonus_percent = defense_bonus_percent
        self.health_bonus_percent = health_bonus_percent
        self.duration = duration


class Character:
    """
    角色类，包含基础属性、成长、效果列表及属性计算方法
    """
    def __init__(self, name: str, level: int, base_attack: float, base_defense: float, max_health: float, attack_growth: float = 0.0, defense_growth: float = 0.0, health_growth: float = 0.0):
        self.name = name  # 角色名
        self.level = level  # 等级
        self.base_attack = base_attack  # 基础攻击
        self.base_defense = base_defense  # 基础防御
        self.max_health = max_health  # 基础生命
        self.attack_growth = attack_growth  # 攻击成长
        self.defense_growth = defense_growth  # 防御成长
        self.health_growth = health_growth  # 生命成长
        self.effects: List[Effect] = []  # 当前作用于角色的效果列表

    def apply_effect(self, effect: Effect):
        """施加一个效果到角色上（可叠加）"""
        self.effects.append(effect)

    def clear_effects(self):
        """清除所有效果（用于测试或回合重置）"""
        self.effects = []

    def calculate_final_attributes(self):
        """
        计算最终属性：
        - 基础属性 + 成长
        - 所有效果的百分比加成叠加
        """
        attack = self.base_attack + (self.level - 1) * self.attack_growth
        defense = self.base_defense + (self.level - 1) * self.defense_growth
        health = self.max_health + (self.level - 1) * self.health_growth
        # 叠加所有效果的百分比加成
        attack_bonus = sum(e.attack_bonus_percent for e in self.effects)
        defense_bonus = sum(e.defense_bonus_percent for e in self.effects)
        health_bonus = sum(e.health_bonus_percent for e in self.effects)
        final_attack = attack * (1 + attack_bonus / 100)
        final_defense = defense * (1 + defense_bonus / 100)
        final_health = health * (1+ health_bonus / 100)
        return {
            'final_attack': final_attack,
            'final_defense': final_defense,
            'final_health': final_health
        }

def load_characters_from_csv(csv_path: str) -> List[Character]:
    """
    从CSV文件加载角色数据，支持自定义字段扩展。
    每行数据转为Character对象，异常行自动记录日志。
    """
    characters = []
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                c = Character(
                    name=row['name'],
                    level=int(row['level']),
                    base_attack=float(row['base_attack']),
                    base_defense=float(row['base_defense']),
                    max_health=float(row['max_health']),
                    attack_growth=float(row.get('attack_growth', 0)),
                    defense_growth=float(row.get('defense_growth', 0)),
                    health_growth=float(row.get('health_growth', 0)),
                )
                # 自动读取attack_bonus/defense_bonus/health_bonus等加成字段
                attack_bonus = 0.0
                defense_bonus = 0.0
                health_bonus = 0.0
                # 兼容不同分隔符（有些csv编辑器会用全角逗号）
                for k in row:
                    if 'attack_bonus' in k:
                        try:
                            attack_bonus = float(row[k])
                        except:
                            pass
                    if 'defense_bonus' in k:
                        try:
                            defense_bonus = float(row[k])
                        except:
                            pass
                    if 'health_bonus' in k:
                        try:
                            health_bonus = float(row[k])
                        except:
                            pass
                if attack_bonus or defense_bonus or health_bonus:
                    c.apply_effect(Effect('CSV加成', attack_bonus_percent=attack_bonus, defense_bonus_percent=defense_bonus, health_bonus_percent=health_bonus))
                characters.append(c)
            except Exception as e:
                logging.error(f"加载角色失败: {row}, 错误: {e}")
    return characters

def boundary_and_exception_tests():
    """
    自动化边界值与异常值测试：
    - 遍历极端/非法输入，检查属性计算合理性与异常处理
    - 结果写入 test_report.csv
    """
    test_cases = [
        # 边界值
        {'desc': 'level=0', 'level': 0, 'base_attack': 10, 'attack_growth': 2},
        {'desc': 'level=MAX_LEVEL', 'level': MAX_LEVEL, 'base_attack': 10, 'attack_growth': 2},
        {'desc': 'base_attack=0', 'level': 10, 'base_attack': 0, 'attack_growth': 2},
        {'desc': 'attack_growth=-10', 'level': 10, 'base_attack': 10, 'attack_growth': -10},
        {'desc': 'effect_percent=200%', 'level': 10, 'base_attack': 10, 'attack_growth': 2, 'effect': Effect('超高加成', attack_bonus_percent=200)},
        # 异常值
        {'desc': '负等级', 'level': -1, 'base_attack': 10, 'attack_growth': 2},
        {'desc': '非数值字符串', 'level': 'abc', 'base_attack': 10, 'attack_growth': 2},
    ]
    report = []
    for case in test_cases:
        try:
            # 构造角色对象
            c = Character(
                name='测试角色',
                level=int(case['level']),
                base_attack=float(case['base_attack']),
                base_defense=5,
                max_health=100,
                attack_growth=float(case['attack_growth'])
            )
            # 如有特殊效果，施加
            if 'effect' in case:
                c.apply_effect(case['effect'])
            attrs = c.calculate_final_attributes()
            # 合理性检查：攻击≥0，生命>0
            pass_check = attrs['final_attack'] >= 0 and attrs['final_health'] > 0
            report.append([
                case['desc'],
                str(case),
                'final_attack >= 0, final_health > 0',
                str(attrs),
                'Pass' if pass_check else 'Fail',
                '' if pass_check else '属性值不合理'
            ])
            logging.info(f"测试: {case['desc']} 输入: {case} 结果: {attrs} 状态: {'Pass' if pass_check else 'Fail'}")
        except Exception as e:
            # 异常处理
            report.append([
                case['desc'],
                str(case),
                '应抛出异常或记录错误',
                '',
                'Error',
                str(e)
            ])
            logging.error(f"测试: {case['desc']} 输入: {case} 错误: {e}")
    # 写入测试报告
    with open('test_report.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['测试项描述', '输入参数', '预期行为', '实际行为', '测试状态', '失败原因/错误信息'])
        writer.writerows(report)
    print('测试完成，报告已生成 test_report.csv')

def logic_consistency_tests():
    """
    逻辑一致性测试：
    - 检查效果叠加是否为线性相加
    - 检查正负效果冲突时是否正确抵消
    """
    # 叠加规则测试：两个+10%攻击效果应为+20%
    c = Character('叠加测试', 10, 10, 5, 100, attack_growth=2)
    c.apply_effect(Effect('攻击+10%', attack_bonus_percent=10))
    c.apply_effect(Effect('攻击+10%', attack_bonus_percent=10))
    attrs = c.calculate_final_attributes()
    expected = (10 + (10 - 1) * 2) * 1.2
    pass_check = abs(attrs['final_attack'] - expected) < 1e-6
    logging.info(f"叠加测试: 期望 {expected}, 实际 {attrs['final_attack']}, 状态: {'Pass' if pass_check else 'Fail'}")
    # 冲突规则测试：+10%和-10%应抵消
    c.clear_effects()
    c.apply_effect(Effect('攻击+10%', attack_bonus_percent=10))
    c.apply_effect(Effect('攻击-10%', attack_bonus_percent=-10))
    attrs2 = c.calculate_final_attributes()
    expected2 = (10 + (10 - 1) * 2) * 1.0
    pass_check2 = abs(attrs2['final_attack'] - expected2) < 1e-6
    logging.info(f"冲突测试: 期望 {expected2}, 实际 {attrs2['final_attack']}, 状态: {'Pass' if pass_check2 else 'Fail'}")
    print('逻辑一致性测试完成，详细见 test_report.log')

import argparse
import os

def main():
    """
    主程序入口：
    - 支持命令行参数加载自定义CSV并显示属性
    - 自动执行边界、异常、逻辑一致性测试
    """
    parser = argparse.ArgumentParser(description='属性计算器自动测试')
    parser.add_argument('--csv', type=str, default=None, help='角色数据CSV文件路径')
    parser.add_argument('--show', action='store_true', help='显示CSV角色属性计算结果')
    args = parser.parse_args()

    print('--- 属性计算器自动测试 ---')
    boundary_and_exception_tests()
    logic_consistency_tests()

    # 如指定csv参数，加载并显示角色属性
    if args.csv and os.path.exists(args.csv):
        chars = load_characters_from_csv(args.csv)
        print(f'从 {args.csv} 加载角色 {len(chars)} 个:')
        for c in chars:
            attrs = c.calculate_final_attributes()
            print(f"角色: {c.name} 等级: {c.level} 攻击: {attrs['final_attack']:.2f} 防御: {attrs['final_defense']:.2f} 生命: {attrs['final_health']:.2f}")
    elif args.csv:
        print(f'未找到CSV文件: {args.csv}')
    print('全部测试完成。')

if __name__ == '__main__':
    main()
