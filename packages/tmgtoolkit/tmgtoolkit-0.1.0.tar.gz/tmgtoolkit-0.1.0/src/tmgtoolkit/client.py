from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import time_series, spm, plotting, tmgio
from constants import DataConstants


def test_tmg_excel_to_ndarray():
    fname = DataConstants.SAMPLE_DATA['xlsx']['sample']
    data = tmgio.tmg_excel_to_ndarray(fname)
    print(data)
    print(data.shape)


def test_split_data_for_spm():
    data = np.loadtxt(str(DataConstants.SAMPLE_DATA['csv']['tmg']), delimiter=',')
    numsets = 2
    n1 = 2
    n2 = 1
    group1, group2 = tmgio.split_data_for_spm(data, numsets, n1, n2)
    print("Group 1")
    print(group1)
    print("Group 2")
    print(group2)
    print("Group 1 shape: {}".format(group1.shape))
    print("Group 2 shape: {}".format(group2.shape))


def test_get_tmg_parameters_of_time_series():
    data = np.loadtxt(str(DataConstants.SAMPLE_DATA['csv']['tmg']), delimiter=',')
    t = np.arange(data.shape[0])
    y = data[:, 0]
    params = time_series.get_tmg_parameters_of_time_series(y, t=t)
    print("TMG parameters:")
    print(params)


def test_get_derivative_of_time_series():
    data = np.loadtxt(str(DataConstants.SAMPLE_DATA['csv']['tmg']), delimiter=',')
    t = np.arange(data.shape[0])
    y = data[:, 0]
    dydt = time_series.get_derivative_of_time_series(y, t=t)

    fig, axes = plt.subplots(2, 1)
    ax = axes[0]
    ax.set_xlabel("Time")
    ax.set_ylabel("Displacement")
    ax.set_title("TMG signal")
    ax.plot(t, y)
    ax = axes[1]
    ax.set_xlabel("Time")
    ax.set_ylabel("Derivative")
    ax.set_title("Derivative")
    ax.plot(t, dydt)
    plt.tight_layout()
    plt.show()


def test_get_extremum_parameters_of_time_series():
    data = np.loadtxt(str(DataConstants.SAMPLE_DATA['csv']['triangle']), delimiter=',')
    t = np.arange(data.shape[0])
    y = data[:, 0]
    params = time_series.get_extremum_parameters_of_time_series(y, t=t)
    print("Extremum params:")
    print(params)


def test_get_spm_t_statistic():
    skiprows = 1  # to avoid zero-variance first row
    data = np.loadtxt(str(DataConstants.SAMPLE_DATA['csv']['spm']), delimiter=',', skiprows=skiprows)
    t = np.arange(skiprows, data.shape[0] + skiprows)
    numsets = 8
    n1 = 1
    n2 = 1
    group1, group2 = tmgio.split_data_for_spm(data, numsets, n1, n2)
    spm_ts = spm.get_spm_t_statistic(group1, group2, mitigate_iir_filter_artefact=False)
    spm_t = spm_ts.t_statistic

    fig, ax = plt.subplots()
    ax.set_xlabel("Time")
    ax.set_ylabel("SPM{t}")
    ax.set_title("SPM t-statistic")
    ax.plot(t, spm_t)
    plt.tight_layout()
    plt.show()


def test_get_spm_t_inference():
    skiprows = 1  # to avoid zero-variance first row
    data = np.loadtxt(DataConstants.SAMPLE_DATA['csv']['spm'], delimiter=',', skiprows=skiprows)
    t = np.arange(skiprows, data.shape[0] + skiprows)
    numsets = 8
    n1 = 1
    n2 = 1
    group1, group2 = tmgio.split_data_for_spm(data, numsets, n1, n2)
    spm_ts = spm.get_spm_t_statistic(group1, group2, mitigate_iir_filter_artefact=False)
    spm_ti = spm.get_spm_t_inference(spm_ts, t=t)
    print("SPM inference parameters:")
    print(spm_ti)


