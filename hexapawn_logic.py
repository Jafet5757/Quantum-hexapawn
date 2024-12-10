from prettytable import PrettyTable
import pandas as pd

class Hexapawn:
  def __init__(self):
    self.board = ['X', 'X', 'X','-', '-', '-', 'O', 'O', 'O']
    self.current_player = 'O'

  def print_board(self):
    print("\033c", end="") # Clear the console
    
    for i, row in enumerate(self.board):
      print(row, end=" " if i%3 != 2 else "\n")

  def clean_board(self):
    self.board = ['-', '-', '-', 
                  '-', '-', '-', 
                  '-', '-', '-']

  def create_play(self):
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

if __name__ == '__main__':
  while True:
    game = Hexapawn()
    game.print_board()
    game.create_play()
    if input("\nDesea parar? (s/n): ") == 's':
      break