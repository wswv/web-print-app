# ----------------------------------------------------
# 阶段 1：构建阶段 (用于编译 pycups 和安装所有系统依赖)
# ----------------------------------------------------
FROM python:3.11-alpine AS builder

# 1. 安装所有系统依赖 (运行时 + 编译时)
RUN apk update && \
    apk add --no-cache \
        cups \
        libreoffice \
        build-base \
        cups-dev && \
    pip install --upgrade pip

# 设置工作目录
WORKDIR /usr/src/app

# 复制 requirements.txt 并安装 Python 依赖 (gunicorn 在此安装)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


# ----------------------------------------------------
# 阶段 2：最终运行阶段 (仅包含运行时所需文件)
# ----------------------------------------------------
FROM python:3.11-alpine AS final

# 设置工作目录
WORKDIR /usr/src/app

# 1. 安装最终运行时所需的系统依赖
RUN apk update && \
    apk add --no-cache \
        cups \
        libreoffice \
        bash \
        # 确保基础系统可以执行 cups 和 libreoffice
        fontconfig \
        libstdc++ && \		
    rm -rf /var/cache/apk/*

# 2. 【关键修正】先创建非 Root 用户和设置权限
ARG PUID=1000
ARG PGID=1000
RUN addgroup -g ${PGID} john \
    && adduser -u ${PUID} -G john -s /bin/bash -D john

# 为 'john' 用户添加 CUPS 客户端权限
RUN addgroup john lp

# 3. 从 builder 阶段复制 Python 依赖 (site-packages)
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 4. 复制项目代码和入口脚本
COPY . .
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
COPY setup_db.py /usr/src/app/setup_db.py

# 5. 设置入口脚本的权限
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# 6. 设置工作目录和文件的所有者为非 Root 用户
# 【修改】移除 `touch users.db`，让初始化脚本去创建
RUN mkdir -p /usr/src/app/uploads && \
    chown -R john:john /usr/src/app && \
    chown -R john:john /usr/local/bin

# 7. 最终容器以 'john' 用户运行
USER john

# 暴露 Flask 默认端口
EXPOSE 5000

# 【关键修改】使用 ENTRYPOINT 脚本进行条件初始化，CMD 仅包含最终要运行的命令
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["gunicorn", "run:app", "-w", "4", "--bind", "0.0.0.0:5000"]