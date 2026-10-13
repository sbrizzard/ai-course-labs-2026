"""容器内运行的实验 Web 服务，同时示范输入输出持久化。"""
import json
import os
from pathlib import Path
from flask import Flask, jsonify

app = Flask(__name__)
DATA_DIR = Path(os.environ.get("DATA_DIR", "/data"))


@app.get("/")
def index():
    return "<h1>Hello Docker!</h1><p>241820001 孙晞皓 - 实验3</p>"


@app.get("/process")
def process():
    data = json.loads((DATA_DIR / "input.json").read_text(encoding="utf-8"))
    result = {"count": len(data["numbers"]), "sum": sum(data["numbers"]),
              "environment": os.environ.get("APP_ENV", "unknown")}
    (DATA_DIR / "output.json").write_text(json.dumps(result), encoding="utf-8")
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
