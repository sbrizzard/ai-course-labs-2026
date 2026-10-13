# 实验3：Docker Web 与 Compose

```sh
docker build -t sxh241820001-lab3:v1 .
docker run -d --name lab3-web -p 127.0.0.1:18000:8000 --mount type=bind,source=<data绝对路径>,target=/data sxh241820001-lab3:v1
```

访问 / 返回页面，/process 读取 data/input.json，生成 output.json。

在本机创建不提交到仓库的 .env，设置 MONGO_PASSWORD 与 WEB_PASSWORD，然后运行 docker compose -p sxh241820001-lab3 up -d --wait。Mongo Express 端口18081，用户名labviewer；数据库用户名labadmin。

Docker Hub 上传与验证已于2026-10-14完成。镜像：sbrizzard/sxh241820001-lab3:v1。

仓库：https://hub.docker.com/r/sbrizzard/sxh241820001-lab3

摘要：sha256:32269f8e267aa0fda528088fe7458762591c5b541b912844fd088917719cdfba

远程manifest检查、按摘要拉取与运行测试均通过，HTTP 200。
