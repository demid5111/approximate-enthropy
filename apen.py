import operator
from math import log

from supporting import CalculationType

__author__ = 'demidovs'


class ApEn:
    def __init__(self, m):
        self.N = -1
        self.m = m
        self.r = -1
        self.u_list = []
        self.x_list = []
        self.c_list = []

    def read_series(self, fileName, useThreshold, thresholdValue):
        self.u_list = []
        with open(fileName, "r") as f:
            for val in f.readlines():
                self.u_list.append(float(val.strip().replace(',', '.')))
        assert self.u_list, "File is either missed or corrupted"
        if useThreshold:
            assert len(self.u_list) >= thresholdValue, "Sample length is too small. Need more than {}" \
                .format(str(thresholdValue))
        self.N = len(self.u_list)

    def create_vectors(self, m):
        self.x_list = []
        for i in range(self.N - m + 1):
            self.x_list.append(self.u_list[i:i + m])

    def calculate_distance(self, x1, x2):
        assert len(x1) == len(x2), "Vectors should be of equal sizes: " + str(x1) + " : " + str(x2)
        return max(map(abs, map(operator.sub, x1, x2)))

    def calculate_c(self, m):
        self.c_list = []
        assert self.r >= 0, "Filtering threshold should be positive"
        for i in range(0, self.N - m + 1):
            similar_vectors = 0
            for j in range(0, self.N - m + 1):
                res = self.calculate_distance(self.x_list[i], self.x_list[j])
                if res < self.r:
                    similar_vectors += 1
            self.c_list.append(similar_vectors / (self.N - m + 1))

    def _final(self, m):
        res = []
        for i in range(self.N - m + 1):
            tmp = log(self.c_list[i]) if self.c_list[i] else 0.0
            res.append(tmp)
        return sum(res) * ((self.N - m + 1) ** (-1))

    def calculate_final(self, m):
        # 3. Form a sequence of vectors so that
        # x[i] = [u[i],u[i+1],...,u[i+m-1]]
        # i ~ 0:N-m because indexes start from 0
        self.create_vectors(m=m)

        # 4. Construct the C(i,m) - portion of vectors "similar" to i-th
        # similarity - d[x(j),x(i)], where d = max(a)|u(a)-u*(a)|
        # this is just the respective values subtraction
        self.calculate_c(m=m)

        return self._final(m=m)

    def calculate_apen(self, m):
        return self.calculate_final(m) - self.calculate_final(m + 1)

    def calculate_deviation(self, seq):
        total_sum_norm = sum(self.u_list) / self.N
        return (sum([(i - total_sum_norm) ** 2 for i in seq]) / (self.N)) ** (1 / 2)

    def make_sdds(self, seq):
        return self.calculate_deviation([seq[i] - seq[i - 1] for (i, v) in enumerate(seq[1:])])

    def calculate_complex_r(self, sddsDeviation, deviation, len_seq):
        if not deviation:
            return 0
        else:
            return (-0.036 + 0.26 * (sddsDeviation / deviation) ** (1 / 2)) / ((len_seq / 1000) ** (1 / 4))

    def calculate_r(self, calculation_type, r, dev_coef_value, seq):
        res_r = 0
        if calculation_type == CalculationType.CONST:
            res_r = r * 0.2
        elif calculation_type == CalculationType.DEV:
            res_r = r * dev_coef_value
        elif calculation_type == CalculationType.COMPLEX:
            sdds_deviation = self.make_sdds(seq)
            res_r = self.calculate_complex_r(sdds_deviation, r, len(seq))
        return res_r

    def prepare_calculate_apen(self, m, file_name, calculation_type, dev_coef_value, use_threshold, threshold_value):
        self.read_series(file_name, use_threshold, threshold_value)
        deviation = self.calculate_deviation(self.u_list)
        self.r = self.calculate_r(calculation_type, deviation, dev_coef_value, self.u_list)
        return self.calculate_apen(m=m)

    def get_average_rr(self, seq):
        return float(sum(seq)) / len(seq)


def makeReport(fileName="results/results.csv", filesList=None, apEnList=None, rList=None, nList=None, avg_rr_list=None,
               is_ap_en=True):
    if not filesList:
        print("Error in generating report")
    with open(fileName, "w") as f:
        if is_ap_en:
            type = 'Approximate Enthropy'
        else:
            type = 'Sample Enthropy'
        f.write(','.join(['File name', type, 'R', 'N', 'Average RR']) + '\n')
        for index, name in enumerate(filesList):
            res_list = ['"{}"'.format(name),
                        str(apEnList[index]),
                        str(rList[index]) if rList else '',
                        str(nList[index]) if nList else '',
                        str(avg_rr_list[index]) if avg_rr_list else '']
            f.write(','.join(res_list) + '\n')

if __name__ == "__main__":
    # 2. Fix m and r
    # TODO: compute r later as the value from the deviation
    m = 2  # m is 2 in our case
    r = 500  # r is now random, not sure which are real values

    apEn = ApEn(m=2)
    # 1. Read values: u(1), u(2),...,u(N)
    apEn.read_series("data/samp_en/ApEn_SampEn.txt", False, 0)
    apEn.calculate_deviation(apEn.u_list)
    apEn.r = 3
    res1 = apEn.calculate_apen(m=m)
    print("ApEn for data/samp_en/ApEn_SampEn.txt", res1)
# # test if there are multiple files
# series = ["data/sample.dat","data/sample.dat","data/sample.dat"]
# results = []
# for i in series:
# 	tmpApEn = ApEn(m=2)
# 	results.append(ApEn(m=2).prepare_calculate_apen(m=m,series=i))
#
# makeReport(filesList=series,apEnList=results)
