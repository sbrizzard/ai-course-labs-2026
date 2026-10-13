# 学习任务管理器

作者：孙晞皓（241820001）。AI 辅助实现的命令行学习任务管理器。

Python 3.10+，项目本身不需要第三方依赖。

```sh
python3 task_manager.py add "完成实验2"
python3 task_manager.py list
python3 task_manager.py done 1
python3 -m pytest -q
```

数据文件相对程序位置保存，支持中文标题、连续编号、完成状态与输入检查。
