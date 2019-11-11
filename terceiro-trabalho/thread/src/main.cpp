#include <iostream>
#include <thread>
#include <mutex>
#include <math.h>

int n = 1000;

bool shared_n(int num)
{
    // std::cout << num << " ";
    // para evitar aqueles erros citados coloquei um mutex
    // pras threads acessarem o valor n um por vez
    std::mutex mu;
    mu.lock();
    n -= num;
    mu.unlock();
    // std::cout << n << " ";
    // return n;
}

bool isPrime(int num)
{
    shared_n(num); // Eu esperava que a função me trouxesse o número atualizado, mas não traz
    int resultado = 0;
    for (int i = 2; i <= n / 2; i++)
    {
        if (n % i == 0)
        {
            resultado++;
        }
    }
    
    // esses valores ainda estão meio cagados, tem número negativo e tals
    if (resultado == 0)
    {
        std::cout << n << ": Primo!" << std::endl;
    }
    else
    {
        std::cout << n << ": Não!" << std::endl;
    }
    return resultado == 0;
}

int main()
{
    static const int t = 2;
    std::thread threads[t];

    if(n % 2 == 0){
        n -= 1;
    }

    for (int i = 0; i < n; ++i) // percorre os n numeros
    {
        // int t_aux = t;
        for (int j = 0; j < t; ++j) // percorre as threads
        {
            threads[j] = std::thread(isPrime, pow(t, (j+1))); // atribui threads ao vetor e manda número n pra função isPrime
        }
        
        // Sem esperar para matar as threads dá segmentation
        for (int j = 0; j < t; ++j)
        {
            threads[j].join();
        }
    }

    return 0;
}