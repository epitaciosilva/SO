
import sys
import time
import json
import math
import random
import pygame
import socket, pickle
import select
import tkinter as tk
from tkinter import messagebox
from snake import snake, cube, randomSnack, redrawWindow

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    cobra = snake((255,0,0), (10,10)) # cria snake do cliente 
    print(cobra.body)
    s.connect((HOST, PORT))
    s.sendall(pickle.dumps(cobra.body)) # enviando cobra do cliente pro servidor
    # data = s.recv(1024)