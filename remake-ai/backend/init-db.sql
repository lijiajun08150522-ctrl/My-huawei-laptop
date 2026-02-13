-- Remake AI 数据库初始化脚本
-- PostgreSQL 版本

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) UNIQUE NOT NULL,
    username VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_users_user_id ON users(user_id);

-- 创建改造记录表
CREATE TABLE IF NOT EXISTS remake_records (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    item_name VARCHAR(200) NOT NULL,
    remake_image_url TEXT,
    carbon_offset DECIMAL(10, 2) NOT NULL DEFAULT 0.0,
    description TEXT,
    material_type VARCHAR(50),
    value_score INTEGER,
    category VARCHAR(50),
    reuse_potential VARCHAR(20),
    suggestions JSONB,
    diy_ideas JSONB,
    status VARCHAR(20) DEFAULT 'completed',
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_remake_records_user_id ON remake_records(user_id);
CREATE INDEX IF NOT EXISTS idx_remake_records_item_name ON remake_records(item_name);
CREATE INDEX IF NOT EXISTS idx_remake_records_created_at ON remake_records(created_at);
CREATE INDEX IF NOT EXISTS idx_remake_records_material_type ON remake_records(material_type);

-- 创建碳排放因子表
CREATE TABLE IF NOT EXISTS carbon_factors (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) UNIQUE NOT NULL,
    item_type VARCHAR(100) NOT NULL,
    carbon_saved_per_kg DECIMAL(10, 2) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_carbon_factors_category ON carbon_factors(category);

-- 插入默认碳排放因子数据
INSERT INTO carbon_factors (category, item_type, carbon_saved_per_kg, description) VALUES
    ('织物', '纺织品/服装', 15.5, '纺织品类物品每kg平均碳排放量'),
    ('塑料', '塑料制品', 3.5, '塑料类物品每kg平均碳排放量'),
    ('金属', '金属制品', 8.2, '金属类物品每kg平均碳排放量'),
    ('玻璃', '玻璃器皿', 0.8, '玻璃类物品每kg平均碳排放量'),
    ('纸', '纸制品', 1.2, '纸制品类每kg平均碳排放量'),
    ('木材', '木制品', 12.0, '木材类物品每kg平均碳排放量'),
    ('电子', '电子产品', 50.0, '电子类物品每kg平均碳排放量'),
    ('其他', '其他物品', 5.0, '其他类别物品每kg平均碳排放量')
ON CONFLICT (category) DO NOTHING;

-- 创建会话表（用于 JWT token 管理，可选）
CREATE TABLE IF NOT EXISTS user_sessions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_user_sessions_token_hash ON user_sessions(token_hash);
CREATE INDEX IF NOT EXISTS idx_user_sessions_expires_at ON user_sessions(expires_at);

-- 创建审计日志表（可选）
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100),
    action VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50),
    resource_id VARCHAR(100),
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs(action);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);

-- 授予权限
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO remake_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO remake_user;
