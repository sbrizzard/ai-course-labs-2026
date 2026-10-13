# 实验3：Docker Web 与 Compose

```sh
docker build -t sxh241820001-lab3:v1 .
docker run -d --name lab3-web -p 127.0.0.1:18000:8000 --mount type=bind,source=<data绝对路径>,target=/data sxh241820001-lab3:v1
```

访问 / 返回页面，/process 读取 data/input.json，生成 output.json。

在本机创建不提交到仓库的 .env，设置 MONGO_PASSWORD 与 WEB_PASSWORD，然后运行 docker compose -p sxh241820001-lab3 up -d --wait。Mongo Express 端口18081，用户名labviewer；数据库用户名labadmin。

Docker Hub 上传尚待账号注册与登录；本地镜像已构建并运行，不能将本地成功等同于上传成功。
