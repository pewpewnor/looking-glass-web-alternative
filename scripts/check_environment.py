#!/usr/bin/env python3

"""
Environment check script - Verify all dependencies and system requirements
Usage: python scripts/check_environment.py
"""

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}", end="")
    if version >= (3, 10):
        print(" ✓")
        return True
    print(" ✗ (Requires Python 3.10+)")
    return False

def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name

    try:
        __import__(import_name)
        print(f"{package_name:30} ✓")
        return True
    except ImportError:
        print(f"{package_name:30} ✗ (Not installed)")
        return False

def check_models():
    """Check if model files exist"""
    base_dir = REPO_ROOT / "models"
    models = {
        'groundingdino_swint_ogc.pth': 'GroundingDINO weights',
        'groundingdino_swin_t_ogc.py': 'GroundingDINO config'
    }

    print("\nModel Files:")
    all_exist = True
    for filename, description in models.items():
        path = base_dir / filename
        if path.exists():
            print(f"  {description:35} ✓")
        else:
            print(f"  {description:35} ✗ (Missing)")
            all_exist = False

    return all_exist

def check_directories():
    """Check if required directories exist"""
    base_dir = REPO_ROOT
    dirs = {
        'backend': 'Backend folder',
        'frontend': 'Frontend folder',
        'models': 'Model configuration folder',
        'data': 'Evaluation data folder',
    }

    print("\nDirectory Structure:")
    all_exist = True
    for dirname, description in dirs.items():
        path = base_dir / dirname
        if path.exists() and path.is_dir():
            print(f"  {description:35} ✓")
        else:
            print(f"  {description:35} ✗ (Missing)")
            all_exist = False

    return all_exist

def check_files():
    """Check if key files exist"""
    base_dir = REPO_ROOT
    files = {
        'backend/app.py': 'Flask app',
        'backend/pipeline.py': 'ML pipeline',
        'backend/requirements.txt': 'Python requirements',
        'frontend/index.html': 'Frontend HTML',
        'frontend/app.js': 'Frontend JavaScript',
        'models/groundingdino_swin_t_ogc.py': 'GroundingDINO config',
        'README.md': 'Documentation',
    }

    print("\nKey Files:")
    all_exist = True
    for filepath, description in files.items():
        path = base_dir / filepath
        if path.exists() and path.is_file():
            print(f"  {description:35} ✓")
        else:
            print(f"  {description:35} ✗ (Missing)")
            all_exist = False

    return all_exist

def main():
    print("=" * 60)
    print("Looking Glass Web Alternative - Environment Check")
    print("=" * 60)

    results = []

    # Check Python
    print("\nPython:")
    results.append(("Python >= 3.10", check_python_version()))

    # Check directories
    results.append(("Directory structure", check_directories()))

    # Check files
    results.append(("Key files", check_files()))

    # Check models
    model_check = check_models()
    if not model_check:
        print("  ℹ️  Add the missing local model files before starting the app")
    results.append(("Model files", model_check))

    # Check Python packages (only if in backend directory context)
    try:
        print("\nCore Python Packages:")
        packages = [
            ('Flask', 'flask'),
            ('PyTorch', 'torch'),
            ('Transformers', 'transformers'),
            ('OpenCV', 'cv2'),
            ('Pillow', 'PIL'),
            ('NumPy', 'numpy'),
            ('faster-whisper', 'faster_whisper'),
            ('TTS', 'TTS'),
        ]

        any_missing = False
        for package_name, import_name in packages:
            if not check_package(package_name, import_name):
                any_missing = True

        if any_missing:
            print("\n⚠️  Some packages are missing!")
            print("Install with: python -m pip install -r backend/requirements.txt")
            results.append(("Python packages", False))
        else:
            results.append(("Python packages", True))

    except Exception:
        print("\n⚠️  Could not check packages")
        results.append(("Python packages", None))

    # Summary
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)

    passed = sum(1 for _, result in results if result is True)
    failed = sum(1 for _, result in results if result is False)

    for name, result in results:
        status = "✓" if result is True else ("✗" if result is False else "?")
        print(f"{name:35} {status}")

    print(f"\nPassed: {passed}/{len(results)}")

    if failed == 0:
        print("\n✓ All checks passed! Ready to go!")
        print("\nNext steps:")
        print("1. python -m pip install -r backend/requirements.txt")
        print("2. python app.py")
        print("3. Open http://localhost:5001")
        return 0
    else:
        print(f"\n✗ {failed} check(s) failed. Please fix above issues.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
