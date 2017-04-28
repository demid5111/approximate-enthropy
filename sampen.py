from math import log

from apen import ApEn

__author__ = 'demidovs'


class SampEn(ApEn):
    def calculate_c(self, m):
        self.c_list = []
        assert self.r >= 0, "Filtering threshold should be positive"
        similar_vectors = 0
        for i in range(0, self.N - m + 1):
            for j in range(0, self.N - m + 1):
                res = self.calculate_distance(self.x_list[i], self.x_list[j])
                if res < self.r:
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
        for_m = self.calculate_final(m)
        if not for_m:
            return 0
        for_m_next = self.calculate_final(m+1)
        if not for_m_next:
            return 0
        else:
            return -log(self.calculate_final(m+1)/self.calculate_final(m))

    def prepare_calculate_sampen(self, m, series, calculation_type, dev_coef_value, use_threshold, threshold_value):
        self.read_series(series, use_threshold, threshold_value)
        deviation = self.calculate_deviation(self.u_list)
        self.r = self.calculate_r(calculation_type, deviation, dev_coef_value, self.u_list)
        return self.calculate_sampen(m=m)

if __name__ == "__main__":
    # 2. Fix m and r
    # TODO: compute r later as the value from the deviation
    m = 2  # m is 2 in our case
    r = 500  # r is now random, not sure which are real values

    apEn = SampEn(m=2)
    # 1. Read values: u(1), u(2),...,u(N)
    apEn.read_series("data/samp_en/0.txt", False, 0)
    apEn.calculate_deviation(apEn.u_list)
    apEn.r = 3
    res1 = apEn.calculate_sampen(m=m)
    print("data/samp_en/0.txt",res1)
