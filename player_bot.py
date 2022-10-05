#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    This is an example of a bot for the 3rd project.
    ...a pretty bad bot to be honest -_-
"""

from logging import DEBUG, debug, getLogger
from math import sqrt

# We use the debugger to print messages to stderr
# You cannot use print as you usually do, the vm would intercept it
# You can hovever do the following:
#
# import sys
# print("HEHEY", file=sys.stderr)

getLogger().setLevel(DEBUG)


def parse_field_info():
    """
    Parse the info about the field.

    However, the function doesn't do anything with it. Since the height of the field is
    hard-coded later, this bot won't work with maps of different height.

    The input may look like this:

    Plateau 15 17:
    """
    line = input()
    # debug(f"Description of the field: {l}")
    return line[:-1].split()[1:]


def parse_field():
    """
    Parse the field.

    First of all, this function is also responsible for determining the next
    move. Actually, this function should rather only parse the field, and return
    it to another function, where the logic for choosing the move will be.

    Also, the algorithm for choosing the right move is wrong. This function
    finds the first position of _our_ character, and outputs it. However, it
    doesn't guarantee that the figure will be connected to only one cell of our
    territory. It can not be connected at all (for example, when the figure has
    empty cells), or it can be connected with multiple cells of our territory.
    That's definitely what you should address.

    Also, it might be useful to distinguish between lowecase (the most recent piece)
    and uppercase letters to determine where the enemy is moving etc.

    The input may look like this:

        01234567890123456
    000 .................
    001 .................
    002 .................
    003 .................
    004 .................
    005 .................
    006 .................
    007 ..O..............
    008 ..OOO............
    009 .................
    010 .................
    011 .................
    012 ..............X..
    013 .................
    014 .................

    :param player int: Represents whether we're the first or second player
    """
    size = parse_field_info()
    list_of_rows = []
    for _ in range(int(size[0])+1):
        line = input()
        list_of_rows.append(line[4:])
    return list_of_rows[1:], size


def parse_figure():
    """
    Parse the figure.

    The function parses the height of the figure (maybe the width would be
    useful as well), and then reads it.
    It would be nice to save it and return for further usage.

    The input may look like this:

    Piece 2 2:
    **
    ..
    """
    line = input()
    piece_margins = line[:-1].split()[1:]
    # debug(f"Piece: {l}")
    height = int(line.split()[1])
    piece=[]
    for _ in range(height):
        line = input()
        piece.append(line)
        # debug(f"Piece: {l}")
    return piece, piece_margins

def move_checker(i_f, j_f, piece_margins, piece, field, player_sym_lil, \
    player_sym_lorge, enemy_sym_lorge, enemy_sym_lil):
    """
    checks if the place is ok
    """
    num_our = 0
    num_enemy = 0
    for i_p in range(int(piece_margins[0])):
        for j_p in range(int(piece_margins[1])):
            if piece[i_p][j_p]=='*':
                if field[i_f+i_p][j_f+j_p] == player_sym_lorge\
                    or field[i_f+i_p][j_f+j_p] == player_sym_lil:
                    num_our+=1
                    if num_our>1:
                        return False
                if field[i_f+i_p][j_f+j_p] == enemy_sym_lorge\
                    or field[i_f+i_p][j_f+j_p] == enemy_sym_lil:
                    num_enemy+=1
                    if num_enemy>0:
                        return False
    if num_our==1:
        return True
    else:
        return False


def ok_places(field, field_margins, piece, piece_margins, player):
    """
    returns set of all moves that player can do
    >>> ok_places(['..O..OOOOOOOOOOOO', '.OOOOOOOOOOOOOOOO', 'OOOOOOOOOOOOOOOOO', \
        'OOOOOOOOOOOOOOOOO', 'OOOOOOOOOOOOOOOOO', 'OOOOOOOOOOOOOOOOO', \
        'OOOOOOOOOOOOOOOOO', 'OOOOOOOOOOOOOOOOO', 'OOOOOOOOOOOOOOOOO', 'OOOOOOOOOOOOOOOOO', \
        'OOOOOOOOOOOOOOOOO', 'OOOOOOOOOOOOOOOOO', 'OOOOOOXXXXXXXXXXX', 'OOOOOOOOOOOOOOOOO', \
        'OOOOOOOOOOOOOOOOO'], ['15', '17'], ['*', '*'], ['2', '1'], 1)
        {(0, 1), (1, 0), (0, 3), (0, 4)}
    """
    if player == 1:
        player_sym_lorge='O'
        enemy_sym_lil='x'
        player_sym_lil='o'
        enemy_sym_lorge='X'
    if player == 2:
        enemy_sym_lorge='O'
        player_sym_lil='x'
        enemy_sym_lil='o'
        player_sym_lorge='X'
    field_margins = [int(field_margins[0])-int(piece_margins[0])+1, \
        int(field_margins[1])-int(piece_margins[1])+1]
    possible_moves=set()
    enemy_coords = set()
    for i_f in range(int(field_margins[0])):
        for j_f in range(int(field_margins[1])):
            if field[i_f][j_f] == enemy_sym_lorge\
                    or field[i_f][j_f] == enemy_sym_lil:
                enemy_coords.add((i_f, j_f))
            if move_checker(i_f, j_f, piece_margins, piece, field, player_sym_lil, \
                player_sym_lorge, enemy_sym_lorge, enemy_sym_lil):
                possible_moves.add((i_f, j_f))
    return possible_moves, enemy_coords

def closest_enemy(possible_moves, enemy):
    """
    finds the move that is closest to enemy territory
    """
    min_dist_dick = dict()
    for move in possible_moves:
        min_dist = 1000
        for enemy_coord in enemy:
            dist = int(sqrt((move[0]-enemy_coord[0])**2+(move[1]-enemy_coord[1])**2))
            if dist<min_dist:
                min_dist=dist
        min_dist_dick[min_dist]=move
    if len(min_dist_dick)==0:
        return None
    return min_dist_dick[min(min_dist_dick.keys())]


def step(player: int):
    """
    Perform one step of the game.

    :param player int: Represents whether we're the first or second player
    """
    move = None
    field, field_size = parse_field()
    figure, figure_size = parse_figure()
    okey, enemy = ok_places(field, field_size, figure, figure_size, player)
    move=closest_enemy(okey, enemy)
    # debug(f"!!!!!!!!!!!!!!!!!: {field, field_size, figure, figure_size, player, okey}")
    return move


def play(player: int):
    """
    Main game loop.

    :param player int: Represents whether we're the first or second player
    """
    while True:
        move = step(player)
        if move is None:
            print()
        else:
            print(*move)


def parse_info_about_player():
    """
    This function parses the info about the player

    It can look like this:

    $$$ exec p2 : [./player1.py]
    """
    i = input()
    # debug(f"Info about the player: {i}")
    return 1 if "p1 :" in i else 2


def main():
    player = parse_info_about_player()
    try:
        play(player)
    except EOFError:
        debug("Cannot get input. Seems that we've lost ):")


if __name__ == "__main__":
    main()
