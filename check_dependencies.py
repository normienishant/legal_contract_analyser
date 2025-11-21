"""Check if ML training dependencies are installed."""
import sys

dependencies = {
    'torch': 'PyTorch',
    'transformers': 'Transformers',
    'sklearn': 'scikit-learn',
    'pandas': 'pandas',
    'numpy': 'numpy',
    'datasets': 'datasets',
}

missing = []
installed = []

for module, name in dependencies.items():
    try:
        __import__(module)
        installed.append(name)
        print(f"[OK] {name}: Installed")
    except ImportError:
        missing.append(name)
        print(f"[MISSING] {name}: Not installed")

print("\n" + "="*50)
if missing:
    print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
    print("\nInstall with:")
    print("pip install torch transformers scikit-learn pandas numpy datasets")
    sys.exit(1)
else:
    print("\n✅ All dependencies installed! Ready to train.")
    sys.exit(0)

