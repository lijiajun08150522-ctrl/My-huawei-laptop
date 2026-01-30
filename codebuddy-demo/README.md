# CodeBuddy Introduction Video

macOS 风格的 CodeBuddy 介绍视频，使用 Remotion 框架制作。

## 视频内容

### 场景结构

1. **开场场景** (0-4秒)
   - CodeBuddy Logo 和标题
   - 副标题：你的 AI 编程助手
   - 渐变背景 + 装饰元素

2. **功能展示** (4-10秒)
   - 4 个核心功能卡片：
     - 🤖 AI 智能辅助
     - 🎯 精准定位问题
     - ⚡ 高效开发
     - 📚 丰富文档
   - 卡片依次淡入动画

3. **代码演示** (10-16秒)
   - macOS 窗口风格代码编辑器
   - 代码打字动画
   - 语法高亮
   - 光标闪烁效果

4. **结尾场景** (16-18秒)
   - 庆祝图标 🎉
   - 标语：让编程更简单
   - 号召行动

## 设计特点

### macOS 风格元素

- **窗口样式**
  - 圆角边框 (12px)
  - 渐变标题栏
  - 交通灯按钮（红/黄/绿）
  - 阴影效果

- **字体系统**
  - SF Pro Display（标题）
  - SF Pro Text（正文）
  - Menlo/Consolas（代码）

- **配色方案**
  - 渐变背景 (#667eea → #764ba2)
  - 深色编辑器 (#1e1e1e)
  - 语法高亮（VS Code 配色）

### 动画效果

- **开场**
  - Logo 缩放弹入
  - 标题淡入
  - 装饰元素飘动

- **功能卡片**
  - 依次淡入
  - 上滑位移
  - 悬停效果

- **代码演示**
  - 打字机效果
  - 光标闪烁
  - 窗口弹出动画

- **结尾**
  - 缩放弹入
  - 整体淡入

## 技术规格

- **分辨率**: 1920x1080 (1080p)
- **帧率**: 30 fps
- **总时长**: 18 秒 (540 帧)
- **格式**: 支持 MP4, WebM, GIF

## 安装和运行

### 前置要求

1. **Node.js** (v14 或更高)
2. **FFmpeg** (用于视频编码)

### 安装依赖

```bash
cd codebuddy-demo
npm install
```

### 启动预览

```bash
npm start
```

访问 http://localhost:3000 预览视频

### 导出视频

```bash
# 默认导出 (MP4)
npm run build -- --props='{}' --code=codebuddy-intro

# 指定输出文件
npm run build -- --props='{}' --code=codebuddy-intro --output=codebuddy-demo.mp4

# 不同格式
npm run build -- --props='{}' --code=codebuddy-intro --format=webm
```

## 文件结构

```
codebuddy-demo/
├── src/
│   ├── Root.tsx              # 入口文件
│   └── CodeBuddyIntro.tsx    # 主视频组件
├── public/                   # 静态资源
├── package.json             # 项目配置
├── tsconfig.json            # TypeScript 配置
├── remotion.config.ts       # Remotion 配置
└── README.md               # 本文档
```

## 自定义

### 修改文本

编辑 `src/CodeBuddyIntro.tsx` 中的文本内容：

- 标题、副标题
- 功能描述
- 代码内容

### 调整动画

修改动画参数：

- `durationInFrames`: 每个场景的时长
- `delay`: 元素延迟时间
- `spring`: 弹簧动画参数
- `interpolate`: 线性插值参数

### 修改配色

更新 CSS 变量或内联样式：

- 背景渐变
- 窗口颜色
- 文字颜色

## 性能优化

- 使用 `AbsoluteFill` 优化布局
- 静态内容使用 `Still` 组件
- 图片使用 WebP 格式
- 避免不必要的重渲染

## 故障排除

### 视频无法渲染

确保 FFmpeg 已安装并在 PATH 中：
```bash
ffmpeg -version
```

### 音频同步问题

使用 Remotion 的 `<Audio>` 组件而非 HTML `<audio>`

### 性能问题

- 降低预览分辨率
- 优化组件渲染
- 使用 `React.memo` 缓存组件

## 许可证

MIT License
