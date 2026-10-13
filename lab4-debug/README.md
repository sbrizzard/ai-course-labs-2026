# 实验4：消费统计 Debug 项目

最终版本已在 Ubuntu 中通过原有的8项测试。原始缺陷和中间失败记录保存在交付包 evidence 中。

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q --basetemp .pytest-temp
opencode mcp list
opencode
```

项目规则见 AGENTS.md，Skill 位于 .opencode/skills/debug-cycle/SKILL.md。
使用 opencode.example.json 配置示例时，根据本机模型端点调整 baseURL，再另存为 opencode.json。
项目 MCP 只提供文件清单和固定测试命令，不执行任意用户传入命令。

权限实验：python3 --version 被 allow 执行；printf approval-check 触发 ask，非交互 CLI 自动拒绝；rm --version 被 deny 拦截，没有删除任何文件。
