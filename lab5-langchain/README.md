# 实验5：课程学习助手

作者：孙晞皓，241820001。真实运行结果见 demo_results.json。

Python 3.10+，建议创建独立虚拟环境，然后安装 requirements.txt。

```sh
ollama pull qwen3:4b-instruct
ollama create qwen3-lab -f Modelfile
python -m pip install -r requirements.txt
python agent.py --demo --thread your-new-thread
python agent.py --thread your-new-thread
python lcel_demo.py
python -m pytest -q
```

默认本地端点为 http://127.0.0.1:11434；可以用 OLLAMA_URL 和 OLLAMA_MODEL 调整。
SQLite 状态保存在项目目录的 checkpoints.sqlite。重复 --demo 使用新的 thread_id，避免把旧实验消息重复加入历史。

三个工具分别做金额求和、日期差和本地课程知识查询。Agent 先进行工具调用，随后模型原生 JSON Schema 输出经过 StudyReply 校验，生成结构化结果。
Trim 只缩减本次模型输入，数据库仍保存完整历史。CLI 支持 q、quit、exit 退出。
