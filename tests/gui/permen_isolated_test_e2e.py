from gui_version import App

from tests.gui.app_testing_bed import PermEnTestingBed
from tests.gui.common import check_report


def test_permen_wo_windows(qtbot):
    window = App()
    qtbot.addWidget(window)

    test_app = PermEnTestingBed(qtbot=qtbot, window=window)

    qtbot.waitForWindowShown(window)

    test_app.press_windows_cb()
    test_app.press_samen_apen_cb()
    test_app.press_cordim_cb()
    test_app.press_fracdim_cb()

    assert not test_app.calculate_btn_state()
    test_app.choose_any_file()

    assert test_app.calculate_btn_state()
    test_app.press_calculate_btn()

    test_app.wait_until_calculation_is_done()
    path = test_app.check_modal_not_error()
    check_report(path)


def test_permen_wo_windows_wo_norm(qtbot):
    window = App()
    qtbot.addWidget(window)

    test_app = PermEnTestingBed(qtbot=qtbot, window=window)

    qtbot.waitForWindowShown(window)

    test_app.press_windows_cb()
    test_app.press_samen_apen_cb()
    test_app.press_cordim_cb()
    test_app.press_norm_permen_cb()
    test_app.press_fracdim_cb()

    assert not test_app.calculate_btn_state()
    test_app.choose_any_file()

    assert test_app.calculate_btn_state()
    test_app.press_calculate_btn()

    test_app.wait_until_calculation_is_done()
    path = test_app.check_modal_not_error()
    check_report(path)


def test_permen_wo_windows_wo_norm_w_strides(qtbot):
    window = App()
    qtbot.addWidget(window)

    test_app = PermEnTestingBed(qtbot=qtbot, window=window)

    qtbot.waitForWindowShown(window)

    test_app.press_windows_cb()
    test_app.press_samen_apen_cb()
    test_app.press_cordim_cb()
    test_app.press_norm_permen_cb()
    test_app.press_strides_permen_cb()
    test_app.set_strides_permen('2')
    test_app.press_fracdim_cb()

    assert not test_app.calculate_btn_state()
    test_app.choose_any_file()

    assert test_app.calculate_btn_state()
    test_app.press_calculate_btn()

    test_app.wait_until_calculation_is_done()
    path = test_app.check_modal_not_error()
    check_report(path)


def test_permen_w_windows(qtbot):
    window = App()
    qtbot.addWidget(window)

    test_app = PermEnTestingBed(qtbot=qtbot, window=window)

    qtbot.waitForWindowShown(window)

    test_app.press_samen_apen_cb()
    test_app.press_cordim_cb()
    test_app.press_fracdim_cb()

    assert not test_app.calculate_btn_state()
    test_app.choose_any_file()

    assert test_app.calculate_btn_state()
    test_app.press_calculate_btn()

    test_app.wait_until_calculation_is_done()
    path = test_app.check_modal_not_error()
    check_report(path)
