def pairing(number_list):
    if len(number_list) % 2 != 0:
        return [number_list[0:2], [number_list[2]]]
    else:
        return [number_list]
