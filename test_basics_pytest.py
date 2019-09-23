# return_two function
def return_two():
    return 2


def should_return_two():
    assert return_two() == 2


# second_lowest_number function
def second_lowest_number(numbers):
    numbers.sort()
    return numbers[1]


def test_basic_number_list():
    assert second_lowest_number([9, 1, 4, 15, 7]) is 4


# second_highest_number function
def second_highest_number(number_list):
    number_list.sort(reverse=True)
    return number_list[1]


def test_number_list():
    assert second_highest_number([1, 2, 3, 4, 5]) == 4


def test_random_number_list():
    assert second_highest_number([5, 6, 9, 2, 1]) == 6


def test_negative_numbers():
    assert second_highest_number([-5, -6, -9, -2, -1]) == -2


def test_all_identical_numbers():
    assert second_highest_number([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]) == 1


def test_list_of_floats():
    assert second_highest_number([2.5, 4.6, 7.9, 10.99, 34.99, 50.5, 5.4]) == 34.99


def test_list_of_floats_ints():
    assert second_highest_number([2.5, 4.6, 7.9, 10, 34.99, 50, 5, 34]) == 34.99
