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

def INT_handler(sig_num, arg):
    if mapped_memory != None: 
        mapped_memory.close()
        posix_ipc.unlink_shared_memory("results")
    sys.exit(0)	

# def multiplicacao_matrizes_processos(row_a, col_a, index_row, index_col, processo, results):
#     processo = os.fork()
#     soma = 0
#     # mutex = multiprocessing.Lock()
#     # mutex.acquire()
#     if processo == 0: # se o processo for filho
#         for i in range(len(row_a)):
#             soma += row_a[i] * col_a[i]
#         results[index_row][index_col] = soma
#     else:
#         # o pai espera seus filhos terminarem de processar
#         os.waitpid(processo, 0)
#     return processo

def multiplicacao_matrizes_processos(row_a, col_b, index_row, index_col, len_cols):
    processo = os.fork()
    if processo == 0:
        soma = 0
        for i in range(len(row_a)):
            soma += row_a[i] * col_b[i]

        mapped_memory.seek((index_row*len_cols*4) + (index_col*4))
        mapped_memory.write(struct.pack('>i',soma))
        exit(0)

def get_col(arr, col):
    return list(map(lambda x : x[col], arr))

def multiplicacao_matrizes_threads(row_a, col_b, index_row, index_col, results):
    threading.currentThread()
    soma = 0
    for i in range(len(row_a)):
        soma += row_a[i] * col_b[i]
    
    results[index_row][index_col] = soma

def unroll(args, func, method, results):
    matriz_aleatoria = matriz_randomica(len(args[0]), random.randint(1,3))
    # Dimensão das matrizes
    
    rows_args = len(args)
    cols_args = len(args[0]) 
    
    rows_aleatoria = len(matriz_aleatoria)
    cols_aleatoria = len(matriz_aleatoria[0])


    # ---------- Threads ----------
    # A soma de cada elemento é feito dentro de uma thread
    if method == "thread":
        # List das threads criadas
        threads = []

        results = [[0 for i in range(cols_aleatoria)] for j in range(rows_args)]
        for j in range(cols_aleatoria):
            m = []
            for i in range(rows_aleatoria):
                m.append(matriz_aleatoria[i][j])
            for index, arg in enumerate(args):
                threads.append([])
                threads[-1] = threading.Thread(target=func, args=(arg, m, index, j, results))
                threads[-1].start() 

        threads[-1].join()
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
        global mapped_memory
        mapped_memory = None
        signal.signal(signal.SIGINT, INT_handler)
        # dim(results) = rows_args x cols_aleatoria
        print(rows_args*cols_aleatoria*4)
        memory = posix_ipc.SharedMemory("results", flags = posix_ipc.O_CREAT, mode = 0o777, size = rows_args*cols_aleatoria*4)
        mapped_memory = mmap.mmap(memory.fd, memory.size)
        memory.close_fd()

        for j in range(cols_aleatoria):
            m = []
            for i in range(rows_aleatoria):
                m.append(matriz_aleatoria[i][j])
            for index, arg in enumerate(args):
                func(arg,m,index, j, cols_aleatoria) 
                
        time.sleep(0.1)
        print("------ Args ------")
        print_matriz(args)
        
        print("\n------ Aleatoria ------")
        print_matriz(matriz_aleatoria)
        
        print("\n------ Matriz multiplicada ------")
        for i in range(rows_args):
            for j in range(cols_aleatoria):
                mapped_memory.seek( (i*cols_aleatoria*4) + (j*4))
                read_val = struct.unpack('>i',mapped_memory.read(4))
                print(read_val[0], end=", ")
            print()
            # processos = []
            # return
            # mutex.release()
            
if __name__ == '__main__':
    res = []
    # unroll([[-1,3],[4,2]], multiplicacao_matrizes_processos, 'process', res)
    unroll([[2,3,1],[-1, 0, 2]], multiplicacao_matrizes_threads, 'thread', res)
