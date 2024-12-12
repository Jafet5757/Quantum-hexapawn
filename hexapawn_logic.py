from prettytable import PrettyTable
import pandas as pd
import random
import time

class Hexapawn:
  def __init__(self):
    self.board = ['X', 'X', 'X','-', '-', '-', 'O', 'O', 'O']
    self.current_player = 'O'

  def print_board(self):
    """ 
    Print the current board 
    """
    print("\033c", end="") # Clear the console
    
    for i, row in enumerate(self.board):
      print(row, end=" " if i%3 != 2 else "\n")

  def clean_board(self):
    self.board = ['-', '-', '-', 
                  '-', '-', '-', 
                  '-', '-', '-']

  def create_play(self):
    """ 
    Create a specifica play for the current player

    -------
    return: None 
    """
    self.clean_board()
    print("Ingrese la jugada a realizar")
    print("Formato: x1, x2, x3, o1, o2, o3")
    print("Ejemplo: 1 5 2 6 8 9")
    play = input()
    play = play.split(" ")
    play = list(map(int, play))
    # Update board
    for i, p in enumerate(play):
      symbol = 'X' if i < 3 else 'O'
      if p != -1: # -1 means the piece was captured
        self.board[p-1] = symbol
    self.print_board()
    self.save_play()

  def get_representations(self, board=None):
    """ 
    Get the general, x player and o player representations of the board in binary format

    Parameters:
    board: list
      The board to get the representations

    -------
    return: tuple
      The general, x player and o player representations of the board
    """
    board = self.board if board is None else board
    general = ''.join(map((lambda x: '1' if x == 'X' or x =='O' else '0'), board))
    x_player = ''.join(map((lambda x: '1' if x == 'X' else '0'), board))
    o_player = ''.join(map((lambda x: '1' if x == 'O' else '0'), board))
    return general, x_player, o_player

  def save_play(self, filename="movements.csv"):
    # Obtener la representación actual
    general, x_player, o_player = self.get_representations()
    print(f"Actual state: {general}, {x_player}, {o_player}")
    
    # Obtener los movimientos posibles
    moves = self.get_moves()  # Retorna un array de tuplas con los posibles estados
    print(moves)
    
    # Leer el archivo CSV
    df = pd.read_csv(filename)
    
    # Crear un diccionario para la nueva fila
    new_row = {
        'actual_state_general': general,
        'actual_state_x': x_player,
        'actual_state_o': o_player
    }
    
    # Agregar las jugadas posibles al diccionario
    for i, move in enumerate(moves):
        new_row[f'play{i+1}_state_general'] = move[0]
        new_row[f'play{i+1}_state_x'] = move[1]
        new_row[f'play{i+1}_state_o'] = move[2]
    
    # Convertir el diccionario en un DataFrame
    new_row_df = pd.DataFrame([new_row])
    
    # Concatenar la nueva fila con el DataFrame existente
    df = pd.concat([df, new_row_df], ignore_index=True)
    
    # Guardar el archivo actualizado
    #df.to_csv(filename, index=False)
      

  def get_moves(self):
    """ 
    Returns a list of possible moves for the current player

    -------
    return: list of tuples with the possible moves 
    """
    moves = []
    for i, p in enumerate(self.board):
      if p == 'X':
        if i+3 < 9 and self.board[i+3] == '-':
          temp_board = self.board.copy()
          temp_board[i] = '-'
          temp_board[i+3] = 'X'
          g, x, o = self.get_representations(temp_board)
          moves.append((g, x, o))
        if i+4 < 9 and self.board[i+4] == 'O' and (i+1) % 3 != 0:
          temp_board = self.board.copy()
          temp_board[i] = '-'
          temp_board[i+4] = 'X'
          g, x, o = self.get_representations(temp_board)
          moves.append((g, x, o))
        if i+2 < 9 and self.board[i+2] == 'O' and i % 3 != 0:
          temp_board = self.board.copy()
          temp_board[i] = '-'
          temp_board[i+2] = 'X'
          g, x, o = self.get_representations(temp_board)
          moves.append((g, x, o))

    return moves
  
  def is_valid_move(self, current_index:int, new_index:int, current_player:str = 'O')->bool:
    """ 
    Check if the move is valid 

    Parameters:
    current_index: int
      The index of the current piece
    new_index: int
      The index of the new position
    current_player: str
      The current player

    -------
    return: bool
      True if the move is valid, False otherwise
    """
    current_index = int(current_index) - 1
    new_index = int(new_index) - 1
    enemy = 'X' if current_player == 'O' else 'O'
    # Go to up
    if current_player == "O":
      if new_index == current_index - 3 and current_index - 3 >= 0:
        return True
      if new_index == current_index - 4 and current_index % 3 != 0 and self.board[current_index-4] == enemy and current_index - 4 >= 0:
        return True
      if new_index == current_index - 2 and current_index % 3 != 2 and self.board[current_index-2] == enemy and current_index - 2 >= 0:
        return True
    # Go to down
    else:
      if new_index == current_index + 3 and current_index + 3 < 9:
        return True
      if new_index == current_index + 4 and current_index % 3 != 0 and self.board[current_index+4] == enemy and current_index + 4 < 9:
        return True
      if new_index == current_index + 2 and current_index % 3 != 2 and self.board[current_index+2] == enemy and current_index + 2 < 9:
        return True
    return False

  def user_move(self):
    """ 
    Ask the user for a move and update the board if the move is valid 
    """
    while True:
      try:
        move = input("Ingresa la casilla actual y la nueva [1 2]: ")
        move = move.split(" ")
        move = list(map(int, move))
        isValid = self.is_valid_move(move[0], move[1])
        if isValid:
          # Update board
          self.board[move[1]-1] = self.board[move[0]-1]
          self.board[move[0]-1] = '-'
          self.print_board()
          break
        else:
          print("Movimiento inválido")
          continue
      except:
        c = input("\nError, Desea parar? (s/n): ")
        if c == 's':
          break
        else:
          continue

  def get_random_move(self):
    """ 
     Get a random move for the machine player
    """
    moves = self.get_moves()
    selected = random.choice(moves) # Tuple: (general, x, o)
    # Update board
    for i, p in enumerate(selected[1]):
      # Update x player
      if selected[1][i] == '1':
        self.board[i] = 'X'
      # Update o player
      if selected[2][i] == '1':
        self.board[i] = 'O'
      # Update empty space
      if selected[0][i] == '0':
        self.board[i] = '-'
    self.print_board()
  
  def game_finished(self)->bool:
    """ 
    Check if the game is finished 

    -------
    return: bool
      True if the game is finished, False otherwise
    """
    if 'X' not in self.board:
      print("Ganó el jugador O")
      return True
    if 'O' not in self.board:
      print("Ganó el jugador X")
      return True
    representations = self.get_representations()
    # id there are 1 in the first 3 positions of the x player representation, the player X won
    if '1' in representations[1][6:]:
      print("Ganó el jugador X")
      return True
    # id there are 1 in the last 3 positions of the x player representation, the player O won
    if '1' in representations[2][:3]:
      print("Ganó el jugador O")
      return True
    return False

if __name__ == '__main__':

  game = Hexapawn()
  game.print_board()
  while True:
    game.user_move()
    time.sleep(1)
    game.get_random_move()
    if game.game_finished():
      break