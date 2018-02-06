import numpy as np


class BinomialModel(object):
    def __init__(self, *args):
        # black == False. args: S0, u, d, R
        # or
        # black == True. args:  S0, u, d, R, q
        self.S0 = args[0]
        self.u = args[1]
        self.d = args[2]
        self.R = args[3]
        self.euro = args[5]
        self.call = args[6]
        self.black = args[7]

        if self.black:
            self.q = args[4]
        else:
            self.q = (self.R - self.d) / (self.u - self.d)

        self.up, self.down = self.create_branches()
        # Value of root
        self.c = 0

    def create_branches(self):
        # Down and up moves
        return self.S0 * self.u, self.S0 * self.d

    def set_c_values(self, bi_1, bi_2, K):
        if self.euro:
            self.c = sum(np.array([self.q, 1-self.q]) * [bi_1.c, bi_2.c])/self.R
        else:
            if self.call:
                self.c = max(sum(np.array([self.q, 1 - self.q]) * [bi_1.c, bi_2.c])/self.R,
                             self.S0 - K)
            else:
                self.c = max(sum(np.array([self.q, 1 - self.q]) * [bi_1.c, bi_2.c])/self.R,
                             K - self.S0)

        self.c = self.c


class MultibinomialModel(object):
    def __init__(self, *args, euro=True, call=True, black=False):
        # black == False. args: S0, u, d, R
        # or
        # black == True. args:  S0, u, d, R, q
        self.S0 = args[0]
        self.u = args[1]
        self.d = args[2]
        self.R = args[3]
        self.t = args[4]
        self.euro = euro
        self.call = call
        self.black = black

        if self.black:
            self.q = args[5]
        else:
            self.q = (self.R - self.d)/(self.u - self.d)

        self.branches = []

        # Init root
        self.branches.append([BinomialModel(self.S0, self.u, self.d, self.R, self.q,
                                            self.euro, self.call, self.black)])

        # Init first values
        self.S = []
        self.S.append([self.S0])
        self.S.append([])
        self.S[-1].append(self.branches[0][0].up)
        self.S[-1].append(self.branches[0][0].down)

        self.init_branches()

        # Values
        self.C = []

    def init_branches(self):
        for i in range(1, self.t):
            self.branches.append([])
            self.S.append([])
            for num in self.S[i]:
                new_model = BinomialModel(num, self.u, self.d, self.R, self.q, self.euro, self.call, self.black)
                self.branches[-1].append(new_model)

                if len(self.S[-1]) > 1:
                    self.S[-1].append(new_model.down)
                else:
                    self.S[-1].append(new_model.up)
                    self.S[-1].append(new_model.down)

    def count_all_values(self, K):
        # All values for every node in every period
        S = np.array(self.S[-1])

        if self.call:
            S = S - K
        else:
            S = K - S

        S = list(map(lambda x: 0 if x < 0 else x, S))

        # Init values of last branches and layer
        self.C.append([])
        self.C[-1] = S

        ls = []
        for i in range(len(self.branches[-1])):
            if self.euro:
                self.branches[-1][i].c = sum(np.array([self.q, 1-self.q]) *
                                             [self.C[-1][i],
                                              self.C[-1][i+1]])/self.R
            else:
                if self.call:
                    self.branches[-1][i].c = max(sum(np.array([self.q, 1-self.q]) *
                                                 [self.C[-1][i],
                                                  self.C[-1][i+1]])/self.R, self.branches[-1][i].S0 - K)
                else:
                    self.branches[-1][i].c = max(sum(np.array([self.q, 1-self.q]) *
                                                     [self.C[-1][i],
                                                      self.C[-1][i+1]])/self.R,
                                                 K - self.branches[-1][i].S0)

            ls.append(self.branches[-1][i].c)
        self.C.append(ls)
        del ls

        for i in range(len(self.branches)-2, -1, -1):
            self.C.append([])
            for j in range(len(self.branches[i])):
                self.branches[i][j].set_c_values(self.branches[i+1][j], self.branches[i+1][j+1], K)
                self.C[-1].append(self.branches[i][j].c)

        self.C = list(reversed(self.C))
        return self.C

    def create_trading_strategies(self):
        for i in range(1, len(self.S)):
            print("Layer {}".format(i-1))
            for j in range(len(self.S[i])-1):
                a = np.array([[self.S[i][j], self.R**i],
                              [self.S[i][j+1], self.R**i]])

                b = np.array([[self.C[i][j]],
                              [self.C[i][j+1]]])

                solution = np.linalg.solve(a, b)

                x = solution[0]
                y = solution[1]

                print("x: {}"
                      "\ny: {}".format(np.round(x, 2), np.round(y, 2)))

                value = np.round(x * self.S[i-1][j] + y * self.R**(i-1), 2)

                print("Value is {}".format(value[0]))
                print()
