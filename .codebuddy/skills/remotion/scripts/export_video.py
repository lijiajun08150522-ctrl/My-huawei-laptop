#!/usr/bin/env python3
"""
Export a Remotion video with custom parameters.
"""

import argparse
import subprocess
import os
import sys
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a shell command and return output."""
    print(f"🔧 Running: {cmd}")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr}")
        raise


def export_video(project_path, composition, output_file=None, format="mp4", fps=30, quality=90):
    """
    Export a Remotion video.

    Args:
        project_path: Path to Remotion project
        composition: Composition ID to export
        output_file: Output filename (default: {composition}.mp4)
        format: Video format (mp4, webm, gif)
        fps: Frame rate (default: 30)
        quality: Quality 1-100 (default: 90)
    """
    print(f"🎬 Exporting Remotion video...")
    print(f"   Project: {project_path}")
    print(f"   Composition: {composition}")
    print(f"   Format: {format}")
    print(f"   FPS: {fps}")
    print(f"   Quality: {quality}\n")

    if not output_file:
        output_file = f"{composition}.{format}"

    # Build the export command
    cmd = f"npm run build -- --props='{JSON.stringify({})}' --format={format} --output={output_file}"

    # Add quality parameter if supported
    if format == "gif":
        cmd += f" --quality={quality}"

    try:
        result = run_command(cmd, cwd=project_path)

        if result.returncode == 0:
            print(f"\n✅ Video exported successfully!")
            print(f"   Output: {Path(project_path) / output_file}")
        else:
            print(f"\n❌ Export failed")
            print(f"   Error: {result.stderr}")

        return result.returncode == 0

    except Exception as e:
        print(f"❌ Error during export: {e}")
        return False


def preview_video(project_path, composition):
    """Preview a video composition in the browser."""
    print(f"👁️  Previewing composition: {composition}")
    cmd = "npm start"
    run_command(cmd, cwd=project_path)


def list_compositions(project_path):
    """List all available compositions in the project."""
    print(f"📋 Listing compositions in: {project_path}")

    # This would typically involve reading Root.tsx or using Remotion CLI
    # For now, provide instructions
    print(f"\nTo list compositions manually:")
    print(f"   1. Open {Path(project_path) / 'src/Root.tsx'}")
    print(f"   2. Look for <Composition> elements")
    print(f"   3. Note the 'id' values")


def check_dependencies(project_path):
    """Check if project dependencies are installed."""
    package_json = Path(project_path) / "package.json"
    node_modules = Path(project_path) / "node_modules"

    if not package_json.exists():
        print(f"❌ package.json not found in {project_path}")
        return False

    if not node_modules.exists():
        print(f"⚠️  node_modules not found. Run 'npm install' in the project directory")
        return False

    print(f"✅ Dependencies are installed")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Remotion video")
    parser.add_argument("project", help="Path to Remotion project")
    parser.add_argument("--composition", help="Composition ID to export")
    parser.add_argument("--output", help="Output filename")
    parser.add_argument("--format", choices=["mp4", "webm", "gif"], default="mp4", help="Video format")
    parser.add_argument("--fps", type=int, default=30, help="Frame rate")
    parser.add_argument("--quality", type=int, default=90, help="Quality (1-100)")
    parser.add_argument("--list", action="store_true", help="List available compositions")
    parser.add_argument("--preview", action="store_true", help="Preview in browser")
    parser.add_argument("--check-deps", action="store_true", help="Check dependencies")

    args = parser.parse_args()

    # Check dependencies if requested
    if args.check_deps:
        check_dependencies(args.project)
        sys.exit(0)

    # List compositions if requested
    if args.list:
        list_compositions(args.project)
        sys.exit(0)

    # Preview if requested
    if args.preview:
        if not args.composition:
            print("❌ --composition required for preview")
            sys.exit(1)
        preview_video(args.project, args.composition)
        sys.exit(0)

    # Export video
    if not args.composition:
        print("❌ --composition required for export")
        print(f"   Use --list to see available compositions")
        sys.exit(1)

    export_video(
        args.project,
        args.composition,
        args.output,
        args.format,
        args.fps,
        args.quality
    )
