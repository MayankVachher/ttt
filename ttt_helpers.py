from bottle import Bottle, route, run

app = Bottle()

def refactor_str(board):
	
	if len(board) < 9:
		board = board.ljust(9, '_')

	board = board.replace('0', 'O')
	board = board.upper()

	N_x = board.count('X')
	N_o = board.count('O')

	refactored = {}

	for i, x in enumerate(board):
		refactored[i] = x

	return (refactored, N_x, N_o)

def check_win(board, player):
	w_rows = [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
	w_cols = [(0, 3, 6), (1, 4, 7), (2, 5, 8)]
	w_diag = [(0, 4, 8), (2, 4, 6)]

	wins = w_rows + w_cols + w_diag

	for pos_tpl in wins:
		pos1, pos2, pos3 = pos_tpl

		if board[pos1] == player and /
		   board[pos2] == player and /
		   board[pos3] == player:
			return True

	return False

def check_board_complete(board):
	for pos in board:
		if board[pos] == '_':
			return False

	return True


@app.route('/')
def callback():
	return "Hello!"

@app.route('/check')
@app.route('/check/')
@app.route('/check/<board>')
def check_callback(board='_'*9):

	if not set(board).issubset(set('XxoO0_')):
		return "Invalid"
	
	board_cleaned, N_x, N_o = refactor_str(board)

	if (N_o > N_x) or (N_x - N_o > 1):
		return "Invalid"

	if check_win(board_cleaned, 'O'):
		if check_win(board_cleaned, 'X'):
			return "Invalid"
		elif N_x != N_o:
			return "Invalid"
		else:
			return "Valid"

	elif check_win(board_cleaned, 'X'):
		if N_x != N_o + 1:
			return "Invalid"
		else:
			return "Valid"

	else:
		return "Valid"

@app.route('/win')
@app.route('/win/')
@app.route('/win/<board>')
def win_callback(board='_'*9):

	if check_callback(board) == "Invalid":
		return "InvalidState"

	board_cleaned, _, _ = refactor_str(board)

	if check_win(board_cleaned, 'O'):
		return "O"

	elif check_win(board_cleaned, 'X'):
		return "X"

	elif check_board_complete(board_cleaned):
		return "Draw"

	else:
		return "IncompleteGame"

run(app, host='localhost', port=7777, debug=True)