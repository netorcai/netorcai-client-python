#!/usr/bin/env python3
from netorcai.agent import *
import sys

def main():
    try:
        client = Agent()

        print("Connecting to netorcai...", end=' ', flush=True)
        client.connect()
        print("done")

        print("Logging in as a special player...", end=' ', flush=True)
        client.send_login("py-splayer", "special player")
        client.read_login_ack()
        print("done")

        print("Waiting for GAME_STARTS...", end=' ', flush=True)
        game_starts = client.read_game_starts()
        print("done")

        for i in range(game_starts.nb_turns_max):
            print("Waiting for TURN...", end=' ', flush=True)
            turn = client.read_turn()
            print("done")

            actions = [{"player": "python"}]
            print("Sending actions {}...".format(actions), end=' ', flush=True)
            client.send_turn_ack(turn.turn_number, actions)
            print("done")
    except Exception as e:
        print(e)
        sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':
    main()
