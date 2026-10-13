"""实验专用 MCP：只提供当前项目文件清单和 pytest 测试摘要。"""
from pathlib import Path
import subprocess
import sys
from mcp.server.fastmcp import FastMCP

ROOT = Path(__file__).resolve().parent
server = FastMCP("lab-project")


@server.tool()
def project_files() -> list[str]:
    """列出消费统计项目源码、测试和示例数据，不扫描凭据或其他目录。"""
    paths = [ROOT / "expense.py", ROOT / "AGENTS.md", *sorted((ROOT / "tests").glob("test_*.py")),
             *sorted((ROOT / "data").glob("*.json"))]
    return [str(p.relative_to(ROOT)) for p in paths if p.is_file()]


@server.tool()
def run_project_tests() -> dict:
    """运行固定 pytest 命令，返回退出码和测试输出，不接受任意命令参数。"""
    result = subprocess.run([sys.executable, "-m", "pytest", "tests", "-q",
                             "--basetemp", str(ROOT / ".pytest-temp")], cwd=ROOT,
                            capture_output=True, text=True, timeout=60)
    return {"exit_code": result.returncode, "output": result.stdout + result.stderr}


if __name__ == "__main__":
    server.run(transport="stdio")
