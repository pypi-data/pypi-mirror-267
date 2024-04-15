"""
Unit tests for filters
"""

import os
import pickle

import numpy as np
from numpy.testing import assert_allclose, assert_equal, assert_raises

from signal_filters.filters import (
    band_pass_block,
    bandpass_block_filter,
    butterworth_filter,
    filter_signal,
    kaiser_bandpass_filter,
)

# set this flag true only in the first run to generate the data files
WRITE_DATA = False
ATOL = 1e-4


def make_signal_orig_and_noisy():
    """make a noisy test signal"""
    period_time = 10
    total_time = 1000
    f_sample = 10
    n_points = total_time * f_sample
    amplitude = 1.0
    ap = 0.5 * amplitude
    time = np.linspace(0, total_time, num=n_points, endpoint=False)

    y_original = amplitude * np.sin(2 * np.pi * time / period_time)
    np.random.seed(0)
    y_noise = np.random.normal(scale=ap, size=time.size)
    y_total = y_original + y_noise

    return time, y_original, y_total


def test_band_pass_block():
    """test the band pass block filter"""
    n_size = 20
    frequencies = np.linspace(0, 2.5, n_size, endpoint=False)

    result = band_pass_block(omega=frequencies, lowcut=0.1, highcut=0.2)

    result_expected = np.array(
        [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ]
    )

    assert_allclose(result, result_expected, atol=ATOL)


def test_kaiser_filter():
    time, y_orig, y_tot = make_signal_orig_and_noisy()

    f_s = 1 / (time[1] - time[0])

    y_filter = kaiser_bandpass_filter(
        y_tot, lowcut=0.05, highcut=0.15, fs=f_s, f_width_edge=0.1
    )

    data_file = "data/kaiser_filter_bp.pkl"
    if not os.path.exists(data_file):
        data_file = os.path.join("..", data_file)

    if WRITE_DATA:
        with open(data_file, "wb") as out_stream:
            pickle.dump(y_filter, out_stream, pickle.HIGHEST_PROTOCOL)

    with open(data_file, "rb") as in_stream:
        y_filter_expected = pickle.load(in_stream)

    assert_allclose(y_filter, y_filter_expected, atol=ATOL)

    # this is a front end to the kaiser filter, so_y_filter2 should be identical to
    # y_filter
    y_filter2 = filter_signal(
        y_tot,
        f_cut_low=0.05,
        f_cut_high=0.15,
        f_sampling=f_s,
        f_width_edge=0.1,
        filter_type="kaiser",
    )
    assert_equal(y_filter, y_filter2)


def test_block_filter():
    time, y_orig, y_tot = make_signal_orig_and_noisy()

    y_filter = bandpass_block_filter(
        time, y_tot, wfiltlo=2 * np.pi * 0.05, wfiltup=2 * np.pi * 0.15
    )

    data_file = "data/block_filter_bp.pkl"
    if not os.path.exists(data_file):
        data_file = os.path.join("..", data_file)

    if WRITE_DATA:
        with open(data_file, "wb") as out_stream:
            pickle.dump(y_filter, out_stream, pickle.HIGHEST_PROTOCOL)

    with open(data_file, "rb") as in_stream:
        y_filter_expected = pickle.load(in_stream)

    assert_allclose(y_filter, y_filter_expected, atol=ATOL)

    # this is a front end to the block filter, so_y_filter2 should be identical to
    # y_filter
    f_s = 1 / (time[1] - time[0])
    y_filter2 = filter_signal(y_tot, f_cut_low=0.05, f_cut_high=0.15, f_sampling=f_s)
    assert_equal(y_filter, y_filter2)


