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
    read_list = []
    
    width = 500
    rows = 20
    
    snakes = {} # dicionario com {ip: cobra}
    snack = [] # array de comidas
    snack.append(cube(randomSnack(rows, snakes), color=(0, 255, 0)))
    snakes['snacks'] = snack

    win = pygame.display.set_mode((500,500))
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
                if sock is s:
                    conn, addr = sock.accept()
                    # print("connection received from ", addr)
                    read_list.append(conn)
                    data = conn.recv(4096)
                    snake_client = pickle.loads(data) #recebe snake do socket
                    # if snake: # talvez esse if seja desnecessário
                    snakes[addr] = snake_client
                    conn.send(pickle.dumps(addr))
                else:
                    data = sock.recv(1024)
                    if data:
                        m = pickle.loads(data)
                        if type(m) == str:
                            snakes[sock.getpeername()].move(m)

                        for i in snakes:
                            if i != 'snacks':
                                snakes[i].move()

                        if (time.clock() - t) > 0.5:  # recupera o tempo
                            snack.append(cube(randomSnack(rows, snakes), color=(0, 255, 0)))
                            snakes['snacks'] = snack
                            t = time.clock()  # reseta clock

                        # Caso dê tempo usar threads para melhorar o processamento disso
                        # Separa tudo isso por funções, por que tá feio esse código, tudo misturado
                        for i in snack:
                            for j in snakes:
                                if j != 'snacks':
                                    if snakes[j].body != [] and snakes[j].body[0].pos == i.pos:
                                        snakes[j].addCube()
                                        snack.remove(i)
                                        snack.append(cube(randomSnack(rows, snakes), color=(0, 255, 0)))

                        # Caso dê tempo usar threads para melhorar o processamento disso
                        # for i in snakes:
                        #     for x in range(len(snakes[i].body)):
                        #         if snakes[i].body[x].pos in list(map(lambda z: z.pos, snakes[i].body[x+1:])):
                        #             for i in snakes[i].body:
                        #                 snack.append(cube(i.pos, color=(0, 255, 0)))
                        #             snakes[i].reset((random.randint(0,30), random.randint(0,30)))
                        #             break
                        # print("received", repr(data))

                        sock.send(pickle.dumps(snakes))
                    else:
                        sock.close()
                        read_list.remove(sock)
            

# def main(snk):
    
start_server()