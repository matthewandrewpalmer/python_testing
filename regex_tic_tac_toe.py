import re

gameList = ["XXX-O-O-O", "X--OOOX-X", "O--OO-XXX", "O-XOX-O-X", "OXOOXOXX-", "X-O-OOXXO", "XO--X-OOX", "X-OXOOOXX"]


def regex_tic_tac_toe_win_checker(board):
    # your code here
    match_three_down = re.search(r'(X([-OX]{2})){2}X|(O([-OX]{2})){2}O|[O]{3}[-OX]{3}', board)
    match_three_across = re.search(r'(^|[-OX]{3})([O]{3}|[X]{3})($|[-OX]{3})', board)
    match_three_diagonal = re.search(r'^X([-OX]{3}X[-OX]{3})X$|^O([-OX]{3}O[-OX]{3})O$|[-OX]{2}((X[-OX]){3})|[-OX]{2}((O[-OX]){3})', board)
    if match_three_down or match_three_across or match_three_diagonal:
        return True
    return False


for game in gameList:
    print(game)
    result = regex_tic_tac_toe_win_checker(game)
    print(result)
