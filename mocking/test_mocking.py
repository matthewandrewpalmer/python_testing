from unittest.mock import MagicMock

from mocking import pairing


def test_list_split_into_pairs():
    one = MagicMock()
    two = MagicMock()

    assert pairing([one, two]) == [[one, two]]


def test_odd_number_in_list_splits_into_pairs_and_extra_item():
    one = MagicMock()
    two = MagicMock()
    three = MagicMock()

    assert pairing([one, two, three]) == [[one, two], [three]]
