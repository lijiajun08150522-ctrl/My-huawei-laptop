/**
 * Slideshow Template
 *
 * Use this template for creating image slideshows,
  * photo galleries, and visual presentations.
 */

import {
  AbsoluteFill,
  useCurrentFrame,
  interpolate,
  spring,
  Series,
} from 'remotion';

interface Slide {
  title?: string;
  subtitle?: string;
  image?: string;
  backgroundColor?: string;
  textColor?: string;
}

interface SlideshowTemplateProps {
  slides: Slide[];
  transition?: 'fade' | 'slide' | 'zoom' | 'wipe';
  transitionDuration?: number;
  slideDuration?: number;
}

export const SlideshowTemplate: React.FC<SlideshowTemplateProps> = ({
  slides,
  transition = 'fade',
  transitionDuration = 30,
  slideDuration = 90,
}) => {
  return (
    <Series>
      {slides.map((slide, index) => (
        <Series.Sequence
          key={index}
          durationInFrames={slideDuration + transitionDuration}
        >
          <SlideElement
            slide={slide}
            index={index}
            total={slides.length}
            transition={transition}
            transitionDuration={transitionDuration}
            slideDuration={slideDuration}
          />
        </Series.Sequence>
      ))}
    </Series>
  );
};

interface SlideElementProps {
  slide: Slide;
  index: number;
  total: number;
  transition: string;
  transitionDuration: number;
  slideDuration: number;
}

const SlideElement: React.FC<SlideElementProps> = ({
  slide,
  transition,
  transitionDuration,
  slideDuration,
}) => {
  const frame = useCurrentFrame();

  const {
    backgroundColor = '#667eea',
    textColor = '#ffffff',
  } = slide;

  // Calculate transition progress
  const transitionProgress = frame < transitionDuration
    ? frame / transitionDuration
    : frame > slideDuration
      ? 1 - (frame - slideDuration) / transitionDuration
      : 1;

  // Transition effects
  const transitionStyle = getTransitionStyle(transition, transitionProgress);

  return (
    <AbsoluteFill style={{
      backgroundColor,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      ...transitionStyle,
    }}>
      {slide.image && (
        <img
          src={slide.image}
          alt={slide.title}
          style={{
            width: '80%',
            height: '60%',
            objectFit: 'contain',
            marginBottom: '40px',
            opacity: transitionProgress,
            transform: `scale(${transitionProgress})`,
          }}
        />
      )}

      {slide.title && (
        <div style={{
          fontSize: '80px',
          fontWeight: 'bold',
          color: textColor,
          marginBottom: '20px',
          opacity: transitionProgress,
        }}>
          {slide.title}
        </div>
      )}

      {slide.subtitle && (
        <div style={{
          fontSize: '50px',
          color: textColor,
          opacity: transitionProgress * 0.8,
        }}>
          {slide.subtitle}
        </div>
      )}
    </AbsoluteFill>
  );
};

function getTransitionStyle(transition: string, progress: number): React.CSSProperties {
  switch (transition) {
    case 'fade':
      return {
        opacity: progress,
      };

    case 'slide':
      return {
        transform: `translateX(${(1 - progress) * 100}%)`,
      };

    case 'zoom':
      return {
        transform: `scale(${progress})`,
        opacity: progress,
      };

    case 'wipe':
      return {
        clipPath: `inset(0 ${(1 - progress) * 100}% 0 0)`,
      };

    default:
      return {
        opacity: progress,
      };
  }
}

// Example usage
/*
export const ExampleSlideshow: React.FC = () => {
  const slides: Slide[] = [
    {
      title: 'Slide 1',
      subtitle: 'Introduction',
      backgroundColor: '#667eea',
    },
    {
      title: 'Slide 2',
      subtitle: 'Content',
      backgroundColor: '#764ba2',
    },
    {
      title: 'Slide 3',
      subtitle: 'Conclusion',
      backgroundColor: '#f093fb',
    },
  ];

  return (
    <SlideshowTemplate
      slides={slides}
      transition="fade"
      transitionDuration={30}
      slideDuration={90}
    />
  );
};
*/
