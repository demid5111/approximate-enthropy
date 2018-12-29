import os
import itertools

from PyQt5.QtCore import *


class AppTestingBed:
    def __init__(self, qtbot, window):
        self.qtbot = qtbot
        self.window = window

    def _click(self, what):
        self.qtbot.mouseClick(what, Qt.LeftButton)

    def press_windows_cb(self):
        self._click(self.window.table_widget.window_cb)

    def press_apen_cb(self):
        self._click(self.window.table_widget.ent_widget.ap_en_cb)

    def press_sampen_cb(self):
        self._click(self.window.table_widget.ent_widget.samp_en_cb)

    def press_samen_apen_cb(self):
        self._click(self.window.table_widget.is_use_ent_cb)

    def press_pertropy_cb(self):
        self._click(self.window.table_widget.is_use_pertropy_cb)

    def press_cordim_cb(self):
        self._click(self.window.table_widget.pertropy_widget.normalize_cb)

    def press_norm_permen_cb(self):
        self._click(self.window.table_widget.is_use_cor_dim_cb)

    def press_fracdim_cb(self):
        self._click(self.window.table_widget.is_use_frac_dim_cb)

    def press_calculate_btn(self):
        self._click(self.window.table_widget.run_calculate)

    def calculate_btn_state(self):
        return self.window.table_widget.run_calculate.isEnabled()

    def get_file_chooser(self):
        return self.window.table_widget.file_chooser_widget

    def choose_any_file(self):
        self.choose_file(os.path.join('data', 'ApEn_1.txt'))

    def choose_zero_deviation_file(self):
        self.choose_file(os.path.join('data', 'ApEn_0.txt'))

    def choose_file(self, relative_path):
        cur_path = os.path.realpath(__file__)
        path_to_root = os.path.abspath(os.path.join(cur_path, os.pardir, os.pardir, os.pardir))
        path_to_file = os.path.join(path_to_root, relative_path)
        self.get_file_chooser().file_names_edit.setText(path_to_file)
        self.window.table_widget.on_new_files_chosen()

    def wait_until_calculation_is_done(self):
        with self.qtbot.waitSignal(self.window.table_widget.calc_thread.done, timeout=10000):
            print('Done calculating')

    def check_modal_not_error(self) -> str:
        raise NotImplementedError


class SampleEnTestingBed(AppTestingBed):
    def check_modal_not_error(self):
        text = self.window.table_widget.dialog.text()
        assert 'SampEn calculated for' in text
        assert 'Saved report in' in text
        return text.split('Saved report in')[1].strip()


class ApEnTestingBed(AppTestingBed):
    def check_modal_not_error(self):
        text = self.window.table_widget.dialog.text()
        assert 'ApEn calculated for' in text
        assert 'Saved report in' in text
        return text.split('Saved report in')[1].strip()


class ComboApEnSampEnTestingBed(AppTestingBed):
    def check_modal_not_error(self):
        text = self.window.table_widget.dialog.text()
        assert 'ApEn,SampEn calculated for' in text or 'SampEn,ApEn calculated for' in text
        assert 'Saved report in' in text
        return text.split('Saved report in')[1].strip()


class ComboApEnSampEnPermEnTestingBed(AppTestingBed):
    def check_modal_not_error(self):
        text = self.window.table_widget.dialog.text()
        combos = list(itertools.permutations(['ApEn', 'SampEn', 'PermEn']))
        existed = ['{} calculated for'.format(','.join(sub)) in text for sub in combos]
        assert any(existed)
        assert 'Saved report in' in text
        return text.split('Saved report in')[1].strip()


class PermEnTestingBed(AppTestingBed):
    def check_modal_not_error(self):
        text = self.window.table_widget.dialog.text()
        assert 'PermEn calculated for' in text
        assert 'Saved report in' in text
        return text.split('Saved report in')[1].strip()
