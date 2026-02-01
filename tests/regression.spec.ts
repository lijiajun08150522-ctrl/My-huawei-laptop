import { test, expect, Page } from '@playwright/test';

/**
 * CodeBuddy系统回归测试套件
 * 
 * 测试范围:
 * 1. 路径测试: 检查/, /game, /api/tasks是否正常响应
 * 2. 逻辑测试: 首页导航到游戏页面，检查Canvas加载
 */

/**
 * 测试配置
 */
const TEST_CONFIG = {
  baseURL: process.env.BASE_URL || 'http://localhost:5000',
  paths: {
    home: '/',
    game: '/game',
    api: '/api/tasks'
  },
  timeouts: {
    default: 10000,
    navigation: 30000
  }
};

/**
 * ==================== 路径测试 ====================
 */

test.describe('路径测试 (Path Tests)', () => {
  
  /**
   * 测试1: 首页路径检查
   * 验证: 首页能正常访问，返回200状态码
   */
  test('首页路径 / 应该正常响应', async ({ page }) => {
    // 访问首页
    const response = await page.goto(TEST_CONFIG.paths.home, {
      waitUntil: 'domcontentloaded'
    });

    // 检查状态码
    expect(response?.status()).toBe(200);

    // 检查页面标题
    await expect(page).toHaveTitle(/CodeBuddy/i);

    // 检查关键元素是否存在
    await expect(page.locator('.logo')).toBeVisible();
    await expect(page.locator('.navigation-center')).toBeVisible();

    // 截图
    await page.screenshot({ path: 'test-results/homepage.png' });
  });

  /**
   * 测试2: 游戏页面路径检查
   * 验证: 游戏页面能正常访问，返回200状态码
   */
  test('游戏路径 /game 应该正常响应', async ({ page }) => {
    // 访问游戏页面
    const response = await page.goto(TEST_CONFIG.paths.game, {
      waitUntil: 'domcontentloaded'
    });

    // 检查状态码
    expect(response?.status()).toBe(200);

    // 检查页面标题
    await expect(page).toHaveTitle(/贪吃蛇|Snake/i);

    // 截图
    await page.screenshot({ path: 'test-results/gamepage.png' });
  });

  /**
   * 测试3: API路径检查
   * 验证: API端点返回有效的JSON数据
   */
  test('API路径 /api/tasks 应该返回有效的JSON', async ({ request }) => {
    // 发送GET请求
    const response = await request.get(TEST_CONFIG.paths.api);

    // 检查状态码
    expect(response.status()).toBe(200);

    // 检查Content-Type
    expect(response.headers()['content-type']).toContain('application/json');

    // 解析JSON
    const data = await response.json();

    // 验证数据结构
    expect(data).toHaveProperty('success');
    expect(data).toHaveProperty('tasks');
    expect(Array.isArray(data.tasks)).toBe(true);
  });

  /**
   * 测试4: 404错误处理
   * 验证: 不存在的路径返回404
   */
  test('不存在的路径应该返回404', async ({ page }) => {
    // 访问不存在的路径
    const response = await page.goto('/non-existent-path');

    // 检查状态码
    expect(response?.status()).toBe(404);

    // 或者检查Flask的404页面
    const bodyText = await page.body();
    expect(bodyText).toMatch(/404|not found/i);
  });
});

/**
 * ==================== 逻辑测试 ====================
 */

