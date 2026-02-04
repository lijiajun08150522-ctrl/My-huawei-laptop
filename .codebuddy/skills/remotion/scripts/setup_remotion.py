#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup a new Remotion project with templates and configuration.
"""

import argparse
import subprocess
import os
import json
import sys
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def run_command(cmd, cwd=None):
    """Run a shell command and return output."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Error: {e.stderr}")
        raise


def setup_remotion_project(project_name, template="default"):
    """
    Initialize a new Remotion project with templates.

    Args:
        project_name: Name of the project directory
        template: Template type (default, explainer, code-animation, slideshow)
    """
    print(f"🚀 Setting up Remotion project: {project_name}")
    print(f"   Template: {template}\n")

    # Create project directory
    project_path = Path(project_name)
    if project_path.exists():
        print(f"❌ Directory {project_name} already exists")
        return False

    project_path.mkdir(parents=True)

    # Initialize Remotion project
    print("📦 Initializing Remotion project...")
    try:
        run_command(f"npm create video@latest {project_name}", cwd=".")
    except:
        # Fallback: create basic structure manually
        print("⚠️  npm create failed, creating basic structure manually...")
        create_basic_project_structure(project_path, template)

    print("\n✅ Remotion project setup complete!")
    print(f"   Location: {project_path.absolute()}")
    print(f"\nNext steps:")
    print(f"   1. cd {project_name}")
    print(f"   2. npm install")
    print(f"   3. npm start")

    return True


def create_basic_project_structure(project_path, template):
    """Create basic Remotion project structure manually."""
    # Create directories
    (project_path / "src").mkdir()
    (project_path / "public").mkdir()

    # Create package.json
    package_json = {
        "name": project_path.name,
        "version": "1.0.0",
        "scripts": {
            "start": "remotion studio",
            "build": "remotion render",
            "upgrade": "remotion upgrade"
        },
        "dependencies": {
            "remotion": "^4.0.0",
            "react": "^18.2.0",
            "react-dom": "^18.2.0"
        },
        "devDependencies": {
            "@remotion/cli": "^4.0.0",
            "@types/react": "^18.2.0",
            "@types/react-dom": "^18.2.0",
            "typescript": "^5.0.0"
        }
    }

    with open(project_path / "package.json", "w") as f:
        json.dump(package_json, f, indent=2)

    # Create remotion.config.ts
    config_content = f"""import {{Config}} from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
Config.setOverwriteOutput(true);

Config.setRenderingFps(30);
Config.setConcurrency(5);

export const config = Config.getPurgedConfig();
"""
    with open(project_path / "remotion.config.ts", "w") as f:
        f.write(config_content)

    # Create Root.tsx
    root_content = generate_root_content(template)
    with open(project_path / "src/Root.tsx", "w") as f:
        f.write(root_content)

    # Create composition based on template
    composition_content = generate_composition_content(template)
    composition_file = project_path / "src" / "MyComposition.tsx"
    with open(composition_file, "w") as f:
        f.write(composition_content)

    # Create tsconfig.json
    tsconfig_content = {
        "compilerOptions": {
            "target": "ES2022",
            "module": "ES2022",
            "lib": ["DOM", "DOM.Iterable", "ESNext"],
            "jsx": "react-jsx",
            "strict": True,
            "moduleResolution": "bundler",
            "resolveJsonModule": True,
            "esModuleInterop": True,
            "skipLibCheck": True,
            "forceConsistentCasingInFileNames": True,
            "isolatedModules": True
        },
        "include": ["src/**/*"],
        "exclude": ["node_modules"]
    }

    with open(project_path / "tsconfig.json", "w") as f:
        json.dump(tsconfig_content, f, indent=2)


def generate_root_content(template):
    """Generate Root.tsx content based on template."""
    return """import {Composition} from 'remotion';
import {MyComposition} from './MyComposition';

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="my-composition"
        component={MyComposition}
        durationInFrames={180}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{}}
      />
    </>
  );
};
"""


def generate_composition_content(template):
    """Generate composition content based on template type."""
    if template == "code-animation":
        return generate_code_animation_composition()
    elif template == "explainer":
        return generate_explainer_composition()
    elif template == "slideshow":
        return generate_slideshow_composition()
    else:
        return generate_default_composition()


