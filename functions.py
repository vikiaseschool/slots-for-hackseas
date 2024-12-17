import random

def get_slot():
    symbols = ['skibidi', 'hawk_tuah', 'sigma', 'rizzler', 'darius', 'freakbob']

    probabilities = [1 / 2400, 1 / 2400, 1 / 4000, 1 / 4000, 1 / 6400, 1 / 10]
    total_probability = sum(probabilities)
    normalized_probabilities = [p / total_probability for p in probabilities]

    def choose_symbol():
        return random.choices(symbols, normalized_probabilities)[0]


    def generate_grid():

        grid = [[choose_symbol() for _ in range(3)] for _ in range(3)]

        def check_win(grid):
            for row in grid:
                if row[0] == row[1] == row[2]:
                    return True
            for col in range(3):
                if grid[0][col] == grid[1][col] == grid[2][col]:
                    return True

            if grid[0][0] == grid[1][1] == grid[2][2]:
                return True
            if grid[0][2] == grid[1][1] == grid[2][0]:
                return True
            return False

        for p in normalized_probabilities:
            if random.random() < p:
                while not check_win(grid):
                    grid = [[choose_symbol() for _ in range(3)] for _ in range(3)]
                break

        return grid

    return generate_grid()


def check_winnings(grid):
    winnings = []
    if grid[0][0] == grid[0][1] == grid[0][2]:
        winnings.append(grid[0][0])
    if grid[1][0] == grid[1][1] == grid[1][2]:
        winnings.append(grid[1][0])
    if grid[2][0] == grid[2][1] == grid[2][2]:
        winnings.append(grid[2][0])

    if grid[0][0] == grid[1][1] == grid[2][2]:
        winnings.append(grid[0][0])
    if grid[2][0] == grid[1][1] == grid[0][2]:
        winnings.append(grid[2][0])

    return winnings

def get_winnings_value(winnings):
    symbols = ['skibidi', 'hawk_tuah', 'sigma', 'rizzler', 'darius', 'freakbob']
    probabilities = [3, 3, 5, 5, 8, 10]
    win = 0
    for symbol in winnings:
        win += probabilities[symbols.index(symbol)]
    return win

def get_win_song(winnings):
    symbols = ['skibidi', 'hawk_tuah', 'sigma', 'rizzler', 'darius', 'freakbob']
    highest_index = -1
    highest_symbol = None

    for winning_symbol in winnings:
        index = symbols.index(winning_symbol)
        if index > highest_index:
            highest_index = index
            highest_symbol = winning_symbol
    return f'{highest_symbol}.mp3'


def check_winning_lines(slot_symbols):
    winning_lines = []
    for row in range(len(slot_symbols)):
        if len(set(slot_symbols[row])) == 1:
            winning_lines.append([(row, col) for col in range(len(slot_symbols[row]))])


    if len(slot_symbols) == len(slot_symbols[0]):
        diagonal1 = [slot_symbols[i][i] for i in range(len(slot_symbols))]
        if len(set(diagonal1)) == 1:
            winning_lines.append([(i, i) for i in range(len(slot_symbols))])

        diagonal2 = [slot_symbols[i][len(slot_symbols) - 1 - i] for i in range(len(slot_symbols))]
        if len(set(diagonal2)) == 1:
            winning_lines.append([(i, len(slot_symbols) - 1 - i) for i in range(len(slot_symbols))])

    return winning_lines
