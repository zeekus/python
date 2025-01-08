# Sample transaction data
data = [
    {"txid": "LFWBMP-6KB4V-XXC6PU", "amount": -979.3789, "fee": 0, "asset": "USD"},
    {"txid": "LYS6X3-MM4LQ-2PDAZX", "amount": 1103.62749009, "fee": 2.42798095, "asset": "ADA"},
    {"txid": "LRIK7D-4VESV-W3PUGM", "amount": -550.59975457, "fee": 0, "asset": "ADA"},
    {"txid": "LOBFPX-6GBUW-XIULVQ", "amount": 506.5518, "fee": 1.1144, "asset": "USD"},
    {"txid": "LXOJTZ-ZNTBK-KGMIFW", "amount": -550.59975457, "fee": 0, "asset": "ADA"},
    {"txid": "LBM5AC-GMJGN-DSOVAL", "amount": 510.1896, "fee": 1.1224, "asset": "USD"},
]

# Initialize lists for tracking purchases and sales
ada_purchases = []
profits = []

# Process each transaction
for transaction in data:
    amount = transaction["amount"]
    fee = transaction["fee"]
    asset = transaction["asset"]

    if asset == 'USD' and amount > 0:  # Sale of USD
        sale_amount = amount - fee
        ada_sold = -sum([ada["amount"] for ada in ada_purchases])  # Total ADA sold
        cost_basis = 0
        
        # Calculate profit using FIFO
        while ada_sold > 0 and ada_purchases:
            purchase = ada_purchases[0]
            if purchase["amount"] <= ada_sold:
                # If we can sell all of this purchase
                cost_basis += purchase["cost"]
                ada_sold -= purchase["amount"]
                ada_purchases.pop(0)  # Remove this purchase from the list
            else:
                # Partially sell this purchase
                cost_basis += (ada_sold / purchase["amount"]) * purchase["cost"]
                purchase["amount"] -= ada_sold
                ada_sold = 0
        
        profit = sale_amount - cost_basis
        profits.append({"sale_amount": sale_amount, "cost_basis": cost_basis, "profit": profit})

    elif asset == 'ADA':  # Purchase of ADA
        total_cost = -amount - fee  # Total spent in USD for this ADA purchase
        # Calculate cost basis per ADA and store it
        cost_per_ada = total_cost / -amount
        ada_purchases.append({"amount": -amount, "cost": total_cost})

# Display results
for i, result in enumerate(profits):
    print(f"Transaction {i + 1}: Sale Amount: ${result['sale_amount']:.2f}, Cost Basis: ${result['cost_basis']:.2f}, Profit: ${result['profit']:.2f}")

