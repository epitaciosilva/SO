import os

def matriz_randomica(tam_linha):
    matriz = []
    for i in range(tam_linha):
        matriz.append([i, 2*i])
    return matriz

def func(var1,var2):
    print(str(var1) + ", " + str(var2))

def unroll(args, func, method, results):
    if method == 'proc':
        print("Matriz processo filho")
        matriz_aleatoria = matriz_randomica(len(args))
        val = os.fork() # criar-se um novo processo
        
        # para que as matrizes sejam escritas antes do resultado soma/multiplicacao, 
        # eh preciso isso rode no processo pai/original

        if val != 0: # val != 0 indica que eh o processo original
            print("---- Args ----")   
            for i in args:
                results.append(func(i[0], i[1]))
            
            print("---- Aleatoria ----")   
            for i in matriz_aleatoria:
                results.append(func(i[0], i[1]))

        else: # igual a 0 diz que eh do processo filho
            matriz = []

            for item_args, item_aleatoria in zip(args, matriz_aleatoria):
                matriz.append([item_aleatoria[0]+item_args[0], item_aleatoria[1]+item_args[1]]) # soma das matrizes

            print("\n----- Matriz resultante da soma -----")
            for i in matriz:
                func(i[0], i[1])
           
res = []
unroll([[0, 1],[2,3],[4,5]], func, 'proc', res)

