"""命令行学习任务管理器：标准库实现，数据写入项目目录。"""
import argparse
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent / "tasks.json"


def load_tasks(path=DATA):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else []


def add_task(title, path=DATA):
    if not title.strip():
        raise ValueError("任务标题不能为空")
    tasks = load_tasks(path)
    task = {"id": max((t["id"] for t in tasks), default=0) + 1,
            "title": title.strip(), "done": False}
    tasks.append(task)
    path.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")
    return task


def finish_task(task_id, path=DATA):
    tasks = load_tasks(path)
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            path.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding="utf-8")
            return task
    raise ValueError(f"任务 {task_id} 不存在")


def main():
    parser = argparse.ArgumentParser(description="学习任务管理器")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add"); add.add_argument("title")
    sub.add_parser("list")
    done = sub.add_parser("done"); done.add_argument("id", type=int)
    args = parser.parse_args()
    try:
        if args.command == "add":
            print("已添加:", add_task(args.title))
        elif args.command == "done":
            print("已完成:", finish_task(args.id))
        else:
            for task in load_tasks():
                print(f'{task["id"]} [{"完成" if task["done"] else "待办"}] {task["title"]}')
    except ValueError as exc:
        parser.exit(1, f"错误: {exc}\n")


if __name__ == "__main__":
    main()
