import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def random_array(size):
    """Generate a random NumPy array of given size."""
    return np.random.rand(size)

def mean(data):
    """Calculate the mean of a NumPy array or Pandas Series."""
    return np.mean(data)

def mode(data):
    """Calculate the mode of a NumPy array or Pandas Series."""
    return stats.mode(data)[0][0]

def median(data):
    """Calculate the median of a NumPy array or Pandas Series."""
    return np.median(data)

def std_deviation(data):
    """Calculate the standard deviation of a NumPy array or Pandas Series."""
    return np.std(data)

def variance(data):
    """Calculate the variance of a NumPy array or Pandas Series."""
    return np.var(data)

def histogram(data):
    """
    Plot a histogram of a NumPy array or Pandas Series.
    Determine the bins based on the length of the data.
    """
    plt.hist(data, bins=int(1 + np.log2(len(data))))
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram')
    plt.show()

def pie(data, labels):
    """Create a pie chart."""
    plt.pie(data, labels=labels, autopct='%1.1f%%')
    plt.title('Pie Chart')
    plt.show()

def line_plot(x, y):
    """Create a line plot of two sets of data."""
    plt.plot(x, y)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Line Plot')
    plt.show()

def scatter_plot(x, y):
    """Create a scatter plot of two sets of data."""
    plt.scatter(x, y)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Scatter Plot')
    plt.show()

def bar(categories, values):
    """Create a bar chart."""
    plt.bar(categories, values)
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.title('Bar Chart')
    plt.show()

def t_test(data1, data2):
    """Perform a t-test for two samples using scipy.stats."""
    return stats.ttest_ind(data1, data2)

def correlation(data1, data2):
    """Calculate the Pearson correlation coefficient between two datasets."""
    return np.corrcoef(data1, data2)[0, 1]

def standardize(data):
    """Standardize the values of a dataset."""
    return (data - np.mean(data)) / np.std(data)

def boxplot(data):
    """Create a box plot of a dataset."""
    plt.boxplot(data)
    plt.xlabel('Data')
    plt.ylabel('Value')
    plt.title('Box Plot')
    plt.show()

def linear_regression(x, y):
    """Perform linear regression on two sets of data."""
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    return slope, intercept, r_value, p_value, std_err

def resample_bootstrap(data, n_samples):
    """Perform bootstrap resampling on a dataset."""
    boot_samples = [np.random.choice(data, len(data), replace=True) for _ in range(n_samples)]
    return boot_samples
