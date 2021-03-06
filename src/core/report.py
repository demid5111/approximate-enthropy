import csv
import json
import os

from src.utils.supporting import AnalysisType, ARTIFACTS_DIR

__author__ = 'demidovs'


class IReport:
    def __init__(self):
        self.err_msg = None
        self.prefix = ''
        self.dimension = 'N/A'

    def set_window_size(self, w):
        self.window_size = w

    def get_window_size(self):
        return self.window_size

    def set_step_size(self, s):
        self.step_size = s

    def get_step_size(self):
        return self.step_size

    def set_result_values(self, s):
        self.result_values = s

    def get_result_values(self):
        return self.result_values

    def get_result_value(self, idx):
        return self.result_values[idx]

    def get_len_results(self):
        return len(self.result_values)

    def set_dimension(self, d):
        self.dimension = d

    def get_dimension(self):
        return self.dimension

    def set_file_name(self, f):
        self.file_name = f

    def get_file_name(self):
        return self.file_name

    def get_seq_len(self):
        return self.seq_len

    def set_seq_len(self, new_len):
        self.seq_len = new_len

    def set_error(self, msg):
        self.err_msg = msg

    def is_error(self):
        return bool(self.err_msg)

    def to_json(self):
        return {
            'file_name': self.get_file_name(),
            'dimension': self.get_dimension(),
            'window_step': self.get_step_size(),
            'window_size': self.get_window_size(),
            'result_values': self.get_result_values()
        }

    def __str__(self):
        return json.dumps(self.to_json())


class EnReport(IReport):
    def set_r_values(self, r_list):
        self.r_values = r_list

    def get_r_value(self, idx):
        return self.r_values[idx]

    def get_r_values(self):
        return self.r_values

    def set_avg_rr(self, rr_list):
        self.avg_rr_values = rr_list

    def get_avg_rr_value(self, idx):
        return self.avg_rr_values[idx]

    def get_avg_rr_values(self):
        return self.avg_rr_values

    def get_report_list_per_window(self, window_idx):
        if self.is_error():
            return ['error', ] * 3
        result = str('{0:.10f}'.format(self.get_result_value(window_idx)))
        r = self.get_r_value(window_idx)
        rr = self.get_avg_rr_value(window_idx)
        return [str(result), str(r), str(rr)]

    def to_json(self):
        if self.is_error():
            return {'error': 'true'}
        res_dic = super().to_json()
        res_dic['r_values'] = self.get_r_values()
        res_dic['avg_rr_values'] = self.get_avg_rr_values()
        return res_dic


class ApEnReport(EnReport):
    prefix = 'ap_en'

    @classmethod
    def get_prefix(cls):
        return cls.prefix


class SampEnReport(EnReport):
    prefix = 'samp_en'

    @classmethod
    def get_prefix(cls):
        return cls.prefix


class CorDimReport(IReport):
    prefix = 'cor_dim'

    @classmethod
    def get_prefix(cls):
        return cls.prefix

    def set_radius(self, r):
        self.r = r

    def get_radius(self):
        return self.r

    def get_report_list_per_window(self, window_idx):
        if self.is_error():
            return ['error', ] * 2
        result = str('{0:.10f}'.format(self.get_result_value(window_idx)))
        radius = self.get_radius()
        return [str(result), str(radius)]

    def to_json(self):
        if self.is_error():
            return {'error': 'true'}
        res_dic = super().to_json()
        res_dic['radius'] = self.get_radius()
        return res_dic


class FracDimReport(IReport):
    prefix = 'frac_dim'

    @classmethod
    def get_prefix(cls):
        return cls.prefix

    def set_max_k(self, k):
        self.max_k = k

    def get_max_k(self):
        return self.max_k

    def get_report_list_per_window(self, window_idx):
        if self.is_error():
            return ['error', ] * 2
        result = str('{0:.10f}'.format(self.get_result_value(window_idx)))
        max_k = self.get_max_k()
        return [str(result), str(max_k)]

    def to_json(self):
        if self.is_error():
            return {'error': 'true'}
        res_dic = super().to_json()
        res_dic['max_k'] = self.get_max_k()
        return res_dic


