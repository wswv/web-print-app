#!/bin/sh

# Flask-SQLAlchemy 默认使用 /usr/src/app/users.db
DB_FILE="/usr/src/app/users.db"

# 检查数据库文件是否存在且大小是否大于零。
# -f: 文件是否存在
# -s: 文件大小是否大于零（确保不是空的 touch 文件）
if [ ! -f "$DB_FILE" ] || [ ! -s "$DB_FILE" ]; then
    echo "=================================================="
    echo "  Database file not found or empty. Initializing..."
    echo "=================================================="
    
    # 确保用户 'john' 对数据库文件所在目录有写权限
    if [ ! -d "$(dirname "$DB_FILE")" ]; then
        mkdir -p "$(dirname "$DB_FILE")"
    fi
    # 确保文件可以被创建 (尽管在 Dockerfile 中已 touch)
    touch "$DB_FILE" 

    # 运行数据库初始化脚本
    /usr/local/bin/python /usr/src/app/setup_db.py
    
    echo "=================================================="
    echo "  Initialization complete. Starting application."
    echo "=================================================="
else
    echo "Database file $DB_FILE found and initialized. Skipping setup."
fi

# 执行传递给 ENTRYPOINT 的原始 CMD (即 Gunicorn 命令)
exec "$@"