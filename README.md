# 角色属性计算器

本项目为一个 Python 命令行程序，用于模拟游戏内角色在不同条件下的属性（如攻击力、防御力、生命值）变化，并自动进行边界值、异常值和逻辑一致性测试，帮助发现潜在的设计或配置错误。

## 主要功能
- 支持角色/物品属性成长、技能/效果叠加
- 支持自定义角色数据（CSV文件）
- 自动化边界值、异常值、逻辑一致性测试
- 详细日志与测试报告输出

## 文件说明
- `main.py`：主程序
- `characters.csv`：角色数据示例文件，可自定义扩展
- `test_report.csv`：自动化测试报告
- `test_report.log`：详细日志

## 依赖环境
- Python 3.7 及以上

## 使用方法

### 1. 运行自动化测试

```powershell
python main.py
```

运行后会自动进行边界值、异常值、逻辑一致性测试，并生成 `test_report.csv` 和 `test_report.log`。

### 2. 加载自定义角色数据并显示属性

编辑或新增 `characters.csv`，格式如下：

```
name,level,base_attack,base_defense,max_health,attack_growth,defense_growth,health_growth
勇者,1,15,8,120,2.5,1.2,10
法师,5,10,5,80,3.0,0.8,8
战士,10,20,12,200,1.8,1.5,15
```

然后运行：

```powershell
python main.py --csv characters.csv --show
```

即可在控制台看到每个角色的最终属性。

### 3. 参数说明
- `--csv <文件路径>`：指定角色数据CSV文件
- `--show`：显示CSV角色属性计算结果

## 扩展说明
- 可自定义/扩展角色字段、技能/效果模型
- 可拓展更多测试用例与规则

## 报告与日志
- `test_report.csv`：每个测试用例的输入、预期、实际、结论等
- `test_report.log`：详细计算与异常日志