class PermutationEntropyReport(IReport):
    prefix = 'per_en'

    def __init__(self):
        super().__init__()
        self.avg_rr_values = []
        self.normalized_values = []
        self.stride = None

    def set_avg_rr(self, rr_list):
        self.avg_rr_values = rr_list

    def get_avg_rr_values(self):
        return self.avg_rr_values

    def set_stride_value(self, val):
        self.stride = val

    def get_stride_value(self):
        return self.stride

    @classmethod
    def get_prefix(cls):
        return cls.prefix

    def get_avg_rr_value(self, idx):
        return self.avg_rr_values[idx]

    def get_normalized_result_value(self, idx):
        return self.normalized_values[idx]

    def get_report_list_per_window(self, window_idx):
        if self.is_error():
            return ['error', ] * 2
        result = str('{0:.10f}'.format(self.get_result_value(window_idx)))
        try:
            normalized_result = str('{0:.10f}'.format(self.get_normalized_result_value(window_idx)))
        except IndexError:
            normalized_result = -1
        rr = self.get_avg_rr_value(window_idx)
        return [str(result), str(normalized_result), str(rr), str(self.get_stride_value())]

    def set_normalized_values(self, values):
        self.normalized_values = values

    def get_normalized_values(self):
        return self.normalized_values

    def to_json(self):
        if self.is_error():
            return {'error': 'true'}
        res_dic = super().to_json()
        res_dic['avg_rr_values'] = self.get_avg_rr_values()
        res_dic['normalized_values'] = self.get_avg_rr_values()
        res_dic['stride'] = self.get_stride_value()
        return res_dic


