from game import InfiniteTicTacToe

def preety_board(move):
    for row in move['board']:
        print(' '.join(row))

gra = InfiniteTicTacToe()

start = gra.start_game()
print(start)

moves = [(1,1),(1,1),(0,0),(0,1),(2,1),(0,2),(1,1),(2,0),(2,2),(1,1),(1,2)]

for m in moves:
    move = gra.make_move(m[0],m[1])
    print(move)
    preety_board(move)


