def find_combinations(target_sum, num_count, start=0, combination=[]):
    if num_count == 0:
        if target_sum == 0:
            print(combination)
        return

    for i in range(start, 10):
        if target_sum - i < 0:
          break
        #find_combinations(target_sum - i, num_count - 1, i + 1, combination + [i])

        #find all combinations with out every order
        #find_combinations(target_sum - i, num_count - 1, i, combination + [i])

        #all combinations in every order
        find_combinations(target_sum - i, num_count - 1, 0, combination + [i])


if __name__ == "__main__":
    target_sum = 15
    num_count = 3
    find_combinations(target_sum, num_count)
