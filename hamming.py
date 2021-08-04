from noice import generate_noise
from bitarray import bitarray
from constants import *
from functools import reduce
import math
import operator as op


def get01(data):
    bit_instance = bitarray()
    bit_instance.frombytes(data.encode(ENCODING_FORMAT))
    return bit_instance.to01()


def is_perfect_square(number):
    root = math.sqrt(number)
    if int(root + 0.5) ** 2 == number:
        return True
    else:
        return False


def get_mod_diff(mod, value):
    return (((mod - (value % mod)) % mod))


def set_parity_values(bitstring_represntation, number_of_parity_checks):
    parity_values = {}
    sum_of_parity = 0
    for i in range(number_of_parity_checks):
        index_to_check = 2**i
        counter = 0
        reached = False
        # print("Validacion ", index_to_check)
        for s_position, s in enumerate(bitstring_represntation):
            if reached:
                if s_position != index_to_check:
                    # print(
                    #     "Valor: ", bitstring_represntation[s_position], " Posicion: ", s_position)
                    sum_of_parity += int(bitstring_represntation[s_position])
                counter -= 1
                reached = counter != 0
            else:
                counter += 1
                reached = counter == index_to_check

        # Set parity index value
        # print(sum_of_parity)
        if sum_of_parity % 2 == 0:
            parity_values[index_to_check] = "0"
        else:
            parity_values[index_to_check] = "1"
        sum_of_parity = 0

    # Set values
    bitstring_represntation_list = list(bitstring_represntation)

    for index in parity_values:
        bitstring_represntation_list[index] = parity_values[index]
    if sum([int(i) for i in bitstring_represntation_list if int(i)]) % 2 != 0:
        bitstring_represntation_list[0] = "1"
    return ''.join(bitstring_represntation_list)


def normalize_text_with_parity_bits(data):
    _data = data+""
    data_size = len(_data)
    _mod = 16

    # bytes_to_add = (_mod - (data_size % _mod))
    bytes_to_add = get_mod_diff(_mod, data_size)
    # print("Agregaremos", bytes_to_add)
    if not is_perfect_square(bytes_to_add + data_size):
        bytes_to_add = ((bytes_to_add + data_size) * 2) - data_size
        size = bytes_to_add + data_size
    else:
        size = bytes_to_add + data_size

    number_of_parity_checks = round(math.log2(size))
    # print("Parity", number_of_/parity_checks)
    _data = '0'*(bytes_to_add) + _data

    output = ""

    parity_dictionary = {"positions": {}, "add": bytes_to_add}
    for index in range(len(_data)):
        if index == 0:
            parity_dictionary["positions"][0] = _data[index]
            output += "0"
        elif math.log2(index).is_integer():
            pos = 2**round(math.log2(index))
            parity_dictionary["positions"][pos] = _data[pos]
            output += "0"
        else:
            output += _data[index]
    return parity_dictionary, set_parity_values(output, number_of_parity_checks)


def correct_dummies(data):
    length = len(data)
    number_of_parity_checks = int(math.log2(length))
    pointer = 0
    current_2 = 2**pointer
    _data = list(data)
    for position in range(int(length/2) + number_of_parity_checks):
        if position != 0 and position != current_2:
            if(data[position] != "0"):
                _data[position] == "0"
            if position >= current_2:
                pointer += 1
                current_2 = 2**pointer
    return ''.join(_data)


def hamming_correct(data):
    index_error = reduce(lambda x, y: x ^ y, [i
                         for (i, v) in enumerate(data) if int(v)])
    if index_error != 0:

        error_position = index_error
        data = list(data)
        data[error_position] = "0" if data[error_position] == "1" else "1"
        data = ''.join(data)

    return data


def hamming_original(corrected, dictionary):
    corrected = list(corrected)

    for index in dictionary["positions"]:

        corrected[int(index)] = dictionary["positions"][index]
    return ''.join(corrected)[int(dictionary["add"]):]


# res = 2**10
# print(res)
# print(math.sqrt(res))
# print(get01('a'))
# print(16-(32 % 16))
# bit_instance = bitarray()
# bit_instance.frombytes(
#     "block pasamos un monton de tiempo pero aunquesea encontramos el maldito error block pasamos un monton de tiempo pero aunquesea encontramos el maldito error".encode(ENCODING_FORMAT))
# data = bit_instance.to01()

# dictionary, normalized = normalize_text_with_parity_bits(bit_instance.to01())
# out = ""

# for i, v in enumerate(normalized):
#     out += v
#     if (i+1) % 16 == 0 and i != 0:
#         out += "\n"

# # print(out)

# # Real
# # "1111000111110101011001010010000011110000011000010111001101101111101000000110001101101111011011110110111101101111"
# # Error
# # "0111000111/010101011001010010000011110000011000010111001101101111001000000100001101101111011011110110111101101111"
# # "0111000111010101011001010010000011110000011000010111001101101111001000000100001101101111011011110110111101101111"
# # Corrected
# # ""
# corrupted = generate_noise(normalized, 100)
# # print("Corrupted: ", corrupted)
# # print("Real: ", normalized)
# # print("Are equal? ", normalized == corrupted)
# # number_of_parity_checks = int(math.log2(len(corrupted)))
# # print(set_parity_values(corrupted, number_of_parity_checks))

# corrected = hamming_correct(corrupted)

# print(bitarray(hamming_original(corrected, dictionary)
#                ).tobytes().decode(ENCODING_FORMAT))
# # corrected = list(corrected)
# # for index in dictionary:
# #     corrected[index] = dictionary[index]
# # print(''.join(corrected))
# # print(get01("aa"))
