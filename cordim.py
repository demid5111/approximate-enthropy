from math import log

from apen import ApEn


class CorDim(ApEn):
    @staticmethod
    def calc_heviside(radius, diff):
        return 0 if radius - diff < 0 else 1

    @staticmethod
    def calc_cor_func(seq, radius):
        res = []
        for i in seq:
            for j in seq:
                res.append(CorDim.calc_heviside(radius, ApEn.calculate_distance(i, j)))
        return (1/(len(seq)**2)) * sum(res)

    @staticmethod
    def calc_attractor(cor_func_res, radius):
        return log(cor_func_res) / log(radius)


if __name__ == '__main__':
    dimension = 2
    radius = 0.99

    corDim = CorDim()
    seq = CorDim.read_series('data/ApEn_amolituda_2.txt', False, False)
    portrait = CorDim.slice_intervals(dimension, seq)
    res = CorDim.calc_cor_func(portrait, radius)
    attractor = CorDim.calc_attractor(res, radius)
    print(attractor)
