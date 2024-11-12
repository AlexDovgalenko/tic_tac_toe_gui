import tkinter
from dataclasses import dataclass
from enum import StrEnum, auto, IntEnum


class ColorPalette(StrEnum):
    RED = "#c90404"
    BLUE = "#2196F3"
    YELLOW = "#FFEB3B"
    GRAY = "#363434"
    L_GRAY = "#90A4AE"

class GameStateEnum(IntEnum):
    RUNNING = auto()
    GAME_OVER = auto()

@dataclass
class Player:
    name: str
    char: str
    txt_color: "ColorPalette"

player_x = Player(name="Player_X", char="X", txt_color=ColorPalette.BLUE)
player_o = Player(name="Player_O", char="O", txt_color=ColorPalette.RED)

# @dataclass
class GameState:
    def __init__(self):

        self.state: "GameStateEnum" = GameStateEnum.RUNNING
        self.current_player: "Player" = player_x
        self.step_number = 0

game_state = GameState()

default_color = ColorPalette.GRAY
default_font = "Consolas"

board = [[0,0,0], [0,0,0], [0,0,0]]

def set_tile(row, column, game_state=game_state) -> None:
    if game_state.state == GameStateEnum.GAME_OVER:
        return
    if board[row][column]["text"]:
        return
    board[row][column]["text"] = game_state.current_player.char
    board[row][column]["foreground"] = game_state.current_player.txt_color
    game_state.current_player = player_o if game_state.current_player == player_x else player_x
    caption["text"] = f"Player <{game_state.current_player.char}>'s turn!"
    game_state.step_number += 1

    result = check_winner(board)
    if result:
        caption["text"] = f"Player <{result}> WINS!!!"
        caption["foreground"] = ColorPalette.YELLOW
        game_state.state = GameStateEnum.GAME_OVER
        return

    if game_state.step_number == 9:
        caption["text"] = f"GAME OVER!"
        caption["foreground"] = ColorPalette.RED
        return


def reset_game() -> None:
    game_state.step_number = 0
    game_state.current_player = player_o if game_state.current_player == player_x else player_x
    caption["text"] = f"Player <{game_state.current_player.char}>'s turn!"
    caption["foreground"] = ColorPalette.L_GRAY
    reset_board(board)
    game_state.state = GameStateEnum.RUNNING

def check_horizontal(board):
    for row in board:
        if all(element["text"] == row[0]["text"] for element in row) and row[0] is not None:
            print(row[0]["text"])
            return row[0]["text"]
    return None

def check_vertical(board):
    for column in range(len(board[0])):
        first_element = board[0][column]["text"]
        if first_element is not None and all(board[row][column]["text"] == first_element for row in range(1, len(board))):
            print(first_element)
            return first_element
    return None

def check_diagonal(board):
    # Check main diagonal (top-left to bottom-right)
    first_element = board[0][0]["text"]
    if first_element is not None and all(board[i][i]["text"] == first_element for i in range(1, len(board))):
        return first_element
    # Check anti-diagonal (top-right to bottom-left)
    first_element = board[0][len(board) - 1]
    if first_element is not None and all(board[i][len(board) - 1 - i]["text"] == first_element for i in range(1, len(board))):
        return first_element
    return None


def check_winner(board):
    result = check_horizontal(board)
    if result:
        return result
    result = check_vertical(board)
    if result:
        return result
    result = check_diagonal(board)
    if result:
        return result
    return None

def reset_board(board):
    board_dimension = len(board)
    for row in range(board_dimension):
        for column in range(board_dimension):
            board[row][column] = tkinter.Button(field, text="", font=(default_font, 60, "bold"), background=ColorPalette.RED, foreground=ColorPalette.BLUE, width=4, height=2, command=lambda row=row, column=column: set_tile(row, column, game_state))
            board[row][column].grid(row=row+1, column=column)

window = tkinter.Tk()
window.resizable(None, None)
frame = tkinter.Frame(window)
caption = tkinter.Label(frame, text=f"Player <{game_state.current_player.char}>'s turn!", font=(default_font, 25),
                        background=default_color, pady=3, padx=3)
field = tkinter.Frame(frame, background=ColorPalette.YELLOW)
reset_board(board=board)
reset_button = tkinter.Button(frame, text="Reset", font=(default_font, 25), command=reset_game)

caption.grid(row=0, column=0, columnspan=3, sticky="we")
field.grid(row=1, column=0)
reset_button.grid(row=2, column=0, columnspan=3, sticky="we")
frame.pack()

window.mainloop()
