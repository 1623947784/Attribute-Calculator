
# 角色属性计算器

一个简单的 Python 命令行工具，用于批量计算游戏角色属性并自动测试。

## 快速使用

1. 运行自动测试：
	 ```powershell
	 python main.py
	 ```
	 生成测试报告：`test_report.csv`、`test_report.log`

2. 计算自定义角色属性：
	 - 编辑 `characters.csv`，示例：
		 ```
		 name,level,base_attack,base_defense,max_health,attack_growth,defense_growth,health_growth,attack_bonus
		 勇者,1,15,8,120,2.5,1.2,10,50
		 法师,5,10,5,80,3.0,0.8,8,10
		 战士,10,20,12,200,1.8,1.5,15,20
		 ```
	 - 运行：
		 ```powershell
		 python main.py --csv characters.csv --show
		 ```

## 参数说明
- `--csv 文件`：指定角色数据文件
- `--show`：输出每个角色的属性

## 注意
- CSV表头字段需与示例一致，字段间用英文逗号分隔
- 支持 attack_bonus/defense_bonus/health_bonus 字段自动加成

如遇问题请检查CSV格式或查看日志。


