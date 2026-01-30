# Remotion Skill 使用指南

## ✅ Remotion Skill 已创建完成！

### 📦 Skill 概览

**名称**: `remotion`
**位置**: `.codebuddy/skills/remotion/`
**大小**: ~3,000 行代码

---

## 🎯 Skill 内容

### 核心文件

| 文件 | 大小 | 用途 |
|------|------|------|
| `SKILL.md` | ~600 行 | 完整使用指南和最佳实践 |
| `scripts/setup_remotion.py` | ~200 行 | 初始化 Remotion 项目 |
| `scripts/export_video.py` | ~150 行 | 导出视频 |
| `scripts/validate_project.py` | ~180 行 | 验证项目结构 |
| `references/animation_patterns.md` | ~400 行 | 动画模式参考 |
| `references/best_practices.md` | ~350 行 | 最佳实践指南 |
| `assets/templates/code-animation-template.tsx` | ~100 行 | 代码动画模板 |
| `assets/templates/explainer-template.tsx` | ~150 行 | 解释视频模板 |
| `assets/templates/slideshow-template.tsx` | ~120 行 | 幻灯片模板 |

---

## 🚀 快速开始

### 1. 调用 Skill

当您想创建视频时，只需说：

```
"用 Remotion 制作一个视频"
"创建一个代码演示视频"
"制作贪吃蛇开发过程的动画"
```

系统会自动加载 Remotion Skill，提供完整的指导。

---

### 2. 初始化项目

```bash
# 创建一个新的 Remotion 项目
python .codebuddy/skills/remotion/scripts/setup_remotion.py my-project --template code-animation

# 可选模板：
# - default: 默认模板（简单文字动画）
# - code-animation: 代码动画（带语法高亮）
# - explainer: 解释视频（步骤演示）
# - slideshow: 幻灯片（图片轮播）
```

---

### 3. 创建视频组件

系统会根据您的需求，自动创建相应的视频组件。

**示例：代码动画**

```typescript
import {CodeAnimationTemplate} from './templates/code-animation-template';

export const SnakeGameDev: React.FC = () => {
  const code = `function createSnake() {
  const snake = [
    {x: 5, y: 5},
    {x: 4, y: 5},
    {x: 3, y: 5}
  ];
  return snake;
}`;

  return (
    <CodeAnimationTemplate
      code={code}
      language="javascript"
      typingSpeed={2}
      showLineNumbers={true}
    />
  );
};
```

---

### 4. 导出视频

```bash
# 导出视频
python .codebuddy/skills/remotion/scripts/export_video.py \
  --project my-project \
  --composition snake-game-dev \
  --output video.mp4 \
  --format mp4

# 验证项目
python .codebuddy/skills/remotion/scripts/validate_project.py my-project
```

---

## 📚 Skill 文档说明

### SKILL.md - 完整使用指南

包含以下内容：

#### 1. 快速开始
- 前置条件（Node.js, FFmpeg）
- 项目初始化步骤
- 基础视频结构

#### 2. 核心概念
- Compositions（视频组件）
- 使用当前帧
- 动画效果
- 音频集成
- 转场效果

#### 3. 常用场景
- 代码动画视频
- 解释视频
- 数据可视化
- 产品演示

#### 4. 工作流决策树
- 视频类型选择
- 时长确定
- 分辨率设置
- 导出格式选择

#### 5. 分步工作流
1. 规划视频
2. 设置项目
3. 创建组件
4. 添加资源
5. 预览迭代
6. 导出视频

---

### references/ - 参考文档

#### animation_patterns.md - 动画模式

包含常见动画模式：

- **淡入淡出**
  - 简单淡入
  - 淡出
  - 淡入淡出

- **缩放动画**
  - 放大
  - 缩小
  - 脉冲

- **滑动动画**
  - 从左/右/上/下滑入

- **旋转动画**
  - 持续旋转
  - 旋入旋出

- **文字动画**
  - 打字机效果
  - 逐词显示
  - 字母弹跳

- **路径动画**
  - 沿路径移动
  - 绘制线条

- **弹跳动画**
  - 下落弹跳
  - 弹性弹跳

- **交错动画**
  - 顺序交错
  - 波浪交错

- **转场模式**
  - 交叉淡化
  - 推动转场
  - 缩放转场

#### best_practices.md - 最佳实践

包含：

- **性能优化**
  - 图片优化
  - 静态内容处理
  - 组件记忆化
  - GPU加速

- **代码组织**
  - 项目结构
  - 组件组合
  - 关注点分离

