import csv
from collections import defaultdict

# Create a defaultdict to store transactions for each currency
currency_transactions = defaultdict(list)

# Define the column names
columns = ["transaction_id", "reference_id", "time", "type", "subtype", "asset_class", "asset", "account", "amount", "fee", "balance", "total"]

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
        
        # Add the transaction to the appropriate currency list
        currency = transaction['asset']
        currency_transactions[currency].append(transaction)

# Now you have dynamic lists for each currency
for currency, transactions in currency_transactions.items():
    print(f"{currency}: {len(transactions)} transactions")
    # You can access transactions for each currency using currency_transactions[currency]

# Example: Access USD transactions
usd_transactions = currency_transactions['USD']
print("\nUSD Transactions:")
for transaction in usd_transactions:
    print(f"Refid: {transaction['reference_id']}, Asset: {transaction['asset']}, Time: {transaction['time']}, Amount: {transaction['amount']}, Balance: {transaction['balance']}")




