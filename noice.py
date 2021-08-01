from bitarray import bitarray
import random
from constants import ENCODING_FORMAT


def generate_noise(input_string, probability_value):
    # input_string_b = input_string.encode(ENCODING_FORMAT)
    bit_instance = bitarray(input_string)
    # bit_instance.frombytes(input_string_b)
    bit_instance_copy = bit_instance.copy()
    for index, byte in enumerate(bit_instance):
        prob_check = random.randint(1, 100)
        if prob_check <= probability_value:
            bit_instance.invert(index)
            break

    # print(bit_instance.tobytes().decode(ENCODING_FORMAT))
    # print(bit_instance_copy.tobytes().decode(ENCODING_FORMAT))
    # print(input_string)
    return bit_instance.to01()


# print(generate_noise("a", 100))
