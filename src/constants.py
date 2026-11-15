from pathlib import Path
import sys
import os

def resource_resolver(rel_path: Path) -> Path:
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return base_path / rel_path

SPEED = 1
FPS = 60 if SPEED <= 1 else round(60 * SPEED)
WIDTH = 1280
HEIGHT = 720

BORDER_WALL_THICKNESS = 32

LEVEL_DIR = resource_resolver(Path('levels'))
ASSETS_DIR = resource_resolver(Path('assets'))

LEVEL_PATHS = {
    'testing': LEVEL_DIR / 'testing.txt',
    'level1': LEVEL_DIR / 'level1.txt'
}
