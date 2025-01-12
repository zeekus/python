import csv
from collections import defaultdict
from datetime import datetime

# Create defaultdicts to store transactions and wallets
currency_transactions = defaultdict(list)
reference_transactions = defaultdict(list)
transaction_types = set()
wallets = defaultdict(lambda: defaultdict(list))

# Define the column names
columns = ["transaction_id", "reference_id", "time", "type", "subtype", "asset_class", "asset", "account", "amount", "fee", "balance", "total"]

def update_wallet(wallet_id, asset, amount, price, timestamp):
    wallets[wallet_id][asset].append({
        'amount': amount,
        'price': price,
        'timestamp': timestamp
    })

def calculate_cost_basis(wallet_id, asset, amount_to_sell):
    basis = 0
    remaining = amount_to_sell
    for entry in wallets[wallet_id][asset]:
        if remaining <= 0:
            break
        amount = min(remaining, entry['amount'])
        basis += amount * entry['price']
        remaining -= amount
    return basis

# Read the CSV file
with open('your_file.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row if it exists
    
    # Process each row
    for row in csv_reader:
        # Create a dictionary for the current transaction
        transaction = dict(zip(columns, row))
        
        # Convert numeric fields to appropriate types
        transaction['amount'] = float(transaction['amount'])
        transaction['fee'] = float(transaction['fee'])
        transaction['balance'] = float(transaction['balance'])
        transaction['total'] = float(transaction['total']) if transaction['total'] else None
        
        # Convert time string to datetime object
        transaction['time'] = datetime.strptime(transaction['time'], '%Y-%m-%d %H:%M:%S')
        
        # Add the transaction to the appropriate currency list
        currency = transaction['asset']
        currency_transactions[currency].append(transaction)
        
        # Add the transaction to the reference_id list
        reference_transactions[transaction['reference_id']].append(transaction)
        
        # Add the transaction type to the set of types
        transaction_types.add(transaction['type'])

        # Update wallet
        if transaction['type'] == 'trade' and transaction['amount'] > 0:
            # Assuming the 'total' field represents the cost in USD for buys
            price = abs(transaction['total'] / transaction['amount']) if transaction['total'] else 0
            update_wallet(transaction['account'], currency, transaction['amount'], price, transaction['time'])

# Function to determine if a transaction is a debit or credit
def get_transaction_direction(transaction):
    if transaction['amount'] > 0:
        return 'debit (incoming)'
    elif transaction['amount'] < 0:
        return 'credit (outgoing)'
    else:
        return 'neutral'

# Print all transaction groups sorted by time
print("All transaction groups sorted by time:")
for ref_id, transactions in sorted(reference_transactions.items(), key=lambda x: min(t['time'] for t in x[1])):
    if len(transactions) > 1:
        print(f"\nReference ID: {ref_id}")
        for transaction in sorted(transactions, key=lambda x: x['time']):
            direction = get_transaction_direction(transaction)
            print(f"Time: {transaction['time']}, Asset: {transaction['asset']}, Amount: {transaction['amount']}, Type: {transaction['type']}, Direction: {direction}")

# Print summary of transactions for all currencies
print("\nSummary of transactions for all currencies:")
for currency, transactions in currency_transactions.items():
    print(f"{currency}: {len(transactions)} transactions")

# Print all transaction types found
print("\nTransaction types found:")
for t_type in sorted(transaction_types):
    print(f"- {t_type}")

# Print wallet balances and cost basis
print("\nWallet balances and cost basis:")
for wallet_id, assets in wallets.items():
    print(f"\nWallet: {wallet_id}")
    for asset, entries in assets.items():
        total_amount = sum(entry['amount'] for entry in entries)
        total_cost = sum(entry['amount'] * entry['price'] for entry in entries)
        avg_cost = total_cost / total_amount if total_amount > 0 else 0
        print(f"  {asset}: Amount: {total_amount}, Average Cost Basis: ${avg_cost:.2f}")

# Example of calculating cost basis for a sell transaction
example_wallet = list(wallets.keys())[0]
example_asset = list(wallets[example_wallet].keys())[0]
example_amount = 1.0  # Amount to sell
cost_basis = calculate_cost_basis(example_wallet, example_asset, example_amount)
print(f"\nExample Cost Basis Calculation:")
print(f"Selling {example_amount} {example_asset} from wallet {example_wallet}")
print(f"Cost Basis: ${cost_basis:.2f}")
