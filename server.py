import socket
from constants import BYTES_SIZE, ENCODING_FORMAT, PORT
import json
from hamming import hamming_correct, hamming_original
from fletcher import FletcherChecksumStr, FletcherChecksumBytes
from bitarray import bitarray

HOST = '127.0.0.1'  # Localhost


def invert(a):
    if a == "0":
        return "1"
    return "0"


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        # while True:
        data, address = conn.recvfrom(BYTES_SIZE)
        if not data:
            print("disconnected")
        else:
            json_ser = data.decode(ENCODING_FORMAT)
            json_payload = json.loads(json_ser)
            payload = json_ser.encode(ENCODING_FORMAT)
            if json_payload["type"] == "hamming":
                corrected = hamming_correct(json_payload["value"])
                original = hamming_original(
                    corrected, json_payload["hamming_dic"])
                payload = bitarray(original).tobytes()
            else:
                payload = FletcherChecksumStr.get_fletcher16(
                    json_payload["value"])
                payload = json.dumps(payload).encode(ENCODING_FORMAT)

            conn.sendall(payload)
