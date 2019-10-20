
import sys
import time
import json
import math
import random
import pygame
import socket
import pickle
import select
import copy
import tkinter as tk
from tkinter import messagebox
from snake import snake, cube, randomSnack, redrawWindow

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65433  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    width = 500
    rows = 20
    
    cobra = snake((255, 0, 200), (10, 10))  # cria snake do cliente
    s.connect((HOST, PORT))
    s.sendall(pickle.dumps(cobra))  # enviando cobra do cliente pro servidor
    data = s.recv(1024)  # recebendo dados do servidor
    my_snake = pickle.loads(data)  # recebendo outras cobras do servidor

    s.sendall(pickle.dumps(cobra))  # enviando cobra do cliente pro servidor
    data = s.recv(1024)  # recebendo dados do servidor
    snakes = pickle.loads(data)

    # snack = []
    # snack.append(cube(randomSnack(rows, cobra), color=(0, 255, 0)))

    win = pygame.display.set_mode((width, width))
    flag = True 
    clock = pygame.time.Clock()
    t = time.clock()
    movimento = None

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        # cobra.move()

        if movimento != None:
            s.sendall(pickle.dumps(movimento))
            movimento = None
        else:
            s.sendall(pickle.dumps(snakes))  # enviando cobra do cliente pro servidor

        data = s.recv(1024)  # recebendo dados do servidor
        
        if data:
            snakes = pickle.loads(data)  # recebendo outras cobras do servidor
        else:
            time.sleep(5)
            continue

        # if (time.clock() - t) > 0.5:  # recupera o tempo
        #     snack.append(cube(randomSnack(rows, cobra), color=(0, 255, 0)))
        #     t = time.clock()  # reseta clock

        # for i in snack:
        #     if snakes[my_snake].body != [] and snakes[my_snake].body[0].pos == i.pos:
        #         snakes[my_snake].addCube()
        #         snack.remove(i)
        #         snack.append(cube(randomSnack(rows, snakes[my_snake]), color=(0, 255, 0)))

        # for x in range(len(snakes[my_snake].body)):
        #     if snakes[my_snake].body[x].pos in list(map(lambda z: z.pos, snakes[my_snake].body[x+1:])):
        #         # print('Score: ', len(s.body))
        #         # message_box('You Lost!', 'Play again...')
        #         for i in snakes[my_snake].body:
        #             snack.append(cube(i.pos, color=(0, 255, 0)))
        #         snakes[my_snake].reset((10, 10))
        #         break
        # print(snakes) # Epitácio aqui chega todas as cobras conectadas no servidor
                      # Mas não to conseguindo jogar todas as cobras no tabuleiro
        # snakes[my_snake] = cobra
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    movimento = 'left'

                elif keys[pygame.K_RIGHT]:
                    movimento = 'right'
                    # snakes[my_snake].dirnx = 1
                    # snakes[my_snake].dirny = 0
                    # snakes[my_snake].turns[snakes[my_snake].head.pos[:]] = [snakes[my_snake].dirnx, snakes[my_snake].dirny]

                elif keys[pygame.K_UP]:
                    movimento = 'up'
                    # snakes[my_snake].dirnx = 0
                    # snakes[my_snake].dirny = -1
                    # snakes[my_snake].turns[snakes[my_snake].head.pos[:]] = [snakes[my_snake].dirnx, snakes[my_snake].dirny]

                elif keys[pygame.K_DOWN]:
                    movimento = 'down'
                    # snakes[my_snake].dirnx = 0
                    # snakes[my_snake].dirny = 1
                    # snakes[my_snake].turns[snakes[my_snake].head.pos[:]] = [snakes[my_snake].dirnx, snakes[my_snake].dirny]

        snacks = snakes.pop('snacks')          
        redrawWindow(win, rows, width, snakes, snacks)
    pass
