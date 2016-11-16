from math import log

from apen import ApEn
from supporting import CalculationType

__author__ = 'demidovs'


class SampEn(ApEn):

    def calculate_c(self, m):
        self.c_list = []
        assert self.r >= 0, "Filtering threshold should be positive"
        similar_vectors = 0
        for i in range(0, self.N - m + 1):
            for j in range(0, self.N - m + 1):
                res = self.calculate_distance(self.x_list[i], self.x_list[j])
                if (res < self.r):
                    similar_vectors += 1
        return similar_vectors

    def _final(self, m):
        return sum([log(self.c_list[i]) for i in range(self.N - m + 1)]) \
               * ((self.N - m + 1) ** (-1))

    def calculate_final(self, m):

        # 3. Form a sequence of vectors so that
        # x[i] = [u[i],u[i+1],...,u[i+m-1]]
        # i ~ 0:N-m because indexes start from 0
        self.create_vectors(m=m)

        # 4. Construct the C(i,m) - portion of vectors "similar" to i-th
        # similarity - d[x(j),x(i)], where d = max(a)|u(a)-u*(a)|
        # this is just the respective values subtraction
        return self.calculate_c(m=m)

    def calculate_sampen(self, m):
        return -log(self.calculate_final(m+1)/self.calculate_final(m))

if __name__ == "__main__":
    # 2. Fix m and r
    # TODO: compute r later as the value from the deviation
    m = 2  # m is 2 in our case
    r = 500  # r is now random, not sure which are real values

    apEn = SampEn(m=2)
    # 1. Read values: u(1), u(2),...,u(N)
    apEn.read_series("data/data1.txt", False, 0)
    apEn.calculate_deviation(apEn.u_list)
    apEn.r = 3
    res1 = apEn.calculate_sampen(m=m)
    print(res1)
# # test if there are multiple files
# series = ["data/sample.dat","data/sample.dat","data/sample.dat"]
# results = []
# for i in series:
# 	tmpApEn = ApEn(m=2)
# 	results.append(ApEn(m=2).prepare_calculate_apen(m=m,series=i))
#
# makeReport(filesList=series,apEnList=results)
