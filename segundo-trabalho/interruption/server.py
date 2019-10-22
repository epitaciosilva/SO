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

def receber_conexoes():
    threading.currentThread()
    global enviados, recebidos, snakes
    port = 65433
    read_list = []

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        pygame.time.delay(50)
        s.setblocking(0)
        s.bind(('', port))
        s.listen(5)
        read_list.append(s)
        
        while True:
            pygame.time.delay(50)

            processou = False
            time_io = time.clock()
            readable, _, _ = select.select(read_list,[],[])

            for sock in readable:
                if sock is s: # Abrindo conexão
                    conn, addr = sock.accept()
                    read_list.append(conn)
                    data = conn.recv(4096)
                    snake_client = pickle.loads(data) #recebe snake do socket
                    snakes[addr] = snake_client
                    recebidos.append([conn, data])
                    conn.send(pickle.dumps(addr))
                    processou = True
                else:
                    processou = True
                    data = sock.recv(4096)
                    recebidos.append([sock, data])

            for i,item in enumerate(enviados):
                processou = True
                send = item[0]
                data = item[1]
                if data:
                    send.send(pickle.dumps(data))
                    enviados.remove(item)

            if processou:
                time_io = time.clock() - time_io
                f = open("tempos_io.csv", "a")
                f.write(str(time_io) + "\n")
                f.close()

def start_server():
    # Recebidos é uma lista de dados recebidos dos clientes e precisa ser processada
    # Enviados é uma lista de dados que já foram processadas e precisam de ser enviadas

    global recebidos, enviados, snakes
    width = 500
    rows = 20
    recebidos = []
    enviados = []
    snakes = {} # dicionario com {ip: cobra}

    thread_io = threading.Thread(target=receber_conexoes, args=())
    thread_io.start() 

    snacks = [] # array de comidas
    snacks.append(cube(randomSnack(rows, snakes), color=(0, 255, 0)))
    snakes['snacks'] = snacks

    clock = pygame.time.Clock()
    t = time.clock()

    while True:
        pygame.time.delay(50)
        # clock.tick(10)

        time_jogo = time.clock()

        for i,item in enumerate(recebidos): # verificando se recebeu algo então processa
            sock = item[0]
            data = item[1]
            if data:
                m = pickle.loads(data)
                if type(m) == str: # Verificando se o cliente enviou algum movimento
                    snakes[sock.getpeername()].move(m)

                    # Adicionando snacks
                if (time.clock() - t) > 0.5:  # recupera o tempo
                    snacks.append(cube(randomSnack(rows, snakes), color=(0, 255, 0)))
                    snakes['snacks'] = snacks
                    t = time.clock()  # reseta clock

                for snack in snacks:
                    for j in snakes:
                        if j != 'snacks':
                            if snakes[j].body != [] and snakes[j].body[0].pos == snack.pos:
                                snakes[j].addCube()
                                snacks.remove(snack)
                                snacks.append(cube(randomSnack(rows, snakes), color=(0, 255, 0)))                    

                # colocando cobras para se movimentar
                for i in snakes:
                    if i != 'snacks':
                        snakes[i].move()
                
                time_jogo = time.clock() - time_jogo
                f = open("tempos_jogo.csv", "a")
                f.write(str(time_jogo) + "\n")
                f.close()

                # sock.send(pickle.dumps(snakes))
                enviados.append([sock, snakes]) # Adicionando snakes para ser enviados ao cliente em questão
                recebidos.remove(item) # Remove dos recebidos

start_server()