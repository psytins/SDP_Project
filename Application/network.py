# network.py - This module contains basic networking functions for creating, binding, and listening on sockets.
import socket

def create_socket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def bind_socket(socket, host, port):
    socket.bind((host, port))

def listen(socket):
    socket.listen()
