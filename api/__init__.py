import sys
from pathlib import Path

# Make the huskyadvisor package importable from src/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
