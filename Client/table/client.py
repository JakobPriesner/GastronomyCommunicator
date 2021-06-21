import json
import logging
import sys
from pathlib import Path

import requests

def post_action(url, description):

    data = {
        "description": description,
        "table_id": table_id
    }

    response = requests.post(url, data=data)
    print(response.text)


def prepare_log():
    # init logger
    logging.basicConfig(filename='client.log', level=logging.DEBUG)
    root = logging.getLogger()

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    LOG_FORMAT = '%(asctime)s,%(msecs)d --> %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
    formatter = logging.Formatter(LOG_FORMAT)
    ch.setFormatter(formatter)
    root.addHandler(ch)


if __name__ == "__main__":
    relPath = str(Path(__file__).parent) + "/"
    with open(relPath + "config.json") as config_file:
        client_config = json.load(config_file)

    button_pay_pressed = False
    button_2_pressed = False

    table_id = client_config["id"]

    server_ip = client_config["server_ip"]
    port = client_config["port"]

    server_addr = 'http://' + server_ip + ':' + str(port)

    while True:
        post_action(server_addr + '/api/POST/'+input(), input())