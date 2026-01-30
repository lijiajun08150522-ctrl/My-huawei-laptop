# CodeBuddy 视频启动问题排查指南

## 问题：连接被拒绝 (Connection Refused)

### 原因
服务器还没有启动，或者启动失败。

---

## 解决方案

### 方案 1: 使用批处理文件（推荐）

1. **打开文件夹**
   ```
   d:\SummerProject\codebuddy-demo
   ```

2. **双击 `start.bat`**

3. **等待安装**（第一次需要 2-5 分钟）
   - 会显示 "Installing dependencies..."
   - 下载 remotion, react 等包

4. **自动打开浏览器**
   - 访问 http://localhost:3000
   - 看到 Remotion Studio 界面

---

### 方案 2: 手动命令（如果批处理失败）

#### 第一步：安装依赖

打开 **PowerShell** 或 **命令提示符**：

```powershell
# 切换到项目目录
d:

# 进入 codebuddy-demo 文件夹
cd d:\SummerProject\codebuddy-demo

# 安装依赖
npm install
```

**预期输出**:
```
added 150 packages in 45s
```

**如果失败**:
- 检查网络连接
- 确认 npm 已安装：`npm --version`
- 尝试使用国内镜像：
  ```powershell
  npm config set registry https://registry.npmmirror.com
  npm install
  ```

#### 第二步：启动服务器

```powershell
npm start
```

**预期输出**:
```
[INFO] Starting server...
[INFO] Server listening at http://localhost:3000
```

浏览器会自动打开 http://localhost:3000

**如果失败**:
- 检查端口 3000 是否被占用：
  ```powershell
  netstat -ano | findstr ":3000"
  ```
- 如果被占用，杀死进程或使用其他端口

---

### 方案 3: 检查文件完整性

确认以下文件存在：

```
codebuddy-demo/
├── package.json          ✓ 必需
├── remotion.config.ts   ✓ 必需
├── tsconfig.json        ✓ 必需
├── src/
│   ├── Root.tsx         ✓ 必需
│   └── CodeBuddyIntro.tsx  ✓ 必需
├── public/              ✓ 必需（可以是空的）
└── start.bat            ✓ 启动脚本
```

**检查方法**:
```powershell
dir d:\SummerProject\codebuddy-demo
```

---

### 方案 4: 清除缓存重试

如果安装失败，清除缓存：

```powershell
# 1. 删除 node_modules（如果存在）
rmdir /s /q node_modules 2>nul

# 2. 删除 package-lock.json
del package-lock.json 2>nul

# 3. 清除 npm 缓存
npm cache clean --force

# 4. 重新安装
npm install

# 5. 启动
npm start
```

---

## 常见错误及解决方案

### 错误 1: "ENOENT: no such file or directory"

**原因**: 找不到 package.json

**解决**:
```powershell
# 确认文件存在
dir d:\SummerProject\codebuddy-demo\package.json

# 如果不存在，重新创建（或从 Git 恢复）
cd d:\SummerProject\codebuddy-demo
```

---

### 错误 2: "EADDRINUSE: address already in use :::3000"

**原因**: 端口 3000 已被占用

**解决**:
```powershell
# 查找占用进程
netstat -ano | findstr ":3000"

# 杀死进程（PID 是最后一列的数字）
taskkill /F /PID <PID>

# 重新启动
npm start
```

---

### 错误 3: "Cannot find module 'remotion'"

**原因**: 依赖没有正确安装

**解决**:
```powershell
npm install
```

---

### 错误 4: 浏览器没有自动打开

**原因**: 浏览器配置问题

**解决**:
手动访问：http://localhost:3000

---

### 错误 5: 安装非常慢

**原因**: npm 官方源在国外

**解决**: 使用国内镜像
```powershell
npm config set registry https://registry.npmmirror.com
npm install
```

---

### 错误 6: Windows PowerShell 权限问题

**原因**: 执行策略限制

**解决**:
```powershell
# 以管理员身份运行 PowerShell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 验证步骤

### 1. 检查 Node.js
```powershell
node --version
# 应该显示 v14 或更高
```

### 2. 检查 npm
```powershell
npm --version
# 应该显示版本号
```

### 3. 检查项目文件
```powershell
dir d:\SummerProject\codebuddy-demo
# 应该看到 package.json 等文件
```

### 4. 检查依赖安装
```powershell
dir d:\SummerProject\codebuddy-demo\node_modules
# 应该有很多文件夹（如果已安装）
```

### 5. 检查服务器运行
```powershell
netstat -ano | findstr ":3000"
# 应该看到类似：
# TCP    0.0.0.0:3000    0.0.0.0:0    LISTENING    <PID>
```

---

## 最简操作流程

### 如果什么都试过了，按这个顺序来：

1. **打开命令提示符**
   - Win + R，输入 `cmd`，回车

2. **执行命令**（复制粘贴以下内容）：
   ```cmd
   d:
   cd d:\SummerProject\codebuddy-demo
   npm install
   npm start
   ```

3. **等待自动打开浏览器**
   - 访问 http://localhost:3000

---

## 快速测试

### 测试 npm 是否工作
```powershell
npm --version
```

### 测试项目文件
```powershell
type d:\SummerProject\codebuddy-demo\package.json
```

### 测试网络连接
```powershell
ping registry.npmjs.org
```

---

## 如果还是不行

### 完全重新开始

```powershell
# 1. 删除项目文件夹
rmdir /s /q d:\SummerProject\codebuddy-demo

# 2. 从 Git 恢复
cd d:\SummerProject
git checkout codebuddy-demo

# 3. 重新安装
cd codebuddy-demo
npm install
npm start
```

---

## 联系支持

如果以上方案都无法解决，请提供：

1. 完整的错误信息
2. 使用的操作系统版本
3. npm 版本：`npm --version`
4. Node 版本：`node --version`
5. 执行的命令和输出

---

## 相关文档

- `README.md` - 项目说明
- `CODEBUDDY_VIDEO_GUIDE.md` - 使用指南
- `REMOTION_SKILL_README.md` - Remotion Skill 文档
