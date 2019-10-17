import sys
import time
import math
import random
import pygame
import socket, pickle
import select
import tkinter as tk
from tkinter import messagebox
from snake import snake, cube, randomSnack, redrawWindow

def start_server():
    port = 65433
    snakes = {} # dicionario com {ip: cobra}
    sacks = [] # array de comidas
    read_list = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setblocking(0)
        s.bind(('', port))
        s.listen(5)
        read_list.append(s)
        while True:
            readable, writeable, error = select.select(read_list,[],[])
            for sock in readable:
                if sock is s:
                    conn, addr = sock.accept()
                    # print("connection received from ", addr)
                    read_list.append(conn)
                    data = conn.recv(4096)
                    snake = pickle.loads(data) #recebe snake do socket
                    # if snake: # talvez esse if seja desnecessário
                    snakes[addr] = snake
                    print(snakes)
                    conn.send(pickle.dumps(snakes))
                else:
                    data = sock.recv(1024)
                    if data:
                        print("received", repr(data))
                        sock.send(pickle.dumps(snakes))
                    else:
                        sock.close()
                        read_list.remove(sock)
            

# def main(snk):
    
start_server()