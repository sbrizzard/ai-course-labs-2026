import json
import pytest
from task_manager import add_task, finish_task, load_tasks


def test_add_and_persist(tmp_path):
    path = tmp_path / "tasks.json"
    assert add_task("学习 Linux", path)["id"] == 1
    assert load_tasks(path)[0]["title"] == "学习 Linux"
    assert add_task("学习 Git", path)["id"] == 2


def test_finish_and_missing(tmp_path):
    path = tmp_path / "tasks.json"
    add_task("提交报告", path)
    assert finish_task(1, path)["done"] is True
    assert json.loads(path.read_text(encoding="utf-8"))[0]["done"] is True
    with pytest.raises(ValueError):
        finish_task(99, path)


def test_blank_title(tmp_path):
    with pytest.raises(ValueError):
        add_task("  ", tmp_path / "tasks.json")
