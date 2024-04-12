
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def generate_random_array(size):
    """Generate a random NumPy array of given size."""
    return np.random.rand(size)

def calculate_mean(data):
    """Calculate the mean of a NumPy array or Pandas Series."""
    return np.mean(data)

def plot_histogram(data):
    """Plot a histogram of a NumPy array or Pandas Series."""
    plt.hist(data, bins=10)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram')
    plt.show()

def perform_t_test(data1, data2):
    """Perform a t-test for two samples using scipy.stats."""
    return stats.ttest_ind(data1, data2)
