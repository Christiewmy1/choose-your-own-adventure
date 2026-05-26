import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # loads .env so GEMINI_API_KEY is available everywhere

# Make the huskyadvisor package importable from src/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
