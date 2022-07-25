given_value = 2
a_list = [1, 5, 8]
absolute_difference_function = lambda list_value : abs(list_value - given_value)
closest_value = min(a_list, key=absolute_difference_function)
print(closest_value)