class ReportManager:
    report_path = None

    @classmethod
    def get_report_path(cls):
        return cls.report_path

    @classmethod
    def prepare_write_report(cls, file_name="results/results.csv", res_dic=None, analysis_types=()):
        if not res_dic:
            print("Error in generating report")

        header_lines = ReportManager.prepare_header(analysis_types, res_dic)

        analysis_lines = []
        for f_name, reports in res_dic.items():
            analysis_lines.extend(ReportManager.prepare_analysis_report_single_file(f_name, reports))
        os.makedirs(os.path.join(ARTIFACTS_DIR, os.path.dirname(file_name)), exist_ok=True)
        cls.report_path = os.path.join(ARTIFACTS_DIR, file_name)
        ReportManager.write_report(cls.report_path, header_lines, analysis_lines)

    @staticmethod
    def write_report(file_name="results/results.csv", header_lines=(), analysis_lines=()):
        print('Saving to {}'.format(file_name))
        with open(file_name, 'w') as resultFile:
            wr = csv.writer(resultFile, delimiter=',')
            wr.writerows(header_lines)
            wr.writerows(analysis_lines)

    @staticmethod
    def get_analysis_types(res_dic):
        any_file = list(res_dic.keys())[0]
        reports = res_dic[any_file]
        analysis_names = []
        for r in reports:
            if isinstance(r, CorDimReport):
                analysis_names.append(AnalysisType.COR_DIM)
            if isinstance(r, FracDimReport):
                analysis_names.append(AnalysisType.FRAC_DIM)
            if isinstance(r, ApEnReport):
                analysis_names.append(AnalysisType.AP_EN)
            if isinstance(r, SampEnReport):
                analysis_names.append(AnalysisType.SAMP_EN)
            if isinstance(r, PermutationEntropyReport):
                analysis_names.append(AnalysisType.PERM_EN)
        return analysis_names

    @staticmethod
    def compile_column_names(analysis_types):
        # need to prepare column names with prefixes of the particular type
        # mandatory columns
        column_names = ['File name', 'Window number']
        en_column_names = ['Entropy', 'R', 'Average_RR']
        if AnalysisType.AP_EN in analysis_types:
            ap_en_names = ['{}_{}'.format(ApEnReport.get_prefix(), n) for n in en_column_names]
            column_names.extend(ap_en_names)
        if AnalysisType.SAMP_EN in analysis_types:
            samp_en_names = ['{}_{}'.format(SampEnReport.get_prefix(), n) for n in en_column_names]
            column_names.extend(samp_en_names)
        if AnalysisType.COR_DIM in analysis_types:
            cor_dim_column_names = ['Result', 'Radius']
            cor_dim_names = ['{}_{}'.format(CorDimReport.get_prefix(), n) for n in cor_dim_column_names]
            column_names.extend(cor_dim_names)
        if AnalysisType.FRAC_DIM in analysis_types:
            frac_dim_column_names = ['Result', 'Max_K']
            frac_dim_names = ['{}_{}'.format(FracDimReport.get_prefix(), n) for n in frac_dim_column_names]
            column_names.extend(frac_dim_names)
        if AnalysisType.PERM_EN in analysis_types:
            perm_en_column_names = ['Entropy', 'Normalized_Entropy','Average_RR', 'Stride']
            perm_en_names = ['{}_{}'.format(PermutationEntropyReport.get_prefix(), n) for n in perm_en_column_names]
            column_names.extend(perm_en_names)
        return column_names

    @staticmethod
    def prepare_header(analysis_types, res_dic: dict):
        header_lines = [
            ['Analysis applied', *analysis_types],
        ]
        # get sample size of window and step
        any_file = list(res_dic.keys())[0]
        any_report = res_dic[any_file][0]
        try:
            dimension = any_report.get_dimension()
        except AttributeError:
            dimension = 'error'
        header_lines.append(['Dimension', dimension])

        any_report_per_file = [res_dic[i][0] for i in res_dic.keys()]
        try:
            min_length = min(map(lambda x: x.get_seq_len(), any_report_per_file))
        except AttributeError:
            min_length = 'error'
        header_lines.append(['Minimum number of points', min_length])

        try:
            max_length = max(map(lambda x: x.get_seq_len(), any_report_per_file))
        except AttributeError:
            max_length = 'error'
        header_lines.append(['Maximum number of points', max_length])

        try:
            window_size = any_report.get_window_size()
        except AttributeError:
            window_size = 'error'
        header_lines.append(['Window size', window_size if window_size else 'full sequence length'])

        try:
            step_size = any_report.get_step_size()
        except AttributeError:
            step_size = 'error'
        header_lines.append(['Step size', step_size])

        column_names = ReportManager.compile_column_names(analysis_types)
        header_lines.append(column_names)
        return header_lines

    @staticmethod
    def prepare_analysis_report_single_file(file_name, reports=()):
        analysis_lines = []
        # find not error-report
        len_res = 1  # if all reports are with errors, iterate at least once to write error messages to file
        for r in reports:
            try:
                len_res = r.get_len_results()
                break
            except AttributeError:
                continue

        for index in range(len_res):
            line_values = ['{}'.format(file_name), str(index)]
            ap_en_values = []
            samp_en_values = []
            cor_dim_values = []
            frac_dim_values = []
            perm_en_values = []
            for report in reports:
                if isinstance(report, ApEnReport):
                    ap_en_values = report.get_report_list_per_window(index)
                elif isinstance(report, SampEnReport):
                    samp_en_values = report.get_report_list_per_window(index)
                elif isinstance(report, CorDimReport):
                    cor_dim_values = report.get_report_list_per_window(index)
                elif isinstance(report, FracDimReport):
                    frac_dim_values = report.get_report_list_per_window(index)
                elif isinstance(report, PermutationEntropyReport):
                    perm_en_values = report.get_report_list_per_window(index)
            # the order is important
            # the biggest possible order
            # file_name, window_index,
            # ap_en_res, ap_en_r, ap_en_avg_rr,
            # samp_en_res, samp_en_r, samp_en_avg_rr,
            # cordim_res, cordim_radius,
            # fracdim_res, fracdim_start, fracdim_interval, fracdim_max_k, fracdim_max_m
            # perm_en_res, perm_en_normalized_res, perm_en_avg_rr, perm_en_stride
            line_values.extend(ap_en_values)
            line_values.extend(samp_en_values)
            line_values.extend(cor_dim_values)
            line_values.extend(frac_dim_values)
            line_values.extend(perm_en_values)
            analysis_lines.append(line_values)
        return analysis_lines
