import pandas as pd
from collections import defaultdict

class Asset:
    def __init__(self):
        self.purchases = []
        print("DEBUG: Initialized Asset with empty purchase list")

    def add_purchase(self, quantity, purchase_price):
        self.purchases.append({'quantity': quantity, 'purchase_price': purchase_price})
        print(f"DEBUG: Added purchase - Quantity: {quantity}, Purchase Price: {purchase_price}")

    def calculate_fifo_cost_basis(self, quantity_sold):
        remaining_quantity = quantity_sold
        cost_basis = 0.0
        print(f"DEBUG: Calculating FIFO cost basis for quantity sold: {quantity_sold}")

        while remaining_quantity > 0 and self.purchases:
            purchase = self.purchases[0]
            print(f"DEBUG: Processing purchase: {purchase}")
            if purchase['quantity'] <= remaining_quantity:
                # Use the entire quantity of this purchase
                cost_basis += purchase['quantity'] * purchase['purchase_price']
                print(f"DEBUG: Using entire purchase - Cost basis: {cost_basis}, Remaining quantity: {remaining_quantity}")
                remaining_quantity -= purchase['quantity']
                self.purchases.pop(0)
            else:
                # Use only part of this purchase
                cost_basis += remaining_quantity * purchase['purchase_price']
                purchase['quantity'] -= remaining_quantity
                print(f"DEBUG: Using partial purchase - Cost basis: {cost_basis}, Remaining quantity: {remaining_quantity}")
                remaining_quantity = 0

        if remaining_quantity > 0:
            # Debug statement to help identify the issue
            print(f"DEBUG: Not enough assets to cover the sale of {quantity_sold} units.")
            print(f"DEBUG: Remaining quantity to cover: {remaining_quantity}")
            print(f"DEBUG: Current purchases: {self.purchases}")
            raise ValueError("Not enough assets to cover the sale.")

        return cost_basis

class Portfolio:
    def __init__(self):
        self.assets = defaultdict(Asset)
        print("DEBUG: Initialized Portfolio with empty assets")

    def add_asset_purchase(self, asset_name, quantity, usd_amount, fee):
        net_quantity = quantity - fee
        purchase_price_per_unit = usd_amount / net_quantity
        print(f"DEBUG: Adding asset purchase - Asset: {asset_name}, Quantity: {quantity}, USD Amount: {usd_amount}, Fee: {fee}")
        print(f"DEBUG: Net Quantity: {net_quantity}, Purchase Price Per Unit: {purchase_price_per_unit}")
        self.assets[asset_name].add_purchase(net_quantity, purchase_price_per_unit)

    def calculate_cost_basis(self, asset_name, quantity_sold):
        print(f"DEBUG: Calculating cost basis for asset: {asset_name}, Quantity Sold: {quantity_sold}")
        return self.assets[asset_name].calculate_fifo_cost_basis(quantity_sold)

    def add_transaction(self, asset_name, quantity, amount_usd, fee, time):
        print(f"DEBUG: Processing transaction at {time}: Asset: {asset_name}, Quantity: {quantity}, Amount USD: {amount_usd}, Fee: {fee}")
        
        if amount_usd < 0:
            # Purchase
            print("DEBUG: Transaction is a purchase")
            net_quantity = quantity - fee
            purchase_price_per_unit = -amount_usd / net_quantity
            print(f"DEBUG: Net Quantity: {net_quantity}, Purchase Price Per Unit: {purchase_price_per_unit}")
            self.add_asset_purchase(asset_name, net_quantity, -amount_usd, 0)
        else:
            # Sale
            print("DEBUG: Transaction is a sale")
            quantity_sold = quantity
            cost_basis = self.calculate_cost_basis(asset_name, quantity_sold)
            sale_proceeds = amount_usd - fee
            profit = sale_proceeds - cost_basis
            print(f"DEBUG: Sold {quantity_sold} units of {asset_name} for ${amount_usd:.2f}")
            print(f"DEBUG: Cost basis: ${cost_basis:.2f}, Sale Proceeds: ${sale_proceeds:.2f}, Profit: ${profit:.2f}")

def process_csv(file_path):
    portfolio = Portfolio()
    df = pd.read_csv(file_path, delimiter='\t')
    print(f"DEBUG: Loaded CSV file - {file_path}")

    for index, row in df.iterrows():
        print(f"DEBUG: Processing row {index}: {row.to_dict()}")
        if row['type'] == 'trade' and row['aclass'] == 'currency' and pd.notnull(row['amountusd']):
            asset = row['asset']
            amount = abs(row['amount'])
            amount_usd = row['amountusd']
            fee = row['fee']
            time = row['time']
            
            portfolio.add_transaction(asset, amount, amount_usd, fee, time)
        else:
            print(f"DEBUG: Skipped row {index} due to missing or invalid 'amountusd'")

# Update the file path to your CSV file
process_csv('example.csv')
