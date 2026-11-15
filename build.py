import os
import shutil
import PyInstaller.__main__

for folder in ("build", "dist"):
    if os.path.exists(folder):
        shutil.rmtree(folder)

sep = ";" if os.name == "nt" else ":"

PyInstaller.__main__.run([
    "game.py",
    "--name=game",
    '--windowed',
    f"--add-data=assets{sep}assets",
    f"--add-data=levels{sep}levels",
    "--hidden-import=pygame-ce",
    "--clean",
    "--noconfirm",
])
