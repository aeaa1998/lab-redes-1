import socket
from constants import BYTES_SIZE, ENCODING_FORMAT, PORT
from helpers import *
from bitarray import bitarray
from noice import generate_noise
from hamming import normalize_text_with_parity_bits
import json
from fletcher import FletcherChecksumStr, FletcherChecksumBytes


def get01(data):
    bit_instance = bitarray()
    bit_instance.frombytes(data.encode(ENCODING_FORMAT))
    return bit_instance.to01()


def prepare_fletcher(data, corrupt_percentage):
    bit_instance = bitarray()
    bit_instance.frombytes(data.encode(ENCODING_FORMAT))
    payload_json = {
        "value": generate_noise(bit_instance.to01(), corrupt_percentage),
        "type": "checksum"
    }
    return FletcherChecksumStr.get_fletcher16(bit_instance.to01()), payload_json


def prepare_hamming(data, corrupt_percentage):
    bit_instance = bitarray()
    bit_instance.frombytes(data.encode(ENCODING_FORMAT))
    dic, hamming_value = normalize_text_with_parity_bits(bit_instance.to01())

    payload_json = {
        "hamming_dic": dic,
        "value": generate_noise(hamming_value, corrupt_percentage),
        "type": "hamming"
    }
    return payload_json


HOST = '127.0.0.1'  # The server's hostname or IP address
# The port used by the server
correction_or_detection = ["Corrección", "Detección"]
list_options = ["Código de Hamming"]
detection_list_options = ["Fletcher checksum"]


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # while True:
    user_input = required_input("Ingrese el valor a procesar\n")
    noise = int_input_range("Ingrese la probabilidad de ruido sobre 100\n")

    option = None
    option_one = get_index_from_list(correction_or_detection)
    payload_json = None
    fletcher = None
    if option_one == 0:
        option_two = get_index_from_list(list_options)
        option = list_options[option_two]
        payload_json = prepare_hamming(user_input, noise)
    else:
        option_two = get_index_from_list(detection_list_options)
        option = detection_list_options[option_two]
        fletcher, payload_json = prepare_fletcher(user_input, noise)
    payload = json.dumps(payload_json)

    s.sendall(payload.encode(ENCODING_FORMAT))
    data = s.recv(BYTES_SIZE)
response = data.decode(ENCODING_FORMAT)
if payload_json["type"] == "hamming":
    print('El server resolvio hamming y retorno: ', response)
else:
    json_payload = json.loads(response)
    if fletcher["dec"] == json_payload["dec"]:
        print("No hubieron errores en el mensaje")
    else:
        print("Se encontro error\n {}".format(fletcher["time"]))
