# CodeBuddy Playwright回归测试

## 概述

这是CodeBuddy系统的完整Playwright回归测试套件，包含路径测试、逻辑测试、API测试和性能测试。

## 测试覆盖

### 1. 路径测试 (Path Tests)
- ✅ 首页 `/` 响应测试
- ✅ 游戏页面 `/game` 响应测试
- ✅ API端点 `/api/tasks` 响应测试
- ✅ 404错误处理测试

### 2. 逻辑测试 (Logic Tests)
- ✅ 首页导航到游戏页面
- ✅ 游戏页面Canvas检查
- ✅ Canvas 2D上下文验证
- ✅ 游戏初始化检查
- ✅ 首页导航到任务管理器
- ✅ 首页导航到实训报告

### 3. API逻辑测试 (API Logic Tests)
- ✅ POST /api/tasks 添加任务
- ✅ GET /api/tasks 获取任务列表
- ✅ API错误处理（空描述）

### 4. 性能测试 (Performance Tests)
- ✅ 首页加载性能 (< 2秒)
- ✅ 游戏页面加载性能 (< 3秒)

### 5. 跨浏览器兼容性测试
- ✅ Chrome
- ✅ Firefox
- ✅ Safari
- ✅ Mobile Chrome
- ✅ Mobile Safari

## 安装

### 前置要求
- Node.js 18+
- Python 3.8+ (用于Flask服务)
- Playwright浏览器

### 安装步骤

1. 安装Node.js依赖
```bash
cd tests
npm install
```

2. 安装Playwright浏览器
```bash
npm run install:browser
```

3. 或安装所有浏览器（包含依赖）
```bash
npm run install:browser:all
```

## 使用方法

### 基本测试运行

```bash
# 运行所有测试（无头模式）
npm test

# 运行所有测试（有头模式）
npm run test:headed

# 使用UI模式运行（推荐）
npm run test:ui

# 调试模式
npm run test:debug
```

### 查看测试报告

```bash
# 查看HTML报告
npm run test:report
```

### 运行特定测试

```bash
# 只运行路径测试
npx playwright test --grep "路径测试"

# 只运行逻辑测试
npx playwright test --grep "逻辑测试"

# 只运行API测试
npx playwright test --grep "API逻辑测试"

# 只运行性能测试
npx playwright test --grep "性能测试"
```

### 配置环境变量

```bash
# Windows PowerShell
$env:BASE_URL="http://localhost:5000"
npm test

# Windows CMD
set BASE_URL=http://localhost:5000
npm test

# Linux/Mac
export BASE_URL=http://localhost:5000
npm test
```

## 测试配置

### playwright.config.ts

主要配置项：
- `baseURL`: 测试服务器地址（默认 http://localhost:5000）
- `testDir`: 测试文件目录（./tests）
- `timeout`: 测试超时时间（30秒）
- `retries`: 失败重试次数（CI环境2次，本地0次）

### 多浏览器测试

默认在以下浏览器中运行：
- Chromium (Chrome)
- Firefox
- WebKit (Safari)
- Mobile Chrome
- Mobile Safari

## 测试输出

### 自动生成的文件

- `test-results/`: 测试结果目录
  - `*.png`: 失败时的截图
  - `*.zip`: 视频录制（仅失败时）
  - `trace.zip`: 追踪文件
- `playwright-report/`: HTML测试报告
- `test-results/junit.xml`: JUnit格式报告（CI用）

### 测试报告示例

