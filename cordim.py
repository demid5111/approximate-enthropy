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
        coef = 1/(len(seq)**2) if len(seq) > 0 else 1
        return coef * sum(res)

    @staticmethod
    def calc_attractor(cor_func_res, radius):
        cor_val = log(cor_func_res) if cor_func_res != 0 else 1
        radius_val = log(radius) if radius != 0 and radius != 1 else 1
        return cor_val / radius_val


if __name__ == '__main__':
    dimension = 2
    radius = 0.99

    corDim = CorDim()
    seq = CorDim.read_series('data/ApEn_amolituda_2.txt', False, False)
    portrait = CorDim.slice_intervals(dimension, seq)
    res = CorDim.calc_cor_func(portrait, radius)
    attractor = CorDim.calc_attractor(res, radius)
    print(attractor)
