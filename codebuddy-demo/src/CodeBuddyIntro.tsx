import {
  AbsoluteFill,
  useCurrentFrame,
  interpolate,
  spring,
  Series,
} from 'remotion';

export const CodeBuddyIntro: React.FC = () => {
  return (
    <Series>
      {/* Intro Scene */}
      <Series.Sequence durationInFrames={120}>
        <IntroScene />
      </Series.Sequence>

      {/* Features Scene */}
      <Series.Sequence durationInFrames={180}>
        <FeaturesScene />
      </Series.Sequence>

      {/* Demo Scene */}
      <Series.Sequence durationInFrames={180}>
        <DemoScene />
      </Series.Sequence>

      {/* Outro Scene */}
      <Series.Sequence durationInFrames={60}>
        <OutroScene />
      </Series.Sequence>
    </Series>
  );
};

// macOS Window Component
const MacWindow: React.FC<{
  title: string;
  children: React.ReactNode;
  frame: number;
  delay?: number;
}> = ({title, children, frame, delay = 0}) => {
  const frameWithDelay = Math.max(0, frame - delay);
  const scale = spring({
    frame: frameWithDelay,
    fps: 30,
    config: {damping: 12, stiffness: 100},
  });

  const opacity = Math.min(1, frameWithDelay / 30);

  return (
    <div
      style={{
        position: 'absolute',
        left: '50%',
        top: '50%',
        transform: `translate(-50%, -50%) scale(${scale})`,
        width: '1200px',
        height: '700px',
        opacity,
      }}
    >
      {/* Window Title Bar */}
      <div
        style={{
          width: '100%',
          height: '38px',
          background: 'linear-gradient(to bottom, #3a3a3c 0%, #2c2c2e 100%)',
          borderRadius: '12px 12px 0 0',
          display: 'flex',
          alignItems: 'center',
          padding: '0 16px',
          gap: '8px',
          borderBottom: '1px solid rgba(0, 0, 0, 0.3)',
        }}
      >
        {/* Traffic Lights */}
        <div
          style={{
            width: '12px',
            height: '12px',
            borderRadius: '50%',
            backgroundColor: '#FF5F57',
            boxShadow: '0 0 3px rgba(255, 95, 87, 0.5)',
          }}
        />
        <div
          style={{
            width: '12px',
            height: '12px',
            borderRadius: '50%',
            backgroundColor: '#FEBC2E',
            boxShadow: '0 0 3px rgba(254, 188, 46, 0.5)',
          }}
        />
        <div
          style={{
            width: '12px',
            height: '12px',
            borderRadius: '50%',
            backgroundColor: '#28C840',
            boxShadow: '0 0 3px rgba(40, 200, 64, 0.5)',
          }}
        />

        {/* Window Title */}
        <div
          style={{
            flex: 1,
            textAlign: 'center',
            fontSize: '13px',
            fontWeight: 500,
            color: '#e5e5e5',
            fontFamily: '-apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif',
          }}
        >
          {title}
        </div>
      </div>

      {/* Window Content */}
      <div
        style={{
          width: '100%',
          height: 'calc(100% - 38px)',
          background: '#1e1e1e',
          borderRadius: '0 0 12px 12px',
          overflow: 'hidden',
          boxShadow: '0 20px 60px rgba(0, 0, 0, 0.5)',
        }}
      >
        {children}
      </div>
    </div>
  );
};

