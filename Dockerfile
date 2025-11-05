# Dockerfile（终极·自带 gunicorn 版）
FROM python:3.12-slim AS builder
WORKDIR /app

# 编译 pycups
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc python3-dev libcups2-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --target=/install -r requirements.txt

# 运行时镜像
FROM python:3.12-slim
WORKDIR /app

# 运行依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice poppler-utils cups-client \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f /usr/bin/soffice && ln -sf /usr/bin/libreoffice /usr/bin/soffice

# 复制完整 Python 环境（含 gunicorn 可执行文件）
COPY --from=builder /install /usr/local/lib/python3.12/site-packages
# 关键：把 bin 目录加入 PATH 并软链到标准位置
RUN mkdir -p /usr/local/bin \
    && ln -s /usr/local/lib/python3.12/site-packages/bin/gunicorn /usr/local/bin/gunicorn

COPY . .

EXPOSE 5000
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "run:app"]