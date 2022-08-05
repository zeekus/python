# Pre-defined lists
names = ['United States', 'Australia', 'Japan', 'India', 'Russia', 'Morocco', 'Egypt']
dr =  [True, False, False, False, True, True, True]
cpc = [809, 731, 588, 18, 200, 70, 45]


# Create dictionary my_dict with three key:value pairs: my_dict
my_dict={}
for key in names:
  for value1 in dr:
      for value2 in cpc:
        my_dict[key]=f'country:{key},dr:{value1},cpc:{value2}'

print(my_dict)