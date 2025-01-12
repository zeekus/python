import csv
from collections import defaultdict

# Create defaultdicts to store transactions
currency_transactions = defaultdict(list)
reference_transactions = defaultdict(list)

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
        
        # Add the transaction to the reference_id list
        reference_transactions[transaction['reference_id']].append(transaction)

# Function to determine if a transaction is a debit or credit
def get_trade_type(transaction):
    if transaction['type'] == 'trade':
        return 'debit' if transaction['amount'] > 0 else 'credit'
    return transaction['type']

# Print transaction pairs that match by reference_id
print("Transaction pairs that match by reference_id:")
for ref_id, transactions in reference_transactions.items():
    if len(transactions) > 1 and any(t['type'] == 'trade' for t in transactions):
        print(f"\nReference ID: {ref_id}")
        for transaction in transactions:
            trade_type = get_trade_type(transaction)
            print(f"Asset: {transaction['asset']}, Time: {transaction['time']}, Amount: {transaction['amount']}, Type: {trade_type}")

# Print summary of transactions for all currencies
print("\nSummary of transactions for all currencies:")
for currency, transactions in currency_transactions.items():
    print(f"{currency}: {len(transactions)} transactions")
