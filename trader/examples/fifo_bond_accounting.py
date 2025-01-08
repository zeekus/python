"""
 Copyright (C) 2017 Michael von den Driesch

 This file is just a simple implementation of a python class allowing for various
 *booking* types (LIFO, FIFO, AVCO)

 This *GIST* is free software: you can redistribute it and/or modify it
 under the terms of the BSD-2-Clause (https://opensource.org/licenses/bsd-license.html). 

 This program is distributed in the hope that it will be useful, but WITHOUT
 ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 FOR A PARTICULAR PURPOSE.  See the license for more details.
"""


from collections import deque
import pandas as pd
import numpy as np
import datetime as dt
from enum import Enum

refDate = pd.to_datetime('01.04.2016', format='%d.%m.%Y')

class Trade():
    def __init__(self,date: pd.datetime, quantity: np.float32, price: np.float32):
        self.date = date
        self.quantity = quantity
        self.price = price
    def printT(self):
        return print('Quantity: %i, Price: %f'%(self.quantity, self.price))

class Isin():
    def __init__(self, isin, notinalPerQuantity, listOfTrades):
        self._isin = isin
        self._notinalPerQuantity = notinalPerQuantity
        self._listOfTrades = listOfTrades
    def mtm(self, trade):
        return trade.quantity*trade.price*self._notinalPerQuantity
    def __next__(self):
        return self._listOfTrades.__next__()
    def __iter__(self):
        return self._listOfTrades.__iter__()

class transactionAccounting():
    def __init__(self, isin):
        """
        Initiliase with first entry from left
        """
        print('Initialize trade que')
        self._Isin = isin
        self._notinalPerQuantity = isin._notinalPerQuantity
        self._trades = isin._listOfTrades
        t0 = self._trades[0]
        self._avgprice = 0
        self._quantity = 0
        self._pnl = 0
        self._bookvalue = 0
    def printStat(self):
        print('Pos.Quantity: %i, AvgPrice: %f, PnL: %f, Book: %f'%(self._quantity, 
                                                           self._avgprice,
                                                           self._pnl,
                                                           self._bookvalue))
    def buy(self, trade):
        raise NotImplementedError
        
    def sell(self, trade):
        raise NotImplementedError
            
              
class FifoAccount(transactionAccounting):
    """
    checkout out this site for an example
    http://accountingexplained.com/financial/inventories/fifo-method
    """
    def __init__(self, trades):
        transactionAccounting.__init__(self, trades)
        self._deque = deque()
        for trade in self._trades:
            if trade.quantity>=0:
                self.buy(trade)
            else:
                self.sell(trade)
    def buy(self, trade):
        print('Buy trade')
        trade.printT()
        self._deque.append(trade)
        self._bookvalue += self._Isin.mtm(trade) 
        self._quantity += trade.quantity
        self._avgprice = self._bookvalue / self._quantity / self._notinalPerQuantity
        self.printStat()
    def sell(self, trade):
        print('Sell trade') 
        trade.printT()
        sellQuant = -trade.quantity
        while(sellQuant>0):
            lastTrade = self._deque.popleft()
            price = lastTrade.price
            quantity = lastTrade.quantity
            print('Cancel trade:')
            lastTrade.printT()
            if sellQuant >= quantity:
                self._pnl += -(price - trade.price)*quantity*self._notinalPerQuantity 
                self._quantity -= quantity
                self._bookvalue -= price * quantity * self._notinalPerQuantity
                sellQuant -= quantity
            else:
                #from IPython.core.debugger import Tracer; Tracer()()
                self._pnl += -(price - trade.price)*sellQuant*self._notinalPerQuantity 
                self._quantity -= sellQuant
                self._bookvalue -= price * sellQuant * self._notinalPerQuantity
                lastTrade.quantity -= sellQuant
                self._deque.appendleft(lastTrade)
                sellQuant = 0 
            self.printStat()
            assert(self._quantity > 0)
            



el = [Trade(pd.to_datetime('01.04.2016',
                         format='%d.%m.%Y')+dt.timedelta(days=i)
          , 5-i, 99.8+i) for i in range(0,10)]

el = [Trade(pd.to_datetime('01.03.2016',format='%d.%m.%Y'), 68, 15)]
el.append(Trade(pd.to_datetime('05.03.2016',format='%d.%m.%Y'), 140, 15.5))
el.append(Trade(pd.to_datetime('09.03.2016',format='%d.%m.%Y'), -94, 19))
el.append(Trade(pd.to_datetime('11.03.2016',format='%d.%m.%Y'), 40, 16))
el.append(Trade(pd.to_datetime('16.03.2016',format='%d.%m.%Y'), 78, 16.5))
el.append(Trade(pd.to_datetime('20.03.2016',format='%d.%m.%Y'), -116, 19.5))
el.append(Trade(pd.to_datetime('20.03.2016',format='%d.%m.%Y'), -62, 21))


b = Isin('bond', 1, el)
trans = FifoAccount(b)

