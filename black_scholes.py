import numpy as np
import scipy.stats as stats
from nsedt import equity as eq
from datetime import date as dt
import pandas as pd

# Getting stock returns to calculate the standard deviation

data = eq.get_price(dt(2020, 1, 1), dt(2023, 8, 28), symbol = "RELIANCE")
data = data[['Close Price']]

# Variables
r = 0.0525
s = 2461
k = 2460
T = 4/365
sigma = data.pct_change().apply(lambda x: np.log(1 + x)).std().apply(lambda x: x*np.sqrt(250))

def blackScholes(r, s, k, T, sigma, type = 'c'):
    # Calculate the option price

    d1 = (np.log(s/k) + (r + (sigma**2)/2) * T) / ( sigma * np.sqrt(T))
    d2 = d1 - (sigma * np.sqrt(T))
    global Price

    try:
        if type == 'c':
            Price = (s * stats.norm.cdf(d1, 0, 1)) - k*np.exp(-r * T) * stats.norm.cdf(d2, 0, 1)
        elif type == 'p':
            Price = (k * np.exp(-r * T) * stats.norm.cdf(-d2, 0, 1) - s * stats.norm.cdf(-d1, 0, 1))
        return Price
    except:
        print("Please check your Input Values and specify call OR put option")

value = blackScholes(r, s, k, T, sigma, 'p')
print("Option Price is: ", value)