def test_butter_filter():
    time, y_orig, y_tot = make_signal_orig_and_noisy()

    f_s = 1 / (time[1] - time[0])

    y_filter = butterworth_filter(y_tot, f_cut_low=0.05, f_cut_high=0.15, fs=f_s,
                                  order=4)

    data_file = "data/butter_filter_bp.pkl"
    if not os.path.exists(data_file):
        data_file = os.path.join("..", data_file)

    if WRITE_DATA:
        with open(data_file, "wb") as out_stream:
            pickle.dump(y_filter, out_stream, pickle.HIGHEST_PROTOCOL)

    with open(data_file, "rb") as in_stream:
        y_filt_exp = pickle.load(in_stream)

    # check if we are up to the one digit equal to the input signal without noise
    assert_allclose(y_filter, y_filt_exp, atol=ATOL)

    # this is a front end to the butterworth filter, so_y_filter2 should be identical
    # to y_filter
    y_filter2 = filter_signal(
        y_tot,
        f_cut_low=0.05,
        f_cut_high=0.15,
        f_sampling=f_s,
        filter_type="butterworth",
        order=4,
    )
    assert_equal(y_filter, y_filter2)


def test_kaiser_filter_hp():
    time, y_orig, y_tot = make_signal_orig_and_noisy()

    f_s = 1 / (time[1] - time[0])

    y_filter = kaiser_bandpass_filter(y_tot, lowcut=0.05, fs=f_s, f_width_edge=0.1)

    data_file = "data/kaiser_filter_hp.pkl"
    if not os.path.exists(data_file):
        data_file = os.path.join("..", data_file)

    if WRITE_DATA:
        with open(data_file, "wb") as out_stream:
            pickle.dump(y_filter, out_stream, pickle.HIGHEST_PROTOCOL)

    with open(data_file, "rb") as in_stream:
        y_filt_exp = pickle.load(in_stream)

    assert_allclose(y_filter, y_filt_exp, atol=ATOL)

    # this is a front end to the kaiser filter, so_y_filter2 should be identical to
    # y_filter
    y_filter2 = filter_signal(
        y_tot, f_cut_low=0.05, f_sampling=f_s, f_width_edge=0.1, filter_type="kaiser"
    )
    assert_equal(y_filter, y_filter2)


def test_block_filter_hp():
    time, y_orig, y_tot = make_signal_orig_and_noisy()

    y_filter = bandpass_block_filter(time, y_tot, wfiltlo=2 * np.pi * 0.05)

    data_file = "data/block_filter_hp.pkl"
    if not os.path.exists(data_file):
        data_file = os.path.join("..", data_file)

    if WRITE_DATA:
        with open(data_file, "wb") as out_stream:
            pickle.dump(y_filter, out_stream, pickle.HIGHEST_PROTOCOL)

    with open(data_file, "rb") as in_stream:
        y_filt_exp = pickle.load(in_stream)

    assert_allclose(y_filter, y_filt_exp, atol=ATOL)

    # this is a front end to the block filter, so_y_filter2 should be identical to
    # y_filter
    f_s = 1 / (time[1] - time[0])
    y_filter2 = filter_signal(y_tot, f_cut_low=0.05, f_sampling=f_s)
    assert_equal(y_filter, y_filter2)


def test_butter_filter_hp():
    time, y_orig, y_tot = make_signal_orig_and_noisy()

    f_s = 1 / (time[1] - time[0])

    y_filter = butterworth_filter(y_tot, f_cut_low=0.05, fs=f_s, order=4)

    data_file = "data/butter_filter_hp.pkl"
    if not os.path.exists(data_file):
        data_file = os.path.join("..", data_file)

    if WRITE_DATA:
        with open(data_file, "wb") as out_stream:
            pickle.dump(y_filter, out_stream, pickle.HIGHEST_PROTOCOL)

    with open(data_file, "rb") as in_stream:
        y_filt_exp = pickle.load(in_stream)

    # check if we are up to the one digit equal to the input signal without noise
    assert_allclose(y_filter, y_filt_exp, atol=ATOL)

    # this is a front end to the butterworth filter, so_y_filter2 should be identical
    # to y_filter
    y_filter2 = filter_signal(
        y_tot, f_cut_low=0.05, f_sampling=f_s, filter_type="butterworth", order=4
    )
    assert_equal(y_filter, y_filter2)


