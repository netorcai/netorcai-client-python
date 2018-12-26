#!/usr/bin/env python3
import json

class PlayerInfo:
    def __init__(self, o):
        self.player_id = o["player_id"]
        self.nickname = o["nickname"]
        self.remote_address = o["remote_address"]
        self.is_connected = o["is_connected"]

def parse_players_info(a):
    l = list()
    for element in a:
        l.append(PlayerInfo(element))
    return l

class PlayerActions:
    def __init__(self, o):
        self.player_id = o["player_id"]
        self.turn_number = o["turn_number"]
        self.actions = o["actions"]

def parse_players_actions(a):
    l = list()
    for element in a:
        l.append(PlayerActions(element))
    return l

class LoginAckMessage:
    def __init__(self):
        pass

class GameStartsMessage:
    def __init__(self, o):
        self.player_id = o["player_id"]
        self.nb_players = o["nb_players"]
        self.nb_turns_max = o["nb_turns_max"]
        self.ms_before_first_turn = o["milliseconds_before_first_turn"]
        self.ms_between_turns = o["milliseconds_between_turns"]
        self.players_info = parse_players_info(o["players_info"])
        self.initial_game_state = o["initial_game_state"]

class GameEndsMessage:
    def __init__(self, o):
        self.winner_player_id = o["winner_player_id"]
        self.game_state = o["game_state"]

class TurnMessage:
    def __init__(self, o):
        self.turn_number = o["turn_number"]
        self.players_info = parse_players_info(o["players_info"])
        self.game_state = o["game_state"]

class DoInitMessage:
    def __init__(self, o):
        self.nb_players = o["nb_players"]
        self.nb_turns_max = o["nb_turns_max"]

class DoTurnMessage:
    def __init__(self, o):
        self.player_actions = parse_players_actions(o["player_actions"])
