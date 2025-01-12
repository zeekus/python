import csv
from collections import defaultdict
from datetime import datetime

# Create defaultdicts to store transactions
currency_transactions = defaultdict(list)
reference_transactions = defaultdict(list)
transaction_types = set()

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
        
        # Convert time string to datetime object
        transaction['time'] = datetime.strptime(transaction['time'], '%Y-%m-%d %H:%M:%S')
        
        # Add the transaction to the appropriate currency list
        currency = transaction['asset']
        currency_transactions[currency].append(transaction)
        
        # Add the transaction to the reference_id list
        reference_transactions[transaction['reference_id']].append(transaction)
        
        # Add the transaction type to the set of types
        transaction_types.add(transaction['type'])

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
