#!/usr/bin/env python3
from netorcai.agent import *
import sys
from netorcai.standalone import run_agent

def play(agent):

    print("Connecting to netorcai...", end=' ', flush=True)
    agent.connect()
    print("done")

    print("Logging in as a player...", end=' ', flush=True)
    agent.send_login("py-player", "player")
    agent.read_login_ack()
    print("done")

    print("Waiting for GAME_STARTS...", end=' ', flush=True)
    game_starts = agent.read_game_starts()
    print("done")

    for i in range(game_starts.nb_turns_max):
        print("Waiting for TURN...", end=' ', flush=True)
        turn = agent.read_turn()
        print("done")

        actions = [{"player": "python"}]
        print("Sending actions {}...".format(actions), end=' ', flush=True)
        agent.send_turn_ack(turn.turn_number, actions)
        print("done")

if __name__ == '__main__':
    run_agent(game_logic)
