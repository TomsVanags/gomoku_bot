import requests
import configparser
import time
from logger import setup_logger
from ai import minimax, check_win, get_legal_moves
import random

def get_random_move(self, board):
        valid_moves = get_legal_moves(board)
        if valid_moves:
            random_move = random.choice(valid_moves)
            x_random, y_random = random_move
            self.logger.info(f"Random move : {random_move}")
            return x_random, y_random
        else:
            print("Idk what to do")

class GomokuBot:

    def __init__(self):
        # Load configuration
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.student_id = self.config['game']['student_id']
        self.server_url = self.config['game']['server_url']
        self.port = self.config['game']['port']
        self.max_depth = int(self.config['game']['max_depth'])

        self.logger = setup_logger(self.config['logging']['log_file'])

        self.game_id = None
        self.color = None
        self.board = None
        self.turn = None

    def start_game(self):
        """Start a new game and initialize game state"""
        url = f'http://{self.server_url}:{self.port}/{self.student_id}/start'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            if data["request_status"] == "GOOD":
                self.game_id = data["game_id"]
                self.color = data["color"]
                self.turn = data["turn"]
                self.board = data["gameboard"]
                self.logger.info(f"Game started. Color: {self.color}")

                self.game_status = data["game_status"]
                self.logger.info(f"status: {self.game_status}")

                self.logger.info(f"Game started. Game ID: {self.game_id}, Color: {self.color}")
                return True
            elif data["game_status"] == "LEAVE":
                self.logger.info("Received 'LEAVE' status. Exiting.")
                return False
        else:
            self.logger.error(f"Failed to start the game. Response: {response.text}")
            return False

    def make_move(self):
        """Make a move if it's our turn"""
        if self.turn == self.color:
            move = minimax(self.board, self.max_depth, True, float('-inf'), float('inf'))
            if move:
                print(type(move))
                y_test = move[1]
                print(y_test)
                if y_test != None:
                    xy_test = y_test[0]
                    yy_test = y_test[1]
                    x, y = move
                    self.send_move(xy_test, yy_test)
                    print(f"move just sent: {xy_test}, {yy_test}")
                    print( type(xy_test), type(yy_test))

                    self.logger.info(f"gameboard: {self.board}")
                    self.logger.info(f"status: {self.game_status}")
                else: 
                    x_random, y_random = get_random_move(self, self.board)
                    print(f"X = {x_random}, and y = {y_random}")
                    print(type(x_random), type(y_random))
                    print(f"just sent: {x_random} and {y_random}")
                    self.send_move(x_random, y_random)
                    

    def send_move(self, x, y):
        """Send the move to the server"""
        url = f'http://{self.server_url}:{self.port}/{self.student_id}/{self.game_id}/{x}/{y}'
        
        try:
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                
                if data["request_status"] == "GOOD":
                    self.logger.info(f"Move ({x}, {y}) sent successfully.")
                    self.board = data["gameboard"]  # Update board state
                    self.turn = data["turn"]  # Update turn info
                else:
                    self.logger.error(f"Move rejected: {data}")
            else:
                self.logger.error(f"Failed to send move. Status code: {response.status_code}")
                pass
        
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error: {e}")

    def game_over(self):
        """Check if the game is over based on the last server response"""
        if self.board in ["BLACKWON", "WHITEWON", "DRAW"]:
            self.logger.info(f"Game Over: {self.board}")
            return True
        return False
    
    
