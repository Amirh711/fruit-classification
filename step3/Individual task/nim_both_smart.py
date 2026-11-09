import numpy as np
import pandas as pd

START = (3, 4, 5)           
nodes = 0                   


def moves(piles, order="small_first"):
    """All positions we can reach by taking some stones from ONE pile."""
    result = []
    for i, n in enumerate(piles):
        takes = range(1, n + 1) if order == "small_first" else range(n, 0, -1)
        for take in takes:
            new = list(piles)
            new[i] = n - take
            result.append(tuple(new))
    return result


def minimax(piles, player):
    """+1 if player A wins, -1 if player B wins (both play perfectly)."""
    global nodes
    nodes += 1
    if sum(piles) == 0:                     
        return -1 if player == "A" else 1
    values = [minimax(nxt, "B" if player == "A" else "A") for nxt in moves(piles)]
    return max(values) if player == "A" else min(values)


def alphabeta(piles, player, alpha, beta, order):
    global nodes
    nodes += 1
    if sum(piles) == 0:
        return -1 if player == "A" else 1
    if player == "A":
        value = -2
        for nxt in moves(piles, order):
            value = max(value, alphabeta(nxt, "B", alpha, beta, order))
            alpha = max(alpha, value)
            if alpha >= beta:
                break                       
        return value
    value = 2
    for nxt in moves(piles, order):
        value = min(value, alphabeta(nxt, "A", alpha, beta, order))
        beta = min(beta, value)
        if alpha >= beta:
            break                           
    return value


def best_move(piles, player):
    """Best next position for `player` (A maximizes, B minimizes)."""
    best_nxt, best_value = None, None
    for nxt in moves(piles, "big_first"):
        value = alphabeta(nxt, "B" if player == "A" else "A", -2, 2, "big_first")
        better = best_value is None or (value > best_value if player == "A" else value < best_value)
        if better:
            best_nxt, best_value = nxt, value
    return best_nxt


 





rng = np.random.default_rng(0)
rows = []
for game in range(200):
    piles = tuple(int(x) for x in rng.integers(1, 5, size=3)) 
    nodes = 0
    start_value = alphabeta(piles, "A", -2, 2, "big_first")
    nodes_ab = nodes
    nodes = 0
    minimax(piles, "A")
    nodes_mm = nodes
    board, player, n_moves = piles, "A", 0
    while sum(board) > 0:
        board = best_move(board, player)       
        player = "B" if player == "A" else "A"
        n_moves += 1
    rows.append({"p1": piles[0], "p2": piles[1], "p3": piles[2], "total": sum(piles),
                 "nim_sum": piles[0] ^ piles[1] ^ piles[2], "first_wins": start_value > 0,
                 "nodes_minimax": nodes_mm, "nodes_alphabeta": nodes_ab, "moves": n_moves,
                 "winner": "B" if player == "A" else "A"})

df = pd.DataFrame(rows)
df.to_csv("nim_games_both_smart.csv", index=False)
print(df.head())

# Checks
print("nim_sum != 0 agrees with first_wins:", ((df["nim_sum"] != 0) == df["first_wins"]).mean())
print("winner == A  agrees with first_wins:", ((df["winner"] == "A") == df["first_wins"]).mean())
print("A wins", round((df["winner"] == "A").mean() * 100), "% of the games (both players smart)")
