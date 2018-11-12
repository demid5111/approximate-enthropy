from gui_version import App

from tests.gui.app_testing_bed import ComboApEnSampEnPermEnTestingBed
from tests.gui.common import check_report


def test_combo_apen_sampen_permen_wo_windows(qtbot):
    window = App()
    qtbot.addWidget(window)

    test_app = ComboApEnSampEnPermEnTestingBed(qtbot=qtbot, window=window)

    qtbot.waitForWindowShown(window)

    test_app.press_windows_cb()
    test_app.press_cordim_cb()
    test_app.press_fracdim_cb()

    assert not test_app.calculate_btn_state()
    test_app.choose_any_file()

    assert test_app.calculate_btn_state()
    test_app.press_calculate_btn()

    test_app.wait_until_calculation_is_done()
    path = test_app.check_modal_not_error()
    check_report(path)
    # qtbot.stopForInteraction()


def test_combo_apen_sampen_permen_w_windows(qtbot):
    window = App()
    qtbot.addWidget(window)

    test_app = ComboApEnSampEnPermEnTestingBed(qtbot=qtbot, window=window)

    qtbot.waitForWindowShown(window)

    test_app.press_cordim_cb()
    test_app.press_fracdim_cb()

    assert not test_app.calculate_btn_state()
    test_app.choose_any_file()

    assert test_app.calculate_btn_state()
    test_app.press_calculate_btn()

    test_app.wait_until_calculation_is_done()
    path = test_app.check_modal_not_error()
    check_report(path)
