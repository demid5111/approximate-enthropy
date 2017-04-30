from math import log

from apen import ApEn

__author__ = 'demidovs'


class SampEn(ApEn):
    def calculate_c(self, m, seq, r, n):
        assert r >= 0, "Filtering threshold should be positive"
        similar_vectors = 0
        for i in range(0, n - m + 1):
            for j in range(0, n - m + 1):
                if r > self.calculate_distance(seq[i], seq[j]):
                    similar_vectors += 1
        return similar_vectors

    def calculate_final(self, m, seq, r):
        # 3. Form a sequence of vectors so that
        # x[i] = [u[i],u[i+1],...,u[i+m-1]]
        # i ~ 0:N-m because indexes start from 0
        x_list = self.slice_intervals(m=m, seq=seq)

        # 4. Construct the C(i,m) - portion of vectors "similar" to i-th
        # similarity - d[x(j),x(i)], where d = max(a)|u(a)-u*(a)|
        # this is just the respective values subtraction
        return self.calculate_c(m=m, seq=x_list, r=r, n=len(seq))

    def calculate_sampen(self, m, seq, r):
        assert m > 1, 'm value should be meaningful (> 1)'
        for_m = self.calculate_final(m, seq=seq, r=r)
        if not for_m:
            return 0
        for_m_next = self.calculate_final(m+1, seq=seq, r=r)
        if not for_m_next:
            return 0
        return -log(for_m_next/for_m)

    def prepare_calculate_sampen(self, m, series, calculation_type, dev_coef_value, use_threshold, threshold_value):
        u_list = self.read_series(series, use_threshold, threshold_value)
        deviation = self.calculate_deviation(u_list)
        r_val = self.calculate_r(calculation_type, deviation, dev_coef_value, u_list)
        return {
            'result': self.calculate_sampen(m=m, seq=u_list, r=r_val),
            'average_rr': self.get_average_rr(seq=u_list),
            'r': r_val,
            'n': len(u_list)
        }

if __name__ == "__main__":
    m = 2  # m is 2 in our case
    r = 500  # r is now random, not sure which are real values

    apEn = SampEn()
    # 1. Read values: u(1), u(2),...,u(N)
    u_list = apEn.read_series("data/samp_en/0.txt", False, 0)
    dev = apEn.calculate_deviation(u_list)
    apEn.r = 3
    res1 = apEn.calculate_sampen(m=m, r=r, seq=u_list)
    print("data/samp_en/0.txt",res1)
