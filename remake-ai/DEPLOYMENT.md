# Remake AI Docker 部署指南

## 环境准备

### 1. 安装依赖
- Docker Desktop (Windows/Mac) 或 Docker Engine (Linux)
- Docker Compose

### 2. 克隆项目
```bash
git clone <repository-url>
cd remake-ai
```

### 3. 配置环境变量
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填写必要的配置
# 重要：修改 SECRET_KEY、JWT_SECRET_KEY、POSTGRES_PASSWORD
```

### 4. 生成安全的密钥
```bash
# 生成 SECRET_KEY
python -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))"

# 生成 JWT_SECRET_KEY
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_hex(32))"
```

## 部署方式

### 开发环境部署

#### 方式一：使用 SQLite（快速启动）
```bash
# 1. 修改 .env
DB_TYPE=sqlite
DATABASE_PATH=data/remake_ai.db

# 2. 启动服务（不包含数据库容器）
docker-compose up -d backend

# 3. 查看日志
docker-compose logs -f backend
```

#### 方式二：使用 PostgreSQL（推荐）
```bash
# 1. 修改 .env
DB_TYPE=postgresql
DATABASE_URL=postgresql://remake_user:your-password@db:5432/remake_ai

# 2. 启动所有服务
docker-compose up -d

# 3. 查看服务状态
docker-compose ps
```

### 生产环境部署

#### 1. 配置生产环境变量
```bash
# 编辑 .env
FLASK_ENV=production
FLASK_PORT=5000
LOG_LEVEL=INFO

# 使用强密码
POSTGRES_PASSWORD=<your-strong-password>
```

#### 2. 启动服务（包含 Nginx）
```bash
docker-compose --profile production up -d
```

#### 3. 验证部署
```bash
# 检查健康状态
curl http://localhost:5000/api/health

# 检查数据库连接
docker-compose exec db pg_isready -U remake_user

# 查看日志
docker-compose logs -f
```

## 服务访问

### 开发环境
- 后端 API: http://localhost:5000
- 前端页面: 直接打开 `frontend/index.html` 或使用本地服务器

### 生产环境
- 前端页面: http://localhost
- 后端 API: http://localhost/api/ (通过 Nginx 代理)

## 常用命令

### 服务管理
```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f db
```

### 数据库操作
```bash
# 进入数据库容器
docker-compose exec db psql -U remake_user -d remake_ai

# 备份数据库
docker-compose exec db pg_dump -U remake_user remake_ai > backup.sql

# 恢复数据库
cat backup.sql | docker-compose exec -T db psql -U remake_user -d remake_ai
```

### 容器操作
```bash
# 进入后端容器
docker-compose exec backend bash

# 查看容器资源使用
docker stats

# 清理未使用的资源
docker system prune -a
```

## 环境变量安全

### 敏感信息保护
```bash
# .env 文件已在 .gitignore 中，不会被提交到版本控制
# 生产环境应使用密钥管理服务（如 AWS Secrets Manager、Vault 等）

# Docker Swarm / Kubernetes 中使用 secrets:
# docker secret create jwt_secret jwt_secret.txt
```

### ComfyUI API Key
```bash
# 如果 ComfyUI 需要 API Key 认证
# 在 .env 中设置
COMFYUI_API_KEY=your-comfyui-api-key

# 或通过 Docker secrets
docker secret create comfyui_key comfyui_key.txt
```

## 监控与维护

### 健康检查
```bash
# 后端健康检查
curl http://localhost:5000/api/health

# 数据库健康检查
docker-compose exec db pg_isready -U remake_user
```

### 日志管理
```bash
# 日志轮转配置已在 gunicorn.conf.py 中设置
# 查看实时日志
docker-compose logs -f --tail=100 backend

# 导出日志
docker-compose logs backend > backend.log
```

### 数据备份
```bash
# 创建备份脚本
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./backups"
mkdir -p $BACKUP_DIR

# 备份数据库
docker-compose exec -T db pg_dump -U remake_user remake_ai > $BACKUP_DIR/db_$DATE.sql

# 备份数据文件
docker run --rm -v remake-ai_data:/data -v $BACKUP_DIR:/backup alpine tar czf /backup/data_$DATE.tar.gz /data

echo "Backup completed: $DATE"
EOF

chmod +x backup.sh
./backup.sh
```

## 故障排查

### 容器无法启动
```bash
# 查看详细日志
docker-compose logs backend

# 检查端口占用
netstat -tuln | grep 5000

# 重新构建镜像
docker-compose build --no-cache backend
```

### 数据库连接失败
```bash
# 检查数据库状态
docker-compose ps db

# 进入数据库容器测试
docker-compose exec db psql -U remake_user -d remake_ai

# 检查网络连接
docker-compose exec backend ping db
```

### 内存不足
```bash
# 调整 worker 数量
# 编辑 backend/gunicorn.conf.py
workers = 2  # 减少工作进程数

# 重启服务
docker-compose restart backend
```

## 性能优化

### 1. 启用缓存
```python
# 在 app.py 中添加缓存
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://redis:6379/0'})
```

### 2. 数据库优化
```sql
-- 创建更多索引
CREATE INDEX idx_remake_records_composite ON remake_records(user_id, created_at);

-- 定期清理过期会话
DELETE FROM user_sessions WHERE expires_at < NOW();
```

### 3. Nginx 配置
```nginx
# 启用 gzip 压缩
gzip on;
gzip_types text/plain application/json application/javascript text/css;

# 启用缓存
location /static/ {
    expires 7d;
}
```

## 安全建议

1. **定期更新依赖**
```bash
pip list --outdated
pip install --upgrade package_name
```

2. **启用 HTTPS**
```bash
# 在 nginx 目录配置 SSL 证书
docker-compose --profile production up -d
```

3. **限制数据库访问**
```yaml
# docker-compose.yml 中不要暴露数据库端口
# db:
#   ports: []  # 删除 ports 配置
```

4. **启用防火墙**
```bash
# 只允许必要的端口
ufw allow 80/tcp
ufw allow 443/tcp
```

## 生产环境检查清单

- [ ] 修改所有默认密码
- [ ] 使用 HTTPS
- [ ] 配置 HTTPS 证书
- [ ] 设置 CORS 正确的来源
- [ ] 启用速率限制
- [ ] 配置日志轮转
- [ ] 设置监控告警
- [ ] 配置自动备份
- [ ] 优化数据库性能
- [ ] 限制容器资源（CPU、内存）
- [ ] 使用 secrets 管理敏感信息
- [ ] 定期安全更新

## 技术支持

如有问题，请查看：
- 项目文档: `README.md`
- API 文档: `backend/README.md`
- 问题反馈: GitHub Issues
