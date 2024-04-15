def hne(n):
    def hanoic(n, one='A', two='C', thr='B'):
        if n == 1:
            return 1
        else:
            count1 = hanoic(n-1, one, thr, two)
            count2 = hanoic(n-1, thr, two, one)
            return count1 + count2 + 1

    return hanoic(n)

def hne_move(n, one='A', two='C', thr='B'):
    def hanoim(n, one, two, thr):
        if n == 1:
            return [(one, two)]
        else:
            moves1 = hanoim(n-1, one, thr, two)
            move = (one, two)
            moves2 = hanoim(n-1, thr, two, one)
            return moves1 + [move] + moves2

    moves = hanoim(n, one, two, thr)
    print("이동 경로:")
    for move in moves:
        print(f"기둥 {move[0]}에 있는 맨 위 원판 -> 기둥 {move[1]}으로 이동")
