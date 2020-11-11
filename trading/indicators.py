import numpy as np

def moving_average(stock_price, n=7, weights=[]):
    '''
    Calculates the n-day (possibly weighted) moving average for a given stock over time.

    Input:
        stock_price (ndarray): single column with the share prices over time for one stock,
            up to the current day.
        n (int, default 7): period of the moving average (in days).
        weights (list, default []): must be of length n if specified  . Indicates the weights
            to use for the weighted average. If empty, return a non-weighted average.

    Output:
        ma (ndarray): the n-day (possibly weighted) moving average of the share price over time.
    '''
    # Initial results
    length = len(stock_price)
    ma = np.zeros(length)
    for i in range(0,n):
        ma[i] = np.nan
    # Calculate effective length
    # Calculation without weighting
    if len(weights) == 0:
        for index in range(n-1,length):
            result = sum(stock_price[index - n + 1:index + 1]) / n
            ma[index] = result
        return ma
    # must be of length n if specified
    elif len(weights) == n:
        # For loop step:n
        for index in range(n-1,length):
            # Calculate the product of all data and weights
            step1 = stock_price[index - n + 1:index + 1] * np.array(weights)
            # Calculate moving average with weights
            step2 = sum(step1) / sum(weights)
            # Moving average of the day
            ma[index] = step2
        return ma
    else:
        # Throw error message
        print('Weights length error')
def oscillator(stock_price, n=7, osc_type='stochastic'):
    '''
    Calculates the level of the stochastic or RSI oscillator with a period of n days.

    Input:
        stock_price (ndarray): single column with the share prices over time for one stock,
            up to the current day.
        n (int, default 7): period of the moving average (in days).
        osc_type (str, default 'stochastic'): either 'stochastic' or 'RSI' to choose an oscillator.

    Output:
        osc (ndarray): the oscillator level with period $n$ for the stock over time.
    '''
    # Calculate length
    length = len(stock_price)
    # Initialize array
    osc = np.zeros(length)
    if osc_type == 'stochastic':
        for i in range(n-1,length):
            # Find the highest and lowest prices over the past n days
            min_num = min(stock_price[i - n + 1:i + 1])
            max_num = max(stock_price[i - n + 1:i + 1])
            # Compute the difference between today's price and the lowest price
            delta = stock_price[i] - min_num
            # Compute the difference between the highest price and the lowest price
            delta_max = max_num - min_num
            # The level of the oscillator on this day is the ratio delta / delta_max
            osc[i] = delta / delta_max
        return osc
    elif osc_type == 'RSI':
        # Set initial result list
        sumup = []
        sumdown = []
        RSI = np.zeros(length)
        for i in range(n-1, length):
            list = stock_price[i - n + 1:i + 1]
            # Calculate all the price differences on consecutive days over the past n days.
            for j in range(0, n-1):
                delta = list[j+1] - list[j]
                # Separate positive and negative differences
                if delta > 0:
                    sumup.append(delta)
                else:
                    sumdown.append(-delta)
            # If there is both a rise and a fall calculate the RSI
            if len(sumup) != 0 and len(sumdown) != 0:
                aver_po = sum(sumup) / len(sumup)
                aver_ne = sum(sumdown) / len(sumdown)
                sumup = []
                sumdown = []
                RSI[i] = aver_po / (aver_po + aver_ne)
            # If only rise no fall, RSI = 1
            elif len(sumdown) == 0:
                RSI[i] = 1
            # If only fall no rise, RSI = 0
            elif len(sumup) == 0:
                RSI[i] = 0
            # Other circumstances proved that the calculation was wrong
            else:
                print("error")
        return RSI
