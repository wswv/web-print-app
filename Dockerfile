# 文件名：Dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libssl-dev libffi-dev python3-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

FROM python:3.12-slim
WORKDIR /app
# 复制 Python 包
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
# 安装运行时依赖（含 libreoffice）
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice poppler-utils cups-client \
    && rm -rf /var/lib/apt/lists/* \
    && ln -s /usr/bin/libreoffice /usr/bin/soffice

COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]