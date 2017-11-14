from math import floor

from src.core.apen import ApEn


class DimUtils:
    @staticmethod
    def prepare_windows(file_name, window_size, step_size):
        # 1. read the file
        u_list = ApEn.read_series(file_name, use_threshold=False, threshold_value=0)
        if not window_size:
            window_size = len(u_list)
            step_size = 1
        assert window_size <= len(u_list), "Window size can't be bigger than the size of the overall sequence"

        seq_list = []
        for current_step in range(floor((len(u_list) - window_size) / step_size) + 1):
            next_max = current_step * step_size + window_size
            if next_max > len(u_list):
                break
            new_seq = u_list[current_step * step_size:next_max]
            seq_list.append(new_seq)

        return seq_list, window_size, step_size