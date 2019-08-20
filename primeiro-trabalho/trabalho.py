import os
import threading

def matriz_randomica(tam_linha):
    matriz = []
    for i in range(tam_linha):
        matriz.append([i, 2*i])
    return matriz

def soma_matrizes(matrizA, matrizB):
    matriz = []
    for a, b in zip(matrizA, matrizB):
        matriz.append([b[0]+a[0], b[1]+a[1]]) # soma das matrizes

    return matriz

def func(var1, var2):
    print(str(var1) + ", " + str(var2))

def func_thread(matrizA, matrizB):
    thread = threading.currentThread()
    matriz = soma_matrizes(matrizA, matrizB)
    print("\n----- Matriz resultante da soma -----")
    for i in matriz:
        func(i[0], i[1])


def unroll(args, func, method, results):
    matriz_aleatoria = matriz_randomica(len(args))

    # Fork
    if method == 'proc':
        print("Processo filho")
        val = os.fork() # criar-se um novo processo
        
        # para que as matrizes sejam escritas antes do resultado soma/multiplicacao, 
        # eh preciso que isso rode no processo pai/original

        if val != 0: # val != 0 indica que eh o processo original
            print("---- Args ----")   
            for i in args:
                results.append(func(i[0], i[1]))
            
            print("---- Aleatoria ----")   
            for i in matriz_aleatoria:
                results.append(func(i[0], i[1]))

        else: # igual a 0 diz que eh do processo filho
            matriz = soma_matrizes(args, matriz_aleatoria)

            print("\n----- Matriz resultante da soma -----")
            for i in matriz:
                func(i[0], i[1])

    # Threads                
    else:
        # Com as threads os processo ocorrem simultaneamente, por isso que imprimi as duas coias "ao mesmo tempo"
        # Uma possibilidade eh usar semaforos para impedir que ambas acessem as matrizes simultaneamente. 
        t1 = threading.Thread(target=func_thread, args=(args,matriz_aleatoria))
        t1.start()

        # processo principal
        print("\nProcesso " + str(os.getpid()) + " na thread " + str(t1.ident))

        print("\n---- Args ----")   
        for i in args:
            results.append(func(i[0], i[1]))
            
        print("\n---- Aleatoria ----")   
        for i in matriz_aleatoria:
            results.append(func(i[0], i[1]))
        

res = []
# unroll([[0, 1],[2,3],[4,5]], func, 'proc', res)
unroll([[0, 1],[2,3],[4,5]], func, 'thre', res)
