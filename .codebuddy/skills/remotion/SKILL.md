---
name: remotion
description: This skill should be used when users want to create videos programmatically using React and the Remotion framework. Use it for tasks like creating explainer videos, product demos, code animation videos, educational content, or any scenario requiring video generation from code/data. Trigger when users ask to create videos, make animations, generate video content, or use Remotion for video production.
---

# Remotion Video Creation Skill

## Overview

This skill enables programmatic video creation using Remotion, a React-based framework that allows developers to create videos using familiar web technologies (React, CSS, JavaScript/TypeScript). Transform code, data, and animations into professional-quality videos for presentations, demos, educational content, and marketing materials.

## Quick Start

### Prerequisites

Before creating videos with Remotion, ensure the following are installed:

1. **Node.js** (v14 or higher) - Required for npm and JavaScript runtime
2. **FFmpeg** - Required for video encoding and rendering
   - Download from: https://ffmpeg.org/download.html
   - Add to system PATH

### Initialize a Remotion Project

To create a new Remotion project:

```bash
# Create a new Remotion project
npm create video@latest my-video-project
cd my-video-project

# Install dependencies
npm install

# Start the development server
npm start
```

### Basic Video Structure

A Remotion project consists of:

```
my-video-project/
├── src/
│   ├── Root.tsx           # Composition list entry point
│   └── MyComposition.tsx  # Your video composition
├── package.json
├── remotion.config.ts     # Remotion configuration
└── public/                # Static assets
```

## Core Concepts

### 1. Compositions

A composition is the fundamental unit in Remotion, representing a single video with specific properties:

```typescript
import {Composition} from 'remotion';
import {MyVideo} from './MyVideo';

export const RemotionVideo: React.FC = () => {
  return (
    <>
      <Composition
        id="my-video"
        component={MyVideo}
        durationInFrames={300} // 10 seconds at 30fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{text: "Hello World"}}
      />
    </>
  );
};
```

### 2. Using the Current Frame

Access and manipulate content based on the current frame:

```typescript
import {useCurrentFrame, useVideoConfig} from 'remotion';

export const MyComponent: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const opacity = Math.min(1, frame / 60); // Fade in over 2 seconds

  return (
    <div style={{opacity}}>
      Frame: {frame}
    </div>
  );
};
```

### 3. Animations

Use Remotion's animation utilities:

```typescript
import {interpolate, spring} from 'remotion';
import {useCurrentFrame} from 'remotion';

export const AnimatedBox: React.FC = () => {
  const frame = useCurrentFrame();

  // Linear interpolation
  const x = interpolate(frame, [0, 100], [0, 500]);

  // Spring animation
  const scale = spring({
    frame,
    fps: 30,
    config: {damping: 10, stiffness: 100},
  });

  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        transform: `scale(${scale})`,
      }}
    />
  );
};
```

### 4. Audio

Add audio to videos:

```typescript
import {Audio, useCurrentFrame} from 'remotion';

export const VideoWithAudio: React.FC = () => {
  return (
    <>
      <Audio src="https://example.com/music.mp3" />
      <div>Your video content</div>
    </>
  );
};
```

### 5. Transitions

Use transitions between scenes:

```typescript
import {Series, Transition} from 'remotion';
import {wipe} from '@remotion/transitions/wipe';

export const MyComposition: React.FC = () => {
  return (
    <Series>
      <Series.Sequence durationInFrames={100}>
        <Scene1 />
      </Series.Sequence>
      <Transition.Transition
        presentation={wipe({direction: 'from-right'})}
      />
      <Series.Sequence durationInFrames={100}>
        <Scene2 />
      </Series.Sequence>
    </Series>
  );
};
```

## Common Use Cases

### Use Case 1: Code Animation Video

Create videos showing code execution or development processes:

1. Create composition with code editor UI
2. Animate code typing line by line
3. Show execution results
4. Add explanatory text overlays

### Use Case 2: Explainer Video

Create step-by-step explanation videos:

1. Define keyframes for each step
2. Animate elements appearing sequentially
3. Use transitions between steps
4. Add narration or background music

### Use Case 3: Data Visualization

Create animated charts and graphs:

1. Use charting libraries (Recharts, D3)
2. Animate data points over time
3. Highlight key metrics
4. Add annotations and labels

### Use Case 4: Product Demo

Create product feature demonstrations:

1. Record UI interactions or create mockups
2. Animate feature highlights
3. Show before/after comparisons
4. Add callouts and annotations

## Workflow Decision Tree

