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

# Function to print related transactions
def print_related_transactions(reference_id):
    related = reference_transactions[reference_id]
    print(f"\nTransactions with reference ID {reference_id}:")
    for transaction in related:
        print(f"Asset: {transaction['asset']}, Time: {transaction['time']}, Amount: {transaction['amount']}, Type: {transaction['type']}")

# Example usage
print("Currency transaction counts:")
for currency, transactions in currency_transactions.items():
    print(f"{currency}: {len(transactions)} transactions")

# Ask user for a reference ID to check
while True:
    ref_id = input("\nEnter a reference ID to check (or 'q' to quit): ")
    if ref_id.lower() == 'q':
        break
    if ref_id in reference_transactions:
        print_related_transactions(ref_id)
    else:
        print("No transactions found with that reference ID.")
