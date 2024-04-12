import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

def sample_variance(data):
    """
    표본분산
    Calculate sample variance.

    Parameters:
    data : numpy.ndarray
        입력 데이터 배열

    Returns:
    float
        표본분산 값
    """
    return np.var(data)

def unbiased_variance(data):
    """
    불편분산
    Calculate unbiased variance.

    Parameters:
    data : numpy.ndarray
        입력 데이터 배열

    Returns:
    float
        불편분산 값
    """
    return np.var(data, ddof=1)

def normalization(data):
    """
    정규화
    Normalize data.

    Parameters:
    data : numpy.ndarray
        입력 데이터 배열

    Returns:
    numpy.ndarray
        정규화된 데이터 배열
    """
    return (data - np.min(data)) / (np.max(data) - np.min(data))

def standardization(data):
    """
    표준화
    Standardize data.

    Parameters:
    data : numpy.ndarray
        입력 데이터 배열

    Returns:
    numpy.ndarray
        표준화된 데이터 배열
    """
    return (data - np.mean(data)) / np.std(data)

def mean(data):
    """
    평균
    Calculate mean.

    Parameters:
    data : numpy.ndarray
        입력 데이터 배열

    Returns:
    float
        평균 값
    """
    return np.mean(data)

def average(data):
    """
    평균값
    Calculate mean (same as 'mean').

    Parameters:
    data : numpy.ndarray
        입력 데이터 배열

    Returns:
    float
        평균 값
    """
    return np.mean(data)

def variance(data):
    """
    분산
    Calculate variance.

    Parameters:
    data : numpy.ndarray
        입력 데이터 배열

    Returns:
    float
        분산 값
    """
    return np.var(data)

def length(data):
    """
    길이
    Get length of data.

    Parameters:
    data : numpy.ndarray
        입력 데이터 배열

    Returns:
    int
        데이터의 길이
    """
    return len(data)

def zscore(data):
    """
    Z 점수
    Calculate z-scores.

    Parameters:
    data : numpy.ndarray
        입력 데이터 배열

    Returns:
    numpy.ndarray
        Z 점수 배열
    """
    return stats.zscore(data)

def bar_graph(data, x_label="", y_label="", title=""):
    """
    막대그래프
    Create a bar graph.

    Parameters:
    data : numpy.ndarray
        입력 데이터 배열
    x_label : str, optional
        X 축 라벨 (기본값: "")
    y_label : str, optional
        Y 축 라벨 (기본값: "")
    title : str, optional
        그래프 제목 (기본값: "")

    Returns:
    None
    """
    plt.bar(np.arange(len(data)), data)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend(['Operation'])
    plt.show()

def histogram(data, bins="auto"):
    """
    히스토그램
    Create a histogram.

    Parameters:
    data : numpy.ndarray
        입력 데이터 배열
    bins : int or sequence of scalars or str, optional
        Bin 지정 방법 (기본값: "auto")

    Returns:
    None
    """
    plt.hist(data, bins=bins, edgecolor='black')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.legend(['Operation'])
    plt.show()

def pie_chart(data):
    """
    파이차트
    Create a pie chart.

    Parameters:
    data : numpy.ndarray
        입력 데이터 배열

    Returns:
    None
    """
    plt.pie(data, labels=np.arange(len(data)))
    plt.legend(['Operation'])
    plt.show()

