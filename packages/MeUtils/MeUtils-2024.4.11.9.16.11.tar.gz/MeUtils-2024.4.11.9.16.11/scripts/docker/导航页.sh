#!/usr/bin/env bash
# @Project      : AI @by PyCharm
# @Time         : 2024/4/2 10:48
# @Author       : betterme
# @Email        : 313303303@qq.com
# @Software     : PyCharm
# @Description  :

docker run -d --restart=always -p 39991:3002 \
  -v /www/data/sun-panel/conf:/app/conf \
  -v /www/data/sun-panel/uploads:/app/uploads \
  -v /www/data/sun-panel/database:/app/database \
  --name sun-panel \
  hslr/sun-panel
