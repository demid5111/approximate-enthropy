class LSM:
    """
    LSM implements Line of Best Fit (Least Square Method)
    Link: https://www.varsitytutors.com/hotmath/hotmath_help/topics/line-of-best-fit
    """

    @staticmethod
    def get_slope(pairs_list, mean_x, mean_y):
        x_diffs = []
        acc = 0
        for (x, y) in pairs_list:
            acc += (x - mean_x) * (y - mean_y)
            x_diffs.append((x - mean_x) ** 2)
        return acc / sum(x_diffs)

    @staticmethod
    def get_y_intercept(mean_x, mean_y, slope):
        return mean_y - slope * mean_x

    @staticmethod
    def calculate(pairs_list):
        # mean_x = sum([i for (i,j) in pairs_list])/len(pairs_list)
        # mean_y = sum([j for (i,j) in pairs_list])/len(pairs_list)
        # slope = LSM.get_slope(pairs_list, mean_x, mean_y)
        # y_intercept = LSM.get_y_intercept(mean_x, mean_y, slope)
        # return slope, y_intercept
        sum_x = sum(map(lambda x: x[0], pairs_list))
        sum_squares_x = sum(map(lambda x: x[0] ** 2, pairs_list))
        sum_y = sum(map(lambda x: x[1], pairs_list))
        sum_multiplies = sum(map(lambda x: x[0] * x[1], pairs_list))
        n = len(pairs_list)
        nom = n * sum_multiplies - sum_x * sum_y
        denom = n * sum_squares_x - sum_x ** 2
        return nom / denom


if __name__ == "__main__":
    l = [(8, 3), (2, 10), (11, 3), (6, 6), (5, 8), (4, 12), (12, 1), (9, 4), (6, 9), (1, 14)]
    slope, intercept = LSM.calculate(l)
    print(slope)
    print(intercept)
