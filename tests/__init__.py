import sys

from pathlib import Path


# Add .../tmx_folder to sys.path so tests can do "import functions"
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "tmx_products"))