test.describe('逻辑测试 (Logic Tests)', () => {
  
  /**
   * 测试5: 首页导航到游戏页面
   * 验证: 从首页点击游戏按钮，能正确导航到游戏页面
   */
  test('从首页点击游戏按钮应该导航到游戏页面', async ({ page }) => {
    // 访问首页
    await page.goto(TEST_CONFIG.paths.home);
    await page.waitForLoadState('domcontentloaded');

    // 找到游戏导航卡片
    const gameCard = page.locator('.nav-card').filter({ hasText: /贪吃蛇游戏|Snake/i });
    
    // 等待卡片可见
    await expect(gameCard).toBeVisible();

    // 点击游戏卡片
    await gameCard.click();

    // 等待导航完成
    await page.waitForURL(/game/i, { timeout: 5000 });

    // 验证当前URL包含/game
    expect(page.url()).toContain('game');

    // 截图
    await page.screenshot({ path: 'test-results/navigation-to-game.png' });
  });

  /**
   * 测试6: 游戏页面Canvas检查
   * 验证: 游戏页面包含Canvas元素
   */
  test('游戏页面应该包含Canvas画布', async ({ page }) => {
    // 访问游戏页面
    await page.goto(TEST_CONFIG.paths.game);
    await page.waitForLoadState('domcontentloaded');

    // 等待Canvas加载
    const canvas = page.locator('canvas').first();
    await expect(canvas).toBeVisible({ timeout: 5000 });

    // 检查Canvas属性
    const width = await canvas.getAttribute('width');
    const height = await canvas.getAttribute('height');

    // 验证Canvas尺寸
    expect(parseInt(width || '0')).toBeGreaterThan(0);
    expect(parseInt(height || '0')).toBeGreaterThan(0);

    // 截图
    await page.screenshot({ path: 'test-results/game-canvas.png' });
  });

  /**
   * 测试7: Canvas上下文验证
   * 验证: Canvas能获取到2D上下文
   */
  test('Canvas应该能获取2D上下文', async ({ page }) => {
    // 访问游戏页面
    await page.goto(TEST_CONFIG.paths.game);
    await page.waitForLoadState('domcontentloaded');

    // 执行JavaScript检查Canvas上下文
    const hasContext = await page.evaluate(() => {
      const canvas = document.querySelector('canvas');
      if (!canvas) return false;
      
      try {
        const ctx = canvas.getContext('2d');
        return ctx !== null;
      } catch {
        return false;
      }
    });

    // 验证上下文存在
    expect(hasContext).toBe(true);

    // 截图
    await page.screenshot({ path: 'test-results/canvas-context.png' });
  });

  /**
   * 测试8: 游戏初始化检查
   * 验证: 游戏初始化后，Canvas上有绘制内容
   */
  test('游戏初始化后Canvas应该有绘制内容', async ({ page }) => {
    // 访问游戏页面
    await page.goto(TEST_CONFIG.paths.game);
    await page.waitForLoadState('domcontentloaded');

    // 等待游戏初始化（检查游戏状态变量）
    await page.waitForTimeout(1000);

    // 检查Canvas是否被绘制
    const isDrawn = await page.evaluate(() => {
      const canvas = document.querySelector('canvas') as HTMLCanvasElement;
      if (!canvas) return false;

      const ctx = canvas.getContext('2d');
      if (!ctx) return false;

      // 尝试获取像素数据
      try {
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        // 检查是否有非透明像素
        for (let i = 0; i < imageData.data.length; i += 4) {
          if (imageData.data[i + 3] > 0) { // alpha通道
            return true;
          }
        }
        return false;
      } catch {
        return false;
      }
    });

    // 验证Canvas被绘制
    expect(isDrawn).toBe(true);

    // 截图
    await page.screenshot({ path: 'test-results/game-drawn.png' });
  });

  /**
   * 测试9: 首页导航到任务管理器
   * 验证: 从首页点击任务管理器按钮
   */
  test('从首页点击任务管理器应该导航到任务页面', async ({ page }) => {
    // 访问首页
    await page.goto(TEST_CONFIG.paths.home);
    await page.waitForLoadState('domcontentloaded');

    // 找到任务管理器导航卡片
    const taskCard = page.locator('.nav-card').filter({ hasText: /任务管理器|Task Manager/i });
    
    // 等待卡片可见
    await expect(taskCard).toBeVisible();

    // 点击任务管理器卡片
    await taskCard.click();

    // 等待导航完成
    await page.waitForURL(/tasks|web/i, { timeout: 5000 });

    // 验证导航成功
    const currentUrl = page.url();
    expect(currentUrl).toMatch(/tasks|web/i);

    // 截图
    await page.screenshot({ path: 'test-results/navigation-to-tasks.png' });
  });

  /**
   * 测试10: 首页导航到实训报告
   * 验证: 从首页点击实训报告按钮
   */
  test('从首页点击实训报告应该导航到报告页面', async ({ page }) => {
    // 访问首页
    await page.goto(TEST_CONFIG.paths.home);
    await page.waitForLoadState('domcontentloaded');

    // 找到实训报告导航卡片
    const reportCard = page.locator('.nav-card').filter({ hasText: /实训报告|Presentation/i });
    
    // 等待卡片可见
    await expect(reportCard).toBeVisible();

    // 点击实训报告卡片
    await reportCard.click();

    // 等待导航完成
    await page.waitForURL(/presentation/i, { timeout: 5000 });

    // 验证导航成功
    expect(page.url()).toContain('presentation');

    // 截图
    await page.screenshot({ path: 'test-results/navigation-to-report.png' });
  });
});

