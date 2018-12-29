#!/usr/bin/env python3
from netorcai.client import *
import sys

def main():
    try:
        client = Client()

        print("Connecting to netorcai...", end=' ', flush=True)
        client.connect()
        print("done")

        print("Logging in as a game logic...", end=' ', flush=True)
        client.send_login("py-gl", "game logic")
        client.read_login_ack()
        print("done")

        print("Waiting for DO_INIT...", end=' ', flush=True)
        do_init = client.read_do_init()
        print("done")

        print("Sending DO_INIT_ACK...", end=' ', flush=True)
        client.send_do_init_ack({"all_clients":{"gl": "python"}})
        print("done")

        for i in range(do_init.nb_turns_max):
            print("Waiting for DO_TURN...", end=' ', flush=True)
            do_turn = client.read_do_turn()
            print("done")

            print("Sending DO_TURN_ACK...", end=' ', flush=True)
            client.send_do_turn_ack({"all_clients":{"gl": "python"}}, -1)
            print("done")
    except Exception as e:
        print(e)
        sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':
    main()
