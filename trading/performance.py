# Evaluate performance.
import numpy as np
import trading.data
import trading.process
import trading.strategy
def read_ledger(duration,ledger_file):
    '''
    Reads and reports useful information from ledger_file.
    '''
    current_currency = np.zeros(duration)
    f = open(ledger_file,'r')
    fl = open("ledger.txt",'r')
    read_init = fl.readlines()
    income = []
    spent = []
    earend = []
    read = f.readlines()
    for item in read:
        if float(item.split(',')[4]) > 0:
            earend.append(float(item.split(',')[4]))
        else:
            spent.append(float(item.split(',')[4]))
        income.append(float(item.split(',')[4]))

    print("the total number of transactions performed:",len(read))
    print("the overall profit or loss over 5 years:",sum(income))
    print("spent:",sum(spent))
    print("earned:",sum(earend))

    in_out = np.zeros(duration)
    for item in read_init:
        in_out[int(item.split(',')[1])] += float(item.split(',')[4])
    current_currency[0] = in_out[0]
    for item in read:
        in_out[int(item.split(',')[1])] += float(item.split(',')[4])
    for i in range(1,duration):
        current_currency[i] = current_currency[i-1] + in_out[i]
    fl.close()
    f.close()
    return current_currency

