import sys
import asyncio

print(sys.version_info)

import pygame as pg

from src.game import Game

pg.init()

async def main():
    while game.running:
        game.mainloop()
        await asyncio.sleep(0)

if __name__ == "__main__":

    game = Game(allow_debug=True)

    asyncio.run(main())
