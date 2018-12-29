#!/usr/bin/env python3

import subprocess
import shlex
from netorcai.client import *
from netorcai.message import *

def launch_netorcai_wait_listening(nb_players, nb_visus):
    cmd = 'netorcai --simple-prompt --autostart --delay-first-turn=50 --delay-turns=50 --nb-turns-max=2 --nb-players-max={} --nb-visus-max={}'.format(nb_players, nb_visus)
    p = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, universal_newlines=True)

    line = p.stdout.readline().rstrip()
    if 'Listening incoming connections' in line:
        return p
    else:
        p.terminate()
        raise Exception("netorcai's first output line is not about Listening incoming connections... Line is below.\n{}".format(line))

def test_everything_goes_well():
    n = launch_netorcai_wait_listening(1, 0)

    # Game logic
    gl = Client()
    gl.connect()
    gl.send_login("gl", "game logic")
    gl.read_login_ack()

    # Player
    player = Client()
    player.connect()
    player.send_login("p0", "player")
    player.read_login_ack()

    # Game should start automatically as one player is connected (--autostart)
    doInit = gl.read_do_init()
    gl.send_do_init_ack({"all_clients": {"gl": "python"}})
    player.read_game_starts()

    for i in range(doInit.nb_turns_max - 1):
        gl.read_do_turn()
        gl.send_do_turn_ack({"all_clients": {"gl": "python"}}, -1)

        turn = player.read_turn()
        player.send_turn_ack(turn.turn_number, [{"player": "python"}])

    gl.read_do_turn()
    gl.send_do_turn_ack({"all_clients": {"gl": "python"}}, -1)

    player.read_game_ends()
    n.terminate()
