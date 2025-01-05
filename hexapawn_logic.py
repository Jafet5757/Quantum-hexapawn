from prettytable import PrettyTable
import pandas as pd
import random
import time
from quantum_search import grover_search

class Hexapawn:
  def __init__(self):
    self.board = ['X', 'X', 'X','-', '-', '-', 'O', 'O', 'O']
    self.current_player = 'O'
    self.last_move = None
    self.number_of_pieces = 3
    self.player_winner = False

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
      

  def get_moves(self)->list:
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
          exit()
        else:
          continue

  def update_board(self, state:tuple):
    """ 
    Update the board with the state

    parameters:
    state: tuple
      The state to update the board (general, x, o) 
    """
    # Update board
    for i, p in enumerate(state[1]):
      # Update x player
      if state[1][i] == '1':
        self.board[i] = 'X'
      # Update o player
      if state[2][i] == '1':
        self.board[i] = 'O'
      # Update empty space
      if state[0][i] == '0':
        self.board[i] = '-'
    self.print_board()

  def get_random_move(self):
    """ 
     Get a random move for the machine player
    """
    moves = self.get_moves()
    if not moves:
      print("Ganaste (o perdiste, no sé)")
      exit()
    selected = random.choice(moves) # Tuple: (general, x, o)
    # Update board
    self.update_board(selected)
  
  def game_finished(self)->bool:
    """ 
    Check if the game is finished 

    -------
    return: bool
      True if the game is finished, False otherwise
    """
    if 'X' not in self.board:
      print("Ganó el jugador O")
      self.player_winner = True
      return True
    if 'O' not in self.board:
      print("Ganó el jugador X")
      self.player_winner = False
      return True
    representations = self.get_representations()
    # id there are 1 in the first 3 positions of the x player representation, the player X won
    if '1' in representations[1][6:]:
      print("Ganó el jugador X")
      self.player_winner = False
      return True
    # id there are 1 in the last 3 positions of the x player representation, the player O won
    if '1' in representations[2][:3]:
      print("Ganó el jugador O")
      self.player_winner = True
      return True
    return False
  
  def get_inteligent_move(self, learning:bool=False, filename:str="learned_movements.csv")->tuple:
    """ 
      read the file of learned movements and get a random movement available 

      Parameters:
      learning: bool
        If true update the file of learned movements
      filename: str
        The name of the file to read the learned movements

      -------
      return: tuple
        The selected movement
    """
    # Read the CSV file
    df = pd.read_csv(filename, dtype=str, header=0, skipinitialspace=True)
    # Get the current state
    general, x_player, o_player = self.get_representations()
    # Search the current state in the DataFrame
    possible_movements = df[
        (df['actual_state_general'] == general) &
        (df['actual_state_x'] == x_player) &
        (df['actual_state_o'] == o_player)
    ]
    
    # Search the general state in the Quantum Search
    list_moves = possible_movements[['play1_state_x', 'play2_state_x', 'play3_state_x', 'play4_state_x']]

    if list_moves.empty:
      print("No hay movimientos inteligentes posibles")
      return None
    
    list_moves = list_moves.values.tolist()[0]
    # delete nan
    list_aux = []
    for i in list_moves:
      if pd.notna(i):
        list_aux.append(i)
    print(list_aux)
    qs = grover_search(list_aux)
    
    # Select the best movement
    if qs is not None:
      selected = max(qs, key=qs.get)
    else:
      print("No hay movimientos inteligentes posibles")
      return None
    
    # Get index of the column
    column = possible_movements.eq(selected).idxmax(axis=1).iloc[0] # Get the column of the selected movement
    index_column = possible_movements.columns.get_loc(column)

    # Count how much columns are not None
    count_possible_movements = ((possible_movements.dropna(axis=1, how='all').count(axis=1) / 3) - 1).sum() # Count the number of tuples less the actual state
    
    # If there are not possible movements return none
    if count_possible_movements == 0:
      print("No hay movimientos inteligentes posibles")
      return None
    else:
      while True:
        # Select a random movement
        selected = index_column - 1
        # Get the selected movement (column)
        selected_movement = possible_movements.iloc[0, selected:selected+3] # Get the selected tuple of movement   
        # Si no es None, romper el ciclo
        if selected_movement[0] is not None and pd.notna(selected_movement[0]):
          break
      # Save the last movement
      self.last_move = selected_movement.to_dict()
      # transform to tuple
      selected_movement = (selected_movement[0], selected_movement[1], selected_movement[2])
      # Update board
      self.update_board(selected_movement)
      return selected_movement

  def update_inteligents_moves(self, game_over = False, filename:str = "learned_movements.csv"):
    """ 
    Verify if loss a piece if true delete the last movement in the file, else nothing
    """
    # Get representations
    _, x_player, o_player = self.get_representations()
    # Count the number of pieces of the machine player
    pieces = x_player.count('1') if self.current_player == 'O' else o_player.count('1')
    
    if pieces < self.number_of_pieces or game_over:
      # Delete the last movement in the file
      df = pd.read_csv(filename, dtype=str, header=0, skipinitialspace=True)
      # get keys of last movement
      keys = list(self.last_move.keys())
      # get the last movement
      index_to_drop = df[
          (df[keys[0]] == self.last_move[keys[0]]) &
          (df[keys[1]] == self.last_move[keys[1]]) &
          (df[keys[2]] == self.last_move[keys[2]])
      ].index
      df.loc[index_to_drop, keys] = None
      # Save the file
      df.to_csv(filename, index=False)
      # Update the number of pieces
      self.number_of_pieces = pieces

  def play(self, random:bool = False, learning = False, filename:str="learned_movements.csv"):
    """ 
    Play the game with the machine player
    """
    self.print_board()

    while True:
      self.user_move()

      # Check if the game is finished
      if self.game_finished() and learning:
        self.update_inteligents_moves(game_over=True,filename=filename)
        break

      # wait a moment to move
      time.sleep(1)
      if not random:
        move = self.get_inteligent_move(filename=filename)
        # If there are not possible movements, get a random movement
        if move is None:
          self.get_random_move()
        elif learning:
          # Update the file of learned movements
          self.update_inteligents_moves(filename=filename)
      else:
        # Get a random movement
        self.get_random_move()

      # Check if the game is finished
      if self.game_finished():
        break

if __name__ == '__main__':
  
  game = Hexapawn()
  game.play(random=False, learning=False)