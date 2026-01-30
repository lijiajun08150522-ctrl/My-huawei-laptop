/**
 * Explainer Video Template
 *
 * Use this template for creating step-by-step explainer videos,
 * tutorials, and educational content.
 */

import {
  AbsoluteFill,
  useCurrentFrame,
  interpolate,
  spring,
  Series,
} from 'remotion';

interface ExplainerTemplateProps {
  title: string;
  subtitle: string;
  steps: Array<{
    heading: string;
    content: string;
  }>;
  backgroundColor?: string;
  textColor?: string;
  accentColor?: string;
}

export const ExplainerTemplate: React.FC<ExplainerTemplateProps> = ({
  title,
  subtitle,
  steps,
  backgroundColor = '#667eea',
  textColor = '#ffffff',
  accentColor = '#ffd700',
}) => {
  return (
    <Series>
      {/* Title slide */}
      <Series.Sequence durationInFrames={90}>
        <TitleSlide
          title={title}
          subtitle={subtitle}
          backgroundColor={backgroundColor}
          textColor={textColor}
          accentColor={accentColor}
        />
      </Series.Sequence>

      {/* Step slides */}
      {steps.map((step, index) => (
        <Series.Sequence key={index} durationInFrames={120}>
          <StepSlide
            step={step}
            stepNumber={index + 1}
            totalSteps={steps.length}
            backgroundColor={backgroundColor}
            textColor={textColor}
            accentColor={accentColor}
          />
        </Series.Sequence>
      ))}
    </Series>
  );
};

interface SlideProps {
  title?: string;
  subtitle?: string;
  step?: {heading: string; content: string};
  stepNumber?: number;
  totalSteps?: number;
  backgroundColor: string;
  textColor: string;
  accentColor: string;
}

const TitleSlide: React.FC<SlideProps> = ({
  title,
  subtitle,
  backgroundColor,
  textColor,
  accentColor,
}) => {
  const frame = useCurrentFrame();

  // Fade in
  const opacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateRight: 'clamp',
  });

  // Scale effect
  const scale = spring({
    frame,
    fps: 30,
    config: {damping: 15, stiffness: 100},
  });

  // Background gradient
  const bgOpacity = interpolate(frame, [0, 60], [0.5, 1]);

  return (
    <AbsoluteFill style={{
      background: `linear-gradient(135deg, ${backgroundColor} 0%, ${adjustColor(backgroundColor, -30)} 100%)`,
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      opacity,
    }}>
      <div style={{
        textAlign: 'center',
        transform: `scale(${scale})`,
      }}>
        <div style={{
          fontSize: '150px',
          fontWeight: 'bold',
          color: accentColor,
          marginBottom: '40px',
        }}>
          {title}
        </div>
        <div style={{
          fontSize: '80px',
          color: textColor,
          opacity: 0.9,
        }}>
          {subtitle}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const StepSlide: React.FC<SlideProps> = ({
  step,
  stepNumber,
  totalSteps,
  backgroundColor,
  textColor,
  accentColor,
}) => {
  const frame = useCurrentFrame();

  // Progress indicator
  const progress = interpolate(frame, [0, 30], [0, stepNumber || 1], {
    extrapolateRight: 'clamp',
  });

  // Content fade in
  const contentOpacity = interpolate(frame, [15, 45], [0, 1], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{
      background: `linear-gradient(135deg, ${backgroundColor} 0%, ${adjustColor(backgroundColor, -30)} 100%)`,
      display: 'flex',
      flexDirection: 'column',
      padding: '100px',
    }}>
      {/* Progress bar */}
      <div style={{
        display: 'flex',
        gap: '10px',
        marginBottom: '60px',
      }}>
        {Array.from({length: totalSteps || 1}).map((_, i) => (
          <div
            key={i}
            style={{
              flex: 1,
              height: '8px',
              backgroundColor: i < (stepNumber || 1) ? accentColor : 'rgba(255, 255, 255, 0.3)',
              borderRadius: '4px',
            }}
          />
        ))}
      </div>

      {/* Step number badge */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        marginBottom: '40px',
        opacity: contentOpacity,
      }}>
        <div style={{
          width: '80px',
          height: '80px',
          borderRadius: '50%',
          backgroundColor: accentColor,
          color: backgroundColor,
          fontSize: '40px',
          fontWeight: 'bold',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          marginRight: '20px',
        }}>
          {stepNumber}
        </div>
        <div style={{
          fontSize: '60px',
          fontWeight: 'bold',
          color: textColor,
        }}>
          {step?.heading}
        </div>
      </div>

      {/* Step content */}
      <div style={{
        fontSize: '40px',
        color: textColor,
        lineHeight: '1.6',
        opacity: contentOpacity,
      }}>
        {step?.content}
      </div>
    </AbsoluteFill>
  );
};

// Utility function to adjust color brightness
function adjustColor(color: string, amount: number): string {
  const hex = color.replace('#', '');
  const num = parseInt(hex, 16);
  const r = Math.min(255, Math.max(0, (num >> 16) + amount));
  const g = Math.min(255, Math.max(0, ((num >> 8) & 0x00FF) + amount));
  const b = Math.min(255, Math.max(0, (num & 0x0000FF) + amount));
  return `#${(1 << 24 | r << 16 | g << 8 | b).toString(16).slice(1)}`;
}

// Example usage
/*
export const ExampleExplainer: React.FC = () => {
  const steps = [
    {
      heading: 'Planning',
      content: 'Define objectives, identify audience, outline content'
    },
    {
      heading: 'Development',
      content: 'Write code, implement features, test functionality'
    },
    {
      heading: 'Deployment',
      content: 'Build project, deploy to production, monitor performance'
    },
  ];

  return (
    <ExplainerTemplate
      title="My Project"
      subtitle="A complete guide"
      steps={steps}
    />
  );
};
*/
