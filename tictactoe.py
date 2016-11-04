#!/bin/python

import itertools, copy, pprint

pp = pprint.PrettyPrinter(depth=3)

def newBoard():
	return [[" " for i in range(3)] for j in range(3)]

def winner(board):
	for token in ["X", "O"]:
		for row in board:
			if "".join(row) == token * 3:
				return token
		for i in range(3):
			if "".join([row[i] for row in board]) == token * 3:
				return token
		if board[0][0] == token and board[1][1] == token and board[2][2] == token:
			return token
		if board[2][0] == token and board[1][1] == token and board[0][2] == token:
			return token

	return None

def mkNode(board):
	return {'board': board, 'winner': winner(board), 'children': []}

def genBoards(node, turn):
	board = node['board']
	if not node['winner']:
		for x, y in itertools.product(range(3), range(3)):
			if board[x][y] == " ":
				cpy = copy.deepcopy(board)
				cpy[x][y] = turn
				node['children'].append(mkNode(cpy))
	for children in node['children']:
		genBoards(children, turn="X" if turn=="O" else "O")

	return node

def winningLeaves(node, token):
	if len(node['children']) > 0:
		return sum((winningLeaves(n, token) for n in node['children']))
	else:
		if node['winner'] == token:
			return 1
		else:
			return 0

def playTicTacToe(tree, turn, humanplayer=False, humantoken="X"):
	print(*tree['board'], sep="\n")
	print("---------------")
	opponent = "O" if turn=="X" else "X"
	if (not tree['winner']) and humanplayer and turn == humantoken:
		pos = int(input("Select a board position to play (1-9): ")) - 1
		x, y = int(pos/3), pos % 3
		if pos >= 0 and pos <= 8 and tree['board'][x][y] == " ":
			for node in tree['children']:
				if node['board'][x][y] == humantoken:
					move = node
			playTicTacToe(move, opponent, humanplayer, humantoken)
		else:
			print("That's not a valid move.")
			playTicTacToe(tree, turn, humanplayer, humantoken)
	elif (not tree['winner']) and len(tree['children']) > 0:
		zips = [list(tuple) for tuple in zip([(winningLeaves(n, opponent), -winningLeaves(n, turn)) for n in tree['children']], range(len(tree['children'])), tree['children'])]
		for nextturn in zips:
			if nextturn[2]['winner'] == turn:
				nextturn[0] = (0, float('-inf'))
			for nestedturn in nextturn[2]['children']:
				if nestedturn['winner'] == opponent:
					nextturn[0] = (float('inf'), 0)
		move = min(zips)[2]
		playTicTacToe(move, opponent, humanplayer, humantoken)
	else:
		if tree['winner']:
			if humanplayer:
				if tree['winner'] == humantoken:
					print("You win!")
				else:
					print("I win!")
			else:
				print("{} wins!").format(tree['winner'])
		else:
			print("A strange game. The only winning move is not to play.")

playTicTacToe(genBoards(mkNode(newBoard()), "X"), "X", True)
