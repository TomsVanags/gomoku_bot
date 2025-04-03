import time
from bot import GomokuBot

def main():
    bot = GomokuBot()
    
    if not bot.start_game():
        return
    
    while True:
        if bot.game_over():
            bot.start_game()  # restart the game if over
            time.sleep(2)
            continue
        
        bot.make_move()  #make the move
        time.sleep(0.5)  # because of the request limit
    
if __name__ == '__main__':
    main()
