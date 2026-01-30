# Remotion Best Practices

Guidelines for creating efficient, performant, and maintainable Remotion videos.

## Performance Optimization

### 1. Optimize Images

**Before**:
```typescript
<img src="large-image.png" style={{width: '100%'}} />
```

**After**:
```typescript
<img src="optimized-image.webp" style={{width: '100%'}} />
```

**Tips**:
- Compress images before using (TinyPNG, Squoosh)
- Use WebP format for better compression
- Use appropriate resolution (don't use 4K for 1080p video)
- Consider SVG for vector graphics

### 2. Use Still for Static Content

**Before**:
```typescript
<MyExpensiveComponent />
```

**After**:
```typescript
<Still>
  <MyExpensiveComponent />
</Still>
```

**When to use**:
- Complex DOM trees that don't change
- Heavy calculations or computations
- Static text overlays
- Background graphics

### 3. Memoize Expensive Components

```typescript
import {memo} from 'react';

const ExpensiveComponent = memo(({data}) => {
  // Heavy computation
  const result = complexCalculation(data);

  return <div>{result}</div>;
});
```

**Benefits**:
- Prevents unnecessary re-renders
- Caches computed values
- Improves rendering performance

### 4. Use CSS Transforms Over Layout Changes

**Avoid**:
```typescript
<div style={{width: interpolate(frame, [0, 100], [0, 500])}} />
```

**Prefer**:
```typescript
<div style={{transform: `scaleX(${interpolate(frame, [0, 100], [0, 5])})`}} />
```

**Why**:
- Transforms are GPU-accelerated
- Layout changes trigger reflows
- Transforms are composable

### 5. Lazy Load Resources

```typescript
import {useCurrentFrame} from 'remotion';

const frame = useCurrentFrame();
const shouldLoadAudio = frame > 300;

return (
  <>
    {shouldLoadAudio && <Audio src="background-music.mp3" />}
    <Content />
  </>
);
```

### 6. Use useMemo and useCallback

```typescript
import {useMemo, useCallback} from 'react';
import {useCurrentFrame} from 'remotion';

const MyComponent = () => {
  const frame = useCurrentFrame();

  // Memoize expensive calculation
  const result = useMemo(() => {
    return expensiveCalculation(frame);
  }, [frame]);

  // Memoize event handler
  const handleClick = useCallback(() => {
    console.log('Clicked');
  }, []);

  return <div onClick={handleClick}>{result}</div>;
};
```

## Code Organization

### 1. Project Structure

```
src/
├── compositions/          # Video compositions
│   ├── Explainer.tsx
│   ├── ProductDemo.tsx
│   └── CodeAnimation.tsx
├── components/            # Reusable components
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   └── Text.tsx
│   ├── animations/
│   │   ├── FadeIn.tsx
│   │   ├── SlideUp.tsx
│   │   └── ScaleIn.tsx
│   └── visualization/
│       ├── BarChart.tsx
│       └── LineChart.tsx
├── utils/
│   ├── animations.ts      # Animation helpers
│   ├── colors.ts          # Color palette
│   └── typography.ts      # Typography constants
├── assets/
│   ├── images/
│   ├── audio/
│   └── fonts/
└── Root.tsx              # Entry point
```

### 2. Component Composition

**Good**:
```typescript
const ExplainerVideo: React.FC = () => {
  return (
    <Series>
      <Series.Sequence durationInFrames={60}>
        <Section1 />
      </Series.Sequence>
      <Series.Sequence durationInFrames={60}>
        <Section2 />
      </Series.Sequence>
    </Series>
  );
};

const Section1: React.FC = () => {
  return (
    <AbsoluteFill>
      <FadeIn>
        <Heading>Introduction</Heading>
      </FadeIn>
      <SlideUp>
        <Content>...</Content>
      </SlideUp>
    </AbsoluteFill>
  );
};
```

**Bad**:
```typescript
// Everything in one component
const ExplainerVideo: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <div style={{opacity: interpolate(frame, [0, 30], [0, 1])}}>
      <div style={{transform: `translateY(${interpolate(frame, [0, 60], [50, 0])}px)`}}>
        {/* 1000 more lines... */}
      </div>
    </div>
  );
};
```

### 3. Separate Concerns

```typescript
// Animation logic
const useFadeIn = (duration: number = 30) => {
  const frame = useCurrentFrame();
  return interpolate(frame, [0, duration], [0, 1]);
};

// Presentation component
const FadeIn: React.FC<{children: React.ReactNode}> = ({children}) => {
  const opacity = useFadeIn();
  return <div style={{opacity}}>{children}</div>;
};

// Usage
<FadeIn>
  <MyContent />
</FadeIn>
```

## Asset Management

### 1. Image Optimization

**Checklist**:
- [ ] Compress images (quality 80-90%)
- [ ] Use WebP format when possible
- [ ] Match resolution to video size
- [ ] Remove metadata
- [ ] Use SVG for vector graphics

**Tools**:
- TinyPNG (https://tinypng.com/)
- Squoosh (https://squoosh.app/)
- ImageOptim

### 2. Audio Optimization

**Tips**:
- Use MP3 or AAC format
- Sample rate: 44.1kHz
- Bitrate: 128-192 kbps for music, 64-96 kbps for voice
- Trim silence
- Normalize audio levels

**Tools**:
- Audacity (free)
- ffmpeg (command line)

### 3. Font Management

```typescript
// Load custom font
import {loadFont} from '@remotion/fonts';

// In Root.tsx or before using
loadFont({
  family: 'Custom Font',
  src: 'https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap',
});
```

**Best Practices**:
- Use web-safe fonts when possible
- Load fonts asynchronously
- Use `font-display: swap` for performance
- Limit font weights loaded

## Animation Best Practices

### 1. Use Springs Over Linear Animations

```typescript
// ❌ Linear animation (feels mechanical)
const scale = interpolate(frame, [0, 60], [0, 1]);

// ✅ Spring animation (feels natural)
const scale = spring({
  frame,
  fps: 30,
  config: {damping: 10, stiffness: 100},
});
```

### 2. Keep Animations Short

**Guidelines**:
- Fade in/out: 0.5-1 second (15-30 frames at 30fps)
- Slide transitions: 0.5-1 second
- Scale animations: 0.5-1 second
- Rotation: 0.5-2 seconds

```typescript
// ❌ Too long (2 seconds)
const opacity = interpolate(frame, [0, 60], [0, 1]);

// ✅ Just right (0.5 seconds)
const opacity = interpolate(frame, [0, 15], [0, 1]);
```

### 3. Use Easing Functions

```typescript
const easeOut = (t: number) => 1 - Math.pow(1 - t, 3);
const easeInOut = (t: number) => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

const value = easeOut(progress);
```

### 4. Stagger Animations

```typescript
items.map((item, index) => {
  const delay = index * 5; // 5 frame delay between items
  const frameWithDelay = frame - delay;
  const opacity = Math.min(1, Math.max(0, frameWithDelay / 20));

  return <div key={index} style={{opacity}}>{item}</div>;
});
```

## Audio Best Practices

### 1. Use Remotion Audio Component

```typescript
// ✅ Good: Remotion Audio component
<Audio src="background-music.mp3" />

// ❌ Bad: HTML audio element
<audio src="background-music.mp3" />
```

**Why**:
- Better synchronization
- Better performance
- Proper encoding

### 2. Fade Audio In/Out

```typescript
import {useCurrentFrame, interpolate} from 'remotion';

const frame = useCurrentFrame();
const volume = interpolate(
  frame,
  [0, 30, duration - 30, duration],
  [0, 1, 1, 0],
  {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}
);

<Audio src="music.mp3" volume={volume} />
```

### 3. Audio Level Management

```typescript
// Background music: 0.3-0.5
<Audio src="background-music.mp3" volume={0.4} />

// Narration: 0.8-1.0
<Audio src="narration.mp3" volume={1.0} />

// Sound effects: 0.5-0.7
<Audio src="effect.mp3" volume={0.6} />
```

## Debugging

### 1. Use Console Logging

```typescript
const frame = useCurrentFrame();

// Debug frame-dependent values
if (frame % 30 === 0) {
  console.log(`Frame: ${frame}, Opacity: ${opacity}`);
}
```

### 2. Preview at Different Speeds

```typescript
// Test animations at different frame rates
const {fps} = useVideoConfig();
const adjustedFrame = frame * (30 / fps);
```

### 3. Check Composition Duration

```typescript
import {useVideoConfig} from 'remotion';

const {durationInFrames} = useVideoConfig();

console.log(`Total duration: ${durationInFrames} frames (${durationInFrames / 30}s)`);
```

## Testing

### 1. Test Frame-by-Frame

Use Remotion Studio to preview each frame:
- Navigate to specific frames
- Check animations at key points
- Verify transitions

### 2. Test Different Resolutions

```typescript
// Test at different resolutions
<Composition
  id="my-composition"
  component={MyComponent}
  width={1920}
  height={1080}
  // Also test: 1280x720, 3840x2160
/>
```

### 3. Test at Different Frame Rates

```typescript
<Composition
  id="my-composition"
  component={MyComponent}
  fps={24} // Also test: 30, 60
  // Use frame-rate-independent calculations
/>
```

## Common Pitfalls

### 1. Hardcoded Frame Numbers

```typescript
// ❌ Hardcoded
const opacity = frame < 30 ? 0 : 1;

// ✅ Dynamic
const opacity = Math.min(1, frame / 30);
```

### 2. Not Using AbsoluteFill Correctly

```typescript
// ❌ Wrong - doesn't center properly
<div style={{position: 'absolute', left: '50%', top: '50%'}}>
  Content
</div>

// ✅ Right - uses AbsoluteFill
<AbsoluteFill style={{
  justifyContent: 'center',
  alignItems: 'center'
}}>
  Content
</AbsoluteFill>
```

### 3. Forgetting to Memoize

```typescript
// ❌ Recalculates every render
const calculated = expensiveFunction(data);

// ✅ Cached result
const calculated = useMemo(() => expensiveFunction(data), [data]);
```

### 4. Using Wrong Image Format

```typescript
// ❌ PNG for large photos
<img src="large-photo.png" />

// ✅ WebP or JPEG
<img src="large-photo.webp" />
```

## Performance Checklist

Before exporting, verify:

- [ ] Images are optimized and compressed
- [ ] Audio files are trimmed and normalized
- [ ] Complex static components use `<Still>`
- [ ] Expensive components are memoized
- [ ] Transforms used instead of layout changes
- [ ] Animations are short and smooth
- [ ] No unnecessary re-renders
- [ ] Frame rate is consistent
- [ ] Assets are properly loaded
- [ ] No console errors or warnings

## Production Tips

### 1. Pre-render Complex Scenes

```typescript
// For very complex scenes, pre-render and use as video
<Video src="pre-rendered-scene.mp4" />
```

### 2. Use Appropriate Video Settings

```typescript
// In remotion.config.ts
Config.setVideoImageFormat('jpeg');
Config.setPixelFormat('yuv420p');
Config.setConcurrency(4); // Adjust based on CPU
```

### 3. Export in Batches

For very long videos:
```bash
# Export in segments
npm run build -- --sequence start=0 --duration=900
npm run build -- --sequence start=900 --duration=900
```

### 4. Monitor Resource Usage

- Check CPU usage during rendering
- Monitor memory consumption
- Adjust concurrency if needed

## Additional Resources

- [Remotion Performance Guide](https://www.remotion.dev/docs/performance)
- [React Performance Optimization](https://react.dev/learn/render-and-commit)
- [Web Performance](https://web.dev/performance/)