- **资源管理**
  - 图片优化技巧
  - 音频优化
  - 字体管理

- **动画最佳实践**
  - 使用弹簧动画
  - 保持动画简短
  - 使用缓动函数
  - 交错动画

- **音频最佳实践**
  - 使用 Remotion Audio 组件
  - 淡入淡出
  - 音量管理

- **调试技巧**
  - 控制台日志
  - 逐帧测试
  - 不同分辨率测试

---

### assets/templates/ - 模板库

#### code-animation-template.tsx

**用途**: 创建代码打字动画

**特性**:
- 语法高亮（支持 JavaScript, Python, 等）
- 打字机效果
- 光标闪烁
- 行号显示
- 自定义配色

**使用示例**:

```typescript
<CodeAnimationTemplate
  code={codeString}
  language="javascript"
  typingSpeed={2}
  showLineNumbers={true}
/>
```

---

#### explainer-template.tsx

**用途**: 创建步骤式解释视频

**特性**:
- 标题页动画
- 步骤进度条
- 步骤编号徽章
- 内容淡入效果
- 自定义配色

**使用示例**:

```typescript
<ExplainerTemplate
  title="我的项目"
  subtitle="完整指南"
  steps={[
    {
      heading: "规划",
      content: "定义目标、识别受众、概述内容"
    },
    {
      heading: "开发",
      content: "编写代码、实现功能、测试"
    },
    {
      heading: "部署",
      content: "构建项目、部署生产、监控性能"
    }
  ]}
  backgroundColor="#667eea"
  textColor="#ffffff"
  accentColor="#ffd700"
/>
```

---

#### slideshow-template.tsx

**用途**: 创建图片幻灯片

**特性**:
- 多种转场效果（fade, slide, zoom, wipe）
- 图片显示
- 标题和副标题
- 自定义颜色
- 可配置时长

**使用示例**:

```typescript
<SlideshowTemplate
  slides={[
    {
      title: "幻灯片 1",
      subtitle: "简介",
      image: "slide1.jpg",
      backgroundColor: "#667eea"
    },
    {
      title: "幻灯片 2",
      subtitle: "内容",
      image: "slide2.jpg",
      backgroundColor: "#764ba2"
    }
  ]}
  transition="fade"
  transitionDuration={30}
  slideDuration={90}
/>
```

---

## 🎮 贪吃蛇开发视频创建指南

### 方案 1: 使用 Code Animation 模板

**适合**: 展示代码实现过程

```bash
# 1. 初始化项目
python .codebuddy/skills/remotion/scripts/setup_remotion.py \
  snake-dev-video \
  --template code-animation

# 2. 创建组件
# 系统会自动生成代码动画组件

# 3. 导出视频
python .codebuddy/skills/remotion/scripts/export_video.py \
  --project snake-dev-video \
  --composition snake-game-dev \
  --format mp4
```

---

### 方案 2: 使用 Explainer 模板

**适合**: 讲解开发流程和步骤

```bash
# 1. 初始化项目
python .codebuddy/skills/remotion/scripts/setup_remotion.py \
  snake-dev-explainer \
  --template explainer

# 2. 定义步骤
const steps = [
  {
    heading: "阶段 1: 基础框架",
    content: "创建 Canvas 画布、设计游戏区域、绘制网格"
  },
  {
    heading: "阶段 2: 游戏逻辑",
    content: "蛇的数据结构、移动逻辑、方向控制"
  },
  {
    heading: "阶段 3: 食物系统",
    content: "随机生成、碰撞检测、蛇身增长"
  },
  {
    heading: "阶段 4: 得分系统",
    content: "分数计算、关卡升级、速度递增"
  },
  {
    heading: "阶段 5: 完整游戏",
    content: "UI 界面、碰撞检测、响应式设计"
  }
];

# 3. 导出视频
python .codebuddy/skills/remotion/scripts/export_video.py \
  --project snake-dev-explainer \
  --composition snake-explainer \
  --format mp4
```

---

### 方案 3: 混合使用

**最佳方案**: 结合多种模板

1. **开场** (30秒): 使用 Slideshow 模板
   - 项目标题
   - 核心特性展示

2. **开发过程** (90秒): 使用 Code Animation 模板
   - 代码打字动画
   - 语法高亮

3. **步骤讲解** (60秒): 使用 Explainer 模板
   - 5个开发阶段
   - 逐步讲解

4. **总结** (30秒): 使用 Slideshow 模板
   - 项目成果
   - 总结要点

**总时长**: 3.5 分钟

---

## 🔧 脚本使用说明

