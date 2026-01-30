# Common Animation Patterns

Collection of reusable animation patterns for Remotion videos.

## Fade Animations

### Simple Fade In

```typescript
import {useCurrentFrame, interpolate} from 'remotion';

export const FadeIn: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1]);

  return (
    <div style={{opacity}}>
      Content fades in
    </div>
  );
};
```

### Fade Out

```typescript
const opacity = interpolate(frame, [duration - 30, duration], [1, 0]);
```

### Fade In and Out

```typescript
const opacity = interpolate(
  frame,
  [0, 30, duration - 30, duration],
  [0, 1, 1, 0]
);
```

## Scale Animations

### Scale Up

```typescript
import {useCurrentFrame, spring} from 'remotion';

export const ScaleUp: React.FC = () => {
  const frame = useCurrentFrame();
  const scale = spring({
    frame,
    fps: 30,
    config: {damping: 10, stiffness: 100},
  });

  return (
    <div style={{
      transform: `scale(${scale})`,
      transformOrigin: 'center',
    }}>
      Content scales up
    </div>
  );
};
```

### Scale Down

```typescript
const scale = spring({
  frame,
  fps: 30,
  config: {damping: 15, stiffness: 80},
  reverse: true,
});
```

### Pulse

```typescript
const scale = spring({
  frame,
  fps: 30,
  config: {damping: 5, stiffness: 150},
});

// Oscillate between 1 and 1.2
const pulse = 1 + Math.sin(frame / 10) * 0.2;
```

## Slide Animations

### Slide From Left

```typescript
import {useCurrentFrame, interpolate} from 'remotion';

export const SlideFromLeft: React.FC = () => {
  const frame = useCurrentFrame();
  const x = interpolate(frame, [0, 60], [-100, 0]);

  return (
    <div style={{
      transform: `translateX(${x}%)`,
    }}>
      Content slides in
    </div>
  );
};
```

### Slide From Right

```typescript
const x = interpolate(frame, [0, 60], [100, 0]);
```

### Slide From Top

```typescript
const y = interpolate(frame, [0, 60], [-100, 0]);
```

### Slide From Bottom

```typescript
const y = interpolate(frame, [0, 60], [100, 0]);
```

## Rotation Animations

### Continuous Rotation

```typescript
import {useCurrentFrame} from 'remotion';

const angle = frame * 2; // 2 degrees per frame

<div style={{
  transform: `rotate(${angle}deg)`,
}}>
  Rotating element
</div>
```

### Spin In

```typescript
const angle = interpolate(frame, [0, 60], [360, 0]);
```

### Spin Out

```typescript
const angle = interpolate(frame, [duration - 60, duration], [0, 360]);
```

## Text Animations

### Typewriter Effect

```typescript
import {useCurrentFrame} from 'remotion';

export const Typewriter: React.FC<{text: string}> = ({text}) => {
  const frame = useCurrentFrame();
  const charsToShow = Math.min(text.length, Math.floor(frame / 2));
  const visibleText = text.slice(0, charsToShow);

  return (
    <div>
      {visibleText}<span style={{opacity: 0.5}}>▌</span>
    </div>
  );
};
```

### Word by Word Reveal

```typescript
const words = text.split(' ');
const wordsToShow = Math.min(words.length, Math.floor(frame / 5));
const visibleWords = words.slice(0, wordsToShow).join(' ');
```

### Letter Animation (Bounce)

```typescript
const bounce = (charIndex: number) => {
  const delay = charIndex * 3;
  const frameWithDelay = frame - delay;
  const yOffset = spring({
    frame: Math.max(0, frameWithDelay),
    fps: 30,
    config: {damping: 8, stiffness: 200},
  });

  return {
    transform: `translateY(${(1 - yOffset) * -20}px)`,
  };
};
```

## Path Animations

### Follow Path

```typescript
import {useCurrentFrame, interpolate} from 'remotion';

const getPathPoint = (progress: number) => {
  const t = progress * Math.PI * 2;
  return {
    x: Math.cos(t) * 100,
    y: Math.sin(t) * 100,
  };
};

const frame = useCurrentFrame();
const progress = frame / 300;
const point = getPathPoint(progress);

<div style={{
  position: 'absolute',
  left: '50%',
  top: '50%',
  transform: `translate(${point.x}px, ${point.y}px)`,
}}>
  Follows circular path
</div>
```

