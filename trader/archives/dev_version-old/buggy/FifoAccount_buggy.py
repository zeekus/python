import pandas as pd
from collections import deque
from Trade import Trade

class FifoAccount:
    def __init__(self):
        self.positions = {}
        self.pnl = {}
        self.cash_balance = 0
        self.line_number = 0
        self.fees = {}
        self.total_fees = 0
        self.total_gross_profit = 0
        self.total_net_profit = 0

    def buy(self, trade):
        # Calculate cost basis for the trade
        cost_basis = abs(trade.usd_amount) / trade.actual_crypto_amount
        if trade.crypto_asset not in self.positions:
            self.positions[trade.crypto_asset] = deque()
        self.positions[trade.crypto_asset].append((trade.actual_crypto_amount, cost_basis))
        
        # Update cash balance and fees
        self.cash_balance += trade.usd_amount
        self.fees[trade.crypto_asset] = self.fees.get(trade.crypto_asset, 0) + trade.crypto_fee
        self.total_fees += trade.crypto_fee
        
        print(f"Cash balance after buy: ${self.cash_balance:.2f}")
        print(f"Total {trade.crypto_asset} fees: {self.fees[trade.crypto_asset]:.8f}")
        print(f"Cost basis for this buy: ${cost_basis:.2f} per {trade.crypto_asset}")

    def sell(self, trade):
       # Initialize variables for selling process
       sell_quantity = abs(trade.crypto_amount)
       asset_queue = self.positions[trade.crypto_asset]
       self.cash_balance += abs(trade.usd_amount)  # Update cash balance after sale
       print(f"Cash balance after sell: ${self.cash_balance:.2f}")

       total_profit = 0
       quantity_sold = 0
       total_cost_basis = 0

       while sell_quantity > 0 and asset_queue:
           oldest_trade = asset_queue[0]
           if oldest_trade[0] <= sell_quantity:
               # Fully consume the oldest trade
               sell_quantity -= oldest_trade[0]
               buy_price = oldest_trade[1]
               profit = (abs(trade.usd_amount / trade.crypto_amount) - buy_price) * oldest_trade[0]
               total_profit += profit
               quantity_sold += oldest_trade[0]
               total_cost_basis += buy_price * oldest_trade[0]
               print(f'   Sold {oldest_trade[0]:.8f} {trade.crypto_asset} bought at {buy_price:.2f} USD. Profit: ${profit:.2f}')
               asset_queue.popleft()  # Remove from queue
           else:
               # Partially consume the oldest trade
               buy_price = oldest_trade[1]
               profit = (abs(trade.usd_amount / trade.crypto_amount) - buy_price) * sell_quantity
               total_profit += profit
               quantity_sold += sell_quantity
               total_cost_basis += buy_price * sell_quantity

               # Update remaining amount in the oldest trade
               oldest_trade = (oldest_trade[0] - sell_quantity, oldest_trade[1])
               asset_queue[0] = oldest_trade  # Update queue with remaining amount
               sell_quantity = 0

       if sell_quantity > 0:
           print(f"   Warning: Attempted to sell more {trade.crypto_asset} than available")

       gross_profit = total_profit  
       self.pnl[trade.crypto_asset] += gross_profit  
       self.fees[trade.crypto_asset] += trade.usd_fee  
       self.total_fees += trade.usd_fee  
       self.total_gross_profit += gross_profit  

       average_cost_basis = total_cost_basis / quantity_sold if quantity_sold > 0 else 0
       print(f'   Gross profit for this sale: ${gross_profit:9.2f}')
       print(f'   USD fee for this sale: ${trade.usd_fee:.2f}')  
       print(f'   Net profit for this sale: ${gross_profit:9.2f}')  
       print(f'   Average cost basis: ${average_cost_basis:9.2f} USD per {trade.crypto_asset}')
       print(f'   Average sale price: ${abs(trade.usd_amount) / quantity_sold:9.8f} USD per {trade.crypto_asset}')
       print(f"Running net profit for {trade.crypto_asset}: ${self.pnl[trade.crypto_asset]:9.8f}")

    def process_trade(self, trade):
      self.line_number += 1
      trade.print_trade(self.line_number)

      if trade.crypto_asset not in self.positions:
          self.positions[trade.crypto_asset] = deque()
      if trade.crypto_asset not in self.pnl:
          self.pnl[trade.crypto_asset] = 0
      if trade.crypto_asset not in self.fees:
          self.fees[trade.crypto_asset] = 0

      if trade.is_buy:
          self.buy(trade)
      else:
          self.sell(trade)

    def print_positions(self):
      print("\nCurrent Positions:")
      print(f"----------------------------------------")
      for asset, queue in self.positions.items():
          total_quantity = sum(trade[0] for trade in queue)
          if abs(total_quantity) > 1e-10:  
              print(f"{asset}: {total_quantity:6.8f}")

    def print_cash_balance(self):
        print(f"----------------------------------------")
        print(f"\nCurrent Cash Balance: ${self.cash_balance:9.2f}")
        print(f"----------------------------------------")

    def print_pnl(self):
      print("\nProfit/Loss per Asset:")
      for asset, profit in self.pnl.items():
          fees = self.fees.get(asset, 0)
          net_profit = profit  
          print(f"{asset:<5}: Taxable Profit: ${net_profit:<9.2f}")

      print("----------------------------------------")
      print(f"\nTotal [Taxable] Gross Profits: ${self.total_gross_profit:<9.2f}")
      print("----------------------------------------")

    def print_fees(self):
        print("\nTotal Trading Fees per Asset:")
        print("----------------------------------------")
        for asset, fee in self.fees.items():
            print(f"{asset}: $ {fee:<9.2f}")
        print(f"Total Fees: {sum(self.fees.values()):<9.2f}")

    def calculate_average_cost_basis(self):
        average_cost_basis = {}
    
        for asset, queue in self.positions.items():
            total_cost = 0
            total_units = 0
            
            print(f"Calculating average cost basis for {asset}:")
            
            for amount, cost_basis in queue:
                # Only consider significant amounts
                if abs(amount) > 1e-10:
                    cost_for_this_transaction = amount * cost_basis  # Calculate cost for this transaction
                    total_cost += cost_for_this_transaction  # Aggregate total cost
                    total_units += amount  # Aggregate total units held
                    
                    print(f"   Amount: {amount:.8f}, Cost Basis: {cost_basis:.2f}, "
                          f"Cost for this transaction: {cost_for_this_transaction:.2f}, "
                          f"Total Cost so far: {total_cost:.2f}, Total Units so far: {total_units:.8f}")
            
            # Calculate average if there are units held
            if total_units > 1e-10:
                average_cost = total_cost / total_units
                average_cost_basis[asset] = average_cost
                
                print(f"   Average Cost Basis for {asset}: {average_cost:.2f}")

        return average_cost_basis

    def print_full_data_structure(self):
        """Prints the full data structure of positions."""
        print("\nFull Data Structure of Positions:")
        print(f"----------------------------------------")
        
        for asset, queue in self.positions.items():
            total_cost = 0
            total_units = 0
            
            print(f"\nAsset: {asset}")
            print(f"Transactions:")
            
            for amount, cost_basis in queue:
                # Calculate cost for this transaction
                cost_for_this_transaction = amount * cost_basis
                total_cost += cost_for_this_transaction  # Aggregate total cost
                total_units += amount  # Aggregate total units held
                
                print(f"   Amount: {amount:.8f}, Cost Basis: {cost_basis:.2f}, "
                      f"Cost for this transaction: {cost_for_this_transaction:.2f}")
            
            # Calculate average if there are units held
            if total_units > 1e-10:
                average_cost = total_cost / total_units
                print(f"Total Cost: {total_cost:.2f}, Total Units: {total_units:.8f}")
                print(f"Average Cost Basis for {asset}: {average_cost:.2f}")
            else:
                print(f"No units held for {asset}.")
