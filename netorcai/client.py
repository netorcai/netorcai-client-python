#!/usr/bin/env python3

import socket
import struct

from netorcai.message import *

def recvall(sock, size, flags=0):
    data = sock.recv(size, flags)
    assert len(data) == size
    return data

class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __del__(self):
        self.close()

    def connect(self, hostname="localhost", port=4242):
        self.socket.connect((hostname,port))

    def close(self):
        self.socket.close()

    def send_string(self, s):
        send_buffer = (s + "\n").encode('utf-8')

        # Send string size, as a little-endian uint16
        binary_size = struct.pack("<H", len(send_buffer))
        self.socket.sendall(binary_size)

        # Send string content
        self.socket.sendall(send_buffer)

    def send_json(self, j):
        self.send_string(json.dumps(j))

    def recv_string(self):
        # Read string size, as a little-endian uint16
        raw_bytes = recvall(self.socket, 2)
        content_size = struct.unpack('<H', raw_bytes)[0]

        # Read string content
        s = recvall(self.socket, content_size)
        return s.decode('utf-8')

    def recv_json(self):
        s = self.recv_string()
        return json.loads(s)

    def send_login(self, nickname, role):
        self.send_json({
            "message_type": "LOGIN",
            "nickname": nickname,
            "role": role
        })

    def send_turn_ack(self, turn_number, actions):
        self.send_json({
            "message_type": "TURN_ACK",
            "turn_number": turn_number,
            "actions": actions
        })

    def send_do_init_ack(self, initial_game_state):
        self.send_json({
            "message_type": "DO_INIT_ACK",
            "initial_game_state": initial_game_state
        })

    def send_do_turn_ack(self, game_state, winner_player_id):
        self.send_json({
            "message_type": "DO_TURN_ACK",
            "game_state": game_state,
            "winner_player_id": winner_player_id
        })

    def read_login_ack(self):
        msg = self.recv_json()
        if msg["message_type"] == "LOGIN_ACK":
            return LoginAckMessage()
        elif msg["message_type"] == "KICK":
            raise Exception("Kicked from netorai. Reason: {}".format(msg["kick_reason"]))
        else:
            raise Exception("Unexpected type message received: {}".format(msg["message_type"]))

    def read_game_starts(self):
        msg = self.recv_json()
        if msg["message_type"] == "GAME_STARTS":
            return GameStartsMessage(msg)
        elif msg["message_type"] == "KICK":
            raise Exception("Kicked from netorai. Reason: {}".format(msg["kick_reason"]))
        else:
            raise Exception("Unexpected type message received: {}".format(msg["message_type"]))

    def read_turn(self):
        msg = self.recv_json()
        if msg["message_type"] == "TURN":
            return TurnMessage(msg)
        elif msg["message_type"] == "KICK":
            raise Exception("Kicked from netorai. Reason: {}".format(msg["kick_reason"]))
        elif msg["message_type"] == "GAME_ENDS":
            raise Exception("Game over!")
        else:
            raise Exception("Unexpected type message received: {}".format(msg["message_type"]))

    def read_game_ends(self):
        msg = self.recv_json()
        if msg["message_type"] == "GAME_ENDS":
            return GameEndsMessage(msg)
        elif msg["message_type"] == "KICK":
            raise Exception("Kicked from netorai. Reason: {}".format(msg["kick_reason"]))
        else:
            raise Exception("Unexpected type message received: {}".format(msg["message_type"]))

    def read_do_init(self):
        msg = self.recv_json()
        if msg["message_type"] == "DO_INIT":
            return DoInitMessage(msg)
        elif msg["message_type"] == "KICK":
            raise Exception("Kicked from netorai. Reason: {}".format(msg["kick_reason"]))
        else:
            raise Exception("Unexpected type message received: {}".format(msg["message_type"]))

    def read_do_turn(self):
        msg = self.recv_json()
        if msg["message_type"] == "DO_TURN":
            return DoTurnMessage(msg)
        elif msg["message_type"] == "KICK":
            raise Exception("Kicked from netorai. Reason: {}".format(msg["kick_reason"]))
        else:
            raise Exception("Unexpected type message received: {}".format(msg["message_type"]))
