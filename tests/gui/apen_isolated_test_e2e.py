from gui_version import App

from tests.gui.app_testing_bed import ApEnTestingBed
from tests.gui.common import check_report


def test_apen_wo_windows(qtbot):
    window = App()
    qtbot.addWidget(window)

    test_app = ApEnTestingBed(qtbot=qtbot, window=window)

    qtbot.waitForWindowShown(window)

    test_app.press_windows_cb()
    test_app.press_sampen_cb()
    test_app.press_pertropy_cb()
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


def test_apen_w_windows(qtbot):
    window = App()
    qtbot.addWidget(window)

    test_app = ApEnTestingBed(qtbot=qtbot, window=window)

    qtbot.waitForWindowShown(window)

    test_app.press_sampen_cb()
    test_app.press_pertropy_cb()
    test_app.press_cordim_cb()
    test_app.press_fracdim_cb()

    assert not test_app.calculate_btn_state()
    test_app.choose_any_file()

    assert test_app.calculate_btn_state()
    test_app.press_calculate_btn()

    test_app.wait_until_calculation_is_done()
    path = test_app.check_modal_not_error()
    check_report(path)


def test_apen_w_windows_ideal_seq(qtbot):
    """
    Known issue was that for the ideal sequence there was 0 deviation resulting
    in error propagation.
    """
    window = App()
    qtbot.addWidget(window)

    test_app = ApEnTestingBed(qtbot=qtbot, window=window)

    qtbot.waitForWindowShown(window)

    test_app.press_sampen_cb()
    test_app.press_pertropy_cb()
    test_app.press_cordim_cb()
    test_app.press_fracdim_cb()

    assert not test_app.calculate_btn_state()
    test_app.choose_zero_deviation_file()

    assert test_app.calculate_btn_state()
    test_app.press_calculate_btn()

    test_app.wait_until_calculation_is_done()
    path = test_app.check_modal_not_error()
    check_report(path)


def test_apen_wo_windows_resetting_state(qtbot):
    """
    Known issue was that for the steps:
        1. deselect all items except ApEn/SampEn
        2. deselect ApEn (leave only SampEn)
        3. change threshold value
        4. press calculate - we get only SampEn calculated
        5. deselect ApEn/SampEn entropy completely
        6. select it again
        7. everything should be selected (that was the issue - checkboxes
            did not represent the actual state)
        8. press calculate - we get both ApEn/SampEn calculated
    """
    window = App()
    qtbot.addWidget(window)

    test_app = ApEnTestingBed(qtbot=qtbot, window=window)

    qtbot.waitForWindowShown(window)

    # disable windows and others
    test_app.press_windows_cb()
    test_app.press_pertropy_cb()
    test_app.press_cordim_cb()
    test_app.press_fracdim_cb()

    # disable ApEn
    test_app.press_apen_cb()

    test_app.enter_new_threshold('20')
    test_app.press_threshold_cb()

    assert not test_app.calculate_btn_state()
    test_app.choose_zero_deviation_file()

    assert test_app.calculate_btn_state()
    test_app.press_calculate_btn()

    test_app.wait_until_calculation_is_done()
    path = test_app.check_modal_not_error()
    check_report(path)

    test_app.close_calculation_dialog()
    test_app.press_common_sampen_apen_cb()
    test_app.press_common_sampen_apen_cb()
    assert test_app.is_apen_selected()
    assert test_app.is_sampen_selected()
    assert test_app.is_threshold_selected()
    assert test_app.is_threshold_text('300')
