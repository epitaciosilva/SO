#include <iostream>
#include <cmath>
#include <thread>
#include <mutex>

int n = 2000000;
std::mutex mtx;

bool isPrime(int num)
{
    bool resultado = true;
    for (int i = 2; i <= sqrt(num); i++)
    {
        if (num % i == 0)
        {
            resultado = false;
            break;
        }
    }

    return resultado;
}

void threadFunc() {
    while (n > 2) {
        if (isPrime(n)) {
            // std::cout << n << std::endl;
        }

        mtx.lock();
        n--;
        mtx.unlock();
    }
}

int main()
{
    int numThreads = 4;
    std::thread threads[numThreads];
    
    for (int j = 0; j < numThreads; j++) {
        threads[j] = std::thread(threadFunc);
    }

    for (int j = 0; j < numThreads; j++) {
        threads[j].join();
    }
}