### Draw Line

```typescript
import {useCurrentFrame, interpolate} from 'remotion';

const frame = useCurrentFrame();
const dashOffset = interpolate(frame, [0, 60], [1000, 0]);

<svg width="100%" height="100%">
  <path
    d="M 100 100 L 500 100"
    stroke="black"
    strokeWidth="5"
    strokeDasharray="1000"
    strokeDashoffset={dashOffset}
  />
</svg>
```

## Bounce Animations

### Drop Bounce

```typescript
import {useCurrentFrame, spring} from 'remotion';

const frame = useCurrentFrame();
const y = spring({
  frame,
  fps: 30,
  config: {
    mass: 1,
    damping: 10,
    stiffness: 100,
  },
});

<div style={{
  transform: `translateY(${(1 - y) * 300}px)`,
}}>
  Bouncing element
</div>
```

### Elastic Bounce

```typescript
const y = spring({
  frame,
  fps: 30,
  config: {
    mass: 0.5,
    damping: 5,
    stiffness: 150,
  },
});
```

## Stagger Animations

### Sequential Stagger

```typescript
const items = ['Item 1', 'Item 2', 'Item 3'];

items.map((item, index) => {
  const delay = index * 15;
  const frameWithDelay = frame - delay;
  const opacity = Math.min(1, Math.max(0, frameWithDelay / 30));

  return (
    <div key={index} style={{opacity}}>
      {item}
    </div>
  );
});
```

### Wave Stagger

```typescript
items.map((item, index) => {
  const delay = index * 5;
  const frameWithDelay = frame - delay;
  const scale = spring({
    frame: Math.max(0, frameWithDelay),
    fps: 30,
    config: {damping: 10, stiffness: 100},
  });

  return (
    <div key={index} style={{
      transform: `scale(${scale})`,
    }}>
      {item}
    </div>
  );
});
```

## Transition Patterns

### Crossfade

```typescript
import {useCurrentFrame, interpolate} from 'remotion';

const fadeOut = interpolate(frame, [0, 30], [1, 0]);
const fadeIn = interpolate(frame, [30, 60], [0, 1]);

return (
  <>
    <div style={{opacity: fadeOut}}>Old Content</div>
    <div style={{opacity: fadeIn}}>New Content</div>
  </>
);
```

### Push Transition

```typescript
const oldX = interpolate(frame, [0, 30], [0, -100]);
const newX = interpolate(frame, [0, 30], [100, 0]);

return (
  <>
    <div style={{transform: `translateX(${oldX}%)`}}>Old</div>
    <div style={{transform: `translateX(${newX}%)`}}>New</div>
  </>
);
```

### Zoom Transition

```typescript
const oldScale = interpolate(frame, [0, 30], [1, 0.5]);
const newScale = interpolate(frame, [0, 30], [2, 1]);

return (
  <>
    <div style={{transform: `scale(${oldScale})`}}>Old</div>
    <div style={{transform: `scale(${newScale})`}}>New</div>
  </>
);
```

## Data Visualization Animations

### Bar Chart Growth

```typescript
import {useCurrentFrame, spring} from 'remotion';

const data = [10, 25, 40, 30, 50];

data.map((value, index) => {
  const delay = index * 5;
  const frameWithDelay = frame - delay;
  const height = spring({
    frame: Math.max(0, frameWithDelay),
    fps: 30,
    config: {damping: 10, stiffness: 100},
  }) * value;

  return (
    <div key={index} style={{
      height: `${height}%`,
      backgroundColor: 'blue',
    }}>
    </div>
  );
});
```

### Line Chart Draw

```typescript
const progress = interpolate(frame, [0, 100], [0, 1]);

const points = data.map((value, index) => {
  const x = (index / (data.length - 1)) * 100;
  const y = value;
  return `${x},${y}`;
}).join(' ');

<svg width="100%" height="100%">
  <path
    d={`M ${points}`}
    fill="none"
    stroke="blue"
    strokeWidth="3"
    strokeDasharray={points.length * 100}
    strokeDashoffset={(1 - progress) * points.length * 100}
  />
</svg>
```

