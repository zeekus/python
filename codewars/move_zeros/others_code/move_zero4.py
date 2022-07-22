def move_zeros(array):
    return sorted(array, key=lambda x: not isinstance(x, bool) and x==0)