#!/usr/bin/env python3
import pytest
import subprocess
import shlex
import time
from netorcai.client import *
from netorcai.message import *
import netorcai.version

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

def get_kicked_client():
    c = Client()
    c.connect()
    c.send_string("¿qué?")
    return c

def test_kicked_instead_of_expected_message():
    n = launch_netorcai_wait_listening(10, 20)
    kick_reason = 'Kicked from netorcai. Reason: Invalid first message: Non-JSON message received'

    with pytest.raises(RuntimeError) as err:
        c = get_kicked_client()
        c.read_login_ack()
    print(kick_reason)
    print(str(err))
    assert kick_reason in str(err)

    with pytest.raises(RuntimeError) as err:
        c = get_kicked_client()
        c.read_game_starts()
    assert kick_reason in str(err)

    with pytest.raises(RuntimeError) as err:
        c = get_kicked_client()
        c.read_turn()
    assert kick_reason in str(err)

    with pytest.raises(RuntimeError) as err:
        c = get_kicked_client()
        c.read_game_ends()
    assert kick_reason in str(err)

    with pytest.raises(RuntimeError) as err:
        c = get_kicked_client()
        c.read_do_init()
    assert kick_reason in str(err)

    with pytest.raises(RuntimeError) as err:
        c = get_kicked_client()
        c.read_do_turn()
    assert kick_reason in str(err)

    n.terminate()

def get_logged_player():
    c = Client()
    c.connect()
    c.send_login("I", "player")
    return c;

def test_unexpected_message_but_not_kick():
    n = launch_netorcai_wait_listening(2, 0)
    error_msg = 'Unexpected message type received: LOGIN_ACK'

    # LOGIN_ACK instead of something else
    with pytest.raises(RuntimeError) as err:
        c = get_logged_player()
        c.read_game_starts()
    assert error_msg in str(err)
    c.close()

    with pytest.raises(RuntimeError) as err:
        c = get_logged_player()
        c.read_turn()
    assert error_msg in str(err)
    c.close()
    time.sleep(0.6)

    with pytest.raises(RuntimeError) as err:
        c = get_logged_player()
        c.read_game_ends()
    assert error_msg in str(err)
    c.close()

    with pytest.raises(RuntimeError) as err:
        c = get_logged_player()
        c.read_do_init()
    assert error_msg in str(err)
    c.close()
    time.sleep(0.6)

    with pytest.raises(RuntimeError) as err:
        c = get_logged_player()
        c.read_do_turn()
    assert error_msg in str(err)
    c.close()
    time.sleep(0.6)

    # Start a game
    player1 = get_logged_player()
    player2 = get_logged_player()

    gl = Client()
    gl.connect()
    gl.send_login("gl", "game logic")

    player1.read_login_ack()
    player2.read_login_ack()
    gl.read_login_ack()

    # The game should start automatically (--autostart)
    doInit = gl.read_do_init()
    gl.send_do_init_ack({"all_clients": {"gl": "python"}})

    # Player1 fails now
    with pytest.raises(RuntimeError) as err:
        player1.read_login_ack()
    assert 'Unexpected message type received: GAME_STARTS' in str(err)
    player2.read_game_starts()

    for i in range(doInit.nb_turns_max - 1):
        gl.read_do_turn()
        gl.send_do_turn_ack({"all_clients": {"gl": "python"}}, -1)

        turn = player2.read_turn()
        player2.send_turn_ack(turn.turn_number, [{"player": "python"}])

    gl.read_do_turn()
    gl.send_do_turn_ack({"all_clients": {"gl": "python"}}, -1)

    # Player2 fails now
    with pytest.raises(RuntimeError) as err:
        player2.read_turn()
    assert 'Game over!' in str(err)

    n.terminate()

def test_socket_error():
    for i in range(10):
        n = launch_netorcai_wait_listening(1, 0)

        player = Client()
        player.connect()
        player.send_login("p0", "player")

        n.kill()

        with pytest.raises(Exception) as err:
            player.read_login_ack()

def test_non_critical_metaprotocol_version_mismatch():
    n = launch_netorcai_wait_listening(10, 20)

    netorcai.version.minor += 1

    c = get_logged_player()
    c.read_login_ack()

    netorcai.version.minor -= 1

    n.terminate()