## Particle Effects

### Floating Particles

```typescript
const particles = Array.from({length: 50}, (_, i) => {
  const x = Math.random() * 100;
  const y = Math.random() * 100;
  const size = Math.random() * 10 + 5;
  const speed = Math.random() * 2 + 1;

  const particleFrame = (frame * speed + i * 10) % 200;
  const yOffset = Math.sin(particleFrame / 20) * 50;
  const opacity = Math.sin(particleFrame / 50) * 0.5 + 0.5;

  return (
    <div
      key={i}
      style={{
        position: 'absolute',
        left: `${x}%`,
        top: `${y}%`,
        width: `${size}px`,
        height: `${size}px`,
        backgroundColor: 'rgba(255, 255, 255, 0.5)',
        borderRadius: '50%',
        transform: `translateY(${yOffset}px)`,
        opacity,
      }}
    />
  );
});
```

### Confetti

```typescript
const confetti = Array.from({length: 100}, (_, i) => {
  const x = Math.random() * 100;
  const startY = -20;
  const color = `hsl(${Math.random() * 360}, 70%, 50%)`;
  const speed = Math.random() * 3 + 2;
  const rotation = Math.random() * 360;

  const fallDistance = frame * speed;
  const y = startY + fallDistance;
  const currentRotation = rotation + frame * 5;

  return (
    <div
      key={i}
      style={{
        position: 'absolute',
        left: `${x}%`,
        top: `${y}%`,
        width: '10px',
        height: '10px',
        backgroundColor: color,
        transform: `rotate(${currentRotation}deg)`,
      }}
    />
  );
});
```

## UI Patterns

### List Reveal

```typescript
const items = ['Item 1', 'Item 2', 'Item 3', 'Item 4'];

items.map((item, index) => {
  const delay = index * 10;
  const frameWithDelay = frame - delay;

  const opacity = Math.min(1, Math.max(0, frameWithDelay / 20));
  const translateY = interpolate(frameWithDelay, [0, 20], [20, 0]);

  return (
    <div key={index} style={{
      opacity,
      transform: `translateY(${translateY}px)`,
    }}>
      {item}
    </div>
  );
});
```

### Countdown

```typescript
const duration = 60;
const remaining = duration - frame;

<div style={{
  fontSize: 200,
  fontWeight: 'bold',
}}>
  {remaining > 0 ? remaining : 'Go!'}
</div>
```

### Progress Bar

```typescript
const progress = frame / 300; // 300 frames total

<div style={{
  width: '100%',
  height: '20px',
  backgroundColor: '#eee',
}}>
  <div style={{
    width: `${progress * 100}%`,
    height: '100%',
    backgroundColor: 'blue',
    transition: 'width 0.1s',
  }} />
</div>
```

## Timing Patterns

### Ease In

```typescript
const eased = t => t * t;
const value = interpolate(frame, [0, 100], [0, 500]);
const easedValue = eased(value / 500) * 500;
```

### Ease Out

```typescript
const eased = t => t * (2 - t);
```

### Ease In Out

```typescript
const eased = t => t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
```

## Best Practices

1. **Use springs for natural motion**
   - Physics-based animations feel more natural
   - Adjust damping and stiffness for different feels

2. **Optimize with Still component**
   - Use `<Still>` for complex static content
   - Reduces rendering overhead

3. **Prefer CSS transforms over layout changes**
   - `transform`, `opacity`, `filter` are GPU-accelerated
   - Avoid animating `width`, `height`, `left`, `top`

4. **Stagger animations for better rhythm**
   - Add small delays between related elements
   - Creates visual hierarchy

5. **Keep animations short**
   - Most animations should be 0.5-2 seconds
   - Longer animations feel sluggish

6. **Use easing functions**
   - Linear animations feel mechanical
   - Add easing for natural motion

7. **Test at different frame rates**
   - Animations should work at different fps
   - Use `useVideoConfig().fps` for frame-rate independence
