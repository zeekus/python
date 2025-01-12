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



# Print transactions for all currencies
for currency, transactions in currency_transactions.items():
    print(f"\n{currency} Transactions:")
    for transaction in transactions[:5]:  # Limit to first 5 transactions per currency for brevity
        print(f"Refid: {transaction['reference_id']}, Asset: {transaction['asset']}, Time: {transaction['time']}, Amount: {transaction['amount']}, Balance: {transaction['balance']}")
    if len(transactions) > 5:
        print(f"... and {len(transactions) - 5} more transactions")
    print()  # Add a blank line between currencies