from utils import *

import os
import random
import threading
import time
import mmap
import signal
import posix_ipc
import sys
import struct

def soma_matrizes_processos(elemt_A, elemt_B):
    return elemt_A + elemt_B

def soma_matrizes_threads(elemt_A, elemt_B, posi_i, posi_j, results):
    threading.currentThread()
    results[posi_i][posi_j] = elemt_A + elemt_B

def unroll(args, func, method, results):
    matriz_aleatoria = matriz_randomica(len(args), len(args[0]))

    # ---------- Threads ----------
    # A soma de cada elemento é feito dentro de uma thread
    if method == "thread":
        # List das threads criadas
        threads = []

        # Dimensão das matrizes
        cols = len(args[0])
        rows = len(args)

        results = [[0 for i in range(cols)] for j in range(rows)]
        for i in range(rows):
            for j in range(cols):
                threads.append([])
                threads[-1] = threading.Thread(target=func, args=(args[i][j], matriz_aleatoria[i][j], i, j, results))
                threads[-1].start()
        threads[-1].join()
        print("------ Args ------")
        print_matriz(args)

        print("\n------ Aleatoria ------")
        print_matriz(matriz_aleatoria)

        print("\n------ Matriz soma ------")
        print_matriz(results)
    
    # ---------- PROCESSOS ----------
    else: 
        sem = posix_ipc.Semaphore("test_sem", flags = posix_ipc.O_CREAT, mode = 0o777, initial_value = 1)
        processos = []
         # Dimensão das matrizes
        cols = len(args[0])
        rows = len(args)

        mapped_memory = None

        def INT_handler(sig_num, arg):
            if mapped_memory != None: 
                mapped_memory.close()
                posix_ipc.unlink_shared_memory("results")
            sys.exit(0)	

        signal.signal(signal.SIGINT, INT_handler)

        memory = posix_ipc.SharedMemory("results", flags = posix_ipc.O_CREAT, mode = 0o777, size = cols*rows*4)
        mapped_memory = mmap.mmap(memory.fd, memory.size)
        memory.close_fd()
        processo = 1

        for i in range(rows):
            for j in range(cols):
                processo = os.fork()
                if processo == 0:
                    result = func(args[i][j], matriz_aleatoria[i][j])
                    mapped_memory.seek((i*cols*4) + (j*4))
                    mapped_memory.write(struct.pack('>i',result))
                    exit(0)

        print("------ Args ------")
        print_matriz(args)

        print("\n------ Aleatoria ------")
        print_matriz(matriz_aleatoria)

        # esse sleep é porque não consegui usar semáforos
        time.sleep(0.02)
        if processo != 0:
            print("\n------ Matriz soma ------")
            for i in range(rows):
                for j in range(cols):
                    mapped_memory.seek( (i*cols*4) + (j*4))
                    read_val = struct.unpack('>i',mapped_memory.read(4))
                    print(read_val[0], end=", ")
                print()

if __name__ == '__main__':
    res = []
    unroll([[0, 1, 3, 4, 5],[2, 3, 1, 2, 3],[4, 5, 4, 2, 5]], soma_matrizes_processos, 'proc', res)
    # unroll([[0, 1, 3, 4, 5],[2, 3, 1, 2, 3],[4, 5, 4, 2, 5]], soma_matrizes_threads, 'thre', res)
