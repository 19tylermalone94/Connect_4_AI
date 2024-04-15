import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random


def get_solution(game_state: str) -> dict | None:
    url = 'http://localhost:8080'
    num_tries = 10
    for _ in range(num_tries):
      try:
        response = requests.post(url, data=game_state)
        if response.status_code == 200:
          return {'pos': game_state, 'score': [int(n) for n in response.text.strip().split(' ')]}
        else:
          print("Failed to retrieve solution, status code:", response.status_code)
      except requests.RequestException as e:
        print("Error connecting to server:", str(e))

def new_board() -> np.ndarray:
    return np.zeros((6, 7), dtype=int)


def drop_piece(board: np.ndarray, col: int, piece: int) -> None:
    board[available_row(board, col)][col] = piece


def is_available(board: np.ndarray, col: int) -> bool:
    return board[0][col] == 0


def available_row(board: np.ndarray, col: int) -> int:
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == 0:
            return row
    return 0


def play(board: np.ndarray, col: int, player: int) -> bool:
    if not is_available(board, col):
        return False
    drop_piece(board, col, player)
    return True


def check_winner(board: np.ndarray) -> int | None:
    # horizontal
    for r in range(board.shape[0]):
        for c in range(board.shape[1] - 3):
            if board[r, c] == board[r, c+1] == board[r, c+2] == board[r, c+3] != 0:
                return board[r, c]

    # vertical
    for r in range(board.shape[0] - 3):
        for c in range(board.shape[1]):
            if board[r, c] == board[r+1, c] == board[r+2, c] == board[r+3, c] != 0:
                return board[r, c]

    # positive diagonal
    for r in range(board.shape[0] - 3):
        for c in range(board.shape[1] - 3):
            if board[r, c] == board[r+1, c+1] == board[r+2, c+2] == board[r+3, c+3] != 0:
                return board[r, c]

    # negative diagonal
    for r in range(3, board.shape[0]):
        for c in range(board.shape[1] - 3):
            if board[r, c] == board[r-1, c+1] == board[r-2, c+2] == board[r-3, c+3] != 0:
                return board[r, c]

    return None



output_path = 'connect_4_data/'


def best_move(score: list[int]) -> int:
  max_score = min(score)
  for i in range(len(score)):
    if score[i] > max_score:
      max_score = score[i]
  best_indexes = [i + 1 for i in range(len(score)) if score[i] == max_score]
  return random.choice(best_indexes)


def random_move(seq: str) -> int:
  move = random.randint(1, 7)
  while seq.count(str(move)) >= 6:
    move = random.randint(1, 7)
  return move

  
def game_over(board: np.ndarray, seq: str) -> bool:
    return check_winner(board) is not None or len(seq) == 42


def run_games(num_games: int, perfect: bool=True) -> list:
  games = []
  for i in range(num_games):
    board = new_board()
    seq = ''
    player = 1
    while True:
      score = get_solution(seq)['score']
      games.append([i, seq, score])
      move = best_move(score) if perfect else random_move(seq)
      seq += str(move)
      play(board, move - 1, player)
      if game_over(board, seq):
        break
      player *= -1
    print(f"{'perfect' if perfect else 'random'} games: {int((i / num_games) * 100)}%")
  return games


def write_games(games: tuple[list[list[int]], list[int]], path: str) -> None:
  with open(path, 'w') as f:
    for game in games:
      s = f'{game[0]},{game[1]},{str(game[2])[1:-1]}\n'
      s = s.replace(' ', '')
      f.write(s)


perfect_games = run_games(1000, perfect=True)
random_games = run_games(1000, perfect=False)

write_games(perfect_games, output_path + 'perfect_strategy/data.csv')
write_games(random_games, output_path + 'random_strategy/data.csv')