#!/usr/bin/env python3
import json
from netorcai.message import *

def test_player_info():
    s = '''{
      "player_id": 0,
      "nickname": "jugador",
      "remote_address": "127.0.0.1:59840",
      "is_connected": true
    }'''

    pinfo = PlayerInfo(json.loads(s))
    assert pinfo.player_id == 0
    assert pinfo.nickname == "jugador"
    assert pinfo.remote_address == "127.0.0.1:59840"
    assert pinfo.is_connected == True

def test_parse_players_info():
    s = '''[
      {
        "player_id": 0,
        "nickname": "jugador",
        "remote_address": "127.0.0.1:59840",
        "is_connected": true
      },
      {
        "player_id": 1,
        "nickname": "bot",
        "remote_address": "127.0.0.1:59842",
        "is_connected": false
      }
    ]'''

    pinfos = parse_players_info(json.loads(s))
    assert len(pinfos) == 2
    assert pinfos[0].player_id == 0
    assert pinfos[0].nickname == "jugador"
    assert pinfos[0].remote_address == "127.0.0.1:59840"
    assert pinfos[0].is_connected == True

    assert pinfos[1].player_id == 1
    assert pinfos[1].nickname == "bot"
    assert pinfos[1].remote_address == "127.0.0.1:59842"
    assert pinfos[1].is_connected == False

def test_game_starts():
    s = '''{
      "message_type": "GAME_STARTS",
      "player_id": 0,
      "players_info": [
        {
          "player_id": 0,
          "nickname": "jugador",
          "remote_address": "127.0.0.1:59840",
          "is_connected": true
        }
      ],
      "nb_players": 4,
      "nb_turns_max": 100,
      "milliseconds_before_first_turn": 1000,
      "milliseconds_between_turns": 1000,
      "initial_game_state": {}
    }'''

    m = GameStartsMessage(json.loads(s))
    assert m.player_id == 0
    assert len(m.players_info) == 1
    assert m.players_info[0].player_id == 0
    assert m.players_info[0].nickname == "jugador"
    assert m.players_info[0].remote_address == "127.0.0.1:59840"
    assert m.players_info[0].is_connected == True
    assert m.nb_players == 4
    assert m.nb_turns_max == 100
    assert m.ms_before_first_turn == 1000
    assert m.ms_between_turns == 1000
    assert len(m.initial_game_state) == 0

def test_game_ends():
    s = '''{
      "message_type": "GAME_ENDS",
      "winner_player_id": 0,
      "game_state": {}
    }'''

    m = GameEndsMessage(json.loads(s))
    assert m.winner_player_id == 0
    assert len(m.game_state) == 0

def test_turn():
    s = '''{
      "message_type": "TURN",
      "turn_number": 0,
      "game_state": {},
      "players_info": [
        {
          "player_id": 0,
          "nickname": "jugador",
          "remote_address": "127.0.0.1:59840",
          "is_connected": true
        }
      ]
    }'''

    m = TurnMessage(json.loads(s))
    assert m.turn_number == 0
    assert len(m.game_state) == 0
    assert len(m.players_info) == 1
    assert m.players_info[0].player_id == 0
    assert m.players_info[0].nickname == "jugador"
    assert m.players_info[0].remote_address == "127.0.0.1:59840"
    assert m.players_info[0].is_connected == True

def test_do_init():
    s = '''{
      "message_type": "DO_INIT",
      "nb_players": 4,
      "nb_turns_max": 100
    }'''

    m = DoInitMessage(json.loads(s))
    assert m.nb_players == 4
    assert m.nb_turns_max == 100

def test_player_actions():
    s = '''{
      "player_id": 2,
      "turn_number": 4,
      "actions": []
    }'''

    a = PlayerActions(json.loads(s))
    assert a.player_id == 2
    assert a.turn_number == 4
    assert len(a.actions) == 0

def test_do_turn():
    s = '''{
      "message_type": "DO_TURN",
      "player_actions": [
        {
          "player_id": 1,
          "turn_number": 2,
          "actions": []
        },
        {
          "player_id": 0,
          "turn_number": 3,
          "actions": [ 4 ]
        }
      ]
    }'''

    m = DoTurnMessage(json.loads(s))
    assert len(m.player_actions) == 2
    assert m.player_actions[0].player_id == 1
    assert m.player_actions[0].turn_number == 2
    assert len(m.player_actions[0].actions) == 0
    assert m.player_actions[1].player_id == 0
    assert m.player_actions[1].turn_number == 3
    assert len(m.player_actions[1].actions) == 1
    assert m.player_actions[1].actions[0] == 4