When creating a video, follow this decision tree:

```
START
│
├─ What type of video?
│  ├─ Code animation → Use Case 1
│  ├─ Explainer → Use Case 2
│  ├─ Data viz → Use Case 3
│  └─ Product demo → Use Case 4
│
├─ What duration?
│  ├─ Short (< 30s) → Simple composition, minimal transitions
│  ├─ Medium (30-120s) → Multiple sequences, some transitions
│  └─ Long (> 120s) → Series of compositions, chapter markers
│
├─ What resolution?
│  ├─ Social media → 1080x1920 (vertical) or 1080x1080 (square)
│  ├─ YouTube/ presentations → 1920x1080 (landscape)
│  └─ High quality → 4K (3840x2160)
│
└─ Export format?
   ├─ MP4 → Standard, widely compatible
   ├─ GIF → Short, loopable, lower quality
   └─ WebM → Web optimized, good compression
```

## Step-by-Step Workflow

### Step 1: Plan the Video

1. **Define objectives**: What should the video achieve?
2. **Identify audience**: Who is watching?
3. **Outline content**: List key scenes/segments
4. **Determine duration**: Estimate total time needed
5. **Choose resolution**: 1080p for most use cases

### Step 2: Set Up Project

1. Initialize Remotion project using `scripts/setup_remotion.py`
2. Configure project settings in `remotion.config.ts`
3. Create composition structure
4. Add static assets to `public/` folder

### Step 3: Create Compositions

1. Define composition metadata (duration, fps, size)
2. Implement composition component
3. Add animations and transitions
4. Test with preview server

### Step 4: Add Assets

1. **Images**: Place in `public/` folder
2. **Audio**: Add background music or narration
3. **Fonts**: Import custom fonts if needed
4. **Data**: Load JSON/CSV data for dynamic content

### Step 5: Preview and Iterate

1. Start dev server: `npm start`
2. Preview in browser
3. Adjust timing, animations, styling
4. Test audio sync

### Step 6: Export Video

1. Choose export format
2. Run: `npm run build` or use `scripts/export_video.py`
3. Monitor rendering progress
4. Verify output file

## Resource Directory Structure

### scripts/

**Purpose**: Executable scripts for common Remotion operations

**Available scripts**:
- `setup_remotion.py` - Initialize a new Remotion project with templates
- `export_video.py` - Export video with custom parameters
- `validate_project.py` - Validate Remotion project structure

**Usage**:
```bash
python scripts/setup_remotion.py my-project
python scripts/export_video.py --composition my-video --format mp4
```

### references/

**Purpose**: Detailed documentation and reference material

**Available references**:
- `api_reference.md` - Complete Remotion API documentation
- `animation_patterns.md` - Common animation patterns and examples
- `best_practices.md` - Performance optimization and best practices

**When to load**:
- When implementing complex animations
- When optimizing video performance
- When debugging issues

### assets/

**Purpose**: Reusable assets for video creation

**Available assets**:
- `templates/` - Composition templates for common use cases
- `audio/` - Sample audio files (background music, effects)
- `images/` - Sample images and graphics
- `fonts/` - Custom font files

**Usage**:
- Copy templates to new projects
- Use sample assets for quick prototyping
- Customize assets as needed

## Templates

### Template 1: Simple Text Video

```typescript
import {AbsoluteFill, useCurrentFrame} from 'remotion';

export const SimpleTextVideo: React.FC<{text: string}> = ({text}) => {
  const frame = useCurrentFrame();
  const opacity = Math.min(1, frame / 30);

  return (
    <AbsoluteFill style={{backgroundColor: 'white'}}>
      <div
        style={{
          fontSize: 100,
          opacity,
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};
```

### Template 2: Image Slideshow

```typescript
import {Series, AbsoluteFill} from 'remotion';
import image1 from './images/image1.png';
import image2 from './images/image2.png';

export const Slideshow: React.FC = () => {
  return (
    <AbsoluteFill>
      <Series>
        <Series.Sequence durationInFrames={90}>
          <img src={image1} style={{width: '100%', height: '100%'}} />
        </Series.Sequence>
        <Series.Sequence durationInFrames={90}>
          <img src={image2} style={{width: '100%', height: '100%'}} />
        </Series.Sequence>
      </Series>
    </AbsoluteFill>
  );
};
```

### Template 3: Code Typing Animation

