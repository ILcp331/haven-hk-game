from src.main import Game

if __name__ == "__main__":
    game = Game(allow_debug=False)

    while game.running:
        game.mainloop()
