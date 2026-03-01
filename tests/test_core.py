import pytest
import math

from solo_pm_tdd_lab.core import clamp, zscore

NAN = float("nan")

def test_clamp_inside_range():
    assert clamp(5, 0, 10) == 5

def test_clamp_below_range():
    assert clamp(-1, 0, 10) == 0

def test_clamp_above_range():
    assert clamp(11, 0, 10) == 10

def test_clamp_invalid_bounds():
    with pytest.raises(ValueError):
        clamp(5, 10, 0)


def assert_list_close_with_nans(got, expected, *, rel=1e-12, abs=0.0):
    assert isinstance(got, list)
    assert len(got) == len(expected)
    for g, e in zip(got, expected):
        if math.isnan(e):
            assert math.isnan(g)
        else:
            assert g == pytest.approx(e, rel=rel, abs=abs)


def test_basic_no_nan_ddof0():
    x = [1.0, 2.0, 3.0]
    # mean=2, std=sqrt(2/3)
    expected = [-1.224744871391589, 0.0, 1.224744871391589]
    out = zscore(x, ddof=0, nan_policy="omit")
    assert_list_close_with_nans(out, expected)

def test_ddof1_changes_result():
    x = [1.0, 2.0, 3.0]
    # sample std (ddof=1) = 1
    expected = [-1.0, 0.0, 1.0]
    out = zscore(x, ddof=1, nan_policy="omit")
    assert_list_close_with_nans(out, expected)

def test_omit_nan_keeps_nan_positions():
    x = [1.0, NAN, 3.0]
    # mean over non-nan = 2, std over non-nan (ddof=0) = 1
    expected = [-1.0, NAN, 1.0]
    out = zscore(x, nan_policy="omit", ddof=0)
    assert_list_close_with_nans(out, expected)

def test_propagate_nan_all_nan():
    x = [1.0, NAN, 3.0]
    out = zscore(x, nan_policy="propagate")
    assert all(math.isnan(v) for v in out)

def test_raise_nan_throws():
    x = [1.0, NAN, 3.0]
    with pytest.raises(ValueError):
        zscore(x, nan_policy="raise")

def test_all_nan_returns_all_nan():
    x = [NAN, NAN]
    out = zscore(x, nan_policy="omit")
    assert all(math.isnan(v) for v in out)

def test_constant_returns_zeros_for_non_nan():
    x = [5.0, 5.0, 5.0]
    out = zscore(x, nan_policy="omit")
    assert_list_close_with_nans(out, [0.0, 0.0, 0.0])

def test_constant_with_nan_omit_returns_zero_and_nan():
    x = [5.0, NAN, 5.0]
    out = zscore(x, nan_policy="omit")
    assert_list_close_with_nans(out, [0.0, NAN, 0.0])

def test_singleton_ddof0_zero():
    x = [7.0]
    out = zscore(x, ddof=0, nan_policy="omit")
    assert_list_close_with_nans(out, [0.0])

def test_singleton_ddof1_undefined_returns_nan():
    x = [7.0]
    out = zscore(x, ddof=1, nan_policy="omit")
    assert_list_close_with_nans(out, [NAN])

def test_empty_returns_empty():
    out = zscore([], nan_policy="omit")
    assert out == []

def test_int_input_outputs_float_list():
    out = zscore([1, 2, 3])
    assert all(isinstance(v, float) for v in out)

def test_invalid_nan_policy_raises():
    with pytest.raises(ValueError):
        zscore([1.0, 2.0], nan_policy="banana")

def test_negative_ddof_raises():
    with pytest.raises(ValueError):
        zscore([1.0, 2.0], ddof=-1)

def test_ddof_too_large_returns_nan_for_non_nan():
    # n=2, ddof=2 => denom = 0 => undefined -> NaNs
    out = zscore([1.0, 2.0], ddof=2, nan_policy="omit")
    assert all(math.isnan(v) for v in out)

def test_accepts_iterables_like_tuples_and_generators():
    out1 = zscore((1.0, 2.0, 3.0))
    out2 = zscore((v for v in [1.0, 2.0, 3.0]))
    expected = [-1.224744871391589, 0.0, 1.224744871391589]
    assert_list_close_with_nans(out1, expected)
    assert_list_close_with_nans(out2, expected)