```typescript
import {useCurrentFrame, interpolate} from 'remotion';

export const CodeTyping: React.FC<{code: string}> = ({code}) => {
  const frame = useCurrentFrame();
  const charsToShow = Math.min(code.length, Math.floor(frame / 2));
  const visibleCode = code.slice(0, charsToShow);

  return (
    <pre style={{fontSize: 24, fontFamily: 'monospace', whiteSpace: 'pre-wrap'}}>
      {visibleCode}<span style={{opacity: 0.5}}>_</span>
    </pre>
  );
};
```

## Common Patterns

### Pattern 1: Sequence of Steps

```typescript
import {Series} from 'remotion';

export const StepSequence: React.FC = () => {
  return (
    <Series>
      <Series.Sequence durationInFrames={60}>
        <Step1 />
      </Series.Sequence>
      <Series.Sequence durationInFrames={60}>
        <Step2 />
      </Series.Sequence>
      <Series.Sequence durationInFrames={60}>
        <Step3 />
      </Series.Sequence>
    </Series>
  );
};
```

### Pattern 2: Parallel Elements

```typescript
import {AbsoluteFill} from 'remotion';

export const ParallelElements: React.FC = () => {
  return (
    <AbsoluteFill>
      <LeftPanel />
      <RightPanel />
      <Overlay />
    </AbsoluteFill>
  );
};
```

### Pattern 3: Reveal Animation

```typescript
import {useCurrentFrame, interpolate} from 'remotion';

export const Reveal: React.FC = () => {
  const frame = useCurrentFrame();
  const progress = Math.min(1, frame / 60);

  return (
    <div style={{
      width: `${progress * 100}%`,
      height: 100,
      backgroundColor: 'blue'
    }}>
      Revealing content
    </div>
  );
};
```

## Best Practices

### Performance Optimization

1. **Avoid excessive re-renders**: Use `React.memo` for expensive components
2. **Optimize images**: Compress images before using
3. **Use SVG over PNG**: Vector graphics scale better
4. **Lazy load audio**: Load audio only when needed
5. **Cache expensive computations**: Use `useMemo` and `useCallback`

### File Organization

```
src/
├── compositions/     # Video compositions
│   ├── MyVideo.tsx
│   └── AnotherVideo.tsx
├── components/       # Reusable components
│   ├── Button.tsx
│   └── TextOverlay.tsx
├── utils/           # Helper functions
│   ├── animations.ts
│   └── colors.ts
├── assets/          # Static assets
│   ├── images/
│   └── audio/
└── Root.tsx         # Entry point
```

### Naming Conventions

- Compositions: PascalCase (e.g., `MyComposition`)
- Components: PascalCase (e.g., `MyComponent`)
- Hooks: camelCase with "use" prefix (e.g., `useCustomHook`)
- Utilities: camelCase (e.g., `calculatePosition`)

## Troubleshooting

### Common Issues

**Issue**: Video doesn't render
- **Solution**: Check FFmpeg is installed and in PATH
- **Solution**: Verify composition ID matches in config

**Issue**: Audio is out of sync
- **Solution**: Use `Audio` component instead of HTML `<audio>`
- **Solution**: Check frame rate consistency

**Issue**: Poor performance in preview
- **Solution**: Reduce canvas size during development
- **Solution**: Optimize component rendering
- **Solution**: Use `still` frame for complex static content

**Issue**: Export fails
- **Solution**: Check available disk space
- **Solution**: Verify file paths are correct
- **Solution**: Check for special characters in file names

## Integration with Existing Projects

### Using Scripts

The skill includes helper scripts for common tasks:

```bash
# Set up a new project
python scripts/setup_remotion.py my-project --template explainer

# Export a video
python scripts/export_video.py --project my-project --composition my-video --output video.mp4

# Validate project structure
python scripts/validate_project.py my-project
```

### Loading References

When working on complex animations, load relevant references:

- Load `references/animation_patterns.md` for animation examples
- Load `references/api_reference.md` for API details
- Load `references/best_practices.md` for optimization tips

## Example Workflow

To create a "Snake Game Development" video:

1. **Plan**: 5 stages, 30fps, 1080p, ~60 seconds
2. **Setup**: `python scripts/setup_remotion.py snake-dev --template code-animation`
3. **Create compositions**: One composition per development stage
4. **Add content**: Use code editor UI, animate code typing
5. **Export**: `python scripts/export_video.py --project snake-dev --format mp4`

## Summary

This skill provides everything needed to create professional videos programmatically using Remotion. Use the scripts for automation, references for detailed information, and assets for quick prototyping. Follow the workflow decision tree and step-by-step guide to ensure successful video creation.