def line_chart(x, y, x_label="", y_label="", title=""):
    """
    선그래프
    Create a line chart.

    Parameters:
    x : numpy.ndarray
        X 축 데이터 배열
    y : numpy.ndarray
        Y 축 데이터 배열
    x_label : str, optional
        X 축 라벨 (기본값: "")
    y_label : str, optional
        Y 축 라벨 (기본값: "")
    title : str, optional
        그래프 제목 (기본값: "")

    Returns:
    None
    """
    plt.plot(x, y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend(['Operation'])
    plt.show()

def scatter_plot(x, y, x_label="", y_label="", title=""):
    """
    산점도
    Create a scatter plot.

    Parameters:
    x : numpy.ndarray
        X 축 데이터 배열
    y : numpy.ndarray
        Y 축 데이터 배열
    x_label : str, optional
        X 축 라벨 (기본값: "")
    y_label : str, optional
        Y 축 라벨 (기본값: "")
    title : str, optional
        그래프 제목 (기본값: "")

    Returns:
    None
    """
    plt.scatter(x, y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend(['Operation'])
    plt.show()

def median(data):
    """
    중앙값
    Calculate median.

    Parameters:
    data : numpy.ndarray
        입력 데이터 배열

    Returns:
    float
        중앙값
    """
    return np.median(data)

def sort_values(data):
    """
    정렬된 값
    Sort values in ascending order.

    Parameters:
    data : numpy.ndarray
        입력 데이터 배열

    Returns:
    numpy.ndarray
        정렬된 데이터 배열
    """
    return np.sort(data)

def mode(data):
    """
    최빈값
    Calculate mode.

    Parameters:
    data : numpy.ndarray
        입력 데이터 배열

    Returns:
    float
        최빈값
    """
    return stats.mode(data).mode[0]

def concat_axis_0(data1, data2):
    """
    축 0을 따른 연결
    Concatenate two arrays along axis 0.

    Parameters:
    data1 : numpy.ndarray
        첫 번째 입력 데이터 배열
    data2 : numpy.ndarray
        두 번째 입력 데이터 배열

    Returns:
    numpy.ndarray
        Concatenated array
    """
    return np.concatenate((data1, data2), axis=0)

def concat_axis_1(data1, data2):
    """
    축 1을 따른 연결
    Concatenate two arrays along axis 1.

    Parameters:
    data1 : numpy.ndarray
        첫 번째 입력 데이터 배열
    data2 : numpy.ndarray
        두 번째 입력 데이터 배열

    Returns:
    numpy.ndarray
        Concatenated array
    """
    return np.concatenate((data1, data2), axis=1)

def histogram_bins(data):
    """
    히스토그램 빈
    Calculate the number of bins for a histogram using Sturges' formula.

    Parameters:
    data : numpy.ndarray
        입력 데이터 배열

    Returns:
    int
        Number of bins
    """
    return int(np.ceil(1 + np.log2(len(data))))

def trim_mean(data, proportiontocut=0.1):
    """
    제한된 평균
    Calculate the trimmed mean.

    Parameters:
    data : numpy.ndarray
        입력 데이터 배열
    proportiontocut : float, optional
        Proportion of data to cut from both ends (기본값: 0.1)

    Returns:
    float
        Trimmed mean value
    """
    return stats.trim_mean(data, proportiontocut)

def skew(data):
    """
    왜도
    Calculate skewness.

    Parameters:
    data : numpy.ndarray
        입력 데이터 배열

    Returns:
    float
        Skewness value
    """
    return stats.skew(data)

def kurtosis(data):
    """
    첨도
    Calculate kurtosis.

    Parameters:
    data : numpy.ndarray
        입력 데이터 배열

    Returns:
    float
        Kurtosis value
    """
    return stats.kurtosis(data)

def display(data):
    """
    표시
    Display data.

    Parameters:
    data : numpy.ndarray
        입력 데이터 배열

    Returns:
    None
    """
    print(data)

def describe(data):
    """
    요약통계
    Display summary statistics.

    Parameters:
    data : numpy.ndarray
        입력 데이터 배열

    Returns:
    None
    """
    print(pd.DataFrame(data).describe())

def set_index(data, index):
    """
    인덱스 설정
    Set index.

    Parameters:
    data : numpy.ndarray
        입력 데이터 배열
    index : array-like
        Index array

    Returns:
    DataFrame
        DataFrame with index set
    """
    return pd.DataFrame(data).set_index(index)

def savefig(filename):
    """
    그림 저장
    Save the current figure.

    Parameters:
    filename : str
        파일 이름

    Returns:
    None
    """
    plt.savefig(filename)

def probability_distribution_table(data):
    """
    확률분포표
    Create a probability distribution table.

    Parameters:
    data : numpy.ndarray or pandas.Series
        입력 데이터 배열 또는 시리즈

    Returns:
    DataFrame
        Probability distribution table
    """
    if isinstance(data, np.ndarray):
        data = pd.Series(data)
    return data.value_counts().reset_index().rename(columns={"index": "variable", data.name: "count"})
