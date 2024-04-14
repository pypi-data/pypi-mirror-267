import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def randomarr(size):
    """지정된 크기의 랜덤한 NumPy 배열을 생성합니다."""
    return np.random.rand(size)
    
def array(data):
    """ Numpy 배열 선언 """
    return np.array(data)
    
def mean(data):
    """NumPy 배열 또는 Pandas Series의 평균을 계산합니다."""
    return np.mean(data)

def mode(data):
    """NumPy 배열 또는 Pandas Series의 최빈값을 계산합니다."""
    return stats.mode(data)[0][0]

def med(data):
    """NumPy 배열 또는 Pandas Series의 중앙값을 계산합니다."""
    return np.median(data)

def std(data):
    """NumPy 배열 또는 Pandas Series의 표준편차를 계산합니다."""
    return np.std(data)

def var(data):
    """NumPy 배열 또는 Pandas Series의 분산을 계산합니다."""
    return np.var(data)

def skew(data):
    """데이터의 왜도를 계산합니다."""
    return skew(data)

def kurtosis(data):
    """데이터의 첨도를 계산합니다."""
    return kurtosis(data)
    
def hist(data, xlabel="", ylabel="", title=""):
    """
    NumPy 배열 또는 Pandas Series의 히스토그램을 플로팅합니다.
    데이터의 길이를 기반으로 bin의 수를 결정합니다.
    """
    plt.hist(data, bins=int(1 + np.log2(len(data))))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

def pie(data, labels, title=""):
    """파이 차트를 생성합니다."""
    plt.pie(data, labels=labels, autopct='%1.1f%%')
    plt.title(title)
    plt.show()

def line_plot(x, y, xlabel="", ylabel="", title=""):
    """두 데이터 집합의 선 그래프를 생성합니다."""
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

def scatter_plot(x, y, xlabel="", ylabel="", title=""):
    """두 데이터 집합의 산점도를 생성합니다."""
    plt.scatter(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

def bar(categories, values, xlabel="", ylabel="", title=""):
    """막대 그래프를 생성합니다."""
    plt.bar(categories, values)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()
    
def savefig(filename):
    plt.savefig(filename)

def t_test(data1, data2):
    """scipy.stats를 사용하여 두 샘플에 대한 t-test을 수행합니다."""
    return stats.ttest_ind(data1, data2)

def correlation(data1, data2):
    """두 데이터 집합 사이의 피어슨 상관 계수를 계산합니다."""
    return np.corrcoef(data1, data2)[0, 1]

def standardize(data):
    """데이터 집합의 값을 표준화합니다."""
    return (data - np.mean(data)) / np.std(data)

def box_plot(data, xlabel="", ylabel="", title=""):
    """데이터 집합의 상자 그림을 생성합니다."""
    plt.boxplot(data)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

def linear_regression(x, y):
    """두 데이터 집합에 대한 선형 회귀를 수행합니다."""
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    return slope, intercept, r_value, p_value, std_err

def bootstrap_resample(data, n_samples):
    """데이터 집합에 대한 부트스트랩 재표본을 생성합니다."""
    boot_samples = [np.random.choice(data, len(data), replace=True) for _ in range(n_samples)]
    return boot_samples

def probability_distribution(rv, size=1000):
    """주어진 무작위 변수를 기반으로 확률분포표를 작성합니다."""
    samples = rv.rvs(size=size)
    df = pd.DataFrame(samples, columns=['Value'])
    value_counts = df['Value'].value_counts(normalize=True).reset_index()
    value_counts.columns = ['Value', 'Probability']
    value_counts = value_counts.sort_values(by='Value').reset_index(drop=True)
    return value_counts

def describe(data):
    """NumPy 배열 또는 Pandas의 describe"""
    return pd.DataFrame(data).describe()