def test_plot_time_series():
    data = np.loadtxt(DataConstants.SAMPLE_DATA['csv']['tmg'], delimiter=',')
    t = np.arange(data.shape[0])

    fig, ax = plt.subplots()
    plotting.plot_time_series(ax, data[:, 0], t)
    plt.tight_layout()
    plt.show()


def test_plot_spm_t_statistic():
    skiprows = 1  # to avoid zero-variance first row
    nrows = 150
    data = np.loadtxt(DataConstants.SAMPLE_DATA['csv']['spm'], delimiter=',', skiprows=skiprows, max_rows=nrows)
    t = np.arange(skiprows, data.shape[0] + skiprows)
    numsets = 8
    n1 = 1
    n2 = 1
    group1, group2 = tmgio.split_data_for_spm(data, numsets, n1, n2)
    spm_ts = spm.get_spm_t_statistic(group2, group1)
    spm_ti = spm.get_spm_t_inference(spm_ts, t=t)

    fig, ax = plt.subplots()
    plotting.plot_spm_t_statistic(ax, spm_ts, spm_ti, t=t)
    plt.tight_layout()
    plt.show()


def test_plot_spm_input_data():
    skiprows = 1  # to avoid zero-variance first row
    nrows = 150
    data = np.loadtxt(DataConstants.SAMPLE_DATA['csv']['spm'], delimiter=',', skiprows=skiprows, max_rows=nrows)
    t = np.arange(skiprows, data.shape[0] + skiprows)
    numsets = 8
    n1 = 1
    n2 = 1
    group1, group2 = tmgio.split_data_for_spm(data, numsets, n1, n2)

    fig, ax = plt.subplots()
    plotting.plot_spm_input_data(ax, group1, group2, t)
    plt.tight_layout()
    plt.show()


def test_spm_full():
    skiprows = 1  # to avoid zero-variance first row
    nrows = 150
    data = np.loadtxt(DataConstants.SAMPLE_DATA['csv']['spm'], delimiter=',', skiprows=skiprows, max_rows=nrows)
    t = np.arange(skiprows, data.shape[0] + skiprows)
    numsets = 8
    n1 = 1
    n2 = 1
    group1, group2 = tmgio.split_data_for_spm(data, numsets, n1, n2)
    if no_significance:  # to ensure no difference between groups
        group2 = group1
    spm_ts = spm.get_spm_t_statistic(group1, group2)
    spm_ti = spm.get_spm_t_inference(spm_ts, t=t)

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
    plotting.plot_spm_t_statistic(axes[0], spm_ts, spm_ti, t=t)
    plotting.plot_spm_input_data(axes[1], group1, group2, t)
    plt.tight_layout()
    plt.show()


def test_spm_full_with_no_significance():
    skiprows = 1
    nrows = 150
    data = np.loadtxt(DataConstants.SAMPLE_DATA['csv']['spm'], delimiter=',', skiprows=skiprows, max_rows=nrows)
    t = np.arange(skiprows, data.shape[0] + skiprows)
    numsets = 8
    n1 = 1
    n2 = 1
    group1, group2 = tmgio.split_data_for_spm(data, numsets, n1, n2)

    group2 = group1
    group1 = group1 + 0.001*np.random.randn(group1.shape[0], group1.shape[1])

    spm_ts = spm.get_spm_t_statistic(group1, group2)
    spm_ti = spm.get_spm_t_inference(spm_ts, t=t)

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))
    plotting.plot_spm_t_statistic(axes[0], spm_ts, spm_ti, t=t)
    plotting.plot_spm_input_data(axes[1], group1, group2, t)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # test_tmg_excel_to_ndarray()
    # test_split_data_for_spm()
    # test_get_tmg_parameters_of_time_series()
    # test_get_derivative_of_time_series()
    # test_get_extremum_parameters_of_time_series()
    # test_get_spm_t_statistic()
    # test_get_spm_t_inference()
    # test_plot_time_series()
    # test_plot_spm_t_statistic()
    test_plot_spm_input_data()
    # test_spm_full()
    # test_spm_full_with_no_significance()

