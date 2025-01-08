import sys

def estimate_tax(tokens,value):
   sale=float(tokens)*float(value)
   print (f'Sale: {sale}')
   tax=(float(sale)*0.30)
   print (f'Tax: {tax}')
   gross = sale-tax
   print (f'gross: {gross}')



count=1

house=135000
gift=85000

rate=house+gift
print (f"We need to gross {rate}")

for tokens in sys.argv:
    print (f'place holder :{count}: {tokens}')
    count=count+1

sale_token=sys.argv[1]
value_of_token=sys.argv[2]

estimate_tax(sale_token,value_of_token)


