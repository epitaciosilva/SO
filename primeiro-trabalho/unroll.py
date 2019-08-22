import os
import random
import threading

def matriz_randomica(rows, cols):
    matriz = []
    for i in range(rows):
        matriz.append([])
        for j in range(cols):
            matriz[i].append([])
            matriz[i][j] = random.randint(0,10)
    return matriz

def soma_matrizes(rowA, rowB, results):
    threading.currentThread()
    
    linha_somada = []
    for a,b in zip(rowA, rowB):
        linha_somada.append(b+a) # soma das matrizes

    results.append(linha_somada)

def print_matriz(matriz):
    """Imprime matriz na tela, desde que ela tenha o formato [[]]"""
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            print(matriz[i][j], end=(", " if len(matriz[i])-1 != j else ""))
        print()

def unroll(args, func, method, results):
    matriz_aleatoria = matriz_randomica(len(args), len(args[0]))

    if method == "thre":
        threds = []
        for arg, row_aleatoria in zip(args, matriz_aleatoria):
            threds.append([])
            threds[-1] = threading.Thread(target=func, args=(arg, row_aleatoria, results))
            threds[-1].start()

        print("------ Args ------")
        for i in args:
            for arg in i:
                print(str(arg), end=", ")
            print()
        
        print("\n------ Aleatoria ------")
        for ma in matriz_aleatoria:
            for m in ma:
                print(str(m), end=", ")
            print()
        
        print("\n------ Matriz soma ------")
        print_matriz(results)

if __name__ == '__main__':
    res = []
    # unroll([[0, 1,3],[2,3,4],[4,5,7]], func, 'proc', res)
    unroll([[0, 1, 3, 4, 5],[2, 3, 1, 2, 3],[4, 5, 4, 2, 5]], soma_matrizes, 'thre', res)