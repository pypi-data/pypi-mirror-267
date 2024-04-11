#!/usr/bin/env bash
# @Project      : AI @by PyCharm
# @Time         : 2024/3/22 08:40
# @Author       : betterme
# @Email        : 313303303@qq.com
# @Software     : PyCharm
# @Description  :

#docker run -it -d --init --name emohaa-free-api -p 38766:8000 -e TZ=Asia/Shanghai vinlic/emohaa-free-api

IMAGE=step-free-api
PORT=39001
docker run -it -d --init --name $IMAGE -p $PORT:8000 -e TZ=Asia/Shanghai vinlic/$IMAGE

IMAGE=kimi-free-api
PORT=39002
docker run -it -d --init --name $IMAGE -p $PORT:8000 -e TZ=Asia/Shanghai vinlic/$IMAGE



IMAGE=glm-free-api
PORT=38000
docker run -it -d --init --name $IMAGE -p $PORT:8000 -e TZ=Asia/Shanghai vinlic/$IMAGE

IMAGE=qwen-free-api
PORT=38003
docker run -it -d --init --name $IMAGE -p $PORT:8000 -e TZ=Asia/Shanghai vinlic/$IMAGE
