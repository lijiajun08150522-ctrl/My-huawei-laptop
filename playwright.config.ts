import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright测试配置文件
 * 
 * 项目: CodeBuddy系统回归测试
 * 测试范围: 路径测试、逻辑测试
 */

export default defineConfig({
  // 测试目录
  testDir: './tests',

  // 测试文件匹配模式
  testMatch: [
    '**/*.spec.ts',
    '**/*.test.ts'
  ],

  // 并行执行
  fullyParallel: true,

  // 失败时重试
  retries: process.env.CI ? 2 : 0,

  // 测试超时时间
  timeout: 30 * 1000,

  // 并行worker数
  workers: process.env.CI ? 1 : undefined,

  // 测试报告
  reporter: [
    ['html'],
    ['junit', { outputFile: 'test-results/junit.xml' }],
    ['list']
  ],

  // 全局设置
  use: {
    // 基础URL
    baseURL: process.env.BASE_URL || 'http://localhost:5000',

    // 追踪失败测试
    trace: 'on-first-retry',

    // 失败时截图
    screenshot: 'only-on-failure',

    // 失败时录制视频
    video: 'retain-on-failure',

    // 操作超时
    actionTimeout: 10 * 1000,

    // 导航超时
    navigationTimeout: 30 * 1000,
  },

  // 多浏览器测试
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },

    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },

    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },

    // 移动端测试
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],

  // 开发服务器
  webServer: {
    command: 'python app.py',
    url: 'http://localhost:5000',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
