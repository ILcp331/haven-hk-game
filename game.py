from src.main import Game

from src.constants import LEVEL_PATHS

if __name__ == "__main__":
    game = Game(allow_debug=True)

    while game.running:
        game.mainloop()
