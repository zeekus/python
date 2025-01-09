require 'csv'
require 'date'
require 'set'

# Create hashes to store transactions and wallets
currency_transactions = Hash.new { |h, k| h[k] = [] }
reference_transactions = Hash.new { |h, k| h[k] = [] }
transaction_types = Set.new
wallets = Hash.new { |h, k| h[k] = Hash.new { |h2, k2| h2[k2] = [] } }

# Define the column names
COLUMNS = %w[transaction_id reference_id time type subtype asset_class asset account amount fee balance total]

def update_wallet(wallet_id, asset, amount, price, timestamp)
  wallets[wallet_id][asset] << {
    amount: amount,
    price: price,
    timestamp: timestamp
  }
end

def calculate_fifo_cost_basis(wallets, wallet_id, asset, amount_to_sell)
  basis = 0
  remaining = amount_to_sell
  wallets[wallet_id][asset].each do |entry|
    break if remaining <= 0
    amount = [remaining, entry[:amount]].min
    basis += amount * entry[:price]
    remaining -= amount
  end
  basis
end

def get_transaction_direction(transaction)
  if transaction['amount'] > 0
    'debit (incoming)'
  elsif transaction['amount'] < 0
    'credit (outgoing)'
  else
    'neutral'
  end
end

# Read the CSV file
CSV.foreach('your_file.csv', headers: true).with_index(1) do |row, line_num|
  begin
    puts "Processing line #{line_num}"
    puts "Raw row data: #{row.inspect}"

    # Create a hash for the current transaction, taking only the values
    transaction = {
      'transaction_id' => row['txid'],
      'reference_id' => row['refid'],
      'time' => row['time'],
      'type' => row['type'],
      'subtype' => row['subtype'],
      'asset_class' => row['aclass'],
      'asset' => row['asset'],
      'account' => row['wallet'],
      'amount' => row['amount'],
      'fee' => row['fee'],
      'balance' => row['balance'],
      'total' => row['amountusd'] # Adjusted to match CSV header
    }

    puts "Processed transaction data: #{transaction}"

    # Convert numeric fields to appropriate types
    %w[amount fee balance total].each do |field|
      if transaction[field].nil? || transaction[field].empty?
        puts "Warning: #{field} is nil or empty on line #{line_num}"
        transaction[field] = 0.0
      else
        transaction[field] = transaction[field].to_f
      end
    end

    puts "Transaction after numeric conversion: #{transaction}"

    # Convert time string to Time object
    begin
      transaction['time'] = DateTime.strptime(transaction['time'], '%Y-%m-%d %H:%M:%S').to_time
    rescue ArgumentError
      puts "Error: Invalid time format on line #{line_num}: #{transaction['time']}"
      next
    end

    puts "Final transaction data: #{transaction}"

    # Add the transaction to the appropriate currency list
    currency = transaction['asset']
    currency_transactions[currency] << transaction

    # Add the transaction to the reference_id list
    reference_transactions[transaction['reference_id']] << transaction

    # Add the transaction type to the set of types
    transaction_types.add(transaction['type'])

    # Update wallet for incoming transactions (buys)
    if transaction['type'] == 'trade' && transaction['amount'] > 0
      price = transaction['total'] ? (transaction['total'] / transaction['amount']).abs : 0
      update_wallet(transaction['account'], currency, transaction['amount'], price, transaction['time'])
      
      # Calculate and display cost basis for incoming transactions (debits)
      cost_basis_info = ", Cost Basis: $#{'%.2f' % price}" # Use price as cost basis for incoming trades.
      
      puts "Time: #{transaction['time']}, Asset: #{transaction['asset']}, Amount: #{transaction['amount']}, Type: #{transaction['type']}, Direction: debit (incoming)#{cost_basis_info}"
      
    elsif transaction['type'] == 'trade' && transaction['amount'] < 0 
      # Handle outgoing transactions (credits)
      puts "Time: #{transaction['time']}, Asset: #{transaction['asset']}, Amount: #{transaction['amount']}, Type: #{transaction['type']}, Direction: credit (outgoing)"
      
      amount_to_sell = -transaction['amount']
      
      # Ensure that we have entries in the wallet before calculating cost basis.
      if wallets[transaction['account']][transaction['asset']].any?
        cost_basis = calculate_fifo_cost_basis(wallets, transaction['account'], transaction['asset'], amount_to_sell)
        cost_basis_info = ", Cost Basis: $#{'%.2f' % cost_basis}"
        puts "Cost Basis Info for outgoing trade: #{cost_basis_info}"
      else
        puts "Warning: No wallet entries found for #{transaction['asset']} in account #{transaction['account']}."
      end
      
    end

  rescue => e
    puts "Error processing line #{line_num}: #{e.message}"
    puts "Row data: #{row.inspect}"
  end
end

# Print all summary information as before...

# Print summary of transactions for all currencies
puts "\nSummary of transactions for all currencies:"
currency_transactions.each do |currency, transactions|
  puts "#{currency}: #{transactions.size} transactions"
end

# Print all transaction types found
puts "\nTransaction types found:"
transaction_types.sort.each do |t_type|
  puts "- #{t_type}"
end

# Print wallet balances and average cost basis
puts "\nWallet balances and average cost basis:"
wallets.each do |wallet_id, assets|
  puts "\nWallet: #{wallet_id}"
  
  assets.each do |asset, entries|
    total_amount = entries.sum { |entry| entry[:amount] }
    total_cost = entries.sum { |entry| entry[:amount] * entry[:price] }
    
    avg_cost = total_amount > 0 ? total_cost / total_amount : 0
    
    puts "  #{asset}: Amount: #{total_amount}, Average Cost Basis: $#{'%.2f' % avg_cost}"
  end
end

