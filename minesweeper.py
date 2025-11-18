import random

def create_board(size, mines):
    board = [[{"is_mine": False, "is_revealed": False, "is_flagged": False, "adjacent_mines": 0} for _ in range(size)] for _ in range(size)]

    # Place mines
    placed_mines = 0
    while placed_mines < mines:
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        if not board[row][col]["is_mine"]:
            board[row][col]["is_mine"] = True
            placed_mines += 1

    # Calculate adjacent mines
    for row in range(size):
        for col in range(size):
            if not board[row][col]["is_mine"]:
                board[row][col]["adjacent_mines"] = count_adjacent_mines(board, row, col, size)

    return board

def count_adjacent_mines(board, row, col, size):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            new_row, new_col = row + i, col + j
            if 0 <= new_row < size and 0 <= new_col < size and board[new_row][new_col]["is_mine"]:
                count += 1
    return count

def print_board(board, size):
    # Print column numbers
    print("   " + " ".join(str(i) for i in range(size)))
    for row_index, row in enumerate(board):
        # Print row number followed by the row content
        print(f"{row_index:2} " + " ".join(
            "F" if cell["is_flagged"] else
            "M" if cell["is_mine"] and cell["is_revealed"] else
            str(cell["adjacent_mines"]) if cell["is_revealed"] else
            "#"
            for cell in row
        ))

def reveal_cell(board, row, col, size):
    if board[row][col]["is_revealed"] or board[row][col]["is_flagged"]:
        return

    board[row][col]["is_revealed"] = True

    if board[row][col]["is_mine"]:
        print("Game Over! You hit a mine.")
        return

    if board[row][col]["adjacent_mines"] == 0:
        for i in range(-1, 2):
            for j in range(-1, 2):
                new_row, new_col = row + i, col + j
                if 0 <= new_row < size and 0 <= new_col < size:
                    reveal_cell(board, new_row, new_col, size)

def flag_cell(board, row, col):
    board[row][col]["is_flagged"] = not board[row][col]["is_flagged"]

def play_game():
    size = 10
    mines = 20
    board = create_board(size, mines)

    while True:
        print_board(board, size)
        # have to put into terminal reveal # # to get an output
        action = input("Enter action (reveal/flag) and coordinates (row col): ").split()
        if len(action) != 3:
            print("Invalid input. Try again.")
            continue

        act, row, col = action[0], int(action[1]), int(action[2])
        if act == "reveal":
            reveal_cell(board, row, col, size)
        elif act == "flag":
            flag_cell(board, row, col)
        else:
            print("Unknown action. Use 'reveal' or 'flag'.")

if __name__ == "__main__":
    play_game()