#!/usr/bin/env python3
"""Parsing module of the netorcai client library."""
from netorcai.version import metaprotocol_version


class PlayerInfo:
    def __init__(self, o):
        self.player_id = o["player_id"]
        self.nickname = o["nickname"]
        self.remote_address = o["remote_address"]
        self.is_connected = o["is_connected"]

    def __repr__(self):
        return "<PlayerInfo:%s id=%s>" % (self.nickname, self.player_id)


class PlayerActions:
    def __init__(self, o):
        self.player_id = o["player_id"]
        self.turn_number = o["turn_number"]
        self.actions = o["actions"]

    def __repr__(self):
        return "<PlayerActions:%s>" %  self.__dict__


class LoginAckMessage:
    def __init__(self, o):
        self.metaprotocol_version = o["metaprotocol_version"]
        if self.metaprotocol_version != metaprotocol_version():
            print("Warning: netorcai uses version '{}' while netorcai-client-python uses '{}'".format(
                self.metaprotocol_version, metaprotocol_version()))

    def __repr__(self):
        return "<LoginAckMessage:%s>" % self.__dict__


class GameStartsMessage:
    def __init__(self, o):
        self.player_id = o["player_id"]
        self.nb_players = o["nb_players"]
        self.nb_special_players = o["nb_special_players"]
        self.nb_turns_max = o["nb_turns_max"]
        self.ms_before_first_turn = o["milliseconds_before_first_turn"]
        self.ms_between_turns = o["milliseconds_between_turns"]
        self.players_info = [PlayerInfo(info) for info in o["players_info"]]
        self.initial_game_state = o["initial_game_state"]

    def __repr__(self):
        return "<GameStartsMessage:nb_players=%s nb_special_players=%s nb_turns_max=%s>" % (
            self.nb_players, self.nb_special_players, self.nb_turns_max)


class GameEndsMessage:
    def __init__(self, o):
        self.winner_player_id = o["winner_player_id"]
        self.game_state = o["game_state"]

    def __repr__(self):
        return "<GameEndsMessage:winner=%s>" % self.winner_player_id


class TurnMessage:
    def __init__(self, o):
        self.turn_number = o["turn_number"]
        self.players_info = [PlayerInfo(info) for info in o["players_info"]]
        self.game_state = o["game_state"]

    def __repr__(self):
        return "<TurnMessage for turn %s>" % self.turn_number


class DoInitMessage:
    def __init__(self, o):
        self.nb_players = o["nb_players"]
        self.nb_special_players = o["nb_special_players"]
        self.nb_turns_max = o["nb_turns_max"]

    def __repr__(self):
        return "<DoInitMessage:nb_players=%s nb_special_players=%s nb_turns_max=%s>" % (
            self.nb_players, self.nb_special_players, self.nb_turns_max)


class DoTurnMessage:
    def __init__(self, o):
        self.player_actions = [PlayerActions(action) for action in o["player_actions"]]

    def __repr__(self):
        return "<DoTurnMessage:%s>" % self.__dict__
