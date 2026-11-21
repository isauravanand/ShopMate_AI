import sys
from pathlib import Path

# Ensure backend directory is in sys.path for test discovery and imports
backend_dir = str(Path(__file__).resolve().parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
