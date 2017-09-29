__author__ = 'demidovs'


class IReport:
    def set_window_size(self, w):
        self.window_size = w

    def set_step_size(self, s):
        self.step_size = s

    def set_result_values(self, s):
        self.result_values = s

    def set_dimension(self, d):
        self.dimension = d

    def set_error(self, msg):
        self.err_msg = msg


class ApEnReport(IReport):
    def set_r_values(self, r_list):
        self.r_values = r_list

    def set_avg_rr(self, rr_list):
        self.avg_rr_values = rr_list

    def get_prefix(self):
        return 'ap_en'


class SampEnReport(IReport):
    def set_r_values(self, r_list):
        self.r_values = r_list

    def set_avg_rr(self, rr_list):
        self.avg_rr_values = rr_list

    def get_prefix(self):
        return 'samp_en'


class CorDimReport(IReport):
    def set_radius(self, r):
        self.r = r

    def get_radius(self):
        return self.r

    def get_prefix(self):
        return 'cor_dim'
