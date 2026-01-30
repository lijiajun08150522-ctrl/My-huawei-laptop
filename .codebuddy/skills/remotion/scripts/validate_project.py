#!/usr/bin/env python3
"""
Validate a Remotion project structure and configuration.
"""

import argparse
import json
import sys
from pathlib import Path


def validate_project_structure(project_path):
    """Validate that the project has the required structure."""
    project = Path(project_path)

    print(f"🔍 Validating project structure: {project_path}\n")

    required_files = [
        "package.json",
        "tsconfig.json",
        "remotion.config.ts"
    ]

    required_dirs = [
        "src",
        "src/Root.tsx"
    ]

    errors = []
    warnings = []

    # Check required files
    for file in required_files:
        file_path = project / file
        if file_path.exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - Not found")
            errors.append(f"Missing {file}")

    # Check required directories
    for item in required_dirs:
        item_path = project / item
        if item_path.exists():
            print(f"✅ {item}")
        else:
            print(f"❌ {item} - Not found")
            errors.append(f"Missing {item}")

    return errors, warnings


def validate_package_json(project_path):
    """Validate package.json configuration."""
    print(f"\n📦 Validating package.json:")

    package_json = Path(project_path) / "package.json"

    if not package_json.exists():
        print("❌ package.json not found")
        return False

    with open(package_json) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("❌ Invalid JSON in package.json")
            return False

    # Check required fields
    required_fields = ["name", "version", "dependencies", "scripts"]
    valid = True

    for field in required_fields:
        if field in data:
            print(f"✅ {field}: {data[field]}")
        else:
            print(f"❌ Missing field: {field}")
            valid = False

    # Check for Remotion dependencies
    deps = data.get("dependencies", {})
    dev_deps = data.get("devDependencies", {})

    all_deps = {**deps, **dev_deps}

    remotion_packages = ["remotion", "@remotion/cli"]
    for pkg in remotion_packages:
        if pkg in all_deps:
            print(f"✅ {pkg}: {all_deps[pkg]}")
        else:
            print(f"⚠️  {pkg} not found (may be in devDependencies)")

    return valid


def validate_compositions(project_path):
    """Validate that compositions are properly defined."""
    print(f"\n🎬 Validating compositions:")

    root_file = Path(project_path) / "src" / "Root.tsx"

    if not root_file.exists():
        print("❌ src/Root.tsx not found")
        return False

    with open(root_file, encoding='utf-8') as f:
        content = f.read()

    # Check for Composition imports
    if "Composition" in content:
        print("✅ Composition component imported")
    else:
        print("⚠️  Composition component not imported")

    # Check for at least one composition
    if "<Composition" in content:
        print("✅ At least one composition defined")

        # Count compositions
        count = content.count("<Composition")
        print(f"   Found {count} composition(s)")
    else:
        print("❌ No compositions found")
        return False

    return True


def validate_typescript_config(project_path):
    """Validate TypeScript configuration."""
    print(f"\n🔧 Validating TypeScript config:")

    tsconfig = Path(project_path) / "tsconfig.json"

    if not tsconfig.exists():
        print("❌ tsconfig.json not found")
        return False

    with open(tsconfig) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("❌ Invalid JSON in tsconfig.json")
            return False

    # Check important settings
    important_settings = {
        "compilerOptions.jsx": "react-jsx",
        "include": ["src/**/*"],
    }

    valid = True
    for setting, expected in important_settings.items():
        keys = setting.split(".")
        value = data

        try:
            for key in keys:
                value = value[key]

            if value == expected:
                print(f"✅ {setting}: {value}")
            else:
                print(f"⚠️  {setting}: {value} (expected: {expected})")
        except (KeyError, TypeError):
            print(f"⚠️  {setting} not found")
            valid = False

    return valid


def check_node_modules(project_path):
    """Check if node_modules exists and has necessary packages."""
    print(f"\n📚 Checking node_modules:")

    node_modules = Path(project_path) / "node_modules"

    if not node_modules.exists():
        print("❌ node_modules not found")
        print("   Run 'npm install' to install dependencies")
        return False

    print("✅ node_modules exists")

    # Check for remotion package
    remotion_path = node_modules / "remotion"
    if remotion_path.exists():
        print("✅ remotion package installed")
    else:
        print("⚠️  remotion package not found in node_modules")
        return False

    return True


def generate_report(project_path, errors, warnings):
    """Generate a validation report."""
    print(f"\n{'='*60}")
    print(f"VALIDATION REPORT")
    print(f"{'='*60}")

    if not errors and not warnings:
        print(f"\n✅ All checks passed!")
        print(f"   Project is ready to use.")
        return True
    else:
        if errors:
            print(f"\n❌ Errors ({len(errors)}):")
            for i, error in enumerate(errors, 1):
                print(f"   {i}. {error}")

        if warnings:
            print(f"\n⚠️  Warnings ({len(warnings)}):")
            for i, warning in enumerate(warnings, 1):
                print(f"   {i}. {warning}")

        print(f"\n📝 Recommendations:")
        print(f"   1. Fix all errors before proceeding")
        print(f"   2. Review warnings for potential issues")
        print(f"   3. Run 'npm install' if dependencies are missing")
        print(f"   4. Check Remotion documentation for best practices")

        return False


def main():
    parser = argparse.ArgumentParser(description="Validate Remotion project")
    parser.add_argument("project", help="Path to Remotion project")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")

    args = parser.parse_args()

    project_path = Path(args.project)

    if not project_path.exists():
        print(f"❌ Project path not found: {args.project}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"REMOTION PROJECT VALIDATION")
    print(f"{'='*60}\n")

    all_errors = []
    all_warnings = []

    # Validate structure
    errors, warnings = validate_project_structure(project_path)
    all_errors.extend(errors)
    all_warnings.extend(warnings)

    # Validate package.json
    if not validate_package_json(project_path):
        all_errors.append("Invalid package.json")

    # Validate compositions
    if not validate_compositions(project_path):
        all_errors.append("No valid compositions found")

    # Validate TypeScript config
    if not validate_typescript_config(project_path):
        all_warnings.append("TypeScript configuration may need review")

    # Check node_modules
    if not check_node_modules(project_path):
        all_errors.append("Missing node_modules or dependencies")

    # Generate report
    success = generate_report(project_path, all_errors, all_warnings)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
