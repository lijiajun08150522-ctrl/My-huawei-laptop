/**
 * Code Animation Template
 *
 * Use this template for creating code typing animations,
 * syntax highlighting, and code explanations.
 */

import {
  AbsoluteFill,
  useCurrentFrame,
  interpolate,
  spring,
} from 'remotion';

interface CodeAnimationProps {
  code: string;
  language?: string;
  typingSpeed?: number;
  showLineNumbers?: boolean;
}

export const CodeAnimationTemplate: React.FC<CodeAnimationProps> = ({
  code,
  language = 'javascript',
  typingSpeed = 2,
  showLineNumbers = true,
}) => {
  const frame = useCurrentFrame();

  // Typewriter effect
  const charsToShow = Math.min(code.length, Math.floor(frame / typingSpeed));
  const visibleCode = code.slice(0, charsToShow);

  // Cursor blinking
  const cursorOpacity = Math.abs(Math.sin(frame / 10));

  // Fade in effect
  const opacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateRight: 'clamp',
  });

  // Simple syntax highlighting
  const highlightedCode = highlightCode(visibleCode, language);

  return (
    <AbsoluteFill style={{
      backgroundColor: '#1e1e1e',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      opacity,
    }}>
      <div style={{
        width: '80%',
        height: '80%',
        backgroundColor: '#2d2d2d',
        borderRadius: '10px',
        padding: '40px',
        fontFamily: "'Fira Code', 'Consolas', monospace",
        fontSize: '28px',
        color: '#d4d4d4',
        whiteSpace: 'pre-wrap',
        overflow: 'hidden',
        boxShadow: '0 10px 30px rgba(0, 0, 0, 0.5)',
      }}>
        <pre
          style={{margin: 0, lineHeight: '1.6'}}
          dangerouslySetInnerHTML={{
            __html: highlightedCode + `<span style="opacity: ${cursorOpacity}">▌</span>`
          }}
        />
      </div>
    </AbsoluteFill>
  );
};

// Simple syntax highlighting function
function highlightCode(code: string, language: string): string {
  let html = code;

  // Keywords (blue)
  const keywords = ['function', 'const', 'let', 'var', 'if', 'else', 'for', 'while', 'return', 'import', 'export', 'from', 'class', 'extends', 'new', 'this', 'async', 'await'];
  keywords.forEach(keyword => {
    const regex = new RegExp(`\\b${keyword}\\b`, 'g');
    html = html.replace(regex, `<span style="color: #569cd6">${keyword}</span>`);
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