def test_kaiser_filter_lp():
    time, y_orig, y_tot = make_signal_orig_and_noisy()

    f_s = 1 / (time[1] - time[0])

    y_filter = kaiser_bandpass_filter(y_tot, highcut=0.15, fs=f_s, f_width_edge=0.1)

    data_file = "data/kaiser_filter_lp.pkl"
    if not os.path.exists(data_file):
        data_file = os.path.join("..", data_file)

    if WRITE_DATA:
        with open(data_file, "wb") as out_stream:
            pickle.dump(y_filter, out_stream, pickle.HIGHEST_PROTOCOL)

    with open(data_file, "rb") as in_stream:
        y_filt_exp = pickle.load(in_stream)

    assert_allclose(y_filter, y_filt_exp, atol=ATOL)

    # this is a front end to the kaiser filter, so_y_filter2 should be identical to
    # y_filter
    y_filter2 = filter_signal(
        y_tot, f_cut_high=0.15, f_sampling=f_s, f_width_edge=0.1, filter_type="kaiser"
    )
    assert_equal(y_filter, y_filter2)


def test_block_filter_lp():
    time, y_orig, y_tot = make_signal_orig_and_noisy()

    y_filter = bandpass_block_filter(time, y_tot, wfiltup=2 * np.pi * 0.15)

    data_file = "data/block_filter_lp.pkl"
    if not os.path.exists(data_file):
        data_file = os.path.join("..", data_file)

    if WRITE_DATA:
        with open(data_file, "wb") as out_stream:
            pickle.dump(y_filter, out_stream, pickle.HIGHEST_PROTOCOL)

    with open(data_file, "rb") as in_stream:
        y_filter_expected = pickle.load(in_stream)

    assert_allclose(y_filter, y_filter_expected, atol=ATOL)

    # this is a front end to the block filter, so_y_filter2 should be identical to
    # y_filter
    sampling_frequency = 1 / (time[1] - time[0])
    y_filter2 = filter_signal(y_tot, f_cut_high=0.15, f_sampling=sampling_frequency)
    assert_equal(y_filter, y_filter2)


def test_butter_filter_lp():
    time, y_orig, y_tot = make_signal_orig_and_noisy()

    sample_frequency = 1 / (time[1] - time[0])

    y_filter = butterworth_filter(y_tot, f_cut_high=0.15, fs=sample_frequency, order=4)

    data_file = "data/butter_filter_lp.pkl"
    if not os.path.exists(data_file):
        data_file = os.path.join("..", data_file)

    if WRITE_DATA:
        with open(data_file, "wb") as out_stream:
            pickle.dump(y_filter, out_stream, pickle.HIGHEST_PROTOCOL)

    with open(data_file, "rb") as in_stream:
        y_filter_expected = pickle.load(in_stream)

    # check if we are up to the one digit equal to the input signal without noise
    assert_allclose(y_filter, y_filter_expected, atol=ATOL)

    # this is a front end to the butterworth filter, so_y_filter2 should be identical
    # to y_filter
    y_filter2 = filter_signal(
        y_tot, f_cut_high=0.15, f_sampling=sample_frequency, filter_type="butterworth",
        order=4
    )
    assert_equal(y_filter, y_filter2)


def test_assertion_error():
    time, y_orig, y_tot = make_signal_orig_and_noisy()

    assert_raises(ValueError, butterworth_filter, y_tot)
    assert_raises(ValueError, butterworth_filter, y_tot, f_cut_low=0.15,
                  f_cut_high=0.05)
    assert_raises(ValueError, butterworth_filter, y_tot, f_cut_low=0.05,
                  f_cut_high=0.05)
    assert_raises(ValueError, kaiser_bandpass_filter, y_tot)
    assert_raises(ValueError, kaiser_bandpass_filter, y_tot, lowcut=0.15, highcut=0.05)
    assert_raises(ValueError, kaiser_bandpass_filter, y_tot, lowcut=0.05, highcut=0.05)
    assert_raises(ValueError, bandpass_block_filter, time, y_tot)
    assert_raises(
        ValueError, bandpass_block_filter, time, y_tot, wfiltlo=0.15, wfiltup=0.05
    )
    assert_raises(
        ValueError, bandpass_block_filter, time, y_tot, wfiltlo=0.05, wfiltup=0.05
    )
    assert_raises(ValueError, filter_signal, y_tot)
    assert_raises(ValueError, filter_signal, y_tot, f_cut_low=0.15, f_cut_high=0.05)
    assert_raises(ValueError, filter_signal, y_tot, f_cut_low=0.05, f_cut_high=0.05)
