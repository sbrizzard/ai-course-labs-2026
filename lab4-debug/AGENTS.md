# 实验 4 开发规则

- 使用 Python 3.10+，中文解释观察、假设、计划、执行和验证。
- 源码放在 expense.py；测试放在 tests/；示例数据放在 data/。
- 测试命令：python -m pytest -q。Windows 可使用 ../../environment/venv/Scripts/python.exe。
- 先保留失败日志，再修复；不要把修改测试期望值当作修复。
- 用 Decimal 处理金额，明确拒绝负数，路径相对源码定位。
- 可以修改本项目文件；禁止删除项目外文件、读取凭据、推送远程仓库。
- 额外任务先读取 .opencode/skills/debug-cycle/SKILL.md。
