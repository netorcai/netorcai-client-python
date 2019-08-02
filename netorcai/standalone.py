#!/usr/bin/env python3

import netorcai.agent
import argparse
import socket
from threading import Thread

def run_agent(game_func):
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", help="run as a server", action="store_true")
    parser.add_argument("--port", type=int, help="port to use (as server or client)")
    parser.add_argument("--host", type=str, help="host to connect to (as a client)",
                        default="localhost")
    parser.add_argument("--verbose")

    args = parser.parse_args()

    if args.server:
        serve(args, game_func)
    else:
        run_client(args, game_func)

def run_client(args, game_func):
    agent = netorcai.agent.Agent()

    port = args.port or 4242
    host = args.host or "localhost"

    if args.verbose:
        print("Connecting to netorcai...", end=' ', flush=True)
    agent.connect(hostname=host, port=port)
    if args.verbose:
        print("done")

    try:
        game_func(agent)
    except Exception as e:
        print(e)
        sys.exit(1)
    sys.exit(0)


def serve(args, game_func):

    port = args.port or 4567

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', port))
    sock.listen()

    while True:
        (clientsocket, address) = sock.accept()

        def run_on_sock():
            agent = netorcai.agent.Agent()
            agent.take_over(clientsocket)
            try:
                game_func(agent)
            except Exception as game_exc:
                print("fatal error in game function", game_exc)

        t = Thread(target=run_on_sock)
        t.run()