// Intro Scene
const IntroScene: React.FC = () => {
  const frame = useCurrentFrame();

  const titleOpacity = Math.min(1, frame / 45);
  const subtitleOpacity = Math.max(0, Math.min(1, (frame - 30) / 45));
  const logoScale = spring({
    frame,
    fps: 30,
    config: {damping: 15, stiffness: 120},
  });

  return (
    <AbsoluteFill style={{
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
    }}>
      {/* Logo */}
      <div
        style={{
          fontSize: '180px',
          marginBottom: '40px',
          transform: `scale(${logoScale})`,
          opacity: titleOpacity,
        }}
      >
        💻
      </div>

      {/* Title */}
      <div
        style={{
          fontSize: '100px',
          fontWeight: 700,
          color: '#ffffff',
          marginBottom: '30px',
          fontFamily: '-apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif',
          opacity: titleOpacity,
        }}
      >
        CodeBuddy
      </div>

      {/* Subtitle */}
      <div
        style={{
          fontSize: '48px',
          fontWeight: 400,
          color: 'rgba(255, 255, 255, 0.9)',
          fontFamily: '-apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif',
          opacity: subtitleOpacity,
        }}
      >
        你的 AI 编程助手
      </div>

      {/* Decorative Elements */}
      {[1, 2, 3].map((i) => {
        const delay = i * 10;
        const frameWithDelay = Math.max(0, frame - delay);
        const y = spring({
          frame: frameWithDelay,
          fps: 30,
          config: {damping: 8, stiffness: 150},
        });
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              width: '20px',
              height: '20px',
              borderRadius: '50%',
              backgroundColor: 'rgba(255, 255, 255, 0.3)',
              left: `${20 + i * 30}%`,
              top: `${20 + y * 100}px`,
              opacity: Math.min(1, frameWithDelay / 30),
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

// Features Scene
const FeaturesScene: React.FC = () => {
  const frame = useCurrentFrame();

  const features = [
    {icon: '🤖', title: 'AI 智能辅助', desc: '理解需求，生成代码', delay: 0},
    {icon: '🎯', title: '精准定位问题', desc: '快速找到解决方案', delay: 40},
    {icon: '⚡', title: '高效开发', desc: '节省时间，提高效率', delay: 80},
    {icon: '📚', title: '丰富文档', desc: '自动生成技术文档', delay: 120},
  ];

  return (
    <AbsoluteFill style={{
      background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
    }}>
      <div
        style={{
          width: '1600px',
          height: '900px',
          display: 'grid',
          gridTemplateColumns: 'repeat(2, 1fr)',
          gap: '40px',
          padding: '80px',
        }}
      >
        {features.map((feature, index) => {
          const frameWithDelay = Math.max(0, frame - feature.delay);
          const opacity = Math.min(1, frameWithDelay / 30);
          const translateY = interpolate(
            frameWithDelay,
            [0, 30],
            [50, 0],
            {extrapolateRight: 'clamp'}
          );

          return (
            <div
              key={index}
              style={{
                background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)',
                borderRadius: '20px',
                padding: '40px',
                border: '1px solid rgba(102, 126, 234, 0.2)',
                transform: `translateY(${translateY}px)`,
                opacity,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                textAlign: 'center',
              }}
            >
              <div style={{fontSize: '80px', marginBottom: '20px'}}>
                {feature.icon}
              </div>
              <div
                style={{
                  fontSize: '36px',
                  fontWeight: 700,
                  color: '#ffffff',
                  marginBottom: '12px',
                  fontFamily: '-apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif',
                }}
              >
                {feature.title}
              </div>
              <div
                style={{
                  fontSize: '24px',
                  color: 'rgba(255, 255, 255, 0.8)',
                  fontFamily: '-apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif',
                }}
              >
                {feature.desc}
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// Demo Scene
const DemoScene: React.FC = () => {
  const frame = useCurrentFrame();

  const code = `const createTask = (title) => {
  const task = {
    id: Date.now(),
    title,
    completed: false,
    createdAt: new Date()
  };

  return task;
};

// 创建一个任务
const myTask = createTask("完成项目文档");
console.log(myTask);`;

  const charsToShow = Math.min(code.length, Math.floor(frame / 2));
  const visibleCode = code.slice(0, charsToShow);

  const cursorOpacity = Math.abs(Math.sin(frame / 5));

  return (
    <AbsoluteFill style={{
      background: 'linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%)',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
    }}>
      <MacWindow title="CodeBuddy IDE" frame={frame}>
        <div
          style={{
            width: '100%',
            height: '100%',
            padding: '40px',
            fontFamily: 'Menlo, Monaco, Consolas, monospace',
            fontSize: '28px',
            lineHeight: '1.6',
            color: '#d4d4d4',
            whiteSpace: 'pre-wrap',
            overflow: 'hidden',
          }}
        >
          <code
            dangerouslySetInnerHTML={{
              __html: highlightCode(visibleCode) + `<span style="opacity: ${cursorOpacity}">▌</span>`,
            }}
          />
        </div>
      </MacWindow>
    </AbsoluteFill>
  );
};

// Outro Scene
const OutroScene: React.FC = () => {
  const frame = useCurrentFrame();

  const opacity = Math.min(1, frame / 30);
  const scale = spring({
    frame,
    fps: 30,
    config: {damping: 12, stiffness: 100},
  });

  return (
    <AbsoluteFill style={{
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      opacity,
    }}
    >
      <div
        style={{
          fontSize: '150px',
          marginBottom: '40px',
          transform: `scale(${scale})`,
        }}
      >
        🎉
      </div>

      <div
        style={{
          fontSize: '80px',
          fontWeight: 700,
          color: '#ffffff',
          marginBottom: '30px',
          fontFamily: '-apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif',
        }}
      >
        让编程更简单
      </div>

      <div
        style={{
          fontSize: '40px',
          fontWeight: 400,
          color: 'rgba(255, 255, 255, 0.9)',
          fontFamily: '-apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif',
        }}
      >
        体验 CodeBuddy，开启智能编程之旅
      </div>
    </AbsoluteFill>
  );
};

// Simple syntax highlighting
function highlightCode(code: string): string {
  let html = code;

  // Keywords (purple)
  const keywords = ['const', 'let', 'var', 'function', 'return', 'if', 'else', 'for', 'while'];
  keywords.forEach(keyword => {
    const regex = new RegExp(`\\b${keyword}\\b`, 'g');
    html = html.replace(regex, `<span style="color: #c586c0">${keyword}</span>`);
  });

  // Strings (orange)
  html = html.replace(/(["'`])(.*?)\1/g, `<span style="color: #ce9178">$&</span>`);

  // Numbers (light green)
  html = html.replace(/\b(\d+)\b/g, `<span style="color: #b5cea8">$1</span>`);

  // Comments (gray)
  html = html.replace(/(\/\/.*$)/gm, `<span style="color: #6a9955">$1</span>`);

  // Functions (yellow)
  html = html.replace(/(\w+)\s*\(/g, `<span style="color: #dcdcaa">$1</span>`);

  return html;
}