/**
 * ==================== API逻辑测试 ====================
 */

test.describe('API逻辑测试 (API Logic Tests)', () => {
  
  /**
   * 测试11: 添加任务API
   * 验证: POST /api/tasks 能成功添加任务
   */
  test('POST /api/tasks 应该能添加任务', async ({ request }) => {
    const newTask = {
      description: 'Playwright测试任务',
      priority: 'High',
      category: 'Test'
    };

    // 发送POST请求
    const response = await request.post(TEST_CONFIG.paths.api, {
      data: newTask,
      headers: {
        'Content-Type': 'application/json'
      }
    });

    // 检查响应
    expect(response.status()).toBe(200);

    const data = await response.json();
    expect(data.success).toBe(true);
    expect(data.message).toContain('Added');
    expect(data.task).toBeDefined();
    expect(data.task.description).toBe(newTask.description);
  });

  /**
   * 测试12: 获取任务列表API
   * 验证: GET /api/tasks 返回的任务列表格式正确
   */
  test('GET /api/tasks 应该返回格式正确的任务列表', async ({ request }) => {
    // 发送GET请求
    const response = await request.get(TEST_CONFIG.paths.api);
    const data = await response.json();

    // 验证数据结构
    expect(data.success).toBe(true);
    expect(Array.isArray(data.tasks)).toBe(true);

    // 如果有任务，验证每个任务的结构
    if (data.tasks.length > 0) {
      const firstTask = data.tasks[0];
      expect(firstTask).toHaveProperty('id');
      expect(firstTask).toHaveProperty('description');
      expect(firstTask).toHaveProperty('status');
      expect(firstTask).toHaveProperty('createdAt');
    }
  });

  /**
   * 测试13: API错误处理
   * 验证: 添加空任务时返回400错误
   */
  test('POST /api/tasks 描述为空应该返回400', async ({ request }) => {
    // 发送空描述
    const response = await request.post(TEST_CONFIG.paths.api, {
      data: { description: '' },
      headers: {
        'Content-Type': 'application/json'
      }
    });

    // 检查错误响应
    expect(response.status()).toBe(400);

    const data = await response.json();
    expect(data.success).toBe(false);
    expect(data.message).toContain('描述');
  });
});

/**
 * ==================== 性能测试 ====================
 */

test.describe('性能测试 (Performance Tests)', () => {
  
  /**
   * 测试14: 首页加载性能
   * 验证: 首页在2秒内加载完成
   */
  test('首页应该在2秒内加载完成', async ({ page }) => {
    const startTime = Date.now();

    await page.goto(TEST_CONFIG.paths.home, {
      waitUntil: 'domcontentloaded'
    });

    const loadTime = Date.now() - startTime;

    // 加载时间应该小于2秒
    expect(loadTime).toBeLessThan(2000);

    console.log(`首页加载时间: ${loadTime}ms`);
  });

  /**
   * 测试15: 游戏页面加载性能
   * 验证: 游戏页面在3秒内加载完成
   */
  test('游戏页面应该在3秒内加载完成', async ({ page }) => {
    const startTime = Date.now();

    await page.goto(TEST_CONFIG.paths.game, {
      waitUntil: 'domcontentloaded'
    });

    await page.waitForSelector('canvas', { timeout: 3000 });

    const loadTime = Date.now() - startTime;

    // 加载时间应该小于3秒
    expect(loadTime).toBeLessThan(3000);

    console.log(`游戏页面加载时间: ${loadTime}ms`);
  });
});

/**
 * ==================== 跨浏览器兼容性测试 ====================
 */

test.describe('跨浏览器兼容性', () => {
  
  /**
   * 测试16: Canvas在所有浏览器中可用
   */
  test('Canvas应该在当前浏览器中正常工作', async ({ page, browserName }) => {
    await page.goto(TEST_CONFIG.paths.game);
    
    const canvas = page.locator('canvas').first();
    await expect(canvas).toBeVisible();

    console.log(`浏览器: ${browserName} - Canvas测试通过`);
  });
});
