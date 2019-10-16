
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
    width = 500
    rows = 20
    cobra = snake((255,0,0), (10,10)) # cria snake do cliente 
    s.connect((HOST, PORT))
    s.sendall(pickle.dumps(cobra.body)) # enviando cobra do cliente pro servidor
    data = s.recv(1024) # recebendo dados do servidor
    # snakes = pickle.loads(data) # recebendo outras cobras do servidor
    
    snack = []
    snack.append(cube(randomSnack(rows, cobra), color=(0,255,0)))
    
    win = pygame.display.set_mode((width, width))
    flag = True
    clock = pygame.time.Clock()
    t = time.clock()
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        cobra.move()
        if (time.clock() - t) > 0.5: # recupera o tempo
            snack.append(cube(randomSnack(rows, cobra), color=(0,255,0)))
            t = time.clock() # reseta clock
        
        for i in snack:
            if cobra.body != [] and cobra.body[0].pos == i.pos:
                cobra.addCube()
                snack.remove(i)
                snack.append(cube(randomSnack(rows, cobra), color=(0,255,0)))
                # break

        for x in range(len(cobra.body)):
            if cobra.body[x].pos in list(map(lambda z:z.pos,cobra.body[x+1:])):
                # print('Score: ', len(s.body))
                # message_box('You Lost!', 'Play again...')
                for i in cobra.body:
                    snack.append(cube(i.pos, color=(0,255,0)))
                cobra.reset((10,10))
                break
        redrawWindow(win, rows, width, cobra, snack)
    pass
