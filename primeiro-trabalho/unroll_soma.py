import os
import random
import threading
import time
import mmap
import signal
import posix_ipc
import sys
import struct

def matriz_randomica(rows, cols):
    matriz = []
    for i in range(rows):
        matriz.append([])
        for j in range(cols):
            matriz[i].append([])
            matriz[i][j] = random.randint(0,10)
    return matriz

# def soma_matrizes_processos(rowA, rowB, processo, results):
#     processo = os.fork()
#     if processo == 0:
#         linha_somada = []
#         for a,b in zip(rowA, rowB):
#             linha_somada.append(b+a) # soma das matrizes

#         results.append(linha_somada)  


def soma_matrizes_processos(elemt_A, elemt_B):
    return elemt_A + elemt_B

def soma_matrizes_threads(elemt_A, elemt_B, posi_i, posi_j, results):
    threading.currentThread()
    results[posi_i][posi_j] = elemt_A + elemt_B

def print_matriz(matriz):
    """Imprime matriz na tela, desde que ela tenha o formato [[]]"""
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            print(matriz[i][j], end=(", " if len(matriz[i])-1 != j else ""))
        print()

def unroll(args, func, method, results):
    matriz_aleatoria = matriz_randomica(len(args), len(args[0]))

    # ---------- Threads ----------
    # A soma de cada elemento é feito dentro de uma thread
    if method == "thre":
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

        print("------ Args ------")
        print_matriz(args)

        print("\n------ Aleatoria ------")
        print_matriz(matriz_aleatoria)

        print("\n------ Matriz soma ------")
        print_matriz(results)
    
    # ---------- PROCESSOS ----------
    # Ainda não esta pronto, eh preciso fazer com os processos se comuniquem
    # provavelmente com memoria compartilhada so assim pra conseguir salvar os results 
    # de cada soma das linhas da matriz.
    # No caso o processo original devera imprimir a soma completa da matriz
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
                    mapped_memory.seek((i*4) + j)
                    mapped_memory.write(struct.pack('>i',result))
                    exit(0)

        time.sleep(1)
        print("------ Args ------")
        print_matriz(args)

        print("\n------ Aleatoria ------")
        print_matriz(matriz_aleatoria)

        if processo != 0:
            print("\n------ Matriz soma ------")
            for i in range(rows):
                for j in range(cols):
                    mapped_memory.seek( (i*4) + j)
                    val_bytes = mapped_memory.read(4)
                    read_val = struct.unpack('>i',val_bytes)
                    print(read_val[0], end=", ")
                print()

if __name__ == '__main__':
    res = []
    unroll([[0, 1, 3],[2, 3, 1],[4, 5, 4]], soma_matrizes_processos, 'proc', res)
    # unroll([[0, 1, 3, 4, 5],[2, 3, 1, 2, 3],[4, 5, 4, 2, 5]], soma_matrizes_threads, 'thre', res)