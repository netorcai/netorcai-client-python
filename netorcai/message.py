#!/usr/bin/env python3

import json

class PlayerInfo:
    def __init__(self, o):
        d = json.loads(o)
        self.playerID = o["player_id"]
        self.nickname = o["nickname"]
        self.remoteAddress = o["remote_address"]
        self.isConnected = o["is_connected"]

def parsePlayersInfo(a):
    l = list()
    for element in a:
        l.append(PlayerInfo(element))
    return l

class PlayerActions:
    def __init__(self, o):
        self.playerID = o["player_id"]
        self.turnNumber = o["turn_number"]
        self.actions = o["actions"]

def parsePlayersActions(a):
    l = list()
    for element in a:
        l.append(PlayerActions(element))
    return l

class LoginAckMessage:
    def __init__(self):
        pass

class GameStartsMessage:
    def __init__(self, o):
        self.playerID = o["player_id"]
        self.nbPlayers = o["nb_players"]
        self.nbTurnsMax = o["nb_turns_max"]
        self.msBeforeFirstTurn = o["milliseconds_before_first_turn"]
        self.msBetweenTurns = o["milliseconds_between_turns"]
        self.playersInfo = parsePlayersInfo(o["players_info"])
        self.initialGameState = o["initial_game_state"]

class GameEndsMessage:
    def __init__(self, o):
        self.winnerPlayerID = o["winner_player_id"]
        self.gameState = o["game_state"]

class TurnMessage:
    def __init__(self, o):
        self.turnNumber = o["turn_number"]
        self.playersInfo = parsePlayersInfo(o["players_info"])
        self.gameState = o["game_state"]

class DoInitMessage:
    def __init__(self, o):
        self.nbPlayers = o["nb_players"]
        self.nbTurnsMax = o["nb_turns_max"]

class DoTurnMessage:
    def __init__(self, o):
        self.playerActions = parsePlayersActions(o["player_actions"])
