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

    def press_common_sampen_apen_cb(self):
        self._click(self.window.table_widget.is_use_ent_cb)

    def press_apen_cb(self):
        self._click(self.window.table_widget.ent_widget.ap_en_cb)

    def press_sampen_cb(self):
        self._click(self.window.table_widget.ent_widget.samp_en_cb)

    def press_samen_apen_cb(self):
        self._click(self.window.table_widget.is_use_ent_cb)

    def press_pertropy_cb(self):
        self._click(self.window.table_widget.is_use_pertropy_cb)

    def press_cordim_cb(self):
        self._click(self.window.table_widget.is_use_cor_dim_cb)

    def press_norm_permen_cb(self):
        self._click(self.window.table_widget.pertropy_widget.normalize_cb)

    def press_strides_permen_cb(self):
        self._click(self.window.table_widget.pertropy_widget.strides_cb)

    def set_strides_permen(self, val):
        self.window.table_widget.pertropy_widget.stride_value.setText(val)

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

    def enter_new_threshold(self, text):
        self.window.table_widget.ent_widget.r_threshold.setText(text)

    def press_threshold_cb(self):
        self._click(self.window.table_widget.ent_widget.threshold_cb)
    
    def check_custom_modal_not_error(self, options):
        text = self.window.table_widget.dialog.text()
        to_check = list(itertools.permutations(options))
        res_check = ['{} calculated for'.format(','.join(i)) in text for i in to_check]
        assert any(res_check)
        assert 'Saved report in' in text
        return text.split('Saved report in')[1].strip()

    def close_calculation_dialog(self):
        self._click(self.window.table_widget.ok_button)
    
    def is_apen_selected(self):
        return self.window.table_widget.ent_widget.ap_en_cb.isChecked()
    
    def is_sampen_selected(self):
        return self.window.table_widget.ent_widget.samp_en_cb.isChecked()
    
    def is_threshold_selected(self):
        cb = self.window.table_widget.ent_widget.threshold_cb
        return cb.isChecked() and cb.isEnabled()
    
    def is_threshold_text(self, text):
        return self.window.table_widget.ent_widget.r_threshold.text() == text
    


class SampleEnTestingBed(AppTestingBed):
    def check_modal_not_error(self):
        return self.check_custom_modal_not_error(['SampEn'])


class ApEnTestingBed(AppTestingBed):
    def check_modal_not_error(self):
        return self.check_custom_modal_not_error(['ApEn'])


class ComboApEnSampEnTestingBed(AppTestingBed):
    def check_modal_not_error(self):
        return self.check_custom_modal_not_error(['ApEn', 'SampEn'])


class ComboApEnSampEnPermEnTestingBed(AppTestingBed):
    def check_modal_not_error(self):
        return self.check_custom_modal_not_error(['ApEn', 'SampEn', 'PermEn'])


class PermEnTestingBed(AppTestingBed):
    def check_modal_not_error(self):
        return self.check_custom_modal_not_error(['PermEn'])
