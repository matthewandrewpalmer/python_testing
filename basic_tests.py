def return_two():
    return 2


assert return_two() == 2


def second_lowest_number(numbers):
    numbers.sort()
    return numbers[1]


assert second_lowest_number([9, 1, 4, 15, 7]) is 4


def second_highest_number(number_list):
    number_list.sort(reverse=True)
    return number_list[1]


assert second_highest_number([1, 2, 3, 4, 5]) == 4
assert second_highest_number([5, 6, 9, 2, 1]) == 6
