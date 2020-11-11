import numpy as np


def generate_stock_price(days, initial_price, volatility):
    '''
    Generates daily closing share prices for a company,
    for a given number of days.
    '''
    # Set stock_prices to be a zero array with length days
    stock_prices = np.zeros(days)
    # Set stock_prices in row 0 to be initial_price
    stock_prices[0] = initial_price
    # Set total_drift to be a zero array with length days
    totalDrift = np.zeros(days)
    # Set up the default_rng from Numpy
    rng = np.random.default_rng()
    # Loop over a range(1, days)
    for day in range(1, days):
        # Get the random normal increment
        inc = rng.normal(0,volatility**2)
        # Add stock_prices[day-1] to inc to get NewPriceToday
        NewPriceToday = stock_prices[day-1]+inc
        # Make a function for the news
        def news(chance, volatility):
            '''
            Simulate the news with %chance
            '''
            # Choose whether there's news today
            news_today = rng.choice([0,1], p=chance)
            # The impact of news lasts 3-14 days
            duration = rng.integers(3, 14)
            if news_today:
                # Calculate m and drift
                # Extract from the normal distribution that conforms to (0, 2 ^ 2)
                m = rng.normal(0,4)
                drift = m * volatility
                # Randomly choose the duration
                final = np.zeros(duration)
                for i in range(duration):
                    # Impact list
                    final[i] = drift
                # Return result list
                return final
            else:
                # No news, no impact
                return np.zeros(duration)
        # Get the drift from the news
        # Set probability for news occurrence 1:0.01,0:0.99 and call news()
        d = news([0.99,0.01], volatility)
        # Get the duration
        duration = len(d)
        # Add the drift to the next days
        # News has a cumulative effect
        # Only valid days are calculated
        if day + duration <= days:
            totalDrift[day:day+duration] += d
        else:
            totalDrift[day:days-1] += d[0:days-day-1]
        # Add today's drift to today's price
        NewPriceToday += totalDrift[day]
        # Set stock_prices[day] to NewPriceToday or to NaN if it's negative
        if NewPriceToday <= 0:
            stock_prices[day] = np.nan
        else:
            stock_prices[day] = NewPriceToday
    return stock_prices

def get_data(method, initial_price = 0, volatility = 0,datafile = 'stock_data_5y.txt'):
    '''
    Generates or reads simulation data for one or more stocks over 5 years,
    given their initial share price and volatility.

    Input:
        method (str): either 'generate' or 'read' (default 'read').
            If method is 'generate', use generate_stock_price() to generate
                the data from scratch.
            If method is 'read', use Numpy's loadtxt() to read the data
                from the file stock_data_5y.txt.

        initial_price (list): list of initial prices for each stock (default None)
            If method is 'generate', use these initial prices to generate the data.
            If method is 'read', choose the column in stock_data_5y.txt with the closest
                starting price to each value in the list, and display an appropriate message.

        volatility (list): list of volatilities for each stock (default None).
            If method is 'generate', use these volatilities to generate the data.
            If method is 'read', choose the column in stock_data_5y.txt with the closest
                volatility to each value in the list, and display an appropriate message.

        If no arguments are specified, read price data from the whole file.

    Output:
        sim_data (ndarray): NumPy array with N columns, containing the price data
            for the required N stocks each day over 5 years.

    Examples:
        Returns an array with 2 columns:
            >>> get_data(method='generate', initial_price=[150, 250], volatility=[1.8, 3.2])

        Displays a message and returns None:
            >>> get_data(method='generate', initial_price=[150, 200])
            Please specify the volatility for each stock.

        Displays a message and returns None:
            >>> get_data(method='generate', volatility=[3])
            Please specify the initial price for each stock.

        Returns an array with 2 columns and displays a message:
            >>> get_data(method='read', initial_price=[210, 58])
            Found data with initial prices [200, 50] and volatilities [1.5, 0.7].

        Returns an array with 1 column and displays a message:
            >>> get_data(volatility=[5.1])
            Found data with initial prices [850] and volatilities [5].

        If method is 'read' and both initial_price and volatility are specified,
        volatility will be ignored (a message is displayed to indicate this):
            >>> get_data(initial_price=[210, 58], volatility=[5, 7])
            Found data with initial prices [200, 50] and volatilities [1.5, 0.7].
            Input argument volatility ignored.

        No arguments specified, all default values, returns price data for all stocks in the file:
            >>> get_data()
    '''
    days = 1825
    if method == 'generate':
        # User chooses to generate simulated data, call generate_stock_price(). Save results to sim_data
        sim_data = generate_stock_price(days,initial_price,volatility)
    elif method == 'read':
        # User chooses to generate simulated data
        # Use np.loadtxt read the data from textbook
        # Because the first line is volatility, it is not read.
        # And read to the number of days the user wants
        my_data = np.loadtxt(datafile,skiprows=1)
        sim_data = my_data[0:days]
    # Return the result of the simulated data
    return sim_data