import numpy as np
import pytest

from server.core.calibration import parse_umik_calibration

SAMPLE_FILE = '''"Sens Factor =-1.7240dB, SERNO: 8100123"
"AGain=-9.0dB"
20.000	-0.45
21.500	-0.43
1000.0	0.00
20000.0	-2.10
'''

SAMPLE_NO_AGAIN = '''"Sens Factor =-2.5dB, SERNO: 8100456"
20.0   -0.5
1000.0  0.1
20000.0 -3.0
'''

SAMPLE_WITH_PHASE = '''"Sens Factor =-1.0dB, SERNO: 8100789"
20.0   -0.5  -1.2
100.0   0.0  -0.1
'''


def test_parse_full_file():
    cal = parse_umik_calibration(SAMPLE_FILE)
    assert cal.serial == "8100123"
    assert cal.sens_factor_db == pytest.approx(-1.7240)
    assert cal.again_db == pytest.approx(-9.0)
    assert len(cal.freq_hz) == 4
    np.testing.assert_array_equal(cal.freq_hz, [20.0, 21.5, 1000.0, 20000.0])
    np.testing.assert_array_equal(cal.gain_db, [-0.45, -0.43, 0.0, -2.10])


def test_parse_without_again():
    cal = parse_umik_calibration(SAMPLE_NO_AGAIN)
    assert cal.serial == "8100456"
    assert cal.sens_factor_db == pytest.approx(-2.5)
    assert cal.again_db is None
    assert len(cal.freq_hz) == 3


def test_parse_with_phase_column_ignores_phase():
    cal = parse_umik_calibration(SAMPLE_WITH_PHASE)
    assert len(cal.freq_hz) == 2
    np.testing.assert_array_equal(cal.gain_db, [-0.5, 0.0])


def test_parse_empty_raises():
    with pytest.raises(ValueError, match="no frequency"):
        parse_umik_calibration("")


def test_parse_only_header_raises():
    with pytest.raises(ValueError):
        parse_umik_calibration('"Sens Factor =-1.0dB, SERNO: 8100000"')


def test_parse_skips_comment_lines():
    text = '''"Sens Factor =-1.0dB, SERNO: 8100000"
* this is a comment
* another comment
20.0  -0.5
'''
    cal = parse_umik_calibration(text)
    assert len(cal.freq_hz) == 1
