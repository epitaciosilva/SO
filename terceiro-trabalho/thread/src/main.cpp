#include <iostream>
#include <thread>
#include <mutex>
#include <vector>
#include <cmath>
int n = 100000;
int shared = 2;
int quantidade_primos = 0;

int shared_n(int num)
{
    // para evitar aqueles erros citados coloquei um mutex
    // pras threads acessarem o valor n um por vez
    std::mutex mu;
    mu.lock();
    shared += num;
    mu.unlock();

    return shared;
}

void shared_quantidade_primos(int cont) {
    std::mutex mu;
    mu.lock();
    quantidade_primos += cont;
    mu.unlock();
}

bool isPrimo(int numero) {
    bool resultado = true;
    for (int i = 2; i <= sqrt(numero); i++) {
        if (numero % i == 0) {
            resultado = false;
            break;
        }
    }
    return resultado;
}

// n_primos é o número de números que cada thread vai verificar por vez
void primos(int n_primos) {
    int cont = 0;
    int b = shared_n(n_primos);

    while(b <= n) {
        for(int i = b-n_primos; i <= b; i++) {
            if(isPrimo(i)) {
                cont++;
            } 
        }
        shared_quantidade_primos(cont);
        cont = 0;
        b = shared_n(n_primos);
    }   
}

int main()
{
    static const int t = 2;
    std::thread threads[t];

    for (int j = 0; j < t; ++j)
    {
        threads[j] = std::thread(primos, 1000);
        threads[j].join();
    }

    std::cout << quantidade_primos << std::endl;
    return 0;
}