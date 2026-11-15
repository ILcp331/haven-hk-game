from pathlib import Path
import sys, os

BORDER_WALL_THICKNESS = 32

def src_dir_path() -> Path:
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS)

    return Path(__file__).resolve().parent

LEVEL_DIR = src_dir_path() / 'levels'
ASSETS_DIR = src_dir_path() / 'assets'

LEVEL_PATHS = {
    'testing': LEVEL_DIR / 'testing.txt'
}