### setup_remotion.py

**初始化 Remotion 项目**

```bash
python setup_remotion.py <project-name> [options]

选项:
  --template <template>  模板类型 (default, code-animation, explainer, slideshow)
  --path <path>          创建路径 (默认: .)

示例:
  python setup_remotion.py my-video --template code-animation
  python setup_remotion.py my-video --template explainer --path ./projects
```

---

### export_video.py

**导出 Remotion 视频**

```bash
python export_video.py --project <project> --composition <id> [options]

选项:
  --composition <id>    组件 ID (必需)
  --output <file>       输出文件名 (默认: {composition}.mp4)
  --format <format>     视频格式 (mp4, webm, gif)
  --fps <number>        帧率 (默认: 30)
  --quality <number>    质量 1-100 (默认: 90)
  --list                列出所有组件
  --preview             在浏览器中预览
  --check-deps          检查依赖

示例:
  python export_video.py --project my-video --composition my-video
  python export_video.py --project my-video --composition my-video --format webm --fps 60
  python export_video.py --project my-video --list
```

---

### validate_project.py

**验证 Remotion 项目**

```bash
python validate_project.py <project> [options]

选项:
  --verbose  显示详细输出

检查项:
  - 项目结构
  - package.json 配置
  - 组件定义
  - TypeScript 配置
  - node_modules

示例:
  python validate_project.py my-video
  python validate_project.py my-video --verbose
```

---

## 💡 使用技巧

### 1. 选择合适的模板

- **代码展示**: 使用 `code-animation` 模板
- **步骤讲解**: 使用 `explainer` 模板
- **图片展示**: 使用 `slideshow` 模板

### 2. 优化性能

- 使用 `<Still>` 包裹静态内容
- 压缩图片和音频
- 使用 CSS transform 代替布局变化
- 使用 `React.memo` 记忆化组件

### 3. 动画建议

- 保持动画简短（0.5-2 秒）
- 使用弹簧动画替代线性动画
- 添加缓动函数
- 交错相关元素的动画

### 4. 测试视频

- 使用 Remotion Studio 预览
- 测试不同帧率
- 测试不同分辨率
- 逐帧检查动画

---

## 📊 Skill 特性总结

### ✅ 核心功能

- [x] 完整的 Remotion 集成指南
- [x] Python 自动化脚本
- [x] 可复用的模板库
- [x] 详细的 API 文档
- [x] 动画模式参考
- [x] 最佳实践指南
- [x] 项目验证工具

### 🎯 支持的视频类型

- [x] 代码动画（带语法高亮）
- [x] 解释视频（步骤演示）
- [x] 幻灯片（图片轮播）
- [x] 数据可视化
- [x] 产品演示
- [x] 教育内容

### 🚀 自动化工具

- [x] 项目初始化
- [x] 视频导出
- [x] 项目验证
- [x] 依赖检查
- [x] 组件列表

### 📚 文档资源

- [x] 完整使用指南（SKILL.md）
- [x] API 参考
- [x] 动画模式库
- [x] 最佳实践

---

## 🎉 下一步

现在您可以：

1. **直接使用 Skill**
   ```
   "用 Remotion 制作贪吃蛇开发过程的视频"
   ```

2. **参考文档**
   - 阅读 `SKILL.md` 了解完整功能
   - 查看 `references/` 了解详细文档
   - 使用 `assets/templates/` 快速开始

3. **创建视频**
   ```bash
   python .codebuddy/skills/remotion/scripts/setup_remotion.py my-video --template explainer
   ```

---

## 📦 Git 提交

**Commit**: `deee7ec` - feat: add Remotion Skill for programmatic video creation

**文件**:
- `.codebuddy/skills/remotion/SKILL.md`
- `.codebuddy/skills/remotion/scripts/*.py` (3 个脚本)
- `.codebuddy/skills/remotion/references/*.md` (2 个文档)
- `.codebuddy/skills/remotion/assets/templates/*.tsx` (3 个模板)

**状态**: ✅ 已推送到 GitHub

---

## 🎊 总结

Remotion Skill 已完全创建并可以使用！

**立即开始**:
```bash
# 对我说：
"用 Remotion 制作贪吃蛇开发过程的视频"

# 我会自动：
# 1. 加载 Remotion Skill
# 2. 初始化项目
# 3. 创建视频组件
# 4. 导出视频

# 或者手动执行：
python .codebuddy/skills/remotion/scripts/setup_remotion.py \
  snake-dev-video \
  --template explainer
```

**祝您创建出精彩的视频！🎬✨**
