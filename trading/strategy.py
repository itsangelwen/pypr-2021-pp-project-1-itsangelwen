# Functions to implement our trading strategy.
import numpy as np
import trading.process as proc
import trading.indicators as indi

def random(stock_prices,portfolio,period=7, amount=5000, fees=20, ledger='ledger_random.txt'):
    '''
    Randomly decide, every period, which stocks to purchase,
    do nothing, or sell (with equal probability).
    Spend a maximum of amount on every purchase.

    Input:
        stock_prices (ndarray): the stock price data
        period (int, default 7): how often we buy/sell (days)
        amount (float, default 5000): how much we spend on each purchase
            (must cover fees)
        fees (float, default 20): transaction fees
        ledger (str): path to the ledger file

    Output: None
    '''
    # Calculate effective length
    length = (len(stock_prices[:,0]) - 1) - (len(stock_prices[:,0]) - 1) % period
    # Calculate the number of types of stock
    stocks = len(stock_prices[0])
    for day in range(1, length, period):
        choice = ['buy','sell','nothing']
        # Random select behavior
        rng = np.random.default_rng()
        action = rng.choice(choice)
        if action == 'buy':
            # for loop traverse each stock
            for stock in range(0,stocks):
                # buy stock
                proc.buy(day, stock, amount, stock_prices, fees, portfolio, ledger)
        elif action == 'sell':
            # for loop traverse each stock
            for stock in range(0, stocks):
                # sell all stock
                proc.sell(day,stock,stock_prices,fees,portfolio,ledger)
        else:
            pass

def crossing_averages(n,m,stock_prices,available_capital,fees,portfolio,ledger = 'ledger_crossing_averages.txt'):
    '''
        The relationship between the moving average curve determines whether to buy or sell

        Input:
            n(int): SMA period
            m(int): FMA period
            available_capital(float): Budget for each stock purchased each time
            fees(float): Cost per transaction
            portfolio
            ledger(str): File to store purchase information
        Output: purchase point
        '''
    for stocks in range(len(stock_prices[0])):
        # Calculate the FMA and SMA of each stock
        FMA = indi.moving_average(stock_prices[:,stocks], m)
        SMA = indi.moving_average(stock_prices[:,stocks], n)
        # Initiate the event list of purchase time and sales
        buy_point = []
        sell_point = []
        final = []
        # Find the point where the two curves intersect, according to the size of the stock price on the left and right
        for x in range(1,len(stock_prices)-1):
            if FMA[x-1] < SMA[x-1] and FMA[x+1] > SMA [x+1]:
                buy_point.append(x)
            elif FMA[x-1] > SMA[x-1] and FMA[x+1] < SMA [x+1]:
                sell_point.append(x)
        for day in range(len(stock_prices)):
            if day+1 in buy_point:
                proc.buy(day,stocks,available_capital,stock_prices,fees,portfolio,ledger)
            elif day+1 in sell_point:
                proc.sell(day,stocks,stock_prices,fees,portfolio,ledger)
        final.append([buy_point,sell_point])
    return final

def momentum(stock_prices,available_capital,fees,portfolio,n=7,osc_type='stochastic',ledger = 'ledger_momentum.txt'):
    '''
        OSC decides whether to buy or sell

        Input:
            stock_prices(array): All prices of all stocks
            available_capital(float): Budget for each stock purchased each time
            fees(float): Cost per transaction
            fees(float): Cost per transaction
            portfolio
            ledger(str): File to store purchase information
        Output: None
        '''
    for stocks in range(len(stock_prices[0])):
        # Calculate OSC
        result = indi.oscillator(stock_prices[:,stocks], n=n, osc_type='stochastic').tolist()
        # Initiate the event list of purchase time and sales
        buy_point = []
        sell_point = []
        for i in range(0, len(result)):
            # Judging whether to buy or sell by threshold, the cooling off period for each transaction is 10 days
            if result[i] > 0.2 and result[i] < 0.3:
                if len(buy_point) > 0 and len(sell_point) > 0:
                    if i > max(buy_point[-1],sell_point[-1]) + 5:
                        buy_point.append(i)
                else:
                    buy_point.append(i)
            elif result[i] > 0.7 and result[i] < 0.8:
                if len(buy_point) > 0 and len(sell_point) > 0:
                    if i > max(buy_point[-1],sell_point[-1]) + 5:
                        sell_point.append(i)
                else:
                    sell_point.append(i)
        # Buy and sell stocks according to the time just set
        for day in range(len(stock_prices)):
            if day+1 in buy_point:
                proc.buy(day,stocks,available_capital,stock_prices,fees,portfolio,ledger)
            elif day+1 in sell_point:
                proc.sell(day,stocks,stock_prices,fees,portfolio,ledger)

