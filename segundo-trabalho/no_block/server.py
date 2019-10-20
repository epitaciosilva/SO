import sys
import time
import math
import random
import pygame
import socket, pickle
import select
import threading
import tkinter as tk
from tkinter import messagebox
from snake import snake, cube, randomSnack, redrawWindow

# verificando se alguma cobra comeu um snack
def eat_snack(snack, snacks, snakes):
    threading.currentThread()
    global width, rows

    for j in snakes:
        if j != 'snacks':
            if snakes[j].body != [] and snakes[j].body[0].pos == snack.pos:
                snakes[j].addCube()
                snacks.remove(snack)
                snacks.append(cube(randomSnack(rows, snakes), color=(0, 255, 0)))
                break # Creio que dá um break, pois só come um snack por vez

def start_server():
    port = 65433
    read_list = []
    
    global width, rows
    width = 500
    rows = 20
    
    snakes = {} # dicionario com {ip: cobra}
    snacks = [] # array de comidas
    snacks.append(cube(randomSnack(rows, snakes), color=(0, 255, 0)))
    snakes['snacks'] = snacks

    clock = pygame.time.Clock()
    t = time.clock()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        pygame.time.delay(50)
        clock.tick(10)
        s.setblocking(0)
        s.bind(('', port))
        s.listen(5)
        read_list.append(s)

        while True:
            readable, writeable, error = select.select(read_list,[],[])

            for sock in readable:
                if sock is s: # Abrindo conexão
                    conn, addr = sock.accept()
                    read_list.append(conn)
                    data = conn.recv(4096)
                    snake_client = pickle.loads(data) #recebe snake do socket
                    snakes[addr] = snake_client
                    conn.send(pickle.dumps(addr))
                else:
                    data = sock.recv(4096)
                    
                    if data:
                        m = pickle.loads(data)
                        if type(m) == str: # Verificando se o cliente enviou algum movimento
                            snakes[sock.getpeername()].move(m)

                            # Adicionando snacks
                        if (time.clock() - t) > 0.5:  # recupera o tempo
                            snacks.append(cube(randomSnack(rows, snakes), color=(0, 255, 0)))
                            snakes['snacks'] = snacks
                            t = time.clock()  # reseta clock

                        threads = []
                        for snack in snacks:
                            threads.append([])
                            threads[-1] = threading.Thread(target=eat_snack, args=(snack, snacks, snakes))
                            threads[-1].start() 
                        threads[-1].join()
                        threads.clear()

                        # colocando cobras para se movimentar
                        for i in snakes:
                            if i != 'snacks':
                                snakes[i].move()

                        # Caso dê tempo usar threads para melhorar o processamento disso
                        # for i in snakes:
                        #     for x in range(len(snakes[i].body)):
                        #         if snakes[i].body[x].pos in list(map(lambda z: z.pos, snakes[i].body[x+1:])):
                        #             for i in snakes[i].body:
                        #                 snacks.append(cube(i.pos, color=(0, 255, 0)))
                        #             snakes[i].reset((random.randint(0,30), random.randint(0,30)))
                        #             break
                        # print("received", repr(data))

                        sock.send(pickle.dumps(snakes))
                    else:
                        sock.close()
                        read_list.remove(sock)
            

start_server()