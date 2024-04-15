import numpy as np
import pandas as pd

def hne(n):
    def hanoic(n, one='A', two='C', thr='B'):
        if n == 1:
            return np.array([1])
        else:
            count1 = hanoic(n-1, one, thr, two)
            count2 = hanoic(n-1, thr, two, one)
            return count1 + count2 + 1

    return hanoic(n)

def hne_move(n, one='A', two='C', thr='B'):
    def hanoi(n, one, two, thr):
        if n == 1:
            return pd.DataFrame([(one, two)], columns=['from', 'to'])
        else:
            moves1 = hanoi(n-1, one, thr, two)
            move = pd.DataFrame([(one, two)], columns=['from', 'to'])
            moves2 = hanoi(n-1, thr, two, one)
            return pd.concat([moves1, move, moves2], ignore_index=True)
    
    moves = hanoi(n, one, two, thr)
    print("이동 경로:")
    print(moves)