def generate_default_composition():
    """Generate default composition with simple text animation."""
    return """import {AbsoluteFill, useCurrentFrame, interpolate} from 'remotion';

export const MyComposition: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1]);
  const scale = interpolate(frame, [0, 60], [0.8, 1]);

  return (
    <AbsoluteFill style={{backgroundColor: 'white'}}>
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          fontSize: 150,
          fontWeight: 'bold',
          opacity,
          transform: `scale(${scale})`,
        }}
      >
        Hello Remotion!
      </div>
    </AbsoluteFill>
  );
};
"""


def generate_code_animation_composition():
    """Generate code animation composition."""
    return """import {AbsoluteFill, useCurrentFrame} from 'remotion';

const code = \`function sayHello() {
  console.log("Hello, World!");
}

sayHello();\`;

export const MyComposition: React.FC = () => {
  const frame = useCurrentFrame();
  const charsToShow = Math.min(code.length, Math.floor(frame / 2));
  const visibleCode = code.slice(0, charsToShow);

  return (
    <AbsoluteFill style={{backgroundColor: '#1e1e1e'}}>
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          fontSize: 40,
          fontFamily: 'monospace',
          color: '#d4d4d4',
          whiteSpace: 'pre-wrap',
          textAlign: 'left',
          padding: 100,
        }}
      >
        {visibleCode}<span style={{opacity: 0.5}}>▌</span>
      </div>
    </AbsoluteFill>
  );
};
"""


def generate_explainer_composition():
    """Generate explainer video composition."""
    return """import {AbsoluteFill, useCurrentFrame, Series, interpolate} from 'remotion';

const Step1 = () => (
  <AbsoluteFill style={{backgroundColor: '#f0f0f0'}}>
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontSize: 80,
        fontWeight: 'bold',
        color: '#333',
      }}
    >
      Step 1: Introduction
    </div>
  </AbsoluteFill>
);

const Step2 = () => (
  <AbsoluteFill style={{backgroundColor: '#e0e0e0'}}>
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontSize: 80,
        fontWeight: 'bold',
        color: '#333',
      }}
    >
      Step 2: Explanation
    </div>
  </AbsoluteFill>
);

const Step3 = () => (
  <AbsoluteFill style={{backgroundColor: '#d0d0d0'}}>
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontSize: 80,
        fontWeight: 'bold',
        color: '#333',
      }}
    >
      Step 3: Conclusion
    </div>
  </AbsoluteFill>
);

export const MyComposition: React.FC = () => {
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
"""


def generate_slideshow_composition():
    """Generate slideshow composition."""
    return """import {AbsoluteFill, useCurrentFrame, interpolate} from 'remotion';

const Slide = ({title, subtitle, frame}: {title: string, subtitle: string, frame: number}) => {
  const opacity = interpolate(frame, [0, 30], [0, 1]);
  const scale = interpolate(frame, [0, 30], [0.8, 1]);

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        opacity,
        transform: `scale(${scale})`,
        textAlign: 'center',
      }}
    >
      <h1 style={{fontSize: 120, marginBottom: 40}}>{title}</h1>
      <p style={{fontSize: 60}}>{subtitle}</p>
    </div>
  );
};

export const MyComposition: React.FC = () => {
  const frame = useCurrentFrame();

  if (frame < 60) {
    return (
      <AbsoluteFill style={{backgroundColor: '#667eea'}}>
        <Slide title="Slide 1" subtitle="Introduction" frame={frame} />
      </AbsoluteFill>
    );
  } else if (frame < 120) {
    return (
      <AbsoluteFill style={{backgroundColor: '#764ba2'}}>
        <Slide title="Slide 2" subtitle="Content" frame={frame - 60} />
      </AbsoluteFill>
    );
  } else {
    return (
      <AbsoluteFill style={{backgroundColor: '#f093fb'}}>
        <Slide title="Slide 3" subtitle="Conclusion" frame={frame - 120} />
      </AbsoluteFill>
    );
  }
};
"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Setup a new Remotion project")
    parser.add_argument("project_name", help="Name of the project")
    parser.add_argument("--template", choices=["default", "explainer", "code-animation", "slideshow"],
                       default="default", help="Template type")
    parser.add_argument("--path", default=".", help="Path to create project in")

    args = parser.parse_args()

    # Change to specified path
    os.chdir(args.path)

    # Setup project
    setup_remotion_project(args.project_name, args.template)