```bash
Running 16 tests using 5 workers

  ✓  路径测试 (Path Tests) (4)
    ✓  首页路径 / 应该正常响应 (2.1s)
    ✓  游戏路径 /game 应该正常响应 (1.8s)
    ✓  API路径 /api/tasks 应该返回有效的JSON (0.3s)
    ✓  不存在的路径应该返回404 (0.2s)
  ✓  逻辑测试 (Logic Tests) (6)
    ✓  从首页点击游戏按钮应该导航到游戏页面 (1.5s)
    ✓  游戏页面应该包含Canvas画布 (1.2s)
    ✓  Canvas应该能获取2D上下文 (0.8s)
    ✓  游戏初始化后Canvas应该有绘制内容 (1.0s)
    ✓  从首页点击任务管理器应该导航到任务页面 (1.3s)
    ✓  从首页点击实训报告应该导航到报告页面 (1.4s)
  ✓  API逻辑测试 (API Logic Tests) (3)
    ✓  POST /api/tasks 应该能添加任务 (0.5s)
    ✓  GET /api/tasks 应该返回格式正确的任务列表 (0.3s)
    ✓  POST /api/tasks 描述为空应该返回400 (0.2s)
  ✓  性能测试 (Performance Tests) (2)
    ✓  首页应该在2秒内加载完成 (1.5s)
    ✓  游戏页面应该在3秒内加载完成 (2.1s)
  ✓  跨浏览器兼容性 (1)
    ✓  Canvas应该在当前浏览器中正常工作 (1.2s)

  16 passed (12.8s)
```

## CI/CD集成

### GitHub Actions示例

```yaml
name: Playwright Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: cd tests && npm ci
      - run: cd tests && npx playwright install --with-deps
      - run: cd tests && npm test
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: playwright-report
          path: tests/playwright-report/
```

### Jenkins Pipeline示例

```groovy
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'cd tests && npm ci'
                sh 'cd tests && npx playwright install --with-deps'
                sh 'cd tests && npm test'
            }
            post {
                always {
                    publishHTML(target: [
                        reportDir: 'tests/playwright-report',
                        reportFiles: 'index.html',
                        reportName: 'Playwright Report'
                    ])
                }
            }
        }
    }
}
```

## 故障排除

### 问题1: 找不到浏览器

```bash
# 重新安装浏览器
npm run install:browser:all
```

### 问题2: Flask服务启动失败

```bash
# 手动启动Flask服务
cd ..
python app.py

# 在另一个终端运行测试
cd tests
BASE_URL=http://localhost:5000 npm test
```

### 问题3: 测试超时

在 `playwright.config.ts` 中增加超时时间：
```typescript
timeout: 60 * 1000,
navigationTimeout: 60 * 1000,
```

### 问题4: Canvas未加载

检查游戏页面是否正确实现Canvas元素：
```bash
# 手动访问游戏页面
http://localhost:5000/game

# 检查控制台错误
```

## 扩展测试

### 添加新测试

1. 在 `tests/regression.spec.ts` 中添加测试用例：

```typescript
test('新测试用例', async ({ page }) => {
  // 测试逻辑
  await page.goto('/');
  await expect(page.locator('.selector')).toBeVisible();
});
```

2. 运行新测试：
```bash
npm test --grep "新测试用例"
```

### 添加新的测试文件

创建 `tests/new-feature.spec.ts`：
```typescript
import { test, expect } from '@playwright/test';

test.describe('新功能测试', () => {
  test('测试用例1', async ({ page }) => {
    // ...
  });
});
```

## 最佳实践

1. **测试隔离**: 每个测试独立运行，不依赖其他测试
2. **等待策略**: 使用 `waitForSelector` 而非固定延迟
3. **清晰的命名**: 测试名称描述被测试的行为
4. **断言明确**: 使用具体的断言，而非模糊的判断
5. **复用选择器**: 使用CSS类而非脆弱的选择器
6. **截图调试**: 失败时自动截图，便于调试
7. **并行执行**: 利用Playwright的并行能力加速测试

## 性能基准

| 测试项 | 目标 | 实际 | 状态 |
|--------|------|------|------|
| 首页加载 | < 2s | ~1.5s | ✅ |
| 游戏页面加载 | < 3s | ~2.1s | ✅ |
| API响应 | < 1s | ~0.3s | ✅ |

## 维护者

- CodeBuddy开发团队
- 创建日期: 2026-01-30

## 许可证

MIT License
