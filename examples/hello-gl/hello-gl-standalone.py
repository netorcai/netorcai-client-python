#!/usr/bin/env python3
from netorcai.agent import *
from netorcai.standalone import run_agent

def game_logic(agent):
    print("Logging in as a game logic...", end=' ', flush=True)
    agent.send_login("py-gl", "game logic")
    agent.read_login_ack()
    print("done")

    print("Waiting for DO_INIT...", end=' ', flush=True)
    do_init = agent.read_do_init()
    print("done")

    print("Sending DO_INIT_ACK...", end=' ', flush=True)
    agent.send_do_init_ack({"all_clients":{"gl": "python"}})
    print("done")

    for i in range(do_init.nb_turns_max):
        print("Waiting for DO_TURN...", end=' ', flush=True)
        do_turn = agent.read_do_turn()
        print("done")
        
        print("Sending DO_TURN_ACK...", end=' ', flush=True)
        agent.send_do_turn_ack({"all_clients":{"gl": "python"}}, -1)
        print("done")

if __name__ == '__main__':
    run_agent(game_logic)
