import copy


def judge(board, sel):
    # sel は3x3の2次元リストで，先手が選んだマスは '○'，後手が選んだマスは '×'，
    # 空きマスは 0 となっている．
    # 仮定：先手も後手もともにどこかに3つ並んだ状況の sel は渡されない
    # 横に3つ並んでいるのを見つけたらそれを返す
    for i in range(3):
        if sel[i][0] != 0 and sel[i][0] == sel[i][1] == sel[i][2]:
            return sel[i][0]

    # 縦に3つ並んでいるのを見つけたらそれを返す
    for j in range(3):
        if sel[0][j] != 0 and sel[0][j] == sel[1][j] == sel[2][j]:

            return sel[0][j]
    # 斜めに3つ並んでいるのを見つけたらそれを返す
    if sel[0][0] != 0 and sel[0][0] == sel[1][1] == sel[2][2]:
        return sel[0][0]

    if sel[2][0] != 0 and sel[2][0] == sel[1][1] == sel[0][2]:
        return sel[2][0]

    # 空きマスがなければ，合計点の大きい方を返す
    if 0 not in sel[0] and 0 not in sel[1] and 0 not in sel[2]:
        pO = 0
        pX = 0
        for i in range(3):
            for j in range(3):
                if sel[i][j] == "o":
                    pO += board[i][j]
                elif sel[i][j] == "x":
                    pX += board[i][j]
        """
        「ただし，マスの得点は合計すると必ず奇数になるものとし，これにより必ず勝敗がつくこととします．」
        マスの合計得点が偶数の場合も処理できるアルゴリズムに変更．
        引き分けの場合も処理できる．
        if pO > pX:
            return "o"
        else:
            return "x"
        """
        if pO > pX:
            return "o"
        elif pO < pX:
            return "x"

    # 勝敗がついていなければFalse
    return False


def point(board, sel):
    # ox双方のポイントを返す
    point_o = point_x = 0
    for i in range(3):
        for j in range(3):
            if sel[i][j] == "o":
                point_o += board[i][j]
            elif sel[i][j] == "x":
                point_x += board[i][j]
    return {"o": point_o, "x": point_x}


# Notice
# 添付資料のコードのマル・バツはアルファベットの"o"と"x"ではない．
# ○ => o
# × => x


# テスト
board = [[2, 9, 8], [6, 4, 3], [7, 5, 7]]  # o
# board = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]  # x
# board = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -3]]  # o
# board = [[-1, -1, -1], [-1, -1, -1], [-1, -3, -3]]  # x
# board = [[-6, -3, -3], [-3, -7, -9], [-3, -8, -1]]  # o
# board = [[-8, -3, -8], [-1, -5, -1], [-7, -6, -6]]  # x
# board = [[0, 0, 0], [1, 0, -1], [0, 0, 0]]
# board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

sel = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


class Board_evalation():
    # 勝敗が決定した盤面の評価を記録
    def __init__(self, winner, depth, point):
        self.winner = winner
        self.depth = depth
        self.point = point
        self.record = []


def avairable(sel):
    # 石を置くことができるマスの座標を返す
    for i in range(len(sel)):
        for j in range(len(sel[i])):
            if sel[i][j] == 0:
                yield i, j


def OX(board, sel, turn="o", depth=0, coordinate=[]):
    # 双方が最善手を尽くした場合のBoard_evaluationを返す
    match judge(board, sel):
        case "o" | "x" as winner:
            evalation = Board_evalation(winner, depth, point(board, sel))
            evalation.record.insert(0, coordinate)
            return evalation

        case False:

            judgements = []

            for i, j in avairable(sel):
                # 石を置く
                _sel = copy.deepcopy(sel)
                _sel[i][j] = turn

                # その石が置かれた局面について評価する
                judgements += [OX(board, _sel,
                               {"o": "x", "x": "o"}[turn], depth+1, [i, j, turn])]

            # すべてのマスに石を置き終わっており，勝敗がついていない引き分けのとき
            if judgements == []:
                return Board_evalation(False, None, {"o": None, "x": None})

            # 参考: mini-Max法
            # 自分(turn)にとって最善手を打ち続ければ勝てる局面のとき
            elif turn in [judgement.winner for judgement in judgements]:
                # 自分が勝つ手の中で(filter)、ポイントが最も多く得られる手を選ぶ(max関数と引数key)
                strong = max(filter(lambda judgement: judgement.winner == turn, judgements),
                             key=lambda judgement: judgement.point[turn])
                # 石を置いたマス目の座標を記録する．
                strong.record.insert(0, coordinate)
                return strong

            # 双方が最善手を打ち続けると，引き分けになる局面のとき
            elif False in [judgement.winner for judgement in judgements]:
                return Board_evalation(False, None, {"o": None, "x": None})

            # 自分(turn)にとって、相手が最善手を打ち続けるとき、いかなる手を選んでも勝てない局面のとき
            else:
                # 自分が負けるとわかっている場合でも，相手の点ができるだけ小さくなるようにする
                strong = min(
                    judgements, key=lambda judgement: judgement.point[turn])
                # 石を置いたマス目の座標を記録する．
                strong.record.insert(0, coordinate)
                return strong


print(board)
judgement = OX(board, sel)

# 勝者を出力する
print(f"勝ち: {judgement.winner}")

# oとxそれぞれの点数を出力する
print(f"o: {judgement.point['o']}, x: {judgement.point['x']}")
print("")

# 途中経過の盤面を出力する
board = [["-" for _ in range(3)] for _ in range(3)]
for coordinate in judgement.record[1:]:
    board[coordinate[0]][coordinate[1]] = coordinate[2]
    for y in range(3):
        print(f"{board[y][0]} {board[y][1]} {board[y][2]}")
    print(f"{coordinate[2]}: {coordinate[0]} {coordinate[1]}")
    print("")
